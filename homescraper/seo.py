from __future__ import annotations

import re
from html import escape
from urllib.parse import quote


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def property_meta(*, address: str, city: str, county: str, property_type: str | None = None) -> dict[str, str]:
    """Create SEO metadata only from supplied facts.

    This helper intentionally does not infer prices, condition, investment returns,
    neighborhood quality, or seller circumstances.
    """
    location = ", ".join(part for part in (city, county) if part)
    subject = " | ".join(part for part in (property_type, location) if part)
    title = f"{address} — Property Research{(' | ' + subject) if subject else ''}"
    description = f"Source-traceable property research for {address}{(' in ' + location) if location else ''}."
    return {
        "title": title[:60],
        "description": description[:160],
        "slug": slugify(address),
        "canonical": f"/property/{quote(slugify(address))}",
    }


def json_ld_property(*, name: str, url: str, address: str, city: str, region: str = "IL") -> str:
    """Return conservative schema.org JSON-LD without inventing unavailable facts."""
    import json

    data = {
        "@context": "https://schema.org",
        "@type": "Place",
        "name": name,
        "url": url,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": address,
            "addressLocality": city,
            "addressRegion": region,
        },
    }
    return json.dumps(data, separators=(",", ":"))


def render_breadcrumbs(items: list[tuple[str, str]]) -> str:
    links = " / ".join(
        f'<a href="{escape(url)}">{escape(label)}</a>' for label, url in items
    )
    return f'<nav aria-label="Breadcrumb">{links}</nav>'
