#!/usr/bin/env python3
"""Update address, map embed, and shared assets across all HTML pages."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OFFCANVAS_OLD = "1/287 D, Ashanpadi Kootayi Road, Paravanna, Malappuram, Tirur, Kerala, India, 676502."
OFFCANVAS_NEW = "15/972, Nedumkulangara Rd, Athani, Kakkanad, Kerala 682030"

ADDRESS_BLOCK_OLD = (
    '                    <motion class="ps-3">\n'
    '                        <span class="text-400 fs-5">Address</span>\n'
    '                        <p style="color: black;" class="mb-0"><b>1/287 D, Ashanpadi Kootayi Road , <br>Paravanna, Malappuram, Tirur ,<br> Kerala, India, 676502.</b></p>\n'
    "                    </div>\n"
    '                    <a href="https://maps.google.com/maps?q=1st+avenue,New+York" class="position-absolute top-0 start-0 w-100 h-100"></a>'
).replace("motion", "div")

ADDRESS_BLOCK_NEW = (
    '                    <motion class="ps-3">\n'
    '                        <span class="text-400 fs-5">Address</span>\n'
    '                        <p class="contact-address mb-0 fw-semibold">15/972, Nedumkulangara Rd,<br>Athani, Kakkanad,<br>Kerala 682030, India</p>\n'
    "                    </div>\n"
    '                    <a href="https://www.google.com/maps/search/?api=1&amp;query=Wisemove+consultancy+Kakkanad" '
    'class="position-absolute top-0 start-0 w-100 h-100" aria-label="Open WiseMove Consultancy on Google Maps" '
    'target="_blank" rel="noopener noreferrer"></a>'
).replace("motion", "div")

MAP_ROW = """
        <div class="row mt-5">
            <div class="col-12">
                <motion class="contact-map rounded-4 overflow-hidden">
                    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3928.9639526824176!2d76.3546886!3d10.0198334!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3b080db6053135d7%3A0x10a15d78b8d898fd!2sWisemove%20consultancy!5e0!3m2!1sen!2sin!4v1779099763434!5m2!1sen!2sin" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="WiseMove Consultancy — Kakkanad, Kerala"></iframe>
                </motion>
            </div>
        </div>
""".replace("motion", "div")

CSS_LINK = '<link rel="stylesheet" href="assets/css/site-overrides.css" />'
PRECONNECT = (
    '<link rel="preconnect" href="https://www.google.com" />\n'
    '<link rel="dns-prefetch" href="https://www.google.com" />\n'
)
MARKER_BEFORE_MAP = '    <div class="scroll-move-right position-absolute bottom-0'


def patch_html(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    text = text.replace(OFFCANVAS_OLD, OFFCANVAS_NEW)
    text = text.replace(
        f'<p class="mb-0">{OFFCANVAS_NEW}</p>',
        f'<p class="mb-0 offcanvas-address">{OFFCANVAS_NEW}</p>',
    )
    text = text.replace(ADDRESS_BLOCK_OLD, ADDRESS_BLOCK_NEW)

    if MARKER_BEFORE_MAP in text and "contact-map rounded-4" not in text:
        text = text.replace(MARKER_BEFORE_MAP, MAP_ROW + MARKER_BEFORE_MAP, 1)

    text = text.replace('href="tel:+1-234-567-8901"', 'href="tel:+919995333560"')
    text = text.replace('href="mailto:someone@example.com"', 'href="mailto:info@wisemoveconsultancy.com"')

    if CSS_LINK not in text:
        text = text.replace(
            '<link rel="stylesheet" href="assets/css/main.css" />',
            '<link rel="stylesheet" href="assets/css/main.css" />\n' + CSS_LINK,
        )

    if 'rel="preconnect" href="https://www.google.com"' not in text:
        text = text.replace("<head>", "<head>\n" + PRECONNECT, 1)

    if path.name == "index.html":
        text = text.replace("assets/images/", "assets/Images/")
        for img_path in [
            "assets/Images/202327061844_england_flag.jpg",
            "assets/Images/202327061844_germany_flag.jpg",
            "assets/Images/202327061844_ireland_flag.jpg",
            "assets/Images/Amerika Serikat.jpeg",
            "assets/Images/England.jpeg",
            "assets/Images/Girl.PNG",
            "assets/Images/girl 2.PNG",
        ]:
            old = f'src="{img_path}"'
            new = f'src="{img_path}" loading="lazy" decoding="async"'
            if old in text and new not in text:
                text = text.replace(old, new)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    updated = [html.name for html in sorted(ROOT.glob("*.html")) if patch_html(html)]
    print("Updated:", ", ".join(updated) if updated else "none")


if __name__ == "__main__":
    main()
