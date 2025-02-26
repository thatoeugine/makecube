#!/bin/bash
#file: /idia/projects/oh-mkt/thato_reductions/HATLAS1429/specline/oxkat/SCRIPTS/slurm_WSDMA028.sh:
#SBATCH --job-name=WSDMA028
#SBATCH --time=14-00:00:00
#SBATCH --partition=Main
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=232GB
#SBATCH --output=/idia/projects/oh-mkt/thato_reductions/HATLAS1429/specline/oxkat/cube_large_fov/slurm_WSDMA028.log
#SBATCH --exclude=highmem-003
SECONDS=0
singularity exec /idia/software/containers/oxkat-0.41.sif wsclean -log-time -abs-mem 225 -parallel-reordering 8 -name /idia/projects/oh-mkt/thato_reductions/HATLAS1429/specline/oxkat/cube_large_fov/IMAGES/img_1687191673_chan16500-16999_1024ch_H1429-0028.ms_centroid -save-source-list -data-column CORRECTED_DATA -field 0 -size 512 512 -scale 1.7asec -use-wgridder -no-update-model-required -weight briggs 0.5 -parallel-deconvolution 2560 -niter 80000 -gain 0.15 -mgain 0.9 -channel-range 218 357 -channels-out 139 -circular-beam -fits-mask /idia/projects/oh-mkt/thato_reductions/HATLAS1429/specline/oxkat/IMAGES/img_1687191673_chan16500-16999_1024ch_H1429-0028.ms_pcalmask-MFS-image.mask1.fits 1687191673_chan16500-16999_1024ch_H1429-0028.ms 



# Glue the fits images into a cube
singularity exec /idia/software/containers/STIMELA_IMAGES/stimela_ddfacet_1.3.3.sif fitstool.py --stack cube_COMBINED.fits:FREQ /idia/projects/oh-mkt/thato_reductions/HATLAS1429/specline/oxkat/cube_large_fov/IMAGES/*-image.fits






echo "****ELAPSED "$SECONDS" WSDMA028"
