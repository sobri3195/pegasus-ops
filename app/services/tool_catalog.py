from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from math import ceil


@dataclass(frozen=True, slots=True)
class ToolSpec:
    slug: str
    name: str
    category: str


TOOL_SPECS: tuple[ToolSpec, ...] = (
    ToolSpec("video-cutter", "Video cutter", "Media"),
    ToolSpec("video-merger", "Video merger", "Media"),
    ToolSpec("audio-extractor", "Audio extractor", "Media"),
    ToolSpec("subtitle-generator", "Subtitle generator", "Media"),
    ToolSpec("thumbnail-resizer", "Thumbnail resizer", "Media"),
    ToolSpec("image-compressor", "Image compressor", "Media"),
    ToolSpec("background-remover", "Background remover", "Media"),
    ToolSpec("watermark-tool", "Watermark tool", "Media"),
    ToolSpec("image-format-converter", "Image format converter", "Media"),
    ToolSpec("caption-generator", "Caption generator", "Creator"),
    ToolSpec("hashtag-generator", "Hashtag generator", "Creator"),
    ToolSpec("content-calendar", "Content calendar", "Creator"),
    ToolSpec("bio-generator", "Bio generator", "Creator"),
    ToolSpec("link-in-bio-builder", "Link in bio builder", "Creator"),
    ToolSpec("reply-template-manager", "Reply template manager", "Creator"),
    ToolSpec("engagement-tracker", "Engagement tracker", "Creator"),
    ToolSpec("content-idea-scheduler", "Content idea scheduler", "Creator"),
    ToolSpec("title-generator", "Title generator", "Creator"),
    ToolSpec("keyword-clustering", "Keyword clustering", "Creator"),
    ToolSpec("trend-notes-board", "Trend notes board", "Creator"),
    ToolSpec("json-formatter", "JSON formatter", "Developer"),
    ToolSpec("jwt-decoder", "JWT decoder", "Developer"),
    ToolSpec("base64-encoder-decoder", "Base64 encoder/decoder", "Developer"),
    ToolSpec("hash-generator", "Hash generator", "Developer"),
    ToolSpec("regex-tester", "Regex tester", "Developer"),
    ToolSpec("uuid-generator", "UUID generator", "Developer"),
    ToolSpec("timestamp-converter", "Timestamp converter", "Developer"),
    ToolSpec("color-palette-generator", "Color palette generator", "Developer"),
    ToolSpec("markdown-previewer", "Markdown previewer", "Developer"),
    ToolSpec("api-request-tester", "API request tester", "Developer"),
    ToolSpec("to-do-board", "To-do board", "Productivity"),
    ToolSpec("notes-snippets-manager", "Notes & snippets manager", "Productivity"),
    ToolSpec("password-generator", "Password generator", "Productivity"),
    ToolSpec("qr-code-generator", "QR code generator", "Productivity"),
    ToolSpec("barcode-generator", "Barcode generator", "Productivity"),
    ToolSpec("pdf-merge", "PDF merge", "Document"),
    ToolSpec("pdf-split", "PDF split", "Document"),
    ToolSpec("ocr-dokumen-ringan", "OCR dokumen ringan", "Document"),
    ToolSpec("invoice-template-generator", "Invoice template generator", "Document"),
    ToolSpec("batch-file-renamer", "Batch file renamer", "Document"),
    ToolSpec("website-uptime-checker", "Website uptime checker", "Monitoring"),
    ToolSpec("ssl-checker", "SSL checker", "Monitoring"),
    ToolSpec("dns-lookup", "DNS lookup", "Monitoring"),
    ToolSpec("internal-asset-port-checker", "Internal asset port checker", "Monitoring"),
    ToolSpec("web-performance-audit", "Web performance audit", "Monitoring"),
    ToolSpec("broken-link-checker", "Broken link checker", "Monitoring"),
    ToolSpec("sitemap-validator", "Sitemap validator", "Monitoring"),
    ToolSpec("robots-txt-checker", "Robots.txt checker", "Monitoring"),
    ToolSpec("server-resource-dashboard", "Server resource dashboard", "Monitoring"),
    ToolSpec("log-viewer-alert-ringan", "Log viewer & alert ringan", "Monitoring"),
)

# Backward-compatible shape used by existing importer/tests.
TOOLS = [(tool.slug, tool.name, tool.category) for tool in TOOL_SPECS]


def list_tools() -> tuple[ToolSpec, ...]:
    return TOOL_SPECS


def get_tool_by_slug(slug: str) -> ToolSpec | None:
    return next((tool for tool in TOOL_SPECS if tool.slug == slug), None)


def search_tools(query: str) -> list[ToolSpec]:
    normalized = query.strip().lower()
    if not normalized:
        return list(TOOL_SPECS)
    return [
        tool
        for tool in TOOL_SPECS
        if normalized in tool.slug.lower() or normalized in tool.name.lower() or normalized in tool.category.lower()
    ]


def filter_tools(category: str | None = None, query: str | None = None) -> list[ToolSpec]:
    filtered = search_tools(query or "")
    if not category:
        return filtered

    normalized_category = category.strip().lower()
    return [tool for tool in filtered if tool.category.lower() == normalized_category]


def list_categories() -> list[str]:
    return sorted({tool.category for tool in TOOL_SPECS})


def paginate_tools(tools: list[ToolSpec], page: int = 1, page_size: int = 10) -> dict[str, int | list[ToolSpec]]:
    if page < 1:
        raise ValueError("page minimal 1")
    if page_size < 1 or page_size > 50:
        raise ValueError("page_size harus antara 1 sampai 50")

    total_items = len(tools)
    total_pages = ceil(total_items / page_size) if total_items else 1
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "items": tools[start:end],
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
    }


def related_tools(slug: str, limit: int = 4) -> list[ToolSpec]:
    tool = get_tool_by_slug(slug)
    if not tool:
        return []

    siblings = [item for item in TOOL_SPECS if item.category == tool.category and item.slug != tool.slug]
    return siblings[:limit]


def group_tools_by_category() -> dict[str, list[ToolSpec]]:
    grouped: dict[str, list[ToolSpec]] = defaultdict(list)
    for tool in TOOL_SPECS:
        grouped[tool.category].append(tool)
    return dict(grouped)
