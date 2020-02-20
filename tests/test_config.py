from game.config import Development, get_config


def test_get_default_config_when_invalid():
    assert isinstance(get_config('foo'), Development)


def test_get_default_config_when_none():
    assert isinstance(get_config(None), Development)
