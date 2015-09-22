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
from ts_fortran_nl import get_param

# information
__author__     = "Pascal Spoerri"
__copyright__  = "Copyright 2015, MeteoSwiss"
__license__    = "GPL"
__version__    = "1.0"

def parse():
    from cosmo_timings import COSMO_Run
    env = read_environ()
    rundir = env['RUNDIR']
    cosmolog = env['LOGFILE']
    slurmlog = env['LOGFILE_SLURM']
    name = "Cosmo run in "+rundir
    return COSMO_Run(folder=rundir, name=name, cosmolog=cosmolog, slurmlog=slurmlog)

def get_reference_timings():
    import ConfigParser
    config = ConfigParser.RawConfigParser()
    timings_file = env['TIMINGS']
    config.read(rundir+"/"+timings_file)

    threshold = float(config.get('timings', 'threshold'))
    timings = {}
    for name, value in config.items("timings"):
        if name is "threshold":
            continue
        timings[name] = float(value)
    return (timings, threshold)

def check_value(reference, value, threshold=0):
    if value < (reference*(1.0+threshold/100.0)):
        return True
    return False

def check():
    data = parse()
    print(data)
    timings, threshold = get_reference_timings()
    status = 0
    for name, timing in timings.iteritems():
        data_timing = data[name]
        if name in data and not check_value(timing, data_timing, threshold=threshold):
            print("Fail: Could not validate "+name+": timing"+data_timing+"(reference timing: "+timing+")")
            status = 40
    return status
if __name__ == "__main__":
    sys.exit(check())
