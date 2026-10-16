# -*- coding: utf-8 -*-
# 重新生成 FileRenameManager 图标：优化中间双向(重命名)箭头为更纤细协调的造型
import os
from PIL import Image, ImageDraw

BASE_DIR = r"c:/projects/aardioProjects/FileRenameManager-aardio"
PREVIEW_DIR = os.path.join(BASE_DIR, "icon_src")
os.makedirs(PREVIEW_DIR, exist_ok=True)

N = 1024
SS = 2
W = N * SS

TOP    = (37, 99, 235)
BOTTOM = (6, 182, 212)
SHEET  = (255, 255, 255)
FOLD   = (219, 234, 254)
ARROW  = (29, 78, 216)

def gradient(w, h, c1, c2):
    small = Image.new("RGB", (64, 64))
    sp = small.load()
    for y in range(64):
        for x in range(64):
            t = (x + y) / (2 * 63)
            sp[x, y] = (int(c1[0]+(c2[0]-c1[0])*t), int(c1[1]+(c2[1]-c1[1])*t), int(c1[2]+(c2[2]-c1[2])*t))
    return small.resize((w, h), Image.BICUBIC).convert("RGBA")

def arrow(d, x0, y, x1, th, color, to_right=True):
    # 纤细箭杆(圆头) + 细长三角头，比例协调
    hl = th * 1.15          # 箭头长
    hw = th * 1.75          # 箭头宽
    if to_right:
        sx1 = x1 - hl + th * 0.5
        d.rounded_rectangle([x0, y - th/2, sx1, y + th/2], radius=th/2, fill=color)
        bx = x1 - hl
        d.polygon([(bx, y - hw/2), (bx, y + hw/2), (x1, y)], fill=color)
    else:
        sx0 = x0 + hl - th * 0.5
        d.rounded_rectangle([sx0, y - th/2, x1, y + th/2], radius=th/2, fill=color)
        bx = x0 + hl
        d.polygon([(bx, y - hw/2), (bx, y + hw/2), (x0, y)], fill=color)

# 1) 渐变圆角方块
img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
mask = Image.new("L", (W, W), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, W-1, W-1], radius=int(0.235*W), fill=255)
img.paste(gradient(W, W, TOP, BOTTOM), (0, 0), mask)
d = ImageDraw.Draw(img)

# 2) 白色文档 + 折角
sw, sh = 0.50*W, 0.60*W
sx0, sy0 = (W - sw)/2, (W - sh)/2 - 0.01*W
sx1, sy1 = sx0 + sw, sy0 + sh
fold = 0.16*sw
d.rounded_rectangle([sx0, sy0, sx1, sy1], radius=int(0.09*sw), fill=SHEET)
d.polygon([(sx1-fold, sy0), (sx1, sy0+fold), (sx1-fold, sy0+fold)], fill=FOLD)
d.line([(sx1-fold, sy0), (sx1-fold, sy0+fold), (sx1, sy0+fold)], fill=(191,219,254), width=int(0.012*W))

# 3) 重新设计的双向(重命名)箭头：更纤细、间距更舒展
ath = 0.058 * W                 # 箭杆粗细(比旧版更细)
ax0 = sx0 + 0.135 * sw
ax1 = sx1 - 0.135 * sw
cy  = (sy0 + sy1)/2 + 0.015*sw
gap = 0.235 * sw                # 两箭头中心距(更舒展)
arrow(d, ax0, cy - gap/2, ax1, ath, ARROW, to_right=True)
arrow(d, ax0, cy + gap/2, ax1, ath, ARROW, to_right=False)

# 4) 抗锯齿
base = img.resize((N, N), Image.LANCZOS)

# 5) 预览 + 覆盖 app.ico
base.resize((256,256), Image.LANCZOS).save(os.path.join(PREVIEW_DIR, "logo_256.png"))
base.save(os.path.join(PREVIEW_DIR, "logo_1024.png"))
sizes = [(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)]
base.resize((256,256), Image.LANCZOS).save(os.path.join(BASE_DIR, "app.ico"), format="ICO", sizes=sizes)
print("OK regenerated")
