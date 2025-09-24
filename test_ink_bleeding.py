from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont
import random, math

from Calli_Utils import add_ink_bleed_effect

def enrich_paper_texture(paper_base, grain_intensity=0.2, bleed_intensity=0.3, crosshatch=False):
    """叠加宣纸纹理与笔触渗化效果，增强纸张质感"""
    width, height = paper_base.size

    # 🌾 Rice paper grain (random speckles)
    grain = Image.new('L', (width, height), 255)
    draw = ImageDraw.Draw(grain)
    for _ in range(width * height // 800):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        radius = random.randint(1, 2)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=random.randint(180, 230))

    grain = grain.filter(ImageFilter.GaussianBlur(0.5))
    grain = ImageChops.multiply(grain, Image.new('L', (width, height), int(255 * grain_intensity)))
    grain_rgb = Image.merge('RGB', (grain, grain, grain))
    paper_base = ImageChops.multiply(paper_base, grain_rgb)

    # 🖌️ Brush bleed (soft radial ink diffusion)
    bleed = Image.new('L', (width, height), 255)
    draw = ImageDraw.Draw(bleed)
    for _ in range(10):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(30, 80)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=random.randint(100, 180))

    bleed = bleed.filter(ImageFilter.GaussianBlur(3.0))
    bleed = ImageChops.multiply(bleed, Image.new('L', (width, height), int(255 * bleed_intensity)))

    # debug
    bleed.save("debug_bleed.png")
    
    bleed_rgb = Image.merge('RGB', (bleed, bleed, bleed))
    paper_base = ImageChops.blend(paper_base, bleed_rgb)

    # 🧵 Optional crosshatch fibers
    if crosshatch:
        hatch = Image.new('L', (width, height), 255)
        draw = ImageDraw.Draw(hatch)
        for _ in range(width * height // 1000):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            length = random.randint(30, 100)
            angle = random.choice([0, math.pi / 2])  # horizontal or vertical
            for i in range(length):
                px = int(x1 + i * math.cos(angle))
                py = int(y1 + i * math.sin(angle))
                if 0 <= px < width and 0 <= py < height:
                    hatch.putpixel((px, py), random.randint(150, 200))
        hatch = hatch.filter(ImageFilter.GaussianBlur(1.0))
        hatch_rgb = Image.merge('RGB', (hatch, hatch, hatch))
        paper_base = ImageChops.multiply(paper_base, hatch_rgb)

    return paper_base

def apply_brush_bleed_overlay(base_image, bleed_intensity=0.3, num_bleeds=10):
    """在图像上叠加笔触渗化效果，使用透明层模拟墨迹扩散"""
    from PIL import Image, ImageDraw, ImageFilter

    width, height = base_image.size
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    for _ in range(num_bleeds):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(30, 80)
        alpha = int(255 * bleed_intensity)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(0, 0, 0, alpha))

    overlay = overlay.filter(ImageFilter.GaussianBlur(3.0))

    # Convert base to RGBA if needed
    if base_image.mode != 'RGBA':
        base_image = base_image.convert('RGBA')

    result = Image.alpha_composite(base_image, overlay)
    return result.convert('RGB')


# Step 1: Create base
paper_base = Image.new('RGB', (1400, 700), (242, 232, 212))

# Step 2: Draw text or seal
draw = ImageDraw.Draw(paper_base)
poem_font = ImageFont.truetype("simkai.ttf", 320)
draw.text((100, 100), "乾坤正气", font=poem_font, fill=(0, 0, 0))

# Step 3: Apply texture overlays
# paper_base = apply_brush_bleed_overlay(paper_base, bleed_intensity=0.15)
paper_base = add_ink_bleed_effect(paper_base, intensity=0.3)
paper_base.save("墨迹渗透效果.png")

