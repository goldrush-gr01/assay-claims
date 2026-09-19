"""poidh #1404: a 1989-style handheld start screen for poidh. 160x144, four DMG greens.
Every glyph and the camera are hand-drawn bitmaps below. Outputs: screen.png (native),
screen-x8.png (nearest-neighbour x8), dmg.png (x8 with LCD grid inside a grey handheld surround)."""
import sys, os
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
W, H = 160, 144
PAL = [(155, 188, 15), (139, 172, 15), (48, 98, 48), (15, 56, 15)]   # 0 light .. 3 dark
px = [[0] * W for _ in range(H)]

def put(x, y, c):
    if 0 <= x < W and 0 <= y < H: px[y][x] = c

def blit(bitmap, x0, y0, scale=1, ink=3, shades=None):
    """bitmap: list of equal-length strings. '#'=ink, '+', '-' = extra shades, '.' = transparent."""
    shades = shades or {'#': ink, '+': 2, '-': 1}
    for j, row in enumerate(bitmap):
        for i, ch in enumerate(row):
            if ch == '.': continue
            for dy in range(scale):
                for dx in range(scale):
                    put(x0 + i * scale + dx, y0 + j * scale + dy, shades[ch])

# --- 3x5 caps font -------------------------------------------------------------------------
F = {
'A': ".#. #.# ### #.# #.#", 'B': "##. #.# ##. #.# ##.", 'C': ".## #.. #.. #.. .##", 'D': "##. #.# #.# #.# ##.",
'E': "### #.. ##. #.. ###", 'F': "### #.. ##. #.. #..", 'G': ".## #.. #.# #.# .##", 'H': "#.# #.# ### #.# #.#",
'I': "### .#. .#. .#. ###", 'J': "..# ..# ..# #.# .#.", 'K': "#.# #.# ##. #.# #.#", 'L': "#.. #.. #.. #.. ###",
'M': "#.# ### ### #.# #.#", 'N': "##. #.# #.# #.# #.#", 'O': ".#. #.# #.# #.# .#.", 'P': "##. #.# ##. #.. #..",
'Q': ".#. #.# #.# .## ..#", 'R': "##. #.# ##. #.# #.#", 'S': ".## #.. .#. ..# ##.", 'T': "### .#. .#. .#. .#.",
'U': "#.# #.# #.# #.# ###", 'V': "#.# #.# #.# #.# .#.", 'W': "#.# #.# ### ### #.#", 'X': "#.# #.# .#. #.# #.#",
'Y': "#.# #.# .#. .#. .#.", 'Z': "### ..# .#. #.. ###",
'0': "### #.# #.# #.# ###", '1': ".#. ##. .#. .#. ###", '2': "##. ..# .#. #.. ###", '3': "### ..# .## ..# ###",
'4': "#.# #.# ### ..# ..#", '5': "### #.. ##. ..# ##.", '6': ".## #.. ### #.# ###", '7': "### ..# .#. .#. .#.",
'8': "### #.# ### #.# ###", '9': "### #.# ### ..# ##.",
"'": ".#. .#. ... ... ...", ' ': "... ... ... ... ...", '(': ".#. #.. #.. #.. .#.", ')': ".#. ..# ..# ..# .#.",
'.': "... ... ... ... .#.", '-': "... ... ### ... ...", ':': "... .#. ... .#. ...", '!': ".#. .#. .#. ... .#.",
}
def text(s, x, y, scale=1, ink=3):
    for ch in s:
        blit(F[ch].split(' '), x, y, scale, ink)
        x += 4 * scale
def text_w(s, scale=1): return (len(s) * 4 - 1) * scale

# --- the word "poidh", lowercase, 11 rows (3 ascender, 5 x-height, 3 descender) ---------------
GLYPH = {
'p': ["......", "......", "......", "#####.", "##..##", "##..##", "##..##", "#####.", "##....", "##....", "##...."],
'o': ["......", "......", "......", ".####.", "##..##", "##..##", "##..##", ".####.", "......", "......", "......"],
'i': ["##", "##", "..", "##", "##", "##", "##", "##", "..", "..", ".."],
'd': ["....##", "....##", "....##", ".#####", "##..##", "##..##", "##..##", ".#####", "......", "......", "......"],
'h': ["##....", "##....", "##....", "#####.", "##..##", "##..##", "##..##", "##..##", "......", "......", "......"],
}
def word(s, x, y, scale, ink):
    for ch in s:
        blit(GLYPH[ch], x, y, scale, ink)
        x += (len(GLYPH[ch][0]) + 1) * scale
