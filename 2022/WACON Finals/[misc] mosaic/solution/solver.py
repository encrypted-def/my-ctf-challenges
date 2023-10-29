from PIL import Image, ImageDraw, ImageFont
from hashlib import sha256
import string
R = 104
C = 1104
SIZE = 8
img = Image.new('L', (C, R),255)
#flag = 'WACon{ifuwant2keepas3cretumusta1s0hyd3itfromy0ur5e1f1984}'
charset = string.ascii_lowercase + string.digits

img_mosaic = Image.open("mosaic.png")

def gen_mosaic_image(s):
    img = Image.new('L', (C, R),255)
    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype("./PublicSans-Regular.ttf", 30)
    d.text((50, 35), text = s, font = fnt, fill = 0)
    
    for i in range(0, C, SIZE):
        for j in range(0, R, SIZE):
            color_tot = 0
            for c in range(i, i + SIZE):
                for r in range(j, j + SIZE):
                    color_tot += img.getpixel((c, r))
                    
            for c in range(i, i + SIZE):
                for r in range(j, j + SIZE):
                    img.putpixel((c, r), color_tot // (SIZE * SIZE))    

    return img
# find next character
def go(s):
    cand = []
    for ch in charset:
        img = gen_mosaic_image(s + ch)
        # Find right most non-white pixel
        nonwhite_c = C-1
        while all(img.getpixel((nonwhite_c, i)) == 0xff for i in range(R)):
            nonwhite_c -= 8

        chk = True
        for c in range(0, nonwhite_c-7, SIZE):
            for r in range(0, R, SIZE):
                #print(img.getpixel((c, r)), img_mosaic.getpixel((c,r)))
                if img.getpixel((c, r)) != img_mosaic.getpixel((c,r)):
                    chk = False
                    break
        
        if chk:
            cand.append(ch)
    return cand

def dfs(s):
    print(s)
    if len(s) == 56:
        print("!!!!", s + "}")
    cand = go(s)
    for c in cand:
        dfs(s + c)
    return None

print(dfs("WACon{"))