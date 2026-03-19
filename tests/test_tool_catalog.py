from app.services.tool_catalog import (
    TOOLS,
    catalog_summary,
    compare_tools,
    featured_tools,
    filter_tools,
    get_tool_by_slug,
    group_tools_by_category,
    list_categories,
    new_tools,
    paginate_tools,
    related_tools,
    search_tools,
    sort_tools,
)


def test_feature_count():
    assert len(TOOLS) == 60


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

    audience_result = search_tools("marketing")
    assert any(tool.slug == "email-subject-generator" for tool in audience_result)


def test_filter_categories_and_list_categories():
    filtered = filter_tools(category="developer", query="generator")
    assert all(tool.category == "Developer" for tool in filtered)
    assert any(tool.slug == "uuid-generator" for tool in filtered)

    beta_filtered = filter_tools(release_stage="beta")
    assert len(beta_filtered) == 10

    categories = list_categories()
    assert categories == sorted(categories)
    assert "Media" in categories


def test_paginate_and_related_tools():
    first_page = paginate_tools(search_tools(""), page=1, page_size=7)
    assert first_page["total_items"] == 60
    assert first_page["total_pages"] == 9
    assert len(first_page["items"]) == 7

    related = related_tools("video-cutter", limit=3)
    assert len(related) == 3
    assert all(item.category == "Media" for item in related)


def test_catalog_extras():
    summary = catalog_summary()
    assert summary["total_tools"] == 60
    assert summary["new_tools"] == 10
    assert summary["beta_tools"] == 10

    latest = new_tools(limit=10)
    assert len(latest) == 10
    assert all(tool.is_new for tool in latest)

    featured = featured_tools(limit=4)
    assert len(featured) == 4

    compared = compare_tools(["schema-diff-checker", "sql-prettifier", "missing"])
    assert [tool.slug for tool in compared] == ["schema-diff-checker", "sql-prettifier"]

    sorted_latest = sort_tools(latest, sort_by="newest")
    assert sorted_latest[0].is_new is True
