#!/bin/bash

# COSMO CHECK script
#
# This script run severals check (see testsuite checkers for more info)
# It is expected to be called from the COSMO run directory using single precision executable
# The script prints TEST RESULT : OK and return 0 or TEST RESULT : FAIL and return 1

# Author       Xavier Lapillonne
# Date         26.06.2015
# Mail         xavier.lapillonne@meteoswiss.ch

# Set variables
checktool_dir="../checktools"
status=0

# set environment variables for the checkers
export TS_RUNDIR="."
export TS_LOGFILE="lm_f90.out"
export TS_LOGFILE_SLURM="run.out"
export TS_VERBOSE=1
export TS_REFOUTDIR="./ref"
export TS_NAMELISTDIR="."
export TS_TOLERANCE="TOLERANCE_sp"
export TS_TIMINGS="TIMINGS_sp.cfg"
export TS_BASEDIR="."
export TS_FORCEMATCH="TRUE"

# run checkers
${checktool_dir}/run_success_check.py
if [ $? -gt 15 ]; then
    echo "run_success_check : fail"
    status=1
fi
${checktool_dir}/output_tolerance_check.py
if [ $? -gt 15 ]; then
    echo "output_tolerance_check : fail"
    status=1
fi

${checktool_dir}/checktimings.py
if [ $? -gt 15 ]; then
    echo "checktimings : fail"
    status=1
fi

if [ ${status} == 0 ]; then
    echo TEST RESULT: OK
else
    echo TEST RESULT: FAIL
fi

exit $status



