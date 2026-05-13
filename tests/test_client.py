"""Tests for the Joplin client wrapper."""

from unittest.mock import MagicMock, patch


def test_safe_client_normalizes_null_parent_id_in_notebooks():
    """Should coerce string 'null' notebook parent IDs to empty string."""
    from joplin_mcp.client import SafeClientApi

    client = SafeClientApi(token="token", url="http://localhost:41184")

    fake_response = MagicMock()
    fake_response.json.return_value = {
        "items": [
            {
                "id": "3302974a30e84e40b4cf6903ff90a794",
                "title": "Granola",
                "parent_id": "null",
            },
            {
                "id": "b19cf47a5f054b9aa667d9ad669a337f",
                "title": "Root",
                "parent_id": "",
            },
        ],
        "has_more": False,
    }

    with patch.object(client, "get", return_value=fake_response):
        result = client.get_notebooks(fields="id,title,parent_id")

    assert result.items[0].parent_id == ""
    assert result.items[1].parent_id == ""
