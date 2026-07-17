"""Tests for app config loading and package imports."""

from django.apps import apps


def test_app_config_is_loaded():
    config = apps.get_app_config("delastic")
    assert config.name == "delastic"
    assert apps.is_installed("delastic")


def test_package_reexports_signal_receivers():
    import delastic

    assert callable(delastic.es_index_instance)
    assert callable(delastic.es_delete_instance)


def test_signals_importable():
    from delastic import signals

    for name in (
        "pre_index",
        "post_index",
        "pre_delete",
        "post_delete",
        "mapping_pre_index",
        "mapping_post_index",
        "mapping_pre_delete",
        "mapping_post_delete",
    ):
        assert hasattr(signals, name)
