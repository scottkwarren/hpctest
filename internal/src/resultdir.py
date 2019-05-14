################################################################################
#                                                                              #
#  output.py                                                                   #
#  preserve files and metrics output by running a job                          #
#                                                                              #                                                                              #
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


from common import options, debugmsg



class ResultDir():
    
    def __init__(self, parentdir, name):

        from collections import OrderedDict
        from os import makedirs
        from os.path import join

        self.name = name
        self.dir = join(parentdir, self.name)
        makedirs(self.dir)
        self.outdict = OrderedDict()
        self.numOutfiles = 0


    def __contains__(self, key):
        
        return key in self.outdict
        
    
    def getDir(self):

        return self.dir
        
    
    def makePath(self, nameFmt, label=None):

        from os.path import join

        self.numOutfiles += 1
        path = join(self.dir, ("{:02d}-" + nameFmt).format(self.numOutfiles, label))
        return path


    def add(self, *keysOrValues, **kwargs):
        
        from common import assertmsg, setValueAtKeypath
        assertmsg(len(keysOrValues) >= 2, "Output.add must receive at least 2 arguments")
        
        keypath = kwargs.get("subroot", []) + list(keysOrValues[:-1])   # last element of 'keysOrValues' is value to store
        value   = keysOrValues[-1]
        setValueAtKeypath(self.outdict, keypath, value)


    def get(self, *keypath):    # returns None if keyPath not in results
        
        from common import getValueAtKeypath
        return getValueAtKeypath(self.outdict, keypath)


    def addSummaryStatus(self, status, msg):
        
        self.add("summary", "status",     status)
        self.add("summary", "status msg", msg)
        

    def write(self):

        from os.path import join
        from spackle import writeYamlFile

        writeYamlFile(join(self.dir, "{}.yaml".format(self.name)), self.outdict)







