from PIL import Image, ImageDraw, ImageFont
from hashlib import sha256
import string


flag = 'WACon{??????????????????????????????????????????????????}'
assert len(flag) == 57
assert all(x in string.ascii_lowercase or x in string.digits for x in flag[6:-1])
# You can bruteforce locally. Plz do not bruteforce on server :p
assert sha256(flag.encode()).hexdigest() == '931f585a2d5d558ae8a76a44a10f7c2e08d6eebf0a21e8b263f527bbb7bc11b6'

R = 104
C = 1104
SIZE = 8
img = Image.new('L', (C, R),255)
d = ImageDraw.Draw(img)
fnt = ImageFont.truetype("./PublicSans-Regular.ttf", 30)
d.text((50, 35), text = flag, font = fnt, fill = 0)


for i in range(0, C, SIZE):
    for j in range(0, R, SIZE):
        color_tot = 0
        for c in range(i, i + SIZE):
            for r in range(j, j + SIZE):
                color_tot += img.getpixel((c, r))
                
        for c in range(i, i + SIZE):
            for r in range(j, j + SIZE):
                img.putpixel((c, r), color_tot // (SIZE * SIZE))

img.save('mosaic.png')            
        

