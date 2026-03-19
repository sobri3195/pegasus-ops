from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from math import ceil
import random


@dataclass(frozen=True, slots=True)
class ToolSpec:
    slug: str
    name: str
    category: str
    description: str
    audience: str
    release_stage: str = "stable"
    is_new: bool = False

    def to_dict(self) -> dict[str, str | bool]:
        return asdict(self)


TOOL_SPECS: tuple[ToolSpec, ...] = (
    ToolSpec("video-cutter", "Video cutter", "Media", "Potong video cepat untuk short-form content dan workflow approval.", "Creator"),
    ToolSpec("video-merger", "Video merger", "Media", "Gabungkan beberapa klip menjadi satu output siap publish.", "Creator"),
    ToolSpec("audio-extractor", "Audio extractor", "Media", "Ekstrak audio dari video untuk podcast atau edit lanjutan.", "Creator"),
    ToolSpec("subtitle-generator", "Subtitle generator", "Media", "Generate subtitle dasar untuk distribusi lintas platform.", "Creator"),
    ToolSpec("thumbnail-resizer", "Thumbnail resizer", "Media", "Resize thumbnail sesuai format YouTube, reels, atau ads.", "Creator"),
    ToolSpec("image-compressor", "Image compressor", "Media", "Kompres gambar untuk upload yang lebih ringan tanpa ribet.", "Creator"),
    ToolSpec("background-remover", "Background remover", "Media", "Bersihkan background aset visual untuk materi promosi.", "Creator"),
    ToolSpec("watermark-tool", "Watermark tool", "Media", "Tambahkan branding ke aset gambar dan video operasional.", "Creator"),
    ToolSpec("image-format-converter", "Image format converter", "Media", "Konversi PNG, JPG, dan WebP untuk kebutuhan campaign.", "Creator"),
    ToolSpec("caption-generator", "Caption generator", "Creator", "Buat caption cepat berdasarkan konteks campaign dan CTA.", "Social team"),
    ToolSpec("hashtag-generator", "Hashtag generator", "Creator", "Susun hashtag relevan untuk niche dan momentum konten.", "Social team"),
    ToolSpec("content-calendar", "Content calendar", "Creator", "Rancang jadwal konten mingguan dengan tema yang konsisten.", "Social team"),
    ToolSpec("bio-generator", "Bio generator", "Creator", "Buat bio singkat untuk brand, creator, atau campaign page.", "Social team"),
    ToolSpec("link-in-bio-builder", "Link in bio builder", "Creator", "Kelola kumpulan link penting untuk promosi dan funnels.", "Social team"),
    ToolSpec("reply-template-manager", "Reply template manager", "Creator", "Simpan template balasan cepat untuk DM dan komentar.", "Support"),
    ToolSpec("engagement-tracker", "Engagement tracker", "Creator", "Pantau engagement harian agar eksperimen konten mudah dievaluasi.", "Analyst"),
    ToolSpec("content-idea-scheduler", "Content idea scheduler", "Creator", "Susun backlog ide konten agar tim selalu punya cadangan.", "Social team"),
    ToolSpec("title-generator", "Title generator", "Creator", "Generate headline dan judul konten dengan variasi hook.", "Social team"),
    ToolSpec("keyword-clustering", "Keyword clustering", "Creator", "Kelompokkan keyword untuk SEO planning dan topic map.", "SEO"),
    ToolSpec("trend-notes-board", "Trend notes board", "Creator", "Catat insight tren dan referensi konten di satu papan.", "Social team"),
    ToolSpec("json-formatter", "JSON formatter", "Developer", "Rapikan payload JSON untuk debugging dan dokumentasi API.", "Developer"),
    ToolSpec("jwt-decoder", "JWT decoder", "Developer", "Decode token JWT untuk inspeksi claim dan expiry.", "Developer"),
    ToolSpec("base64-encoder-decoder", "Base64 encoder/decoder", "Developer", "Encode atau decode string Base64 tanpa berpindah tools.", "Developer"),
    ToolSpec("hash-generator", "Hash generator", "Developer", "Generate hash cepat untuk verifikasi integritas data.", "Developer"),
    ToolSpec("regex-tester", "Regex tester", "Developer", "Uji regex terhadap sampel teks secara iteratif.", "Developer"),
    ToolSpec("uuid-generator", "UUID generator", "Developer", "Generate UUID untuk kebutuhan data seed dan tracing.", "Developer"),
    ToolSpec("timestamp-converter", "Timestamp converter", "Developer", "Konversi UNIX timestamp ke format yang mudah dibaca.", "Developer"),
    ToolSpec("color-palette-generator", "Color palette generator", "Developer", "Siapkan kombinasi warna cepat untuk prototipe antarmuka.", "Designer"),
    ToolSpec("markdown-previewer", "Markdown previewer", "Developer", "Preview markdown untuk README, changelog, atau docs internal.", "Developer"),
    ToolSpec("api-request-tester", "API request tester", "Developer", "Uji request HTTP sederhana tanpa keluar dari dashboard.", "Developer"),
    ToolSpec("to-do-board", "To-do board", "Productivity", "Atur task harian tim operasional dalam papan sederhana.", "Operations"),
    ToolSpec("notes-snippets-manager", "Notes & snippets manager", "Productivity", "Simpan snippet kerja dan catatan berulang agar mudah dicari.", "Operations"),
    ToolSpec("password-generator", "Password generator", "Productivity", "Buat password kuat untuk akun internal dan temporary access.", "Operations"),
    ToolSpec("qr-code-generator", "QR code generator", "Productivity", "Generate QR code untuk landing page, event, atau campaign.", "Operations"),
    ToolSpec("barcode-generator", "Barcode generator", "Productivity", "Buat barcode untuk inventaris dan tagging aset fisik.", "Operations"),
    ToolSpec("pdf-merge", "PDF merge", "Document", "Gabungkan beberapa PDF menjadi satu dokumen final.", "Admin"),
    ToolSpec("pdf-split", "PDF split", "Document", "Pisahkan halaman PDF untuk distribusi dokumen lebih cepat.", "Admin"),
    ToolSpec("ocr-dokumen-ringan", "OCR dokumen ringan", "Document", "Ekstrak teks sederhana dari scan dokumen operasional.", "Admin"),
    ToolSpec("invoice-template-generator", "Invoice template generator", "Document", "Generate invoice dasar untuk kebutuhan admin ringan.", "Finance"),
    ToolSpec("batch-file-renamer", "Batch file renamer", "Document", "Rapikan penamaan file agar arsip lebih konsisten.", "Admin"),
    ToolSpec("website-uptime-checker", "Website uptime checker", "Monitoring", "Pantau status online website penting untuk tim ops.", "Operations"),
    ToolSpec("ssl-checker", "SSL checker", "Monitoring", "Cek masa berlaku SSL untuk mencegah incident sederhana.", "Operations"),
    ToolSpec("dns-lookup", "DNS lookup", "Monitoring", "Lihat record DNS dasar saat troubleshooting domain.", "Operations"),
    ToolSpec("internal-asset-port-checker", "Internal asset port checker", "Monitoring", "Periksa port asset internal yang perlu diverifikasi.", "Operations"),
    ToolSpec("web-performance-audit", "Web performance audit", "Monitoring", "Audit performa web ringan untuk halaman penting.", "Operations"),
    ToolSpec("broken-link-checker", "Broken link checker", "Monitoring", "Temukan tautan rusak sebelum campaign tayang.", "Operations"),
    ToolSpec("sitemap-validator", "Sitemap validator", "Monitoring", "Validasi sitemap untuk SEO dan crawling readiness.", "SEO"),
    ToolSpec("robots-txt-checker", "Robots.txt checker", "Monitoring", "Periksa aturan robots.txt sebelum deployment indexable.", "SEO"),
    ToolSpec("server-resource-dashboard", "Server resource dashboard", "Monitoring", "Ringkas pemakaian resource untuk pemantauan cepat.", "Operations"),
    ToolSpec("log-viewer-alert-ringan", "Log viewer & alert ringan", "Monitoring", "Buka log penting dan tandai anomali operasional.", "Operations"),
    ToolSpec("ai-script-writer", "AI script writer", "Creator", "Susun draft script video pendek berdasarkan objective campaign.", "Social team", release_stage="beta", is_new=True),
    ToolSpec("podcast-show-notes", "Podcast show notes", "Creator", "Ubah poin pembahasan menjadi show notes yang rapi dan ringkas.", "Creator", release_stage="beta", is_new=True),
    ToolSpec("email-subject-generator", "Email subject generator", "Creator", "Generate beberapa opsi subject line untuk campaign email.", "Marketing", release_stage="beta", is_new=True),
    ToolSpec("schema-diff-checker", "Schema diff checker", "Developer", "Bandingkan dua skema JSON untuk review perubahan kontrak API.", "Developer", release_stage="beta", is_new=True),
    ToolSpec("cron-expression-builder", "Cron expression builder", "Developer", "Rangkai cron expression dengan bantuan deskripsi yang lebih mudah.", "Developer", release_stage="beta", is_new=True),
    ToolSpec("sql-prettifier", "SQL prettifier", "Developer", "Format query SQL agar review query internal lebih nyaman.", "Developer", release_stage="beta", is_new=True),
    ToolSpec("meeting-recap-generator", "Meeting recap generator", "Productivity", "Susun recap meeting menjadi action items dan follow-up.", "Operations", release_stage="beta", is_new=True),
    ToolSpec("sop-checklist-builder", "SOP checklist builder", "Productivity", "Bangun checklist SOP untuk onboarding atau tugas rutin.", "Operations", release_stage="beta", is_new=True),
    ToolSpec("incident-timeline-tracker", "Incident timeline tracker", "Monitoring", "Catat kronologi incident agar postmortem lebih terstruktur.", "Operations", release_stage="beta", is_new=True),
    ToolSpec("competitor-snapshot-board", "Competitor snapshot board", "Monitoring", "Ringkas snapshot kompetitor untuk review kampanye mingguan.", "Analyst", release_stage="beta", is_new=True),
)

