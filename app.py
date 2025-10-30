from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)

TEMPLATE_PATH = "assets/template.png"
FONT_PATH = "fonts/Montserrat-Regular.ttf"  # you can change font
if not os.path.exists(FONT_PATH):
    FONT_PATH = None  # use default font if not found

@app.route("/api/card")
def generate_card():
    # Get parameters
    name = request.args.get("name", "K BABACHOP")
    uid = request.args.get("uid", "8181818188")
    lvl = request.args.get("lvl", "84")
    guild = request.args.get("guild", "GUILD. MORAL")

    # Load template
    base = Image.open(TEMPLATE_PATH).convert("RGBA")

    # Draw text
    draw = ImageDraw.Draw(base)

    # Setup fonts
    try:
        font_big = ImageFont.truetype(FONT_PATH, 48)
        font_mid = ImageFont.truetype(FONT_PATH, 28)
        font_small = ImageFont.truetype(FONT_PATH, 22)
    except:
        font_big = font_mid = font_small = ImageFont.load_default()

    # Coordinates (you can fine-tune later)
    name_pos = (320, 60)
    uid_pos = (320, 120)
    guild_pos = (320, 210)
    lvl_pos = (850, 210)

    # Name
    draw.text(name_pos, name.upper(), font=font_big, fill=(255, 255, 255, 255))
    # UID
    draw.text(uid_pos, f"UID: {uid}", font=font_mid, fill=(220, 220, 220, 255))
    # Guild
    draw.text(guild_pos, guild.upper(), font=font_small, fill=(255, 255, 255, 255))
    # Level
    draw.text(lvl_pos, f"Lv. {lvl}", font=font_small, fill=(255, 255, 255, 255))

    # Save to bytes
    img_bytes = io.BytesIO()
    base.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return send_file(img_bytes, mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)