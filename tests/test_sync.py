from pathlib import Path
import tempfile
from sync import sync
import shutil

class FakeFileSystem:
    def __init__(self, path_hashes):
        self.path_hashes = path_hashes
        self.actions = []

    def read(self, path):
        return self.path_hashes[path]

    def copy(self, source, dest):
        self.actions.append(('COPY', source, dest))

    def move(self, source, dest):
        self.actions.append(('MOVE', source, dest))

    def delete(self, dest):
        self.actions.append(('DELETE', dest))


def test_when_a_file_exists_in_the_source_but_not_the_destination():
    fake_fs = FakeFileSystem(
        {
            '/src': {"hash1": "fn1"},
            '/dst': {}
        })
    sync('/src', '/dst', filesystem=fake_fs)
    assert fake_fs.actions == [("COPY", Path("/src/fn1"), Path("/dst/fn1"))]

def test_when_a_file_has_been_renamed_in_the_source():
    fake_fs = FakeFileSystem(
        {
            '/src': {"hash1": "fn1"},
            '/dst': {"hash1": "fn2"}
        })
    sync('/src', '/dst', filesystem=fake_fs)
    assert fake_fs.actions == [("MOVE", Path("/dst/fn2"), Path("/dst/fn1"))]
