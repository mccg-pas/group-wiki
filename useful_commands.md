# Useful commands

## SLURM commands

- To submit jobs: `sbatch <jobname>`
- To cancel queued jobs: `scancel <jobid>`
- To view queue: `squeue -u <user>`
- To modify parameters of the job while in queue: `scontrol update jobid <jobid> <parameter>`
- To view job information: `scontrol show jobid <jobid>`  
- To view available nodes: `sinfo`

To modify the output of the `squeue` command, pass the `-o` flag.
For example:

```bash
$ squeue -o "%.10i %.50Z %.10P %.15j %.8u %8Q %.8T %.10M %.4C %.12l %.12L %.6D %.16S %R" -u tmason1
  JOBID                                           WORK_DIR  PARTITION            NAME     USER PRIORITY    STATE       TIME CPUS   TIME_LIMIT    TIME_LEFT  NODES       START_TIME NODELIST(REASON)
```

## PBS commands

- To submit jobs: `qsub <jobname>`
- To cancel jobs: `qdel <jobid>`
- To view queue: `qstat -u <user>`
 
## Supercomputer allocations

- On Raijin: `nci_account -P k96`
- On Magnus: `pawseyAccountBalance --users`
- On Stampede: `/usr/local/etc/taccinfo`

It may be useful to use an alias for these. Set `alias allocation=/usr/local/etc/taccinfo` in your ~./bashrc.


## Plot energies of optimisations in terminal

Faster than loading molden to view the progress of an optimisation.

```bash
alias plotmp2="grep 'E(MP2)' | sed '/NaN/d' | tr -s [:blank:] | cut -d ' ' -f 3 | gnuplot -e \"set terminal dumb; plot '-' with lines notitle\"" # Gamess MP2

alias plotfmo="grep 'E corr MP2(2)=' | tr -s [:blank:] | cut -d ' ' -f 10 | gnuplot -e \"set terminal dumb; plot '-' with lines notitle\"" # Gamess FMO

alias plotgauss="grep 'SCF Done' | tr -s [:blank:] | cut -d ' ' -f 6 | gnuplot -e \"set terminal dumb; plot '-' with lines notitle\"" # Gaussian opt

# To plot:
cat file.log | plotmp2
```
