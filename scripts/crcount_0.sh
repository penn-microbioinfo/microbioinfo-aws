#!/bin/bash
#SBATCH --job-name=crcount_0
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=60g
#SBATCH --time=168:00:00
#SBATCH --partition=r5ad

bash run.bash
