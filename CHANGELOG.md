# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Test suite** (previously none): pytest + pytest-django covering the
  indexer registry and model-to-mapping translation, document cleaning,
  save/delete with signals, the settings host normalization, app config
  loading, and both management commands. All Elasticsearch interaction is
  mocked — the suite runs fully offline. Coverage of `delastic` went from
  0% to 97%.
- **CI workflow** (`.github/workflows/ci.yml`): pytest, Ruff (lint +
  format check), and mypy across Python 3.12 / 3.13 / 3.14 on pushes and
  pull requests to `master`.
- GitHub Actions workflow to publish to PyPI via Trusted Publishing (OIDC)
  on release (`.github/workflows/publish.yml`).
- Ruff lint/format and mypy configuration in `pyproject.toml`, plus a
  `dev` dependency group (pytest, pytest-django, pytest-cov, ruff, mypy).
- Lightweight type annotations for the metaclass-injected indexer
  attributes (`_meta`, `fields`, `registry`) so mypy passes cleanly.

### Changed

- **Moved the package to the `src/` layout** (`delastic/` →
  `src/delastic/`). The installed import path is unchanged
  (`import delastic`); packaging, the example project, and docs were
  updated accordingly.
- **Restructured the README**: what-it-is / install / quickstart within the
  first screenful, plus CI, PyPI, Python-version, and license badges, and a
  roadmap section flagging the unimplemented search view and
  `create_elastic_mapping` stub.
- Reformatted the codebase with `ruff format` and applied mechanical
  `ruff check --fix` cleanups (import sorting, modern syntax).
- **Python target raised to 3.12+** (SPEC 0): `requires-python = ">=3.12"`,
  classifiers now 3.12 / 3.13 / 3.14, and Ruff `target-version = "py312"`.
  Developed and smoke-tested on Python 3.14.
- **Dependencies bumped**: Django `>=5.2,<6.0` (5.2 LTS line; resolves to
  5.2.16) and elasticsearch `>=9.0,<10.0` (resolves to 9.4.1).
- Modernized code to the new baseline via pyupgrade (Ruff `UP` rules):
  removed `# -*- coding: utf-8 -*-` cookies, `class Foo(object)` →
  `class Foo:`, `str.format` → f-strings, and `datetime.now(timezone.utc)` →
  `datetime.now(UTC)`.
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
- Migrated from `setup.py` to a PEP 621 `pyproject.toml` (setuptools
  backend) and completed the metadata (keywords, changelog URL, SPDX
  license expression per PEP 639).
- Trimmed the sdist (no built docs HTML or `.pyc` files) and added project URLs.

### Fixed

- **License metadata mismatch**: `pyproject.toml` declared BSD-3-Clause
  while the repository `LICENSE` file has always been MIT (2016,
  rangertaha). The metadata and classifiers now say MIT; the `LICENSE`
  file itself is untouched.

### Removed

- 19 unused imports (Ruff F401) across `delastic/indexer.py`, the
  management commands, and the example app. Imports kept for their
  side effects (indexer registration, package re-exports) are now
  explicitly marked with `noqa` and a comment.
- Dead code in the example `get_articles` command (unused `image` /
  `description` locals and the now-unneeded BeautifulSoup import).

## [0.0.1] - 2016-08-03

_Reconstructed from git history (2016-07-18 – 2016-08-06) and the PyPI
release uploaded on 2016-08-03._

### Added

- Initial release: `ModelIndex` indexer that maps Django models to
  Elasticsearch documents, with `clean_<field>` overrides and an
  `indexable()` hook.
- Automatic index sync via `post_save`/`post_delete` signal receivers.
- Indexing lifecycle signals (`pre_index`, `post_index`, `pre_delete`,
  `post_delete`, and mapping variants).
- Management commands `create_elastic_index` and `create_elastic_mapping`
  (the latter a stub).
- `DJANGO_ELASTIC` settings with defaults (hosts, port, index).
- Example project (`example/`) with an RSS-fed `Article` model and
  indexer, and Sphinx documentation skeleton (`docs/`).

[Unreleased]: https://github.com/rangertaha/django-elastic/compare/master...HEAD
[0.0.1]: https://pypi.org/project/django-elastic/0.0.1/
