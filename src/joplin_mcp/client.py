"""Joplin client helpers.

Wraps joppy's client to normalize known malformed notebook payloads returned by
some Joplin Web Clipper instances.
"""

from __future__ import annotations

from typing import Any, Optional

import joppy.data_types as dt
from joppy.client_api import ClientApi


def _normalize_notebook_payload(item: dict[str, Any]) -> dict[str, Any]:
    """Normalize notebook payloads before joppy validates IDs.

    Some Joplin instances return the literal string "null" for root notebook
    ``parent_id`` instead of an empty string/null. joppy rejects that as an
    invalid ID, so coerce it to an empty value first.
    """

    normalized = dict(item)
    if normalized.get("parent_id") == "null":
        normalized["parent_id"] = ""
    return normalized


class SafeClientApi(ClientApi):
    """ClientApi variant that normalizes malformed notebook payloads."""

    def get_notebook(self, id_: str, **query: dt.JoplinTypes) -> dt.NotebookData:
        response = self.get(f"/folders/{id_}", query=query).json()
        return dt.NotebookData(**_normalize_notebook_payload(response))

    def get_notebooks(self, **query: dt.JoplinTypes) -> dt.DataList[dt.NotebookData]:
        response = self.get("/folders", query=query).json()
        response["items"] = [
            dt.NotebookData(**_normalize_notebook_payload(item))
            for item in response["items"]
        ]
        return dt.DataList[dt.NotebookData](**response)


def create_joplin_client(token: str, url: str) -> SafeClientApi:
    """Create a normalized Joplin client instance."""

    return SafeClientApi(token=token, url=url)
