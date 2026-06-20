"""Public-safe Argorant search tools."""
from __future__ import annotations

import base64
import json
import re
from typing import Any, Dict, Optional

from mcp.types import ToolAnnotations

from ..config import settings
from .common import ToolError, backend_call, current_identity, error_dict

_READ_OPEN = ToolAnnotations(readOnlyHint=True, openWorldHint=True)
_ACCOUNT_ACTION = ToolAnnotations(readOnlyHint=False, openWorldHint=True)
_DOC_ID_PREFIX = "argorant:"
_DOMAIN_RE = re.compile(r"\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b", re.IGNORECASE)


def _filters(
    q: Optional[str],
    title: Optional[str],
    seniority: Optional[str],
    departments: Optional[str],
    company_name: Optional[str],
    company_domain: Optional[str],
    industry: Optional[str],
    city: Optional[str],
    state: Optional[str],
    country: Optional[str],
    has_email: Optional[bool],
    has_phone: Optional[bool],
    has_linkedin: Optional[bool],
    verified_only: bool,
    geography: Optional[str] = None,
    exclude_title: Optional[str] = None,
) -> Dict[str, Any]:
    # Verification status is never a public/queryable filter (it would expose data
    # quality / invalid volumes). Only positive "verified_only" intent is honored;
    # actual verification happens live at reveal/export and only valid is billed.
    status = "valid" if verified_only else None
    return {
        "q": q,
        "title": title,
        "seniority": seniority,
        "departments": departments,
        "company_name": company_name,
        "company_domain": company_domain,
        "industry": industry,
        "city": city,
        "state": state,
        "country": ",".join([v for v in [country, geography] if v]) or None,
        "exclude_title": exclude_title,
        "has_email": "true" if has_email else None,
        "has_phone": "true" if has_phone else None,
        "has_linkedin": "true" if has_linkedin else None,
        "business_email_only": "true",
        "verify_status": status,
    }


def _extract_domain(query: str) -> Optional[str]:
    match = _DOMAIN_RE.search(query or "")
    if not match:
        return None
    return match.group(0).strip(".,;:()[]{}<>").lower()


def _safe_query(query: str) -> str:
    return " ".join((query or "").strip().split())[:240]


def _compat_filters(query: str) -> Dict[str, Any]:
    clean_query = _safe_query(query)
    domain = _extract_domain(clean_query)
    return _filters(
        q=None if domain else clean_query,
        title=None,
        seniority=None,
        departments=None,
        company_name=None,
        company_domain=domain,
        industry=None,
        city=None,
        state=None,
        country=None,
        has_email=True,
        has_phone=None,
        has_linkedin=None,
        verified_only=False,
    )


def _doc_id(kind: str, query: str, filters: Dict[str, Any]) -> str:
    payload = {
        "kind": kind,
        "query": _safe_query(query),
        "filters": {k: v for k, v in filters.items() if v is not None and v != ""},
    }
    encoded = base64.urlsafe_b64encode(
        json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    ).decode("ascii").rstrip("=")
    return _DOC_ID_PREFIX + encoded


def _decode_doc_id(doc_id: str) -> Dict[str, Any]:
    if not doc_id.startswith(_DOC_ID_PREFIX):
        raise ToolError("invalid_document_id", "Argorant fetch IDs must come from the Argorant MCP search tool.")
    raw = doc_id[len(_DOC_ID_PREFIX):]
    raw += "=" * (-len(raw) % 4)
    try:
        payload = json.loads(base64.urlsafe_b64decode(raw.encode("ascii")).decode("utf-8"))
    except Exception as exc:
        raise ToolError("invalid_document_id", "Could not decode the Argorant search result ID.") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("filters"), dict):
        raise ToolError("invalid_document_id", "Argorant search result ID has an invalid payload.")
    return payload


def _result_url(filters: Dict[str, Any]) -> str:
    base = settings.backend_public_url.rstrip("/")
    domain = filters.get("company_domain")
    if domain:
        return f"{base}/company/{domain}"
    return f"{base}/tools/company-lookup"


def _coverage_title(query: str, count: Optional[int]) -> str:
    clean_query = _safe_query(query) or "B2B contacts"
    if count is None:
        return f"Argorant contact coverage for {clean_query}"
    return f"Argorant coverage for {clean_query}: {count:,} matching contacts"


