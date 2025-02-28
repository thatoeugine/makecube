
This Python module automates the process of radio astronomy data reduction and imaging using the Stimela framework. It reads parameters from a JSON file (`params.json`) and performs the following tasks:

1. **Continuum Subtraction on Visibilities**: If enabled, it runs a CASA script (`casa_uvsubsub.py`) to subtract the continuum from the visibility data.
2. **Imaging the Spectral Line**: Depending on the configuration, it uses either `tclean` or `wsclean` to create spectral line images from the visibility data.
3. **Glue FITS Images into a Cube**: If `wsclean` is used, it stacks the resulting FITS images into a data cube.
4. **Continuum Subtraction on the Image Cube**: If enabled, it runs a CASA script (`casa_imcontsub.py`) to subtract the continuum from the image cube.

The module constructs and executes command-line commands using Singularity containers to ensure a consistent software environment.
