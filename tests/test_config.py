import pytest

from qgendapy._config import QGendaConfig, resolve_config
from qgendapy.exceptions import ConfigurationError


class TestResolveConfigExplicitArgs:
    def test_all_args_provided(self):
        cfg = resolve_config(
            email="a@b.com", password="pw", company_key="ck", base_url="https://example.com"
        )
        assert cfg == QGendaConfig(
            email="a@b.com", password="pw", company_key="ck", base_url="https://example.com"
        )

    def test_default_base_url(self):
        cfg = resolve_config(email="a@b.com", password="pw", company_key="ck")
        assert cfg.base_url == "https://api.qgenda.com/v2"

    def test_missing_email_raises(self):
        with pytest.raises(ConfigurationError, match="email"):
            resolve_config(password="pw", company_key="ck")

    def test_missing_password_raises(self):
        with pytest.raises(ConfigurationError, match="password"):
            resolve_config(email="a@b.com", company_key="ck")

    def test_missing_company_key_raises(self):
        with pytest.raises(ConfigurationError, match="company_key"):
            resolve_config(email="a@b.com", password="pw")

    def test_missing_all_raises(self):
        with pytest.raises(ConfigurationError):
            resolve_config()


class TestResolveConfigEnvVars:
    def test_env_vars_used(self, monkeypatch):
        monkeypatch.setenv("QGENDA_EMAIL", "env@test.com")
        monkeypatch.setenv("QGENDA_PASSWORD", "envpw")
        monkeypatch.setenv("QGENDA_COMPANY_KEY", "envck")
        monkeypatch.setenv("QGENDA_BASE_URL", "https://env.example.com")
        cfg = resolve_config()
        assert cfg.email == "env@test.com"
        assert cfg.password == "envpw"
        assert cfg.company_key == "envck"
        assert cfg.base_url == "https://env.example.com"

    def test_explicit_args_override_env(self, monkeypatch):
        monkeypatch.setenv("QGENDA_EMAIL", "env@test.com")
        monkeypatch.setenv("QGENDA_PASSWORD", "envpw")
        monkeypatch.setenv("QGENDA_COMPANY_KEY", "envck")
        cfg = resolve_config(email="explicit@test.com", password="pw", company_key="ck")
        assert cfg.email == "explicit@test.com"

    def test_env_vars_override_ini(self, monkeypatch, tmp_path):
        ini_content = """\
[qgenda]
username = ini@test.com
password = inipw
company_key = inick
"""
        ini_file = tmp_path / "qgenda.ini"
        ini_file.write_text(ini_content)
        monkeypatch.setenv("QGENDA_CONF_FILE", str(ini_file))
        monkeypatch.setenv("QGENDA_EMAIL", "env@test.com")
        monkeypatch.delenv("QGENDA_PASSWORD", raising=False)
        monkeypatch.delenv("QGENDA_COMPANY_KEY", raising=False)
        monkeypatch.delenv("QGENDA_BASE_URL", raising=False)

        cfg = resolve_config()
        assert cfg.email == "env@test.com"  # env overrides INI
        assert cfg.password == "inipw"  # falls through to INI


class TestResolveConfigINI:
    def test_ini_file_used(self, monkeypatch, tmp_path):
        ini_content = """\
[qgenda]
username = ini@test.com
password = inipw
company_key = inick
api_url = https://ini.example.com
api_version = v2
"""
        ini_file = tmp_path / "qgenda.ini"
        ini_file.write_text(ini_content)
        monkeypatch.setenv("QGENDA_CONF_FILE", str(ini_file))

        cfg = resolve_config()
        assert cfg.email == "ini@test.com"
        assert cfg.password == "inipw"
        assert cfg.company_key == "inick"
        assert cfg.base_url == "https://ini.example.com/v2"

    def test_ini_custom_section(self, monkeypatch, tmp_path):
        ini_content = """\
[prod]
username = prod@test.com
password = prodpw
company_key = prodck
api_url = https://prod.example.com
"""
        ini_file = tmp_path / "qgenda.ini"
        ini_file.write_text(ini_content)
        monkeypatch.setenv("QGENDA_CONF_FILE", str(ini_file))
        monkeypatch.setenv("QGENDA_CONF_REGION", "prod")

        cfg = resolve_config()
        assert cfg.email == "prod@test.com"
        assert cfg.base_url == "https://prod.example.com"

    def test_explicit_args_override_ini(self, monkeypatch, tmp_path):
        ini_content = """\
[qgenda]
username = ini@test.com
password = inipw
company_key = inick
"""
        ini_file = tmp_path / "qgenda.ini"
        ini_file.write_text(ini_content)
        monkeypatch.setenv("QGENDA_CONF_FILE", str(ini_file))

        cfg = resolve_config(email="explicit@test.com", password="pw", company_key="ck")
        assert cfg.email == "explicit@test.com"
        assert cfg.password == "pw"

    def test_missing_ini_section_ignored(self, monkeypatch, tmp_path):
        ini_content = """\
[other]
username = x
"""
        ini_file = tmp_path / "qgenda.ini"
        ini_file.write_text(ini_content)
        monkeypatch.setenv("QGENDA_CONF_FILE", str(ini_file))

        with pytest.raises(ConfigurationError):
            resolve_config()
