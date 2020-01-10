from app import create_app


def test_config(app):
    assert app.testing
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
