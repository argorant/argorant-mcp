"""HTTP client for the safe Argorant MCP backend surface."""
from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from .config import settings


class BackendError(Exception):
    def __init__(self, code: str, message: str, *, retry_after: Optional[int] = None, status: Optional[int] = None):
        self.code = code
        self.message = message
        self.retry_after = retry_after
        self.status = status
        super().__init__(message)


def _detail(resp: httpx.Response) -> str:
    try:
        body = resp.json()
        if isinstance(body, dict):
            return str(body.get("detail") or body.get("error") or body)
        return str(body)
    except Exception:
        return (resp.text or "")[:300]


def _raise_for_status(resp: httpx.Response) -> None:
    if resp.status_code < 400:
        return
    detail = _detail(resp)
    if resp.status_code == 401:
        raise BackendError("auth_error", "The Argorant connector needs to be reconnected.", status=401)
    if resp.status_code == 403:
        raise BackendError("not_allowed", f"Argorant denied this connector action: {detail}", status=403)
    if resp.status_code == 429:
        retry_after = int(resp.headers.get("Retry-After") or 60)
        raise BackendError("rate_limited", f"Rate limit reached. Retry after about {retry_after} seconds.", retry_after=retry_after, status=429)
    raise BackendError("backend_error", f"Argorant API error {resp.status_code}: {detail}", status=resp.status_code)


class BackendClient:
    def __init__(self, api_key: str):
        self._headers = {"Authorization": f"Bearer {api_key}"}
        self._base = settings.backend_base_url.rstrip("/")
        self._timeout = settings.backend_timeout_s

    def _get_json(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        clean_params = {k: v for k, v in (params or {}).items() if v is not None and v != ""}
        with httpx.Client(timeout=self._timeout) as client:
            resp = client.get(self._base + path, headers=self._headers, params=clean_params)
        _raise_for_status(resp)
        return resp.json()

    def _post_json(self, path: str, payload: Optional[Dict[str, Any]] = None) -> Any:
        with httpx.Client(timeout=self._timeout) as client:
            resp = client.post(self._base + path, headers=self._headers, json=payload or {})
        _raise_for_status(resp)
        return resp.json()

    def _get_text(self, path: str, params: Optional[Dict[str, Any]] = None) -> str:
        clean_params = {k: v for k, v in (params or {}).items() if v is not None and v != ""}
        with httpx.Client(timeout=self._timeout) as client:
            resp = client.get(self._base + path, headers=self._headers, params=clean_params)
        _raise_for_status(resp)
        return resp.text

    def account(self) -> Dict[str, Any]:
        return self._get_json("/api/mcp/account")

    def people_count(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        return self._get_json("/api/mcp/people/count", filters)

    def people_preview(self, filters: Dict[str, Any], limit: int) -> Dict[str, Any]:
        return self._get_json("/api/mcp/people/preview", {**filters, "limit": limit})

    def people_reveal(self, filters: Dict[str, Any], limit: int) -> Dict[str, Any]:
        return self._get_json("/api/mcp/people/reveal", {**filters, "limit": limit})

    def create_export(
        self,
        filters: Dict[str, Any],
        limit: int,
        *,
        exclude_previously_exported: bool = True,
        email_when_done: bool = False,
    ) -> Dict[str, Any]:
        return self._post_json("/api/mcp/exports/create", {
            "filters": filters,
            "limit": limit,
            "exclude_previously_exported": exclude_previously_exported,
            "email_when_done": email_when_done,
        })

    def export_status(self, job_id: int) -> Dict[str, Any]:
        return self._get_json(f"/api/mcp/exports/{int(job_id)}")

    def export_batch_status(self, batch_id: int) -> Dict[str, Any]:
        return self._get_json(f"/api/mcp/export-batches/{int(batch_id)}")

    def export_download_text(self, job_id: int) -> str:
        return self._get_text(f"/api/mcp/exports/{int(job_id)}/download")

    def create_list(
        self,
        name: str,
        filters: Dict[str, Any],
        *,
        selection_mode: str = "filtered",
        record_ids: Optional[list[str]] = None,
        snapshot_total: Optional[int] = None,
    ) -> Dict[str, Any]:
        return self._post_json("/api/mcp/lists/create", {
            "name": name,
            "filters": filters,
            "selection_mode": selection_mode,
            "record_ids": record_ids,
            "snapshot_total": snapshot_total,
        })

    def list_status(self, list_id: int) -> Dict[str, Any]:
        return self._get_json(f"/api/mcp/lists/{int(list_id)}")

    def export_list(
        self,
        list_id: int,
        *,
        limit: int,
        exclude_previously_exported: bool = True,
        email_when_done: bool = False,
    ) -> Dict[str, Any]:
        return self._post_json(f"/api/mcp/lists/{int(list_id)}/export", {
            "limit": limit,
            "exclude_previously_exported": exclude_previously_exported,
            "email_when_done": email_when_done,
        })