def word_w(s, scale): return (sum(len(GLYPH[c][0]) + 1 for c in s) - 1) * scale

# --- pixel camera, 16x11: '#' outline, '+' body, '-' highlight/flash -------------------------
CAMERA = [
"...####....##...",
"################",
"#+++.#####.++++#",
"#+++#+++++#+--+#",
"#+++#+-+++#+--+#",
"#+++#++#++#++++#",
"#+++#+++++#++++#",
"#+++#+++++#++++#",
"#+++.#####.++++#",
"#++++++++++++++#",
"################",
]
SPARK5 = ["..#..", "..#..", "#####", "..#..", "..#.."]
SPARK3 = [".#.", "###", ".#."]

# --- compose the screen --------------------------------------------------------------------
# double frame
for x in range(3, W - 3): put(x, 3, 3); put(x, H - 4, 3)
for y in range(3, H - 3): put(3, y, 3); put(W - 4, y, 3)
for x in range(6, W - 6): put(x, 6, 1); put(x, H - 7, 1)
for y in range(6, H - 6): put(6, y, 1); put(W - 7, y, 1)
for (cx, cy) in [(3, 3), (W - 6, 3), (3, H - 6), (W - 6, H - 6)]:       # corner blocks
    for dy in range(3):
        for dx in range(3): put(cx + dx, cy + dy, 3)

S = 3
tx = (W - word_w('poidh', S)) // 2
word('poidh', tx + S, 16 + S, S, 2)        # shadow
word('poidh', tx, 16, S, 3)                # ink

tag = "PICS OR IT DIDN'T HAPPEN"
text(tag, (W - text_w(tag)) // 2, 54, 1, 2)

cx = (W - 16 * S) // 2
blit(CAMERA, cx, 66, S)
blit(SPARK5, cx + 16 * S + 6, 68, 1, 2)
blit(SPARK3, cx + 16 * S + 13, 62, 1, 1)

ps = "PRESS START"
text(ps, (W - text_w(ps, 2)) // 2, 108, 2, 3)
cr = "(C) 1989 POIDH"
text(cr, (W - text_w(cr)) // 2, 128, 1, 2)

# --- outputs -------------------------------------------------------------------------------
img = Image.new('RGB', (W, H))
img.putdata([PAL[c] for row in px for c in row])
img.save(os.path.join(OUT, 'screen.png'))
big = img.resize((W * 8, H * 8), Image.NEAREST)
big.save(os.path.join(OUT, 'screen-x8.png'))

# LCD grid: darken a 1px seam between cells
lcd = big.copy(); d = ImageDraw.Draw(lcd, 'RGBA')
for x in range(0, W * 8, 8): d.line([(x, 0), (x, H * 8)], fill=(0, 0, 0, 34))
for y in range(0, H * 8, 8): d.line([(0, y), (W * 8, y)], fill=(0, 0, 0, 34))

# grey handheld surround
CW, CH_ = 1600, 1440
canvas = Image.new('RGB', (CW, CH_), (30, 30, 32))
d = ImageDraw.Draw(canvas)
d.rounded_rectangle([40, 40, CW - 40, CH_ - 40], radius=70, fill=(78, 78, 82), outline=(110, 110, 114), width=3)
sx, sy = (CW - W * 8) // 2, 200
d.rounded_rectangle([sx - 14, sy - 14, sx + W * 8 + 14, sy + H * 8 + 14], radius=10, fill=(40, 40, 42))
canvas.paste(lcd, (sx, sy))
# two coloured stripes and the display legend
d.rectangle([sx, 108, sx + 720, 118], fill=(93, 63, 150)); d.rectangle([sx, 124, sx + 720, 134], fill=(158, 45, 97))
fnt = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 28)
d.text((sx + 750, 104), "DOT MATRIX WITH FOUR GREENS", font=fnt, fill=(215, 215, 220))
fsm = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 22)
d.ellipse([sx - 92, sy + 300, sx - 72, sy + 320], fill=(200, 30, 30))
d.text((sx - 118, sy + 330), "BATTERY", font=fsm, fill=(215, 215, 220))
canvas.save(os.path.join(OUT, 'dmg.png'))
print('wrote screen.png screen-x8.png dmg.png in', OUT)
