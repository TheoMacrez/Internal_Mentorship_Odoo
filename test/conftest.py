from unittest.mock import MagicMock, Mock

import pytest


@pytest.fixture
def fake_connection():
    return Mock(name="fake_connection")


@pytest.fixture
def patch_get_connection(monkeypatch, fake_connection):
    def _patch(module_path):
        connection_context = MagicMock()
        connection_context.__enter__.return_value = fake_connection
        connection_context.__exit__.return_value = False

        get_connection = Mock(return_value=connection_context)
        monkeypatch.setattr(module_path, get_connection)

        return get_connection

    return _patch
