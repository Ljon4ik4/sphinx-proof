import shutil
import pytest

#from sphinx.testing.path import path
from pathlib import Path

pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture
def rootdir(tmpdir):
    src = Path(__file__).resolve().parent / "books"
    dst = tmpdir.join("books")
    shutil.copytree(src, dst)
    books = Path(dst)
    yield books
    shutil.rmtree(dst)


@pytest.fixture
def warnings():
    def read(app):
        return app._warning.getvalue().strip()

    return read