def _preview_lines(results: list[Dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for row in results:
        role = row.get("title") or "Role not shown"
        company = row.get("company") or row.get("company_domain") or "Company not shown"
        location = ", ".join([str(x) for x in [row.get("city"), row.get("state"), row.get("country")] if x])
        parts = [str(row.get("preview") or "Masked contact"), role, company]
        if location:
            parts.append(location)
        # No per-row verification tag: every email Argorant serves is verified at
        # export by guarantee, so a per-record verdict is redundant. The granular
        # provider verdict is never exposed on any public surface.
        lines.append(" - " + " | ".join(parts))
    return lines


def register(mcp) -> None:
    @mcp.tool(
        name="search",
        description=(
            "Search Argorant's safe B2B contact coverage for ChatGPT apps, "
            "deep research, and MCP clients. Returns result handles for aggregate "
            "coverage and masked previews only; use fetch to retrieve the safe summary. "
            "Raw contact details and exports require separate scoped Argorant tools."
        ),
        annotations=_READ_OPEN,
    )
    async def search(query: str) -> Dict[str, Any]:
        ident = current_identity()
        clean_query = _safe_query(query)
        if not clean_query:
            return {"results": []}
        filters = _compat_filters(clean_query)
        try:
            count_result = await backend_call(
                ident["product_credential"],
                lambda client: client.people_count(filters),
            )
        except ToolError as exc:
            return error_dict(exc)
        count = count_result.get("count") if isinstance(count_result, dict) else None
        return {
            "results": [
                {
                    "id": _doc_id("coverage", clean_query, filters),
                    "title": _coverage_title(clean_query, count if isinstance(count, int) else None),
                    "url": _result_url(filters),
                },
                {
                    "id": _doc_id("preview", clean_query, filters),
                    "title": f"Masked Argorant preview rows for {clean_query}",
                    "url": _result_url(filters),
                },
            ]
        }

    @mcp.tool(
        name="fetch",
        description=(
            "Fetch a safe Argorant result returned by the search tool. Returns "
            "aggregate counts, usage status, and capped masked preview rows. Contact "
            "details, phone numbers, profile URLs, and exports require separate scoped Argorant tools."
        ),
        annotations=_READ_OPEN,
    )
    async def fetch(id: str) -> Dict[str, Any]:
        ident = current_identity()
        try:
            payload = _decode_doc_id(id)
            filters = payload["filters"]
            query = _safe_query(str(payload.get("query") or "B2B contacts"))
            kind = str(payload.get("kind") or "coverage")
            count_result = await backend_call(
                ident["product_credential"],
                lambda client: client.people_count(filters),
            )
            preview_result = await backend_call(
                ident["product_credential"],
                lambda client: client.people_preview(filters, 5),
            )
        except ToolError as exc:
            return error_dict(exc)

        count = int((count_result or {}).get("count") or 0)
        returned = int((preview_result or {}).get("returned") or 0)
        results = (preview_result or {}).get("results") or []
        title = _coverage_title(query, count) if kind == "coverage" else f"Masked Argorant preview for {query}"
        text_lines = [
            title,
            "",
            f"Query: {query}",
            f"Matching contacts with business email coverage: {count:,}",
            f"Preview rows returned: {returned}",
            "",
            "Public-safe boundary: Argorant MCP returns aggregate counts and masked preview rows only. "
            "Raw emails, phone numbers, profile URLs, contact reveal, and exports use separate scoped "
            "tools with signed-in Argorant workspace permissions, quota, and billing controls.",
        ]
        if results:
            text_lines.extend(["", "Masked preview rows:", *_preview_lines(results)])
        return {
            "id": id,
            "title": title,
            "text": "\n".join(text_lines),
            "url": _result_url(filters),
            "metadata": {
                "source": "argorant_mcp",
                "data_exposure": "aggregate_counts_and_masked_previews",
                "raw_emails": False,
                "phone_numbers": False,
                "profile_urls": False,
                "exports": False,
                "count": count,
                "preview_rows": returned,
            },
        }

    @mcp.tool(
        name="argorant_count_people",
        description=(
            "Count matching B2B contacts in Argorant by company, role, seniority, department, "
            "industry, or location. Returns aggregate counts only. COST: free. "
            "`country` accepts individual countries OR regions/geographies — e.g. 'Europe', "
            "'EMEA', 'DACH', 'Nordics', 'Benelux', 'APAC', 'LATAM', 'North America', 'GCC' — "
            "and these can be combined comma-separated; use `geography` as an explicit alias. "
            "`title` understands abbreviations both ways (CFO ↔ Chief Financial Officer); pass "
            "comma-separated titles to match any. Use `exclude_title` to exclude roles "
            "(comma-separated, abbreviation-aware)."
        ),
        annotations=_READ_OPEN,
    )
    async def argorant_count_people(
        q: Optional[str] = None,
        title: Optional[str] = None,
        seniority: Optional[str] = None,
        departments: Optional[str] = None,
        company_name: Optional[str] = None,
        company_domain: Optional[str] = None,
        industry: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        geography: Optional[str] = None,
        exclude_title: Optional[str] = None,
        has_email: Optional[bool] = None,
        has_phone: Optional[bool] = None,
        has_linkedin: Optional[bool] = None,
        verified_only: bool = False,
    ) -> Dict[str, Any]:
        ident = current_identity()
        filters = _filters(q, title, seniority, departments, company_name, company_domain, industry,
                           city, state, country, has_email, has_phone, has_linkedin, verified_only,
                           geography=geography, exclude_title=exclude_title)
        try:
            return await backend_call(ident["product_credential"], lambda client: client.people_count(filters))
        except ToolError as exc:
            return error_dict(exc)

    @mcp.tool(
        name="argorant_preview_people",
        description=(
            "Preview matching Argorant contacts without revealing personal contact details. "
            "Returns masked initials, role, company, location, departments, and verification status. "
            "Use Argorant after signing in to reveal emails, phone numbers, direct dials, or exports."
        ),
        annotations=_READ_OPEN,
    )
    async def argorant_preview_people(
        q: Optional[str] = None,
        title: Optional[str] = None,
        seniority: Optional[str] = None,
        departments: Optional[str] = None,
        company_name: Optional[str] = None,
        company_domain: Optional[str] = None,
        industry: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        geography: Optional[str] = None,
        exclude_title: Optional[str] = None,
        has_email: Optional[bool] = True,
        has_phone: Optional[bool] = None,
        has_linkedin: Optional[bool] = None,
        verified_only: bool = False,
        limit: int = 5,
    ) -> Dict[str, Any]:
        ident = current_identity()
        safe_limit = max(1, min(int(limit or 5), settings.owner_max_preview))
        filters = _filters(q, title, seniority, departments, company_name, company_domain, industry,
                           city, state, country, has_email, has_phone, has_linkedin, verified_only,
                           geography=geography, exclude_title=exclude_title)
        try:
            return await backend_call(ident["product_credential"], lambda client: client.people_preview(filters, safe_limit))
        except ToolError as exc:
            return error_dict(exc)

    @mcp.tool(
        name="argorant_reveal_people",
        description=(
            "Reveal actual Argorant contact rows including emails, phones, and profile URLs for a small matching set. "
            "Requires the argorant:unlock_contacts OAuth scope plus Argorant contact-reveal permission. "
            "Consumes reveal quota/credits; use exports for large lists."
        ),
        annotations=_ACCOUNT_ACTION,
    )
    async def argorant_reveal_people(
        q: Optional[str] = None,
        title: Optional[str] = None,
        seniority: Optional[str] = None,
        departments: Optional[str] = None,
        company_name: Optional[str] = None,
        company_domain: Optional[str] = None,
        industry: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        geography: Optional[str] = None,
        exclude_title: Optional[str] = None,
        has_phone: Optional[bool] = None,
        has_linkedin: Optional[bool] = None,
        verified_only: bool = False,
        limit: int = 10,
    ) -> Dict[str, Any]:
        ident = current_identity()
        safe_limit = max(1, min(int(limit or 10), 100))
        filters = _filters(q, title, seniority, departments, company_name, company_domain, industry,
                           city, state, country, True, has_phone, has_linkedin, verified_only,
                           geography=geography, exclude_title=exclude_title)
        try:
            return await backend_call(ident["product_credential"], lambda client: client.people_reveal(filters, safe_limit))
        except ToolError as exc:
            return error_dict(exc)

    @mcp.tool(
        name="argorant_create_export",
        description=(
            "Create an async Argorant lead export from filters. For lists larger than one file, Argorant creates "
            "a tracked export batch. Requires argorant:create_exports scope plus Argorant export permission. "
            "Consumes export quota/credits and returns job or batch IDs to poll."
        ),
        annotations=_ACCOUNT_ACTION,
    )
    async def argorant_create_export(
        q: Optional[str] = None,
        title: Optional[str] = None,
        seniority: Optional[str] = None,
        departments: Optional[str] = None,
        company_name: Optional[str] = None,
        company_domain: Optional[str] = None,
        industry: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        geography: Optional[str] = None,
        exclude_title: Optional[str] = None,
        has_email: Optional[bool] = True,
        has_phone: Optional[bool] = None,
        has_linkedin: Optional[bool] = None,
        verified_only: bool = False,
        limit: int = 1000,
        exclude_previously_exported: bool = True,
        email_when_done: bool = False,
    ) -> Dict[str, Any]:
        ident = current_identity()
        safe_limit = max(1, min(int(limit or 1000), 500000))
        filters = _filters(q, title, seniority, departments, company_name, company_domain, industry,
                           city, state, country, has_email, has_phone, has_linkedin, verified_only,
                           geography=geography, exclude_title=exclude_title)
        filters["record_type"] = "person"
        try:
            return await backend_call(
                ident["product_credential"],
                lambda client: client.create_export(
                    filters,
                    safe_limit,
                    exclude_previously_exported=exclude_previously_exported,
                    email_when_done=email_when_done,
                ),
            )
        except ToolError as exc:
            return error_dict(exc)

    @mcp.tool(
        name="argorant_create_list",
        description=(
            "Save a reusable Argorant lead list from filters or selected record IDs. "
            "Requires argorant:manage_lists scope plus Argorant list permission. "
            "Creating a list does not reveal raw contacts by itself; exporting or revealing consumes quota."
        ),
        annotations=_ACCOUNT_ACTION,
    )
    async def argorant_create_list(
        name: str,
        q: Optional[str] = None,
        title: Optional[str] = None,
        seniority: Optional[str] = None,
        departments: Optional[str] = None,
        company_name: Optional[str] = None,
        company_domain: Optional[str] = None,
        industry: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        geography: Optional[str] = None,
        exclude_title: Optional[str] = None,
        has_email: Optional[bool] = True,
        has_phone: Optional[bool] = None,
        has_linkedin: Optional[bool] = None,
        verified_only: bool = False,
        record_ids: Optional[list[str]] = None,
        snapshot_total: Optional[int] = None,
    ) -> Dict[str, Any]:
        ident = current_identity()
        filters = _filters(q, title, seniority, departments, company_name, company_domain, industry,
                           city, state, country, has_email, has_phone, has_linkedin, verified_only,
                           geography=geography, exclude_title=exclude_title)
        filters["record_type"] = "person"
        ids = [str(v).strip() for v in (record_ids or []) if str(v).strip()]
        selection_mode = "records" if ids else "filtered"
        try:
            return await backend_call(
                ident["product_credential"],
                lambda client: client.create_list(
                    name,
                    filters,
                    selection_mode=selection_mode,
                    record_ids=ids or None,
                    snapshot_total=snapshot_total,
                ),
            )
        except ToolError as exc:
            return error_dict(exc)

    @mcp.tool(
        name="argorant_list_status",
        description="Get metadata for an Argorant saved lead list. Requires list scope and permission.",
        annotations=_READ_OPEN,
    )
    async def argorant_list_status(list_id: int) -> Dict[str, Any]:
        ident = current_identity()
        try:
            return await backend_call(ident["product_credential"], lambda client: client.list_status(list_id))
        except ToolError as exc:
            return error_dict(exc)

    @mcp.tool(
        name="argorant_export_list",
        description=(
            "Create an async export from a saved Argorant lead list. Requires list and export scopes plus "
            "Argorant permissions. Consumes export quota/credits and can skip records already exported."
        ),
        annotations=_ACCOUNT_ACTION,
    )
    async def argorant_export_list(
        list_id: int,
        limit: int = 50000,
        exclude_previously_exported: bool = True,
        email_when_done: bool = False,
    ) -> Dict[str, Any]:
        ident = current_identity()
        safe_limit = max(1, min(int(limit or 50000), 500000))
        try:
            return await backend_call(
                ident["product_credential"],
                lambda client: client.export_list(
                    list_id,
                    limit=safe_limit,
                    exclude_previously_exported=exclude_previously_exported,
                    email_when_done=email_when_done,
                ),
            )
        except ToolError as exc:
            return error_dict(exc)

    @mcp.tool(
        name="argorant_export_status",
        description="Get status/progress for an Argorant MCP-created export job. Requires export scope and permission.",
        annotations=_READ_OPEN,
    )
    async def argorant_export_status(job_id: int) -> Dict[str, Any]:
        ident = current_identity()
        try:
            return await backend_call(ident["product_credential"], lambda client: client.export_status(job_id))
        except ToolError as exc:
            return error_dict(exc)

    @mcp.tool(
        name="argorant_export_batch_status",
        description="Get status/progress for an Argorant multi-file export batch. Requires export scope and permission.",
        annotations=_READ_OPEN,
    )
    async def argorant_export_batch_status(batch_id: int) -> Dict[str, Any]:
        ident = current_identity()
        try:
            return await backend_call(ident["product_credential"], lambda client: client.export_batch_status(batch_id))
        except ToolError as exc:
            return error_dict(exc)

    @mcp.tool(
        name="argorant_download_export_preview",
        description=(
            "Download a completed Argorant export CSV through MCP for small agent handoffs. "
            "Requires export scope and permission. Large exports should be downloaded from the Argorant app."
        ),
        annotations=_ACCOUNT_ACTION,
    )
    async def argorant_download_export_preview(job_id: int, max_characters: int = 20000) -> Dict[str, Any]:
        ident = current_identity()
        try:
            text = await backend_call(ident["product_credential"], lambda client: client.export_download_text(job_id))
        except ToolError as exc:
            return error_dict(exc)
        safe_chars = max(1000, min(int(max_characters or 20000), 50000))
        truncated = len(text) > safe_chars
        return {
            "ok": True,
            "job_id": job_id,
            "content_type": "text/csv",
            "truncated": truncated,
            "characters_returned": min(len(text), safe_chars),
            "text": text[:safe_chars],
        }
