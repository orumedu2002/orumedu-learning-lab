"""Create an original 16:9 editorial illustration for the Learning Lab post."""
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path

W, H = 1600, 900
im = Image.new("RGB", (W, H), "#071523")
d = ImageDraw.Draw(im, "RGBA")

# Quiet editorial background and desk plane.
d.rectangle((0, 0, W, H), fill="#081724")
d.ellipse((-280, -190, 720, 770), fill=(22, 76, 111, 72))
d.ellipse((980, -240, 1870, 650), fill=(32, 67, 106, 46))
d.polygon([(0, 670), (1600, 575), (1600, 900), (0, 900)], fill=(9, 28, 43, 255))
d.line((0, 670, 1600, 575), fill=(111, 159, 188, 80), width=2)

# A single calm figure, looking toward the viewer, with no logo or text.
d.ellipse((1012, 140, 1328, 466), fill=(20, 38, 53, 255))  # hair silhouette
d.ellipse((1047, 175, 1293, 432), fill=(203, 148, 120, 255))  # face
d.ellipse((1067, 205, 1274, 306), fill=(22, 38, 49, 255))  # hair fringe
d.ellipse((1088, 288, 1110, 304), fill=(17, 26, 34, 255))
d.ellipse((1238, 288, 1260, 304), fill=(17, 26, 34, 255))
d.arc((1135, 318, 1200, 365), 10, 165, fill=(111, 58, 51, 230), width=4)
d.polygon([(1010, 435), (1319, 435), (1445, 780), (875, 780)], fill=(25, 54, 76, 255))
d.polygon([(1082, 440), (1180, 545), (1270, 440)], fill=(242, 237, 226, 245))

# Subtle EEG sensor arcs only as non-diagnostic contextual visual language.
for x, y in [(1070, 200), (1132, 172), (1196, 168), (1254, 199)]:
    d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=(68, 172, 226, 255))
    d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(236, 246, 250, 255))
d.arc((1053, 150, 1280, 353), 188, 349, fill=(66, 170, 224, 150), width=3)

# Screen and abstract task cues; intentionally no readable text or medical data.
d.rounded_rectangle((190, 230, 805, 600), radius=26, fill=(14, 37, 55, 255), outline=(100, 173, 211, 170), width=3)
d.rounded_rectangle((220, 264, 775, 535), radius=16, fill=(235, 241, 239, 255))
d.ellipse((300, 335, 376, 411), fill=(24, 108, 158, 255))
d.rounded_rectangle((432, 336, 654, 376), radius=18, fill=(30, 50, 65, 220))
d.rounded_rectangle((432, 404, 590, 433), radius=14, fill=(112, 145, 162, 190))
d.rounded_rectangle((432, 457, 696, 486), radius=14, fill=(112, 145, 162, 150))
d.line((410, 611, 610, 611), fill=(141, 188, 213, 210), width=10)
d.polygon([(450, 611), (570, 611), (640, 720), (375, 720)], fill=(17, 43, 61, 255))

# Desk notebook and a human hand toward it.
d.rounded_rectangle((650, 684, 1005, 818), radius=12, fill=(229, 225, 213, 255))
d.line((690, 724, 966, 724), fill=(74, 119, 145, 105), width=4)
d.line((690, 760, 906, 760), fill=(74, 119, 145, 75), width=4)
d.ellipse((970, 700, 1080, 758), fill=(201, 144, 116, 255))
d.polygon([(1010, 745), (1115, 690), (1140, 740), (1045, 785)], fill=(201, 144, 116, 255))

# Fine neutral lines at left: one observation channel, not a score.
points = [(92, 500), (120, 490), (148, 517), (177, 463), (208, 507), (238, 500), (268, 530), (300, 485), (328, 499)]
d.line(points, fill=(61, 179, 232, 170), width=4)

# Gentle film texture.
noise = Image.effect_noise((W, H), 9).convert("L")
noise = noise.point(lambda p: 30 if p > 140 else 0)
texture = Image.new("RGBA", (W, H), (190, 218, 230, 0))
texture.putalpha(noise)
im = Image.alpha_composite(im.convert("RGBA"), texture).convert("RGB")
im = im.filter(ImageFilter.GaussianBlur(radius=0.25))
out = Path("assets/images/2026-08-30-eeg-task-is-not-learning-verdict-thumbnail.png")
im.save(out, optimize=True)
print(out, im.size, im.width / im.height)
