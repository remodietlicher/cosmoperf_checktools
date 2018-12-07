import argparse
import matplotlib.pyplot as plt
import numpy as np
import sys
# private modules
sys.path.append("./tools") # this is the generic folder for subroutines
sys.path.append('../checktools/tools')
from cosmo_timings import COSMO_Run
from ts_utilities import read_environ, dir_path
import os

def init_parser():
    parser = argparse.ArgumentParser(description='visualize difference for local timers of 2 COSMO runs')
    parser.add_argument('benchmark_dirs', metavar='D', type=str, nargs=2, help='benchmark output files to compare') 

    return parser

def load_timings(benchmark_dir, cosmolog='lm_f90.out', slurmlog='exe.log'):
    name = "Cosmo run in "+benchmark_dir
    return COSMO_Run(folder=benchmark_dir, name=name, cosmolog=cosmolog, slurmlog=slurmlog)

def main(args):
    timings = [load_timings(b) for b in args.benchmark_dirs]
        
    tshow = ['total', 'timeloop max', 'physics max', 'phy_eps max', 'phy_copy_block max', 'phy_microphysics max', 'phy_radiation max', 'phy_turbulence max', 'phy_soil max']

    fig, axes = plt.subplots(ncols=1, nrows=3, figsize=(8,8), sharex=True)

    t0 = timings[0]
    t1 = timings[1]

    v0 = np.array([float(t0[n]) for n in tshow])
    v1 = np.array([float(t1[n]) for n in tshow])

    x = np.arange(0, len(tshow))

    dirs = [d.split('/')[-2] for d in args.benchmark_dirs]

    axes[0].set_title('%s - %s'%(dirs[1], dirs[0]))

    axes[0].bar(x-0.2, v0, width=0.4, align='center', label=dirs[0])
    axes[0].bar(x+0.2, v1, width=0.4, align='center', label=dirs[1])
    axes[0].set_ylabel('absolute times / s')
    axes[0].legend()

    axes[1].bar(x, v1-v0, width=0.4, align='center')
    axes[1].set_ylabel('time difference / s')

    axes[2].bar(x, (v1-v0)/v0*100, width=0.4, align='center')
    axes[2].set_ylabel('time difference / %')

    axes[-1].set_xticks(x)
    axes[-1].set_xticklabels(tshow)

    for tick in axes[-1].get_xticklabels():
        tick.set_rotation(45)

    plt.tight_layout()
    plt.show()
    

if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args()

    main(args)
