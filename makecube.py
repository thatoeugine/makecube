import json
import os

# Load parameter files
with open('params.json') as user_file:
    parsed_json = json.load(user_file)

# Define paths
PATH = parsed_json['directories']['OUTPUT_DIRECTORY']
CONTDIR = '/idia/software/containers/STIMELA_IMAGES/'  # Path to Stimela images

# Construct file paths
myms_file = os.path.join(PATH, parsed_json['directories']['MSFILE'])
myms = os.path.join(PATH, parsed_json['directories']['MSFILE'] + '.contsub')
chanbasename = os.path.join(
    PATH, f"channelmap-briggsrob{parsed_json['cube_imaging_params']['robust']}")
cubename = os.path.join(PATH, 'cube_COMBINED.fits')

# Continuum subtraction on visibilities
if parsed_json['settings']['douvsub']:
    uvsub_cmd = (
        f"singularity exec {CONTDIR}stimela_casa_1.2.6.sif casa -c casa_uvsubsub.py "
        f"--logfile logfile-uvsubsub.log --nogui myms={myms_file} "
        f"uvfitorder={parsed_json['uvsub_uvcontsub_params']['fitorder']}"
    )
    print(uvsub_cmd)
    os.system(uvsub_cmd)

# Imaging the spectral line
if parsed_json['settings']['doimagedata']:
    if parsed_json['cube_imaging_params']['use_tclean']:
        tclean_cmd = (
            f"singularity exec {CONTDIR}stimela_casa_1.2.6.sif casa -c tclean.py "
            f"--logfile logfile-tclean.log --nogui myms={myms} imgname={cubename} "
            f"cellsize={parsed_json['cube_imaging_params']['pixelsize']} "
            f"imagesize={parsed_json['cube_imaging_params']['imsize']} "
            f"rbs={parsed_json['cube_imaging_params']['robust']} "
            f"threshld={parsed_json['cube_imaging_params']['threshold']} "
            f"niters={parsed_json['cube_imaging_params']['niter']} "
            f"numchans={parsed_json['cube_imaging_params']['numchans']} "
            f"wdths={parsed_json['cube_imaging_params']['width']} "
            f"strt={parsed_json['cube_imaging_params']['start']}"
        )
        print(tclean_cmd)
        os.system(tclean_cmd)

    if parsed_json['cube_imaging_params']['use_wsclean']:
        wsclean_cmd = (
            f"singularity exec {CONTDIR}stimela_wsclean_1.2.3.sif wsclean -log-time -abs-mem 225 "
            f"-parallel-reordering 16 -make-psf -no-dirty -name {chanbasename} "
            f"-no-mf-weighting -no-update-model-required -data-column DATA -field 0 "
            f"-weight briggs {parsed_json['cube_imaging_params']['robust']} "
            f"-size {parsed_json['cube_imaging_params']['imsize']} {parsed_json['cube_imaging_params']['imsize']} "
            f"-scale {parsed_json['cube_imaging_params']['pixelsize']} "
            f"-channels-out {parsed_json['cube_imaging_params']['numchans']} "
            f"{myms}"
        )
        print(wsclean_cmd)
        os.system(wsclean_cmd)

        # Apply primary beam correction to images
        pbcor_cmd = (
            f"singularity exec / idia/software/containers/oxkat-0.41.sif python3 pbcor_katbeam.py --band U {PATH}*-image.fits")
        print(pbcor_cmd)
        os.system(pbcor_cmd)

        # Glue the FITS images into a cube
        glue_cmd = (
            f"singularity exec {CONTDIR}stimela_ddfacet_1.3.3.sif fitstool.py "
            f"--stack {cubename}:FREQ {PATH}*-image.pbcor.fits"
        )
        print(glue_cmd)
        os.system(glue_cmd)

# Continuum subtraction on the image cube
if parsed_json['settings']['doimcontsub']:
    for fitorder in parsed_json['imcontsub_params']['fitorder']:
        imcontsub_cmd = (
            f"singularity exec {CONTDIR}stimela_casa_1.2.6.sif casa -c casa_imcontsub.py "
            f"--logfile logfile-imcontsub.log --nogui mycube={cubename} "
            f"imfitorder={fitorder} channels={parsed_json['imcontsub_params']['chans']}"
        )
        print(imcontsub_cmd)
        os.system(imcontsub_cmd)
