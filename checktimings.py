#!/usr/bin/env python2

"""
COSMO TECHNICAL TESTSUITE

This script checks whether the standard output of the COSMO simulation
contains the words "CLEAN UP" which is indicative of a fully successful
simulation
"""

import sys
# private modules
sys.path.append("./tools") # this is the generic folder for subroutines
sys.path.append('../checktools/tools')
from ts_utilities import read_environ, dir_path

# information
__author__     = "Pascal Spoerri"
__copyright__  = "Copyright 2015, MeteoSwiss"
__license__    = "GPL"
__version__    = "1.0"

def check():
    from cosmo_timings import COSMO_Run
    env = read_environ()
    rundir = env['RUNDIR']
    cosmolog = env['LOGFILE']
    slurmlog = env['LOGFILE_SLURM']
    name = "Cosmo run in "+rundir
    data = COSMO_Run(folder=rundir, name=name, cosmolog=cosmolog, slurmlog=slurmlog)
    print(data)
if __name__ == "__main__":
    sys.exit(check())
