#!/usr/bin/env bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
##SBATCH --cpus-per-task=1
#SBATCH --partition=RM-small
#SBATCH --time=00:30:00
#SBATCH --output=log.out
#SBATCH --account=che240027p

#lammps="/ocean/projects/che240027p/ssaha4/softwares/bin/lmp_mpi_mbx"
module reset
module load intelmpi/2021.3.0-intel2021.3.0 gcc/10.2.0
#lammps="/ocean/projects/che240027p/ssaha4/softwares/bin/lmp_mpi_mbx"
lammps="/ocean/projects/che240027p/shared/software/Team_UCSD/lammps_exe/lmp"
mpirun -n 1 $lammps -in lmp.in -log log.lammps

