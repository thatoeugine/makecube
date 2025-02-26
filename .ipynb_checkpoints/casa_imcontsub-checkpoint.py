import sys

# Parse command-line arguments
args = {}
for item in sys.argv[1:]:
    parts = item.split('=')
    if len(parts) == 2:  # Check if parts has both elements
        args[parts[0]] = parts[1]

# Set parameters with default values or provided values
mycube = args.get('mycube', None)
imfitorder = int(args.get('imfitorder', None))
channels = args.get('channels', None)




#mycubecasa = mycubefits + '.im'                                                
#importfits(fitsimage=mycubefits,imagename=mycubecasa)
imcontsub(imagename = mycube, fitorder = imfitorder, 
          linefile = mycube+'fitorder-'+str(imfitorder)+'.linefile',
          contfile = mycube+'fitorder-'+str(imfitorder)+'.contfile' ,chans=channels)


exportfits(imagename=mycube+'fitorder-'+str(imfitorder)+'.linefile',
           fitsimage=mycube+'fitorder-'+str(imfitorder)+'.linefile.fits')
