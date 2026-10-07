import sys
from PIL import Image, ImageEnhance
src = Image.open(sys.argv[1]).convert("RGB")
out = sys.argv[2]
W = src.width // 2
I=6
cells = [src.crop(((i%2)*W+I, (i//2)*W+I, (i%2)*W+W-I, (i//2)*W+W-I)) for i in range(4)]
W -= 2*I
def key(c):
    px = c.load(); a = Image.new("L", c.size); ap = a.load()
    for y in range(c.height):
        for x in range(c.width):
            r,g,b = px[x,y]
            bg = (r - g > 50 and b - g > 50)
            ap[x,y] = 0 if bg else 255
            if bg: px[x,y] = (10,10,14)
    return a
masks = [key(c) for c in cells]
for m in masks: print(m.getbbox())
h0 = masks[0].getbbox(); scale = 36 / (h0[3]-h0[1])
size = round(W*scale)
frames=[]
for c,m in zip(cells,masks):
    c = ImageEnhance.Contrast(c).enhance(1.15)
    s = c.resize((size,size), Image.Resampling.BOX)
    sm = m.resize((size,size), Image.Resampling.BOX).point(lambda v: 255 if v>=128 else 0)
    f = Image.new("RGB",(64,64),(205,205,205))
    f.paste(s,(-round(h0[0]*scale)+6, 13-round(h0[1]*scale)), sm)
    frames.append(f.quantize(32, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB"))
sheet = Image.new("RGB",(256,64))
for i,f in enumerate(frames): sheet.paste(f,(i*64,0))
sheet.resize((2048,512),Image.Resampling.NEAREST).save(out)
import pathlib
d = pathlib.Path("frames"); 
for i,f in enumerate(frames): f.save(d/f"doctor-run-{i+1}.png")
frames[0].save("review/doctor-run-cycle.gif", save_all=True, append_images=frames[1:], duration=250, loop=0)
big=[f.resize((512,512),Image.Resampling.NEAREST) for f in frames]
big[0].save("review/doctor-run-cycle-8x.gif", save_all=True, append_images=big[1:], duration=250, loop=0)
