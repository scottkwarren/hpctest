# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Utility classes for logging the output of blocks of code.
"""
from __future__ import unicode_literals

import atexit
import errno
import multiprocessing
import os
import re
import select
import signal
import sys
import traceback
from contextlib import contextmanager
from types import ModuleType  # novm
from typing import Optional  # novm

from six import StringIO, string_types

import llnl.util.tty as tty

termios = None  # type: Optional[ModuleType]
try:
    import termios as term_mod
    termios = term_mod
except ImportError:
    pass


# Use this to strip escape sequences
_escape = re.compile(r'\x1b[^m]*m|\x1b\[?1034h|\x1b\][0-9]+;[^\x07]*\x07')

# control characters for enabling/disabling echo
#
# We use control characters to ensure that echo enable/disable are inline
# with the other output.  We always follow these with a newline to ensure
# one per line the following newline is ignored in output.
xon, xoff = '\x11\n', '\x13\n'
control = re.compile('(\x11\n|\x13\n)')


@contextmanager
def ignore_signal(signum):
    """Context manager to temporarily ignore a signal."""
    old_handler = signal.signal(signum, signal.SIG_IGN)
    try:
        yield
    finally:
        signal.signal(signum, old_handler)


def _is_background_tty(stream):
    """True if the stream is a tty and calling process is in the background.
    """
    return (
        stream.isatty() and
        os.getpgrp() != os.tcgetpgrp(stream.fileno())
    )


def _strip(line):
    """Strip color and control characters from a line."""
    return _escape.sub('', line)


class keyboard_input(object):
    """Context manager to disable line editing and echoing.

    Use this with ``sys.stdin`` for keyboard input, e.g.::

        with keyboard_input(sys.stdin) as kb:
            while True:
                kb.check_fg_bg()
                r, w, x = select.select([sys.stdin], [], [])
                # ... do something with keypresses ...

    The ``keyboard_input`` context manager disables canonical
    (line-based) input and echoing, so that keypresses are available on
    the stream immediately, and they are not printed to the
    terminal. Typically, standard input is line-buffered, which means
    keypresses won't be sent until the user hits return. In this mode, a
    user can hit, e.g., 'v', and it will be read on the other end of the
    pipe immediately but not printed.

    The handler takes care to ensure that terminal changes only take
    effect when the calling process is in the foreground. If the process
    is backgrounded, canonical mode and echo are re-enabled. They are
    disabled again when the calling process comes back to the foreground.

    This context manager works through a single signal handler for
    ``SIGTSTP``, along with a poolling routine called ``check_fg_bg()``.
    Here are the relevant states, transitions, and POSIX signals::

        [Running] -------- Ctrl-Z sends SIGTSTP ------------.
        [ in FG ] <------- fg sends SIGCONT --------------. |
           ^                                              | |
           | fg (no signal)                               | |
           |                                              | v
        [Running] <------- bg sends SIGCONT ---------- [Stopped]
        [ in BG ]                                      [ in BG ]

    We handle all transitions exept for ``SIGTSTP`` generated by Ctrl-Z
    by periodically calling ``check_fg_bg()``.  This routine notices if
    we are in the background with canonical mode or echo disabled, or if
    we are in the foreground without canonical disabled and echo enabled,
    and it fixes the terminal settings in response.

    ``check_fg_bg()`` works *except* for when the process is stopped with
    ``SIGTSTP``.  We cannot rely on a periodic timer in this case, as it
    may not rrun before the process stops.  We therefore restore terminal
    settings in the ``SIGTSTP`` handler.

    Additional notes:

    * We mostly use polling here instead of a SIGARLM timer or a
      thread. This is to avoid the complexities of many interrupts, which
      seem to make system calls (like I/O) unreliable in older Python
      versions (2.6 and 2.7).  See these issues for details:

      1. https://www.python.org/dev/peps/pep-0475/
      2. https://bugs.python.org/issue8354

      There are essentially too many ways for asynchronous signals to go
      wrong if we also have to support older Python versions, so we opt
      not to use them.

    * ``SIGSTOP`` can stop a process (in the foreground or background),
      but it can't be caught. Because of this, we can't fix any terminal
      settings on ``SIGSTOP``, and the terminal will be left with
      ``ICANON`` and ``ECHO`` disabled until it is resumes execution.

    * Technically, a process *could* be sent ``SIGTSTP`` while running in
      the foreground, without the shell backgrounding that process. This
      doesn't happen in practice, and we assume that ``SIGTSTP`` always
      means that defaults should be restored.

    * We rely on ``termios`` support.  Without it, or if the stream isn't
      a TTY, ``keyboard_input`` has no effect.

    """
    def __init__(self, stream):
        """Create a context manager that will enable keyboard input on stream.

        Args:
            stream (file-like): stream on which to accept keyboard input

        Note that stream can be None, in which case ``keyboard_input``
        will do nothing.
        """
        self.stream = stream

    def _is_background(self):
        """True iff calling process is in the background."""
        return _is_background_tty(self.stream)

    def _get_canon_echo_flags(self):
        """Get current termios canonical and echo settings."""
        cfg = termios.tcgetattr(self.stream)
        return (
            bool(cfg[3] & termios.ICANON),
            bool(cfg[3] & termios.ECHO),
        )

    def _enable_keyboard_input(self):
        """Disable canonical input and echoing on ``self.stream``."""
        # "enable" input by disabling canonical mode and echo
        new_cfg = termios.tcgetattr(self.stream)
        new_cfg[3] &= ~termios.ICANON
        new_cfg[3] &= ~termios.ECHO

        # Apply new settings for terminal
        with ignore_signal(signal.SIGTTOU):
            termios.tcsetattr(self.stream, termios.TCSANOW, new_cfg)

    def _restore_default_terminal_settings(self):
        """Restore the original input configuration on ``self.stream``."""
        # _restore_default_terminal_settings Can be called in foreground
        # or background. When called in the background, tcsetattr triggers
        # SIGTTOU, which we must ignore, or the process will be stopped.
        with ignore_signal(signal.SIGTTOU):
            termios.tcsetattr(self.stream, termios.TCSANOW, self.old_cfg)

    def _tstp_handler(self, signum, frame):
        self._restore_default_terminal_settings()
        os.kill(os.getpid(), signal.SIGSTOP)

    def check_fg_bg(self):
        # old_cfg is set up in __enter__ and indicates that we have
        # termios and a valid stream.
        if not self.old_cfg:
            return

        # query terminal flags and fg/bg status
        flags = self._get_canon_echo_flags()
        bg = self._is_background()

        # restore sanity if flags are amiss -- see diagram in class docs
        if not bg and any(flags):    # fg, but input not enabled
            self._enable_keyboard_input()
        elif bg and not all(flags):  # bg, but input enabled
            self._restore_default_terminal_settings()

    def __enter__(self):
        """Enable immediate keypress input, while this process is foreground.

        If the stream is not a TTY or the system doesn't support termios,
        do nothing.
        """
        self.old_cfg = None
        self.old_handlers = {}

        # Ignore all this if the input stream is not a tty.
        if not self.stream or not self.stream.isatty():
            return self

        if termios:
            # save old termios settings to restore later
            self.old_cfg = termios.tcgetattr(self.stream)

            # Install a signal handler to disable/enable keyboard input
            # when the process moves between foreground and background.
            self.old_handlers[signal.SIGTSTP] = signal.signal(
                signal.SIGTSTP, self._tstp_handler)

            # add an atexit handler to ensure the terminal is restored
            atexit.register(self._restore_default_terminal_settings)

            # enable keyboard input initially (if foreground)
            if not self._is_background():
                self._enable_keyboard_input()

        return self

    def __exit__(self, exc_type, exception, traceback):
        """If termios was available, restore old settings."""
        if self.old_cfg:
            self._restore_default_terminal_settings()
            if sys.version_info >= (3,):
                atexit.unregister(self._restore_default_terminal_settings)

        # restore SIGSTP and SIGCONT handlers
        if self.old_handlers:
            for signum, old_handler in self.old_handlers.items():
                signal.signal(signum, old_handler)


class Unbuffered(object):
    """Wrapper for Python streams that forces them to be unbuffered.

    This is implemented by forcing a flush after each write.
    """
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


def _file_descriptors_work(*streams):
    """Whether we can get file descriptors for the streams specified.

    This tries to call ``fileno()`` on all streams in the argument list,
    and returns ``False`` if anything goes wrong.

    This can happen, when, e.g., the test framework replaces stdout with
    a ``StringIO`` object.

    We have to actually try this to see whether it works, rather than
    checking for the fileno attribute, beacuse frameworks like pytest add
    dummy fileno methods on their dummy file objects that return
    ``UnsupportedOperationErrors``.

    """
    # test whether we can get fds for out and error
    try:
        for stream in streams:
            stream.fileno()
        return True
    except BaseException:
        return False


class FileWrapper(object):
    """Represents a file. Can be an open stream, a path to a file (not opened
    yet), or neither. When unwrapped, it returns an open file (or file-like)
    object.
    """
    def __init__(self, file_like):
        # This records whether the file-like object returned by "unwrap" is
        # purely in-memory. In that case a subprocess will need to explicitly
        # transmit the contents to the parent.
        self.write_in_parent = False

        self.file_like = file_like

        if isinstance(file_like, string_types):
            self.open = True
        elif _file_descriptors_work(file_like):
            self.open = False
        else:
            self.file_like = None
            self.open = True
            self.write_in_parent = True

        self.file = None

    def unwrap(self):
        if self.open:
            if self.file_like:
                if sys.version_info < (3,):
                    self.file = open(self.file_like, 'w')
                else:
                    self.file = open(self.file_like, 'w', encoding='utf-8')  # novm
            else:
                self.file = StringIO()
            return self.file
        else:
            # We were handed an already-open file object. In this case we also
            # will not actually close the object when requested to.
            return self.file_like

    def close(self):
        if self.file:
            self.file.close()


class MultiProcessFd(object):
    """Return an object which stores a file descriptor and can be passed as an
       argument to a function run with ``multiprocessing.Process``, such that
       the file descriptor is available in the subprocess."""
    def __init__(self, fd):
        self._connection = None
        self._fd = None
        if sys.version_info >= (3, 8):
            self._connection = multiprocessing.connection.Connection(fd)
        else:
            self._fd = fd

    @property
    def fd(self):
        if self._connection:
            return self._connection._handle
        else:
            return self._fd

    def close(self):
        if self._connection:
            self._connection.close()
        else:
            os.close(self._fd)


def close_connection_and_file(multiprocess_fd, file):
    # MultiprocessFd is intended to transmit a FD
    # to a child process, this FD is then opened to a Python File object
    # (using fdopen). In >= 3.8, MultiprocessFd encapsulates a
    # multiprocessing.connection.Connection; Connection closes the FD
    # when it is deleted, and prints a warning about duplicate closure if
    # it is not explicitly closed. In < 3.8, MultiprocessFd encapsulates a
    # simple FD; closing the FD here appears to conflict with
    # closure of the File object (in < 3.8 that is). Therefore this needs
    # to choose whether to close the File or the Connection.
    if sys.version_info >= (3, 8):
        multiprocess_fd.close()
    else:
        file.close()


@contextmanager
def replace_environment(env):
    """Replace the current environment (`os.environ`) with `env`.

    If `env` is empty (or None), this unsets all current environment
    variables.
    """
    env = env or {}
    old_env = os.environ.copy()
    try:
        os.environ.clear()
        for name, val in env.items():
            os.environ[name] = val
        yield
    finally:
        os.environ.clear()
        for name, val in old_env.items():
            os.environ[name] = val


class log_output(object):
    """Context manager that logs its output to a file.

    In the simplest case, the usage looks like this::

        with log_output('logfile.txt'):
            # do things ... output will be logged

    Any output from the with block will be redirected to ``logfile.txt``.
    If you also want the output to be echoed to ``stdout``, use the
    ``echo`` parameter::

        with log_output('logfile.txt', echo=True):
            # do things ... output will be logged and printed out

    And, if you just want to echo *some* stuff from the parent, use
    ``force_echo``::

        with log_output('logfile.txt', echo=False) as logger:
            # do things ... output will be logged

            with logger.force_echo():
                # things here will be echoed *and* logged

    Under the hood, we spawn a daemon and set up a pipe between this
    process and the daemon.  The daemon writes our output to both the
    file and to stdout (if echoing).  The parent process can communicate
    with the daemon to tell it when and when not to echo; this is what
    force_echo does.  You can also enable/disable echoing by typing 'v'.

    We try to use OS-level file descriptors to do the redirection, but if
    stdout or stderr has been set to some Python-level file object, we
    use Python-level redirection instead.  This allows the redirection to
    work within test frameworks like nose and pytest.
    """

    def __init__(self, file_like=None, echo=False, debug=0, buffer=False,
                 env=None, filter_fn=None):
        """Create a new output log context manager.

        Args:
            file_like (str or stream): open file object or name of file where
                output should be logged
            echo (bool): whether to echo output in addition to logging it
            debug (int): positive to enable tty debug mode during logging
            buffer (bool): pass buffer=True to skip unbuffering output; note
                this doesn't set up any *new* buffering
            filter_fn (callable, optional): Callable[str] -> str to filter each
                line of output

        log_output can take either a file object or a filename. If a
        filename is passed, the file will be opened and closed entirely
        within ``__enter__`` and ``__exit__``. If a file object is passed,
        this assumes the caller owns it and will close it.

        By default, we unbuffer sys.stdout and sys.stderr because the
        logger will include output from executed programs and from python
        calls.  If stdout and stderr are buffered, their output won't be
        printed in the right place w.r.t. output from commands.

        Logger daemon is not started until ``__enter__()``.

        """
        self.file_like = file_like
        self.echo = echo
        self.debug = debug
        self.buffer = buffer
        self.env = env  # the environment to use for _writer_daemon
        self.filter_fn = filter_fn

        self._active = False  # used to prevent re-entry

    def __call__(self, file_like=None, echo=None, debug=None, buffer=None):
        """This behaves the same as init. It allows a logger to be reused.

        Arguments are the same as for ``__init__()``.  Args here take
        precedence over those passed to ``__init__()``.

        With the ``__call__`` function, you can save state between uses
        of a single logger.  This is useful if you want to remember,
        e.g., the echo settings for a prior ``with log_output()``::

            logger = log_output()

            with logger('foo.txt'):
                # log things; user can change echo settings with 'v'

            with logger('bar.txt'):
                # log things; logger remembers prior echo settings.

        """
        if file_like is not None:
            self.file_like = file_like
        if echo is not None:
            self.echo = echo
        if debug is not None:
            self.debug = debug
        if buffer is not None:
            self.buffer = buffer
        return self

    def __enter__(self):
        if self._active:
            raise RuntimeError("Can't re-enter the same log_output!")

        if self.file_like is None:
            raise RuntimeError(
                "file argument must be set by either __init__ or __call__")

        # set up a stream for the daemon to write to
        self.log_file = FileWrapper(self.file_like)

        # record parent color settings before redirecting.  We do this
        # because color output depends on whether the *original* stdout
        # is a TTY.  New stdout won't be a TTY so we force colorization.
        self._saved_color = tty.color._force_color
        forced_color = tty.color.get_color_when()

        # also record parent debug settings -- in case the logger is
        # forcing debug output.
        self._saved_debug = tty._debug

        # OS-level pipe for redirecting output to logger
        read_fd, write_fd = os.pipe()

        read_multiprocess_fd = MultiProcessFd(read_fd)

        # Multiprocessing pipe for communication back from the daemon
        # Currently only used to save echo value between uses
        self.parent_pipe, child_pipe = multiprocessing.Pipe()

        # Sets a daemon that writes to file what it reads from a pipe
        try:
            # need to pass this b/c multiprocessing closes stdin in child.
            input_multiprocess_fd = None
            try:
                if sys.stdin.isatty():
                    input_multiprocess_fd = MultiProcessFd(
                        os.dup(sys.stdin.fileno())
                    )
            except BaseException:
                # just don't forward input if this fails
                pass

            with replace_environment(self.env):
                self.process = multiprocessing.Process(
                    target=_writer_daemon,
                    args=(
                        input_multiprocess_fd, read_multiprocess_fd, write_fd,
                        self.echo, self.log_file, child_pipe, self.filter_fn
                    )
                )
                self.process.daemon = True  # must set before start()
                self.process.start()

        finally:
            if input_multiprocess_fd:
                input_multiprocess_fd.close()
            read_multiprocess_fd.close()

        # Flush immediately before redirecting so that anything buffered
        # goes to the original stream
        sys.stdout.flush()
        sys.stderr.flush()

        # Now do the actual output rediction.
        self.use_fds = _file_descriptors_work(sys.stdout, sys.stderr)
        if self.use_fds:
            # We try first to use OS-level file descriptors, as this
            # redirects output for subprocesses and system calls.

            # Save old stdout and stderr file descriptors
            self._saved_stdout = os.dup(sys.stdout.fileno())
            self._saved_stderr = os.dup(sys.stderr.fileno())

            # redirect to the pipe we created above
            os.dup2(write_fd, sys.stdout.fileno())
            os.dup2(write_fd, sys.stderr.fileno())
            os.close(write_fd)

        else:
            # Handle I/O the Python way. This won't redirect lower-level
            # output, but it's the best we can do, and the caller
            # shouldn't expect any better, since *they* have apparently
            # redirected I/O the Python way.

            # Save old stdout and stderr file objects
            self._saved_stdout = sys.stdout
            self._saved_stderr = sys.stderr

            # create a file object for the pipe; redirect to it.
            pipe_fd_out = os.fdopen(write_fd, 'w')
            sys.stdout = pipe_fd_out
            sys.stderr = pipe_fd_out

        # Unbuffer stdout and stderr at the Python level
        if not self.buffer:
            sys.stdout = Unbuffered(sys.stdout)
            sys.stderr = Unbuffered(sys.stderr)

        # Force color and debug settings now that we have redirected.
        tty.color.set_color_when(forced_color)
        tty._debug = self.debug

        # track whether we're currently inside this log_output
        self._active = True

        # return this log_output object so that the user can do things
        # like temporarily echo some ouptut.
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Flush any buffered output to the logger daemon.
        sys.stdout.flush()
        sys.stderr.flush()

        # restore previous output settings, either the low-level way or
        # the python way
        if self.use_fds:
            os.dup2(self._saved_stdout, sys.stdout.fileno())
            os.close(self._saved_stdout)

            os.dup2(self._saved_stderr, sys.stderr.fileno())
            os.close(self._saved_stderr)
        else:
            sys.stdout = self._saved_stdout
            sys.stderr = self._saved_stderr

        # print log contents in parent if needed.
        if self.log_file.write_in_parent:
            string = self.parent_pipe.recv()
            self.file_like.write(string)

        # recover and store echo settings from the child before it dies
        try:
            self.echo = self.parent_pipe.recv()
        except EOFError:
            # This may occur if some exception prematurely terminates the
            # _writer_daemon. An exception will have already been generated.
            pass

        # now that the write pipe is closed (in this __exit__, when we restore
        # stdout with dup2), the logger daemon process loop will terminate. We
        # wait for that here.
        self.process.join()

        # restore old color and debug settings
        tty.color._force_color = self._saved_color
        tty._debug = self._saved_debug

        self._active = False  # safe to enter again

    @contextmanager
    def force_echo(self):
        """Context manager to force local echo, even if echo is off."""
        if not self._active:
            raise RuntimeError(
                "Can't call force_echo() outside log_output region!")

        # This uses the xon/xoff to highlight regions to be echoed in the
        # output. We us these control characters rather than, say, a
        # separate pipe, because they're in-band and assured to appear
        # exactly before and after the text we want to echo.
        sys.stdout.write(xon)
        sys.stdout.flush()
        try:
            yield
        finally:
            sys.stdout.write(xoff)
            sys.stdout.flush()


def _writer_daemon(stdin_multiprocess_fd, read_multiprocess_fd, write_fd, echo,
                   log_file_wrapper, control_pipe, filter_fn):
    """Daemon used by ``log_output`` to write to a log file and to ``stdout``.

    The daemon receives output from the parent process and writes it both
    to a log and, optionally, to ``stdout``.  The relationship looks like
    this::

        Terminal
           |
           |          +-------------------------+
           |          | Parent Process          |
           +--------> |   with log_output():    |
           | stdin    |     ...                 |
           |          +-------------------------+
           |            ^             | write_fd (parent's redirected stdout)
           |            | control     |
           |            | pipe        |
           |            |             v read_fd
           |          +-------------------------+   stdout
           |          | Writer daemon           |------------>
           +--------> |   read from read_fd     |   log_file
             stdin    |   write to out and log  |------------>
                      +-------------------------+

    Within the ``log_output`` handler, the parent's output is redirected
    to a pipe from which the daemon reads.  The daemon writes each line
    from the pipe to a log file and (optionally) to ``stdout``.  The user
    can hit ``v`` to toggle output on ``stdout``.

    In addition to the input and output file descriptors, the daemon
    interacts with the parent via ``control_pipe``.  It reports whether
    ``stdout`` was enabled or disabled when it finished and, if the
    ``log_file`` is a ``StringIO`` object, then the daemon also sends the
    logged output back to the parent as a string, to be written to the
    ``StringIO`` in the parent. This is mainly for testing.

    Arguments:
        stdin_multiprocess_fd (int): input from the terminal
        read_multiprocess_fd (int): pipe for reading from parent's redirected
            stdout
        echo (bool): initial echo setting -- controlled by user and
            preserved across multiple writer daemons
        log_file_wrapper (FileWrapper): file to log all output
        control_pipe (Pipe): multiprocessing pipe on which to send control
            information to the parent
        filter_fn (callable, optional): function to filter each line of output

    """
    # If this process was forked, then it will inherit file descriptors from
    # the parent process. This process depends on closing all instances of
    # write_fd to terminate the reading loop, so we close the file descriptor
    # here. Forking is the process spawning method everywhere except Mac OS
    # for Python >= 3.8 and on Windows
    if sys.version_info < (3, 8) or sys.platform != 'darwin':
        os.close(write_fd)

    # Use line buffering (3rd param = 1) since Python 3 has a bug
    # that prevents unbuffered text I/O.
    if sys.version_info < (3,):
        in_pipe = os.fdopen(read_multiprocess_fd.fd, 'r', 1)
    else:
        # Python 3.x before 3.7 does not open with UTF-8 encoding by default
        in_pipe = os.fdopen(read_multiprocess_fd.fd, 'r', 1, encoding='utf-8')

    if stdin_multiprocess_fd:
        stdin = os.fdopen(stdin_multiprocess_fd.fd)
    else:
        stdin = None

    # list of streams to select from
    istreams = [in_pipe, stdin] if stdin else [in_pipe]
    force_echo = False      # parent can force echo for certain output

    log_file = log_file_wrapper.unwrap()

    try:
        with keyboard_input(stdin) as kb:
            while True:
                # fix the terminal settings if we recently came to
                # the foreground
                kb.check_fg_bg()

                # wait for input from any stream. use a coarse timeout to
                # allow other checks while we wait for input
                rlist, _, _ = _retry(select.select)(istreams, [], [], 1e-1)

                # Allow user to toggle echo with 'v' key.
                # Currently ignores other chars.
                # only read stdin if we're in the foreground
                if stdin in rlist and not _is_background_tty(stdin):
                    # it's possible to be backgrounded between the above
                    # check and the read, so we ignore SIGTTIN here.
                    with ignore_signal(signal.SIGTTIN):
                        try:
                            if stdin.read(1) == 'v':
                                echo = not echo
                        except IOError as e:
                            # If SIGTTIN is ignored, the system gives EIO
                            # to let the caller know the read failed b/c it
                            # was in the bg. Ignore that too.
                            if e.errno != errno.EIO:
                                raise

                if in_pipe in rlist:
                    line_count = 0
                    try:
                        while line_count < 100:
                            # Handle output from the calling process.
                            try:
                                line = _retry(in_pipe.readline)()
                            except UnicodeDecodeError:
                                # installs like --test=root gpgme produce non-UTF8 logs
                                line = '<line lost: output was not encoded as UTF-8>\n'

                            if not line:
                                return
                            line_count += 1

                            # find control characters and strip them.
                            clean_line, num_controls = control.subn('', line)

                            # Echo to stdout if requested or forced.
                            if echo or force_echo:
                                output_line = clean_line
                                if filter_fn:
                                    output_line = filter_fn(clean_line)
                                sys.stdout.write(output_line)

                            # Stripped output to log file.
                            log_file.write(_strip(clean_line))

                            if num_controls > 0:
                                controls = control.findall(line)
                                if xon in controls:
                                    force_echo = True
                                if xoff in controls:
                                    force_echo = False

                            if not _input_available(in_pipe):
                                break
                    finally:
                        if line_count > 0:
                            if echo or force_echo:
                                sys.stdout.flush()
                            log_file.flush()

    except BaseException:
        tty.error("Exception occurred in writer daemon!")
        traceback.print_exc()

    finally:
        # send written data back to parent if we used a StringIO
        if isinstance(log_file, StringIO):
            control_pipe.send(log_file.getvalue())
        log_file_wrapper.close()
        close_connection_and_file(read_multiprocess_fd, in_pipe)
        if stdin_multiprocess_fd:
            close_connection_and_file(stdin_multiprocess_fd, stdin)

        # send echo value back to the parent so it can be preserved.
        control_pipe.send(echo)


def _retry(function):
    """Retry a call if errors indicating an interrupted system call occur.

    Interrupted system calls return -1 and set ``errno`` to ``EINTR`` if
    certain flags are not set.  Newer Pythons automatically retry them,
    but older Pythons do not, so we need to retry the calls.

    This function converts a call like this:

        syscall(args)

    and makes it retry by wrapping the function like this:

        _retry(syscall)(args)

    This is a private function because EINTR is unfortunately raised in
    different ways from different functions, and we only handle the ones
    relevant for this file.

    """
    def wrapped(*args, **kwargs):
        while True:
            try:
                return function(*args, **kwargs)
            except IOError as e:
                if e.errno == errno.EINTR:
                    continue
                raise
            except select.error as e:
                if e.args[0] == errno.EINTR:
                    continue
                raise
    return wrapped


def _input_available(f):
    return f in select.select([f], [], [], 0)[0]