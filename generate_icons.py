from PIL import Image, ImageDraw, ImageFont
import os

# Create icons folder
icons_dir = "icons"
os.makedirs(icons_dir, exist_ok=True)

# Feature names and colors
features = {
    "lms": (52, 152, 219),
    "library": (46, 204, 113),
    "bus": (241, 196, 15),
    "hostel": (230, 126, 34),
    "inventory": (155, 89, 182),
    "hr": (231, 76, 60),
    "biometric": (26, 188, 156)
}

# Generate PNG icons
for name, color in features.items():
    img = Image.new("RGBA", (128, 128), color)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    text = name.upper()[:5]

    # Pillow 10+ fix: use textbbox instead of textsize
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    draw.text(((128 - text_w) / 2, (128 - text_h) / 2), text, fill="white", font=font)
    img.save(os.path.join(icons_dir, f"{name}.png"))

print("✅ All icons have been generated in the 'icons' folder.")
