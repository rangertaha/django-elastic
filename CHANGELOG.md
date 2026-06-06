# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- **Python 2 → Python 3.** Modernized the whole codebase: `print`
  statements → `print()`, `__unicode__` → `__str__`, `dict.iteritems()` →
  `dict.items()`, `super(Cls, self)` → `super()`, `__metaclass__` →
  `metaclass=`, and bare `except:` → `except Exception:`.
- **Django 1.9 → Django 4.2–5.2 (LTS).** `MIDDLEWARE_CLASSES` → `MIDDLEWARE`,
  `django.conf.urls.url` → `django.urls.path`, removed `Signal(providing_args=…)`
  (removed in Django 4.0), `default_app_config` removed (auto-detected since
  3.2), dropped `TEMPLATE_DEBUG`/`USE_L10N`, set `USE_TZ = True` and
  `DEFAULT_AUTO_FIELD`.
- **elasticsearch 2.x → 8.18–9.x.** Switched from the standalone
  `elasticsearch-dsl` package to the bundled `elasticsearch.dsl`
  (`String` → `Text`, `InnerObjectWrapper` → `InnerDoc`, `DocType` →
  `Document`). Dropped the removed mapping `doc_type` parameter from
  `index`/`delete`/`Search`, switched `body=` → `document=`, and added scheme
  normalization so hosts resolve to node URLs (e.g. `http://localhost:9200`).
- Timestamps are now timezone-aware (`datetime.now(timezone.utc)`).

### Packaging

- Migrated from `setup.py` to a PEP 621 `pyproject.toml` (setuptools backend).
- Declared `requires-python = ">=3.9"` and current Django/Python classifiers.
- Trimmed the sdist (no built docs HTML or `.pyc` files) and added project URLs.
- Added a GitHub Actions workflow to publish to PyPI via Trusted Publishing
  (OIDC) on release.
