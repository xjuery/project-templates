"""
Infrastructure Layer — In-Memory Employee Repository

Driven adapter (secondary adapter) that implements the EmployeeRepository port
using an in-memory list. Contains all the filter, sort, and pagination logic.

This is the only place in the codebase that knows about the physical layout of
the data — all other layers work through the port abstraction.
"""

from datetime import datetime, timezone
from typing import Any

from app.domain.entities import Employee, FieldDefinition
from app.domain.ports.employee_repository import EmployeeRepository
from app.domain.value_objects import SearchFilter, SearchQuery, SearchResult
from app.infrastructure.sample_data import EMPLOYEES, FIELD_DEFINITIONS

# Build a fast lookup: camelCase field name → FieldDefinition
_FIELD_MAP: dict[str, FieldDefinition] = {f.field: f for f in FIELD_DEFINITIONS}


class InMemoryEmployeeRepository(EmployeeRepository):
    """Concrete implementation storing employees in RAM."""

    def get_field_definitions(self) -> list[FieldDefinition]:
        return list(FIELD_DEFINITIONS)

    # ── Public search interface ───────────────────────────────────────────────

    def search(self, query: SearchQuery) -> SearchResult:
        matched = self._apply_query(query)
        total = len(matched)
        total_pages = max(1, -(-total // query.page_size))  # ceiling division

        start = (query.page - 1) * query.page_size
        page_slice = matched[start : start + query.page_size]

        return SearchResult(
            data=tuple(e.to_dict() for e in page_slice),
            total=total,
            page=query.page,
            page_size=query.page_size,
            total_pages=total_pages,
        )

    def get_all_matching(self, query: SearchQuery) -> list[Employee]:
        return self._apply_query(query)

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _apply_query(self, query: SearchQuery) -> list[Employee]:
        results = list(EMPLOYEES)

        # 1. Full-text search across all string-serialisable values
        if query.text.strip():
            results = [e for e in results if self._matches_text(e, query.text)]

        # 2. Attribute filters combined with AND / OR
        if query.filters:
            if query.combinator == "and":
                results = [e for e in results if all(self._apply_filter(e, f) for f in query.filters)]
            else:
                results = [e for e in results if any(self._apply_filter(e, f) for f in query.filters)]

        # 3. Sort
        results.sort(
            key=lambda e: self._sort_key(e.to_dict(), query.sort_field),
            reverse=(query.sort_order == "desc"),
        )

        return results

    # ── Text search ───────────────────────────────────────────────────────────

    @staticmethod
    def _matches_text(employee: Employee, text: str) -> bool:
        needle = text.lower()
        return any(needle in str(v).lower() for v in employee.to_dict().values())

    # ── Attribute filter dispatch ─────────────────────────────────────────────

    def _apply_filter(self, employee: Employee, f: SearchFilter) -> bool:
        field_def = _FIELD_MAP.get(f.field)
        if not field_def:
            return False

        raw = employee.to_dict().get(f.field)

        match field_def.type:
            case "string":
                return self._filter_string(raw, f.operator, f.value)
            case "number":
                return self._filter_number(raw, f.operator, f.value)
            case "date":
                return self._filter_date(raw, f.operator, f.value)
            case "boolean":
                return self._filter_boolean(raw, f.operator, f.value)
            case _:
                return True

    # ── Per-type filter logic ─────────────────────────────────────────────────

    @staticmethod
    def _filter_string(raw: Any, operator: str, value: Any) -> bool:
        if operator == "is_empty":
            return raw is None or str(raw).strip() == ""
        if operator == "is_not_empty":
            return raw is not None and str(raw).strip() != ""

        if raw is None:
            return False
        sv = str(raw).lower()
        fv = str(value).lower() if value is not None else ""

        match operator:
            case "contains":         return fv in sv
            case "not_contains":     return fv not in sv
            case "equals":           return sv == fv
            case "not_equals":       return sv != fv
            case "starts_with":      return sv.startswith(fv)
            case "ends_with":        return sv.endswith(fv)
            case _:                  return True

    @staticmethod
    def _filter_number(raw: Any, operator: str, value: Any) -> bool:
        if operator == "is_empty":
            return raw is None
        if operator == "is_not_empty":
            return raw is not None

        if raw is None:
            return False
        try:
            num = float(raw)
        except (ValueError, TypeError):
            return False

        try:
            match operator:
                case "equals":               return num == float(value)
                case "not_equals":           return num != float(value)
                case "greater_than":         return num > float(value)
                case "greater_than_or_equal": return num >= float(value)
                case "less_than":            return num < float(value)
                case "less_than_or_equal":   return num <= float(value)
                case "between":
                    lo, hi = (float(v.strip()) for v in str(value).split(",", 1))
                    return lo <= num <= hi
                case _:
                    return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def _parse_dt(s: Any) -> datetime | None:
        if s is None:
            return None
        try:
            return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        except ValueError:
            return None

    def _filter_date(self, raw: Any, operator: str, value: Any) -> bool:
        if operator == "is_empty":
            return raw is None
        if operator == "is_not_empty":
            return raw is not None

        dv = self._parse_dt(raw)
        fv = self._parse_dt(value)
        if dv is None or (fv is None and operator != "between"):
            return False

        match operator:
            case "before":            return dv < fv
            case "after":             return dv > fv
            case "before_or_equals":  return dv <= fv
            case "after_or_equals":   return dv >= fv
            case "equals":            return dv.date() == fv.date()
            case "not_equals":        return dv.date() != fv.date()
            case "between":
                try:
                    parts = str(value).split(",", 1)
                    start = self._parse_dt(parts[0].strip())
                    end   = self._parse_dt(parts[1].strip())
                    return start <= dv <= end
                except (IndexError, TypeError):
                    return False
            case _:
                return True

    @staticmethod
    def _filter_boolean(raw: Any, operator: str, value: Any) -> bool:
        if raw is None:
            return False
        bv = bool(raw)
        fv = value is True or str(value).lower() == "true"
        match operator:
            case "equals":     return bv == fv
            case "not_equals": return bv != fv
            case _:            return True

    # ── Sort key ──────────────────────────────────────────────────────────────

    @staticmethod
    def _sort_key(item: dict, field: str) -> tuple:
        val = item.get(field)
        if val is None:
            return (1, "")       # None → sorts after non-None values
        if isinstance(val, bool):
            return (0, int(val))
        if isinstance(val, (int, float)):
            return (0, val)
        return (0, str(val).lower())
