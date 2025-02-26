import json
import os

# Loading parameter files
with open('params.json') as user_file:
    parsed_json = json.load(user_file)

# Define paths
PATH = parsed_json['directories']['OUTPUT_DIRECTORY']
CONTDIR = '/idia/software/containers/STIMELA_IMAGES/'  # Path to Stimela images

# Construct file paths
myms_file = os.path.join(PATH, parsed_json['directories']['MSFILE'])
myms = os.path.join(PATH, parsed_json['directories']['MSFILE'] + '.contsub')
chanbasename = os.path.join(PATH, 'channelmap-briggsrob%s' % parsed_json['cube_imaging_params']['robust'])
cubename = os.path.join(PATH, 'cube_COMBINED.fits')

# Continuum subtraction on visibilities
if parsed_json['settings']['douvsub']:
    uvsub_cmd = 'singularity exec %sstimela_casa_1.2.6.sif casa -c casa_uvsubsub.py --logfile logfile-uvsubsub.log --nogui myms=%s uvfitorder=%i' % (CONTDIR, myms_file, parsed_json['uvsub_uvcontsub_params']['fitorder'])
    print(uvsub_cmd)
    os.system(uvsub_cmd)

# Imaging the spectral line
if parsed_json['settings']['doimagedata']:
    if parsed_json['cube_imaging_params']['use_tclean']:
        tclean_cmd = 'singularity exec %sstimela_casa_1.2.6.sif casa -c tclean.py --logfile logfile-tclean.log --nogui myms=%s imgname=%s cellsize=%s imagesize=%i rbs=%s threshld=%s niters=%i numchans=%i wdths=%s strt=%s' % (CONTDIR, myms, cubename, parsed_json['cube_imaging_params']['pixelsize'], parsed_json['cube_imaging_params']['imsize'], parsed_json['cube_imaging_params']['robust'], parsed_json['cube_imaging_params']['threshold'], parsed_json['cube_imaging_params']['niter'], parsed_json['cube_imaging_params']['numchans'], parsed_json['cube_imaging_params']['width'], parsed_json['cube_imaging_params']['start'])
        print(tclean_cmd)
        os.system(tclean_cmd)
    
    if parsed_json['cube_imaging_params']['use_wsclean']:
        wsclean_cmd = 'singularity exec %sstimela_wsclean_1.2.3.sif wsclean -abs-mem 225 -name %s -data-column DATA -field 0 -weight briggs %s -size %i %i -scale %s -channels-out %i -niter %i -auto-threshold 0.5 -auto-mask 4 -no-update-model-required -gain 0.1 -mgain 0.95 -local-rms -baseline-averaging 4 -nwlayers-factor 5 -gain 0.15 -mgain 0.9 %s > log_makeChanMaps.txt' % (CONTDIR, chanbasename, parsed_json['cube_imaging_params']['robust'], parsed_json['cube_imaging_params']['imsize'], parsed_json['cube_imaging_params']['imsize'], parsed_json['cube_imaging_params']['pixelsize'], parsed_json['cube_imaging_params']['numchans'], parsed_json['cube_imaging_params']['niter'], myms)
        print(wsclean_cmd)
        os.system(wsclean_cmd)

        # Glue the fits images into a cube
        glue_cmd = "singularity exec %sstimela_ddfacet_1.3.3.sif fitstool.py --stack %s:FREQ %s*-image.fits" % (CONTDIR, cubename, PATH)
        print(glue_cmd)
        os.system(glue_cmd)

# Continuum subtraction on the image cube
if parsed_json['settings']['doimcontsub']:
    for fitorders in parsed_json['imcontsub_params']['fitorder']:
        imcontsub_cmd = 'singularity exec %sstimela_casa_1.2.6.sif casa -c casa_imcontsub.py --logfile logfile-imcontsub.log --nogui mycube=%s imfitorder=%i channels=%s' % (CONTDIR, cubename, fitorders, parsed_json['imcontsub_params']['chans'])
        print(imcontsub_cmd)
        os.system(imcontsub_cmd)
