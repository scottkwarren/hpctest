################################################################################
#                                                                              #
#  report.py                                                                   #
#  print the results from running a test suite by extracting from a testdir    #
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




class Report():
    
    @classmethod
    def printReport(myclass, workspace):

        from os.path import isfile, isdir, join 
        from common import options, debugmsg, sepmsg
        from spackle import readYamlFile
        
        sepmsg(True)
        sepmsg(True)
        debugmsg("reporting on workspace at {} with options {}".format(workspace.path, options), always=True)  # TEMPORARY

        return
    
        reportAll = True    # TODO: get from command line
        
        # collect the results from all the jobs
        results =  set()
        for workname in listdir(workspace.path):
            workPath = join(workspace.path, workname)
            if isdir(workPath) and workname.startswith("workspace-"):
                for jobname in listdir(workspace.path):
                    jobPath = join(workspace.path, jobname)
                    outPath = join(jobPath, "_OUT", "OUT.yaml")
                    if isfile(outPath):
                        resultdict, error = readYamlFile(outPath)   # HANDLE 'error' !!!
                        if reportAll or resultdict["summary"]["status"] != "OK":
                            results.add(resultdict)
                    else:
                        fatalmsg("Test results file OUT.yaml not found for job {}".format(jobPath))
                        
        # xxx
            
                



