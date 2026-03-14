from app.services.tool_catalog import TOOLS, get_tool_by_slug, group_tools_by_category, search_tools


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
