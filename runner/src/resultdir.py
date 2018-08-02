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
        self.dir = join(parentdir, "_" + self.name)
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
        
        from collections import OrderedDict
        from common import assertmsg, fatalmsg
        
        assertmsg(len(keysOrValues) >= 2, "Output.add must receive at least 2 arguments")
        
        # decompose arguments
        keyPath = kwargs.get("subroot", []) + list(keysOrValues[:-1])   # last element of 'keysOrValues' is the value
        lastKey = keysOrValues[-2]  # used to store 'value', but also included in 'keyPath'
        value   = keysOrValues[-1]

        # perform insertion
        ob = self._findValueForPath(*keyPath)
        fmt = kwargs.get("format", None)
        ob[lastKey] = value if fmt is None else float(fmt.format(value))


    def get(self, *keyPath):
        
        return self._findValueForPath(keyPath)


    def addSummaryStatus(self, status, msg):
        
        self.add("summary", "status",     status)
        self.add("summary", "status msg", msg)
        

    def write(self):

        from os.path import join
        from spackle import writeYamlFile

        writeYamlFile(join(self.dir, "{}.yaml".format(self.name)), self.outdict)


    def _isCompatible(self, key, collection):
        
        from collections import OrderedDict
        from common import fatalmsg
    
        ktype, ctype = type(key), type(collection)
        
        if ktype is str:
            return ctype is dict or ctype is OrderedDict
        elif ktype is int:
            return ctype is list
        else:
            fatalmsg("ResultDir._isCompatible: invalid key type ({})".format(ktype))
    
    
    def _findValueForPath(self, *keyPath):
    
        ob = self.outdict
        for k, key in enumerate(keyPath[:-1]):    # last key in 'keyPath' is not traversed, but used to store given 'value'
            if self._isCompatible(key, ob):
                if key not in ob:
                    nextkey = keyPath[k+1]
                    ob[key] = self._collectionForKey(nextkey)
                ob = ob[key]
            else:
                fatalmsg("ResultDir: invalid key for current collection in key path")
        return ob
    
    
    def _collectionForKey(self, key):
    
        from collections import OrderedDict
        from common import fatalmsg
    
        ktype = type(key)
        
        if ktype is str:
            return OrderedDict()
        elif ktype is int:
            return list()
        else:
            fatalmsg("ResultDir._collectionForKey: invalid key type ({})".format(ktype))




