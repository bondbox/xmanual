# coding:utf-8

import gzip
from html import escape
from html import unescape
import os
import re
from tempfile import TemporaryDirectory
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

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

    @classmethod
    def read_xml_tree(cls, page: str) -> Element:
        ctx = man.read_xml(page)
        xml = re.sub("\\&\\w+\\;", lambda x: escape(unescape(x.group(0))), ctx)
        return ElementTree.fromstring(xml)
