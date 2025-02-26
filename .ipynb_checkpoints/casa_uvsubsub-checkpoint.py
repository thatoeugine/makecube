import sys
args = sys.argv
for item in sys.argv:
    parts = item.split('=')
    if parts[0] == 'myms':
        myms = parts[1]
    elif parts[0] == 'uvfitorder':
        uvfitorder = int(parts[1])

uvsub(vis=myms)
uvcontsub(vis=myms,fitorder=uvfitorder) #,fitspw='0:5~35;45~95')
