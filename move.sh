#!/bin/bash
#file: /idia/projects/oh-mkt/thato_reductions/HATLAS1429/specline/oxkat/SCRIPTS/slurm_WSDMA028.sh:
#SBATCH --job-name=WSDMA028
#SBATCH --time=14-00:00:00
#SBATCH --partition=Main
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=5
#SBATCH --mem=10GB
#SBATCH --exclude=highmem-003
SECONDS=0

# Define the source and destination directories
source_dir="/idia/projects/oh-mkt/thato_reductions/HATLAS1429/HELP/HELP_J160314/oxkat/cube/cube201-400"
destination_dir="/idia/projects/oh-mkt/thato_reductions/HATLAS1429/HELP/HELP_J160314/oxkat/cube/cube401-600"

# Move files in the specified range
for i in $(seq -w 0401 0600); do
    mv "${source_dir}/channelmap-briggsrob0.5-${i}-image.fits" "${destination_dir}/"
done