# Backward-compatible shape used by existing importer/tests.
TOOLS = [(tool.slug, tool.name, tool.category) for tool in TOOL_SPECS]


def list_tools() -> tuple[ToolSpec, ...]:
    return TOOL_SPECS


def serialize_tools(tools: list[ToolSpec] | tuple[ToolSpec, ...]) -> list[dict[str, str | bool]]:
    return [tool.to_dict() for tool in tools]


def get_tool_by_slug(slug: str) -> ToolSpec | None:
    return next((tool for tool in TOOL_SPECS if tool.slug == slug), None)


def search_tools(query: str) -> list[ToolSpec]:
    normalized = query.strip().lower()
    if not normalized:
        return list(TOOL_SPECS)
    return [
        tool
        for tool in TOOL_SPECS
        if normalized in tool.slug.lower()
        or normalized in tool.name.lower()
        or normalized in tool.category.lower()
        or normalized in tool.description.lower()
        or normalized in tool.audience.lower()
    ]


def filter_tools(category: str | None = None, query: str | None = None, release_stage: str | None = None) -> list[ToolSpec]:
    filtered = search_tools(query or "")
    if category:
        normalized_category = category.strip().lower()
        filtered = [tool for tool in filtered if tool.category.lower() == normalized_category]
    if release_stage:
        normalized_stage = release_stage.strip().lower()
        filtered = [tool for tool in filtered if tool.release_stage.lower() == normalized_stage]
    return filtered


