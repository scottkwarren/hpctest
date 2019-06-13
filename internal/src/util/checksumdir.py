"""
Adapted from GitHub project https://github.com/cakepietoast/checksumdir:

Function for deterministically creating a single hash for a directory of files,
taking into account only file contents and not filenames.

Usage:
from checksumdir import dirhash
dirhash('/path/to/directory', 'md5')


The MIT License (MIT)
Copyright (c) 2015 cakepietoast

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import os
import hashlib
import re

HASH_FUNCS = {
    'md5': hashlib.md5,
    'sha1': hashlib.sha1,
    'sha256': hashlib.sha256,
    'sha512': hashlib.sha512
}


def dirhash(dirname, hashfunc='md5', excluded_files=None, ignore_hidden=False,
            followlinks=False, excluded_extensions=None):
    hash_func = HASH_FUNCS.get(hashfunc)
    if not hash_func:
        raise NotImplementedError('{} not implemented.'.format(hashfunc))

    if not excluded_files:
        excluded_files = []

    if not excluded_extensions:
        excluded_extensions = []

    if not os.path.isdir(dirname):
        raise TypeError('{} is not a directory.'.format(dirname))
    hashvalues = []
    for root, dirs, files in os.walk(dirname, topdown=True, followlinks=followlinks):
        if ignore_hidden:
            if not re.search(r'/\.', root):
                hashvalues.extend(
                    [_filehash(os.path.join(root, f),
                               hash_func) for f in files if not
                     f.startswith('.') and not re.search(r'/\.', f)
                     and f not in excluded_files
                     and f.split('.')[-1:][0] not in excluded_extensions
                     ]
                )
        else:
            hashvalues.extend(
                [
                    _filehash(os.path.join(root, f), hash_func) 
                    for f in files 
                    if f not in excluded_files
                    and f.split('.')[-1:][0] not in excluded_extensions
                ]
            )
    return _reduce_hash(hashvalues, hash_func)


def _filehash(filepath, hashfunc):
    hasher = hashfunc()
    blocksize = 64 * 1024
    with open(filepath, 'rb') as fp:
        while True:
            data = fp.read(blocksize)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


def _reduce_hash(hashlist, hashfunc):
    hasher = hashfunc()
    for hashvalue in sorted(hashlist):
        hasher.update(hashvalue.encode('utf-8'))
    return hasher.hexdigest()
