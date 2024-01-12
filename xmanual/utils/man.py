# coding:utf-8

import gzip
import os
from tempfile import TemporaryDirectory

from doclifter import main as doclifter


class man:
    def __init__(self):
        pass

    @classmethod
    def where(cls, page: str) -> str:
        return os.popen(f"man --where {page}").read().strip()

    @classmethod
    def read(cls, page: str) -> str:
        path = man.where(page)
        if os.path.splitext(path)[1] == ".gz":
            return gzip.open(path).read().decode()
        else:
            return open(path).read()

    @classmethod
    def read_xml(cls, page: str) -> str:
        with TemporaryDirectory() as tmp:
            path = os.path.join(tmp, page)
            with open(path, "w") as fman:
                fman.write(man.read(page))
            doclifter([path])
            return open(f"{path}.xml").read()
