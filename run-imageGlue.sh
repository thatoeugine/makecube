#!/bin/bash
#SBATCH --job-name=imaGlue
#SBATCH --time=14-00:00:00
#SBATCH --partition=Main
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=230GB
#SBATCH --output=slurm_imGlue.log

SECONDS=0

python3 << EOF
import glob
import os

# Set paths
input_dir = "/idia/projects/oh-mkt/thato_reductions/HATLAS1429/broadband_cubes/SUBMSS/3/oxkat/cube/"
output_dir = "/idia/projects/oh-mkt/thato_reductions/HATLAS1429/broadband_cubes/SUBMSS/3/oxkat/"
container = "/idia/software/containers/STIMELA_IMAGES/stimela_ddfacet_1.3.3.sif"

# Change to input directory
os.chdir(input_dir)

# Get and sort the list of FITS files
fits_files = sorted(glob.glob("*-image.pbcor.fits"))

# Group sizes
full_group_size = 150
n_full_groups = len(fits_files) // full_group_size
remainder = len(fits_files) % full_group_size

groups = []

# Add full groups
for i in range(n_full_groups):
    start = i * full_group_size
    end = start + full_group_size
    groups.append(fits_files[start:end])

# Add remainder group
if remainder:
    groups.append(fits_files[-remainder:])

# Run stacking
for idx, group in enumerate(groups):
    fits_list = " ".join([os.path.join(input_dir, f) for f in group])
    output_cube = os.path.join(output_dir, f"cube_COMBINED{idx + 1}.fits")
    cmd = (
        f"singularity exec {container} fitstool.py --stack {output_cube}:FREQ {fits_list}"
    )
    print(f"Running group {idx + 1} ({len(group)} files):")
    os.system(cmd)
EOF