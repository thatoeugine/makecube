#!/bin/bash
#SBATCH --job-name=Makecube
#SBATCH --time=14-00:00:00
#SBATCH --partition=HighMem
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=1500GB
#SBATCH --output=slurm_Makecube.log
SECONDS=0
python makecube.py
echo "****ELAPSED "$SECONDS" Makecube"