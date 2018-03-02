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

        from os import listdir
        from os.path import isfile, isdir, join, basename, relpath
        from common import homepath, options, debugmsg, fatalmsg, sepmsg
        from spackle import readYamlFile, writeYamlFile
        
        debugmsg("reporting on workspace at {} with options {}".format(workspace.path, options))
    
        reportAll = True    # TODO: get from command line
        
        # collect the results from all the jobs
        results = list()
        for jobname in listdir(workspace.path):
            jobPath = join(workspace.path, jobname)
            outPath = join(jobPath, "_OUT", "OUT.yaml")
            if isfile(outPath):
                resultdict, error = readYamlFile(outPath)
                if error: fatalmsg("result file OUT.yaml cannot be read for test job {}".format(jobPath))
                if reportAll or resultdict["summary"]["status"] != "OK":
                    results.append(resultdict)
            else:
                fatalmsg("Test results file OUT.yaml not found for job {}".format(jobPath))
                        
        # print a summary record for each result, sorted by config spec and then test name
        results.sort(key=lambda result: result["input"]["config spec"])
        for result in results:
            
            # extract job data for reporting
            test           = relpath(result["input"]["test"], join(homepath, "tests")).upper()
            config         = result["input"]["config spec"].upper()
            status         = result["summary"]["status"]
            msg            = result["summary"]["status msg"] if status != "OK" else ""
            overhead       = result["run"]["profiled"]["hpcrun overhead %"]
            hpcrun         = result["run"]["profiled"]["hpcrun summary"]
            if hpcrun != "NA":
                blocked    = hpcrun["blocked"]
                errant     = hpcrun["errant"]
                frames     = hpcrun["frames"]
                intervals  = hpcrun["intervals"]
                recorded   = hpcrun["recorded"]
                samples    = hpcrun["samples"]
                suspicious = hpcrun["suspicious"]
                trolled    = hpcrun["trolled"]
                yielded    = hpcrun["yielded"]
            else:
                blocked    = "----"
                errant     = "----"
                frames     = "----"
                intervals  = "----"
                recorded   = "----"
                samples    = "----"
                suspicious = "----"
                trolled    = "----"
                yielded    = "----"
            
            # format for display           
            line1 = "| {} with {}:  {}{}".format(test, config, status, (", " + msg) if msg != "" else "")
            line2 = ("| overhead: {:>5} | recorded: {:>5} | blocked: {:>5} | errant: {:>5} | suspicious: {:>5} | trolled: {:>5} |"
                    ).format(_pct(overhead, 100), _pct(recorded, samples), _pct(blocked, samples), _pct(errant, samples), _pct(suspicious, samples), _pct(trolled, samples))         
            line1 += " " * (len(line2) - len(line1) - 1) + "|"

            # print job's summary
            sepmsg(len(line1))
            print line1
            print line2
            
        sepmsg(len(line1))


def _pct(s, d):
    
    if type(s) is str:
        formatted = "{:>5}".format(s)
    else:
        percent = (float(s) / float(d)) * 100.0
        formatted = "    0" if s == 0 else (" < 1%" if percent < 1.0 else "{:>5.1f} %".format(percent))
        
    return formatted


    
    
    
    
    
    
    

