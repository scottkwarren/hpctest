################################################################################
#                                                                              #
#  study.py                                                                    #
#  a collection of experimental runs with storage for their results            #
#                                                                              #
#  $HeadURL$                                                                   #
#  $Id$                                                                        #
#                                                                              #
#  --------------------------------------------------------------------------- #
#  Part of HPCToolkit (hpctoolkit.org)                                         #
#                                                                              #
#  Information about sources of support for research and development of        #
#  HPCToolkit is at 'hpctoolkit.org' and in 'README.Acknowledgments'.          #
#  --------------------------------------------------------------------------- #
#                                                                              #
#  Copyright ((c)) 2002-2017, Rice University                                  #
#  All rights reserved.                                                        #
#                                                                              #
#  Redistribution and use in source and binary forms, with or without          #
#  modification, are permitted provided that the following conditions are      #
#  met:                                                                        #
#                                                                              #
#  * Redistributions of source code must retain the above copyright            #
#    notice, this list of conditions and the following disclaimer.             #
#                                                                              #
#  * Redistributions in binary form must reproduce the above copyright         #
#    notice, this list of conditions and the following disclaimer in the       #
#    documentation and/or other materials provided with the distribution.      #
#                                                                              #
#  * Neither the name of Rice University (RICE) nor the names of its           #
#    contributors may be used to endorse or promote products derived from      #
#    this software without specific prior written permission.                  #
#                                                                              #
#  This software is provided by RICE and contributors "as is" and any          #
#  express or implied warranties, including, but not limited to, the           #
#  implied warranties of merchantability and fitness for a particular          #
#  purpose are disclaimed. In no event shall RICE or contributors be           #
#  liable for any direct, indirect, incidental, special, exemplary, or         #
#  consequential damages (including, but not limited to, procurement of        #
#  substitute goods or services; loss of use, data, or profits; or             #
#  business interruption) however caused and on any theory of liability,       #
#  whether in contract, strict liability, or tort (including negligence        #
#  or otherwise) arising in any way out of the use of this software, even      #
#  if advised of the possibility of such damage.                               #
#                                                                              #
################################################################################


# TEMPORARY: simplest possible thing: hold a path to the dir & just make run subdirs on request


# Naming convention for study top-level directories
_prefix = "study-"


class Study():   
    
    def __init__(self, path):
        
        from os import makedirs
        from os.path import basename, exists, isabs, isfile, isdir, join 
        from time import strftime
        import common
        from common import BadStudyPath

        path = path.rstrip("/")  # 'basename'== "" if trailing slash, => 'startswith' returns False
        if not isabs(path):
            path = join(common.homepath, path)
            
        if isdir(path) and basename(path).startswith(_prefix):
                self.path = path
        elif isdir(path):
            timestamp = strftime("%Y-%m-%d--%H-%M-%S")
            self.path = join(path, _prefix + timestamp)
            makedirs(self.path)
        else:
            raise BadStudyPath("bad path given for 'study'".format(path))
        
        self.resultDirs = dict()


    def __str__(self):

        return "Study@{}".format(self.path)
        

    @classmethod
    def isStudyDir(cls, path):
        
        from os.path import basename, isabs, isdir, join
        import common
        
        path = path.rstrip("/")  # 'basename'== "" if trailing slash, => 'startswith' returns False
        if not isabs(path):
            path = join(common.homepath, path)
        
        return isdir(path) and basename(path).startswith(_prefix)
    
    
    def addRunDir(self, description):

        import os
        from os.path import join, isdir

        # TODO: ensure uniqueness
        rundir = join(self.path, description.replace(" ", "_"))
        if isdir(rundir):
            n = 2
            while( isdir(rundir + "-" + str(n))): n += 1
            rundir = rundir + "-" + str(n)
        os.makedirs(rundir)
        
        return rundir


    def addResultDir(self, rundir, name):
        
        from resultdir import ResultDir
        
        rd = ResultDir(rundir, name)
        self.resultDirs[rundir] = rd
        return rd
    
        
    def clean(self):
        
        from shutil import rmtree
        rmtree(self.path, ignore_errors=True)


    def pathToRunDir(self, testName, build, profile):
        
        pass
    