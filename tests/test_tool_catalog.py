from app.services.tool_catalog import (
    TOOLS,
    filter_tools,
    get_tool_by_slug,
    group_tools_by_category,
    list_categories,
    paginate_tools,
    related_tools,
    search_tools,
)


def test_feature_count():
    assert len(TOOLS) == 50


def test_get_tool_by_slug_found_and_missing():
    assert get_tool_by_slug("video-cutter").name == "Video cutter"
    assert get_tool_by_slug("missing-tool") is None


def test_grouping_and_search():
    grouped = group_tools_by_category()
    assert "Media" in grouped
    assert any(tool.slug == "video-cutter" for tool in grouped["Media"])

    result = search_tools("jwt")
    assert len(result) == 1
    assert result[0].slug == "jwt-decoder"


def test_filter_categories_and_list_categories():
    filtered = filter_tools(category="developer", query="generator")
    assert all(tool.category == "Developer" for tool in filtered)
    assert any(tool.slug == "uuid-generator" for tool in filtered)

    categories = list_categories()
    assert categories == sorted(categories)
    assert "Media" in categories


def test_paginate_and_related_tools():
    first_page = paginate_tools(search_tools(""), page=1, page_size=7)
    assert first_page["total_items"] == 50
    assert first_page["total_pages"] == 8
    assert len(first_page["items"]) == 7

    related = related_tools("video-cutter", limit=3)
    assert len(related) == 3
    assert all(item.category == "Media" for item in related)
