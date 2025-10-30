from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

# ✅ Template inside assets folder
TEMPLATE_PATH = "assets/template.png"

def fit_text(draw, text, font_path, max_width, max_height, start_size=60):
    font_size = start_size
    font = ImageFont.truetype(font_path, font_size)
    w, h = draw.textsize(text, font=font)
    while (w > max_width or h > max_height) and font_size > 10:
        font_size -= 2
        font = ImageFont.truetype(font_path, font_size)
        w, h = draw.textsize(text, font=font)
    return font

@app.route("/api/card")
def card():
    name = request.args.get("name", "PLAYER")
    uid = request.args.get("uid", "0000000000")
    lvl = request.args.get("lvl", "00")
    guild = request.args.get("guild", "NONE")

    base = Image.open(TEMPLATE_PATH).convert("RGBA")
    draw = ImageDraw.Draw(base)
    width, height = base.size

    FONT_PATH = "arial.ttf"  # ya apna font path

    # Adjust these percentages according to your template
    name_box  = (width * 0.33, height * 0.20, width * 0.60, height * 0.35)
    uid_box   = (width * 0.33, height * 0.35, width * 0.60, height * 0.50)
    guild_box = (width * 0.33, height * 0.70, width * 0.70, height * 0.85)
    lvl_box   = (width * 0.85, height * 0.70, width * 0.98, height * 0.85)

    name_font  = fit_text(draw, name, FONT_PATH, name_box[2]-name_box[0], name_box[3]-name_box[1])
    uid_font   = fit_text(draw, f"UID {uid}", FONT_PATH, uid_box[2]-uid_box[0], uid_box[3]-uid_box[1], start_size=40)
    guild_font = fit_text(draw, guild, FONT_PATH, guild_box[2]-guild_box[0], guild_box[3]-guild_box[1], start_size=40)
    lvl_font   = fit_text(draw, f"Lv. {lvl}", FONT_PATH, lvl_box[2]-lvl_box[0], lvl_box[3]-lvl_box[1], start_size=40)

    draw.text((name_box[0], name_box[1]), name, font=name_font, fill=(255,255,255,255))
    draw.text((uid_box[0], uid_box[1]), f"UID {uid}", font=uid_font, fill=(200,200,200,255))
    draw.text((guild_box[0], guild_box[1]), guild, font=guild_font, fill=(255,255,255,255))
    draw.text((lvl_box[0], lvl_box[1]), f"Lv. {lvl}", font=lvl_font, fill=(255,255,255,255))

    img_io = io.BytesIO()
    base.save(img_io, "PNG")
    img_io.seek(0)
    return send_file(img_io, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
