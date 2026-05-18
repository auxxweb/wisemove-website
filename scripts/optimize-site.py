#!/usr/bin/env python3
"""Compress images, add SEO meta, lite assets on hub pages, local card images."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.wisemoveconsultancy.com"
OG_IMAGE = f"{SITE}/assets/Images/202327061844_canada_flag.jpg"

HEAVY_PAGES = {"index.html"}

SEO: dict[str, dict[str, str]] = {
    "index.html": {
        "title": "WiseMove Consultancy | Study Abroad Counselling in Kerala",
        "description": "WiseMove Consultancy in Kakkanad, Kerala — expert study abroad counselling for Canada, UK, Germany, Australia, USA. Profile evaluation, visas, IELTS/PTE prep.",
        "keywords": "study abroad consultancy kerala, wisemove consultancy, study in canada, study in uk, kakkanad education consultant",
    },
    "courses.html": {
        "title": "Study Abroad Courses | IT, MBA, Engineering, Nursing | WiseMove",
        "description": "Explore study abroad courses — Computer Science, Business, Engineering, Nursing, Data/AI, Hospitality and more. Course guidance from WiseMove Consultancy, Kerala.",
        "keywords": "study abroad courses, mba abroad, engineering abroad, nursing courses abroad, it courses overseas",
    },
    "services.html": {
        "title": "Study Abroad Services | Admissions, Visa, SOP | WiseMove Kerala",
        "description": "End-to-end study abroad services: profile evaluation, university shortlisting, SOP/LOR support, scholarships, visa guidance, and pre-departure briefing.",
        "keywords": "study abroad services, visa guidance kerala, sop writing, university shortlisting, education consultant kakkanad",
    },
    "destinations.html": {
        "title": "Study Destinations | Canada, UK, Germany, Australia | WiseMove",
        "description": "Compare top study destinations — Canada, UK, Germany, Ireland, Australia, New Zealand, USA. Country-wise guidance from WiseMove Consultancy.",
        "keywords": "study in canada, study in uk, study in germany, study in australia, study abroad destinations",
    },
    "testprep.html": {
        "title": "IELTS, PTE & Duolingo Coaching | WiseMove Consultancy",
        "description": "Prepare for IELTS, PTE, and Duolingo with WiseMove Consultancy. Structured test prep aligned with your study abroad timeline.",
        "keywords": "ielts coaching kerala, pte coaching, duolingo test prep, english test study abroad",
    },
    "about.html": {
        "title": "About WiseMove Consultancy | Study Abroad Experts in Kerala",
        "description": "Learn about WiseMove Consultancy — trusted study abroad guidance in Kerala with transparent counselling and student-first support.",
        "keywords": "about wisemove, study abroad consultancy kerala, education consultants malappuram kakkanad",
    },
    "ourteam.html": {
        "title": "Our Team | WiseMove Study Abroad Consultancy",
        "description": "Meet the WiseMove team — counsellors, admissions specialists, visa experts, and test prep trainers supporting your global education journey.",
        "keywords": "wisemove team, study abroad counsellors kerala",
    },
    "careers.html": {
        "title": "Careers at WiseMove Consultancy | Join Our Team",
        "description": "Career opportunities at WiseMove Consultancy in Kerala. Join our study abroad counselling and student support team.",
        "keywords": "wisemove careers, education consultant jobs kerala",
    },
    "blog-list.html": {
        "title": "Study Abroad Blog | Guides & Tips | WiseMove Consultancy",
        "description": "Read study abroad blogs — country guides, visa updates, scholarships, test prep tips, and student success insights from WiseMove.",
        "keywords": "study abroad blog, visa updates, scholarship guides, ielts tips",
    },
    "blog-details.html": {
        "title": "Study Abroad Article | WiseMove Consultancy Blog",
        "description": "In-depth study abroad articles and guides from WiseMove Consultancy — admissions, visas, and student life abroad.",
        "keywords": "study abroad article, education blog kerala",
    },
    "privacypolicy.html": {
        "title": "Privacy Policy | WiseMove Consultancy",
        "description": "Privacy Policy for WiseMove Consultancy — how we collect, use, and protect your personal information.",
        "keywords": "wisemove privacy policy",
    },
    "terms&conditions.html": {
        "title": "Terms & Conditions | WiseMove Consultancy",
        "description": "Terms and Conditions for using WiseMove Consultancy study abroad counselling services.",
        "keywords": "wisemove terms conditions",
    },
    "disclaimer.html": {
        "title": "Disclaimer | WiseMove Consultancy",
        "description": "Disclaimer for WiseMove Consultancy website and study abroad counselling information.",
        "keywords": "wisemove disclaimer",
    },
    "404.html": {
        "title": "Page Not Found | WiseMove Consultancy",
        "description": "The page you are looking for could not be found. Return to WiseMove Consultancy homepage.",
        "keywords": "404 wisemove",
    },
    "coming-soon.html": {
        "title": "Coming Soon | WiseMove Consultancy",
        "description": "This section is coming soon. Visit WiseMove Consultancy for study abroad counselling in Kerala.",
        "keywords": "wisemove coming soon",
    },
    "work.html": {
        "title": "WiseMove Consultancy",
        "description": "WiseMove Consultancy — study abroad guidance in Kerala.",
        "keywords": "wisemove consultancy",
    },
    "work-single.html": {
        "title": "WiseMove Consultancy",
        "description": "WiseMove Consultancy — study abroad guidance in Kerala.",
        "keywords": "wisemove consultancy",
    },
    "pricing.html": {
        "title": "WiseMove Consultancy",
        "description": "WiseMove Consultancy — study abroad guidance in Kerala.",
        "keywords": "wisemove consultancy",
    },
}

IMAGE_REPLACEMENTS: dict[str, list[tuple[str, str]]] = {
    "courses.html": [
        ("https://images.unsplash.com/photo-1518770660439-4636190af475", "assets/Images/computer and IT.jpg"),
        ("https://images.unsplash.com/photo-1556761175-4b46a572b786", "assets/Images/Businessmanagement.jpg"),
        ("https://futia.edu.ng/wp-content/uploads/2024/04/Mechanical-Engineering-Department-900x500.webp", "assets/Images/EngineeringProgramms.jpg"),
        ("https://www.venkateshwaragroup.in/vgiblog/wp-content/uploads/2024/04/BSc-Nursing-Fees.jpg", "assets/Images/Nursing and healthcare.jpg"),
    ],
    "services.html": [
        ("https://images.unsplash.com/photo-1521791136064-7986c2920216", "assets/Images/Profileevaluation.jpg"),
        ("https://www.edwiseinternational.com/blogs/img/choosing-the-right-university-to-study-abroad-in-Europe-1.webp", "assets/Images/University shortlisting.jpg"),
        ("https://images.unsplash.com/photo-1455390582262-044cdead277a", "assets/Images/soplorapplicationsupport.jpg"),
        ("https://swastikinternational.co.in/images/blog/blog005.jpg", "assets/Images/scholarshipguidance.jpg"),
        ("https://visadone.com/wp-content/uploads/2023/09/visa-application-form.jpg", "assets/Images/Visaguidance.jpg"),
        ("https://images.unsplash.com/photo-1522708323590-d24dbb6b0267", "assets/Images/post arrival support.jpg"),
        ("https://www.startupclubindia.com/public/images/products/1742024898-strategy-consulting.jpg", "assets/Images/Profileevaluation.jpg"),
    ],
    "destinations.html": [
        ("https://www.joinincampus.com/storage/newsletter/1606541072_Study_in_Canada.jpg", "assets/Images/202327061844_canada_flag.jpg"),
        ("https://images.unsplash.com/photo-1469474968028-56623f02e42e", "assets/Images/202327061844_england_flag.jpg"),
        ("https://cdn.sanity.io/images/nxpteyfv/goguides/2bf36f0d5bb919b4772603e6d8852f3fdc4bdd96-1600x1066.jpg", "assets/Images/202327061844_germany_flag.jpg"),
        ("https://assets.studies-overseas.com/Study_in_Australia_1f4284046b.png", "assets/Images/Hospitality.jpg"),
    ],
}

CSS_LITE = """<!-- Libs CSS -->
<link rel="stylesheet" href="assets/css/vendors/bootstrap.min.css" />
<link rel="stylesheet" href="assets/fonts/remixicon/remixicon.css" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;500;600;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="assets/css/main.css" />
<link rel="stylesheet" href="assets/css/site-overrides.css" />
<link rel="stylesheet" href="assets/css/page-lite.css" />"""

CSS_FULL_OPTIMIZED = """<!-- Libs CSS -->
<link rel="stylesheet" href="assets/css/vendors/bootstrap.min.css" />
<link rel="stylesheet" href="assets/css/vendors/swiper-bundle.min.css" />
<link rel="stylesheet" href="assets/css/vendors/aos.css" />
<link rel="stylesheet" href="assets/css/vendors/odometer.css" />
<link rel="stylesheet" href="assets/css/vendors/carouselTicker.css" />
<link rel="stylesheet" href="assets/css/vendors/magnific-popup.css" />
<link rel="stylesheet" href="assets/fonts/remixicon/remixicon.css" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;500;600;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="assets/css/main.css" />
<link rel="stylesheet" href="assets/css/site-overrides.css" />"""

SCRIPTS_LITE = """<!-- Libs JS (lite) -->
<script defer src="assets/js/vendors/jquery-3.7.1.min.js"></script>
<script defer src="assets/js/vendors/bootstrap.bundle.min.js"></script>
<script defer src="assets/js/vendors/aat.min.js"></script>
<script defer src="assets/js/main-lite.js"></script>"""

SCRIPTS_FULL = """<!-- Libs JS -->
<script defer src="assets/js/vendors/jquery-3.7.1.min.js"></script>
<script defer src="assets/js/vendors/bootstrap.bundle.min.js"></script>
<script defer src="assets/js/vendors/swiper-bundle.min.js"></script>
<script defer src="assets/js/vendors/aos.js"></script>
<script defer src="assets/js/vendors/wow.min.js"></script>
<script defer src="assets/js/vendors/smart-stick-nav.js"></script>
<script defer src="assets/js/vendors/jquery.magnific-popup.min.js"></script>
<script defer src="assets/js/vendors/gsap.min.js"></script>
<script defer src="assets/js/vendors/imagesloaded.pkgd.min.js"></script>
<script defer src="assets/js/vendors/isotope.pkgd.min.js"></script>
<script defer src="assets/js/vendors/ScrollTrigger.min.js"></script>
<script defer src="assets/js/vendors/jquery.carouselTicker.min.js"></script>
<script defer src="assets/js/vendors/jquery.odometer.min.js"></script>
<script defer src="assets/js/vendors/jquery.appear.js"></script>
<script defer src="assets/js/vendors/gsap-custom.js"></script>
<script defer src="assets/js/imageRevealHover.js"></script>
<script defer src="assets/js/vendors/aat.min.js"></script>
<script defer src="assets/js/main.js"></script>"""

WHATSAPP_OLD = 'src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg"'
WHATSAPP_NEW = 'src="assets/Images/whatsapp-icon.svg"'


def compress_images() -> int:
    count = 0
    images_dir = ROOT / "assets" / "Images"
    for path in images_dir.iterdir():
        if path.name.startswith("."):
            continue
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        if path.stat().st_size < 400_000:
            continue
        tmp = path.with_suffix(".opt.jpg")
        fmt = "jpeg" if path.suffix.lower() in {".jpg", ".jpeg", ".png"} else path.suffix.lower().replace(".", "")
        cmd = ["sips", "-Z", "1200", "-s", "format", fmt, "-s", "formatOptions", "78", str(path), "--out", str(tmp)]
        if fmt == "png":
            cmd = ["sips", "-Z", "1200", str(path), "--out", str(tmp.with_suffix(".png"))]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            if tmp.exists():
                tmp.replace(path)
                count += 1
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    return count


def build_meta(filename: str, data: dict[str, str]) -> str:
    url = f"{SITE}/" if filename == "index.html" else f"{SITE}/{filename}"
    title = data["title"]
    desc = data["description"]
    keywords = data["keywords"]
    return f"""<title>{title}</title>
