from __future__ import annotations

import configparser
import os
from dataclasses import dataclass

from qgendapy.exceptions import ConfigurationError


@dataclass
class QGendaConfig:
    email: str
    password: str
    company_key: str
    base_url: str = "https://api.qgenda.com/v2"


def _load_ini() -> dict[str, str]:
    """Load config from INI file if QGENDA_CONF_FILE is set."""
    conf_file = os.environ.get("QGENDA_CONF_FILE")
    if not conf_file:
        return {}

    section = os.environ.get("QGENDA_CONF_REGION", "qgenda")
    parser = configparser.ConfigParser()
    parser.read(conf_file)

    if not parser.has_section(section):
        return {}

    result: dict[str, str] = {}
    items = dict(parser.items(section))

    # INI uses "username" which maps to email
    if "username" in items:
        result["email"] = items["username"]
    if "password" in items:
        result["password"] = items["password"]
    if "company_key" in items:
        result["company_key"] = items["company_key"]

    # Combine api_url and api_version into base_url
    api_url = items.get("api_url", "")
    api_version = items.get("api_version", "")
    if api_url:
        base = api_url.rstrip("/")
        if api_version:
            base = f"{base}/{api_version}"
        result["base_url"] = base

    return result


def resolve_config(
    email: str | None = None,
    password: str | None = None,
    company_key: str | None = None,
    base_url: str | None = None,
) -> QGendaConfig:
    """Resolve configuration from args > env vars > INI file > defaults.

    Priority:
        1. Explicit keyword arguments
        2. Environment variables: QGENDA_EMAIL, QGENDA_PASSWORD,
           QGENDA_COMPANY_KEY, QGENDA_BASE_URL
        3. INI file pointed to by QGENDA_CONF_FILE (section from
           QGENDA_CONF_REGION, default "qgenda")
        4. Default base_url only

    Raises ConfigurationError if email, password, or company_key cannot be resolved.
    """
    ini = _load_ini()

    resolved_email = email or os.environ.get("QGENDA_EMAIL") or ini.get("email")
    resolved_password = password or os.environ.get("QGENDA_PASSWORD") or ini.get("password")
    resolved_company_key = (
        company_key or os.environ.get("QGENDA_COMPANY_KEY") or ini.get("company_key")
    )
    resolved_base_url = (
        base_url
        or os.environ.get("QGENDA_BASE_URL")
        or ini.get("base_url")
        or "https://api.qgenda.com/v2"
    )

    missing: list[str] = []
    if not resolved_email:
        missing.append("email")
    if not resolved_password:
        missing.append("password")
    if not resolved_company_key:
        missing.append("company_key")

    if missing:
        raise ConfigurationError(
            f"Missing required configuration: {', '.join(missing)}. "
            "Provide via arguments, environment variables (QGENDA_EMAIL, etc.), "
            "or an INI file (QGENDA_CONF_FILE)."
        )

    # After the missing check above, these are guaranteed to be str
    return QGendaConfig(
        email=resolved_email,  # type: ignore[arg-type]  # narrowed by missing check
        password=resolved_password,  # type: ignore[arg-type]  # narrowed by missing check
        company_key=resolved_company_key,  # type: ignore[arg-type]  # narrowed by missing check
        base_url=resolved_base_url,
    )
