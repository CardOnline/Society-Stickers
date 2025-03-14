import qrcode
import qrcode.image.svg  # ✅ Import SVG support
import os
import re

# ✅ Ensure the output folder exists
output_folder = "stickers"
os.makedirs(output_folder, exist_ok=True)

# ✅ Function to generate QR sticker with embedded SVG QR code
def generate_qr_sticker(flat_number, sticker_id, access_link):
    """Generates a QR sticker as an SVG file with an embedded QR code (SVG format)."""

    # ✅ Generate QR Code in SVG format
    factory = qrcode.image.svg.SvgImage
    qr = qrcode.make(access_link, image_factory=factory)

    # ✅ Save QR code as SVG (temporary file)
    qr_svg_path = f"{output_folder}/{sticker_id}_qr.svg"
    with open(qr_svg_path, "w", encoding="utf-8") as qr_svg_file:
        qr_svg_file.write(qr.to_string().decode("utf-8"))  # ✅ FIXED: Decode bytes to string

    # ✅ Read QR SVG content (Remove XML declaration)
    with open(qr_svg_path, "r", encoding="utf-8") as qr_svg_file:
        qr_svg_content = qr_svg_file.read()

    # ✅ Remove XML declaration to avoid multiple `<?xml ... ?>`
    qr_svg_content = re.sub(r'<\?xml.*?\?>', '', qr_svg_content, flags=re.DOTALL).strip()

    # ✅ Create Final Sticker SVG with Embedded QR Code & Additional Elements
    svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <svg width="3in" height="3in" viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg">
        <!-- Background -->
        <rect width="100%" height="100%" fill="white" stroke="black" stroke-width="3"/>

        <!-- Big Red Exclamation Mark (LEFT side, CENTERED) -->
        <text x="40" y="150" font-size="150" fill="red" font-weight="bold" text-anchor="middle" dominant-baseline="middle">!</text>

        <!-- QR Code (PERFECTLY CENTERED) -->
        <g transform="translate(60,60) scale(1.4)">
            {qr_svg_content}
        </g>

        <!-- Society Name (Above QR, Centered) -->
        <text x="150" y="30" font-size="20" text-anchor="middle" fill="black" font-weight="bold">Anubandh</text>

        <!-- Society Location (Below Society Name) -->
        <text x="150" y="55" font-size="15" text-anchor="middle" fill="black">Pune - 411030</text>

        <!-- Flat Number (Below QR, Centered) -->
        <text x="150" y="270" font-size="20" text-anchor="middle" fill="black" font-weight="bold">{flat_number}</text>

        <!-- Sticker ID (Below Flat Number) -->
        <text x="150" y="290" font-size="15" text-anchor="middle" fill="black">ID: {sticker_id}</text>
    </svg>
    """

    # ✅ Save Final Sticker SVG
    svg_filename = f"{output_folder}/{sticker_id}.svg"
    with open(svg_filename, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"✅ Sticker generated: {svg_filename}")

    return svg_filename

# ✅ Example usage
if __name__ == "__main__":
    generate_qr_sticker(flat_number="A-101", sticker_id="123456", access_link="https://yourdomain.com/access/123456")