<meta name="description" content="{desc}" />
<meta name="keywords" content="{keywords}" />
<meta name="author" content="WiseMove Consultancy" />
<meta name="robots" content="index, follow" />
<link rel="canonical" href="{url}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="WiseMove Consultancy" />
<meta property="og:locale" content="en_IN" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{OG_IMAGE}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{desc}" />
<meta name="twitter:image" content="{OG_IMAGE}" />
<meta name="theme-color" content="#6e4ef2" />"""


def inject_meta(content: str, filename: str) -> str:
    data = SEO.get(filename, SEO["about.html"])
    meta_block = build_meta(filename, data)
    content = re.sub(
        r"<meta name=\"description\"[^>]*>.*?<meta name=\"theme-color\"[^>]*/>\s*",
        "",
        content,
        count=1,
        flags=re.S,
    )
    content = re.sub(r"<title>.*?</title>\s*", "", content, count=1, flags=re.S)
    content = re.sub(
        r'(<meta name="viewport"[^>]*/>\s*)',
        r"\1" + meta_block + "\n",
        content,
        count=1,
    )
    return content


def replace_css_block(content: str, lite: bool) -> str:
    pattern = r"<!-- Libs CSS -->.*?<link rel=\"stylesheet\" href=\"assets/css/site-overrides.css\" />\n"
    replacement = (CSS_LITE if lite else CSS_FULL_OPTIMIZED) + "\n"
    if re.search(pattern, content, flags=re.S):
        return re.sub(pattern, replacement, content, count=1, flags=re.S)
    return content


def replace_scripts_block(content: str, lite: bool) -> str:
    pattern = r"<!-- Libs JS.*?<script defer src=\"assets/js/main(?:-lite)?\.js\"></script>\s*"
    replacement = (SCRIPTS_LITE if lite else SCRIPTS_FULL) + "\n"
    pattern = r"<!-- Libs JS.*?</script>\s*(?:<!-- Theme JS -->\s*)?<script defer src=\"assets/js/main(?:-lite)?\.js\"></script>\s*"
    return re.sub(pattern, replacement, content, count=1, flags=re.S)


def add_lazy_to_card_images(content: str) -> str:
    def repl(match: re.Match) -> str:
        tag = match.group(0)
        if "loading=" in tag:
            return tag
        return tag.replace("<img ", '<img loading="lazy" decoding="async" ', 1)

    return re.sub(r'<img class="card__image"[^>]*>', repl, content)


def patch_file(path: Path) -> list[str]:
    changes: list[str] = []
    name = path.name
    content = path.read_text(encoding="utf-8")
    original = content
    lite = name not in HEAVY_PAGES

    content = inject_meta(content, name)
    content = replace_css_block(content, lite)
    content = replace_scripts_block(content, lite)
    content = content.replace(WHATSAPP_OLD, WHATSAPP_NEW)

    if name in IMAGE_REPLACEMENTS:
        for old, new in IMAGE_REPLACEMENTS[name]:
            content = content.replace(old, new)
        content = add_lazy_to_card_images(content)
        changes.append("local-images")

    if content != original:
        path.write_text(content, encoding="utf-8")
    return changes


def main():
    n = compress_images()
    print(f"Compressed {n} large images")
    for html in sorted(ROOT.glob("*.html")):
        patch_file(html)
        print(f"patched {html.name}")


if __name__ == "__main__":
    main()
