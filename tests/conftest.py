import pytest


@pytest.fixture(autouse=True)
def _register_indexers():
    """Ensure the test indexers are registered before every test."""
    from tests.testapp import indexers  # noqa: F401


@pytest.fixture
def es_client():
    """The mocked Elasticsearch client wired into ``ArticleIndex``."""
    from tests.testapp.indexers import MOCK_ES

    MOCK_ES.reset_mock(return_value=True, side_effect=True)
    yield MOCK_ES
    MOCK_ES.reset_mock(return_value=True, side_effect=True)
