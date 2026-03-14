from app.services.tool_catalog import TOOLS


def test_feature_count():
    assert len(TOOLS) == 50
