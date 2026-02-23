"""
Adapter (secondary) – loads ObjectTypeConfig values from JSON files.

The JSON files live in app/domain/object_types/ and share the exact same
format as the frontend assets/object-types/*.json files.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

from app.domain.entities.field_config import FieldConfig, ObjectTypeConfig, SelectOption
from app.domain.repositories.object_config_repository import ObjectConfigRepository

# Resolved once at import time so the path is correct regardless of the
# working directory from which the server is started.
_DEFAULT_DIR = Path(__file__).resolve().parent.parent.parent / "domain" / "object_types"


class FileObjectConfigRepository(ObjectConfigRepository):
    """Reads every *.json file in the object_types directory at construction."""

    def __init__(self, directory: Path = _DEFAULT_DIR) -> None:
        self._configs: Dict[str, ObjectTypeConfig] = {}
        self._load_all(directory)

    # ------------------------------------------------------------------
    # ObjectConfigRepository port
    # ------------------------------------------------------------------

    def find_all(self) -> List[ObjectTypeConfig]:
        return list(self._configs.values())

    def find_by_resource(self, resource: str) -> Optional[ObjectTypeConfig]:
        """Match by the last segment of apiEndpoint, e.g. 'persons'."""
        for config in self._configs.values():
            if config.resource == resource:
                return config
        return None

    def find_by_object_type(self, object_type: str) -> Optional[ObjectTypeConfig]:
        return self._configs.get(object_type)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load_all(self, directory: Path) -> None:
        for json_file in sorted(directory.glob("*.json")):
            with json_file.open(encoding="utf-8") as fh:
                raw = json.load(fh)
            config = self._parse(raw)
            self._configs[config.object_type] = config

    @staticmethod
    def _parse(raw: dict) -> ObjectTypeConfig:
        fields: List[FieldConfig] = []
        for f in raw.get("fields", []):
            options: Optional[List[SelectOption]] = None
            if "options" in f:
                options = [
                    SelectOption(label=o["label"], value=o["value"])
                    for o in f["options"]
                ]
            fields.append(
                FieldConfig(
                    name=f["name"],
                    label=f["label"],
                    type=f["type"],
                    required=f.get("required", False),
                    min_length=f.get("minLength"),
                    max_length=f.get("maxLength"),
                    min=f.get("min"),
                    max=f.get("max"),
                    pattern=f.get("pattern"),
                    default=f.get("default"),
                    options=options,
                    placeholder=f.get("placeholder"),
                    hint=f.get("hint"),
                )
            )
        return ObjectTypeConfig(
            object_type=raw["objectType"],
            display_name=raw["displayName"],
            api_endpoint=raw["apiEndpoint"],
            fields=fields,
        )