def sort_tools(tools: list[ToolSpec], sort_by: str = "name") -> list[ToolSpec]:
    normalized = sort_by.strip().lower()
    if normalized == "newest":
        return sorted(tools, key=lambda tool: (not tool.is_new, tool.name.lower()))
    if normalized == "category":
        return sorted(tools, key=lambda tool: (tool.category.lower(), tool.name.lower()))
    if normalized == "audience":
        return sorted(tools, key=lambda tool: (tool.audience.lower(), tool.name.lower()))
    return sorted(tools, key=lambda tool: tool.name.lower())


def list_categories() -> list[str]:
    return sorted({tool.category for tool in TOOL_SPECS})


def list_audiences() -> list[str]:
    return sorted({tool.audience for tool in TOOL_SPECS})


def paginate_tools(tools: list[ToolSpec], page: int = 1, page_size: int = 10) -> dict[str, int | list[ToolSpec]]:
    if page < 1:
        raise ValueError("page minimal 1")
    if page_size < 1 or page_size > 60:
        raise ValueError("page_size harus antara 1 sampai 60")

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


def featured_tools(limit: int = 6) -> list[ToolSpec]:
    curated_slugs = (
        "ai-script-writer",
        "schema-diff-checker",
        "meeting-recap-generator",
        "incident-timeline-tracker",
        "video-cutter",
        "website-uptime-checker",
    )
    return [tool for tool in TOOL_SPECS if tool.slug in curated_slugs][:limit]


def new_tools(limit: int = 10) -> list[ToolSpec]:
    return [tool for tool in TOOL_SPECS if tool.is_new][:limit]


def tools_by_audience(audience: str, limit: int = 6) -> list[ToolSpec]:
    normalized = audience.strip().lower()
    return [tool for tool in TOOL_SPECS if tool.audience.lower() == normalized][:limit]


def random_tools(limit: int = 3, seed: int | None = None) -> list[ToolSpec]:
    generator = random.Random(seed)
    items = list(TOOL_SPECS)
    generator.shuffle(items)
    return items[:limit]


def group_tools_by_category() -> dict[str, list[ToolSpec]]:
    grouped: dict[str, list[ToolSpec]] = defaultdict(list)
    for tool in TOOL_SPECS:
        grouped[tool.category].append(tool)
    return dict(grouped)


def catalog_summary() -> dict[str, int | list[dict[str, int | str]]]:
    category_counts = Counter(tool.category for tool in TOOL_SPECS)
    return {
        "total_tools": len(TOOL_SPECS),
        "new_tools": sum(tool.is_new for tool in TOOL_SPECS),
        "beta_tools": sum(tool.release_stage == "beta" for tool in TOOL_SPECS),
        "categories": [
            {"name": category, "count": count}
            for category, count in sorted(category_counts.items(), key=lambda item: item[0])
        ],
    }


def compare_tools(slugs: list[str]) -> list[ToolSpec]:
    requested = {slug.strip().lower() for slug in slugs if slug.strip()}
    return [tool for tool in TOOL_SPECS if tool.slug.lower() in requested]
