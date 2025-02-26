        import sys

# Parse command-line arguments
args = {}
for item in sys.argv[1:]:
    parts = item.split('=')
    if len(parts) == 2:  # Check if parts has both elements
        args[parts[0]] = parts[1]

# Set parameters with default values or provided values
myms = args.get('myms', None)
imgname = args.get('imgname', None)
cellsize = args.get('cellsize', "1.7arcsec")
imagesize = int(args.get('imagesize', 512))
rbs = float(args.get('rbs', 0.5))
threshld =  args.get('threshld', "1e-6Jy")
niters = int(args.get('niters', 80000))
numchans = int(args.get('numchans', -1))
wdths = args.get('wdths',None)
strt =  args.get('strt', None)



# Check if required parameters are provided
if myms is None or imgname is None:
    print("Error: Missing required parameters. Please provide values for myms and imgname.")
    sys.exit(1)

# Run tclean

tclean(vis=myms,
       imagename=imgname,
       datacolumn='corrected',
       specmode='cube',
       outframe='LSRK',
       deconvolver='hogbom',
       gridder='standard',
       imsize= imagesize,
       cell=cellsize,
       weighting='briggs',
       robust=rbs,
       restoringbeam='common',
       interactive=False,
       threshold=threshld,
       nchan = numchans,
       niter=niters,
       width = wdths,
       start = strt,
       phasecenter='J2000 13h15m39.55s +29d22m21.6s')
