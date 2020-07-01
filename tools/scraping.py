#!/usr/bin/env python

# e.g.
#     python scraping.py -f charts.html > temp.txt
# or
#     python scraping.py https://www.unicode.org/charts/ > temp.txt
#
# temp.txt may be modified if you need.
# you can copy temp.txt into charset.py

import sys
import requests
from html.parser import HTMLParser
import json
import re

re_1 = re.compile("^([0-9a-fA-F]+)\s*$")
re_2 = re.compile("^([0-9a-fA-F]+)[-\u2013]([0-9a-fA-F]+)\s*$")
re_4 = re.compile("^([0-9a-fA-F]+)[-\u2013]([0-9a-fA-F]+),\s([0-9a-fA-F]+)[-\u2013]([0-9a-fA-F]+)\s*$")

convert_charrefs = True

class MyHTMLParser(HTMLParser):

    def __init__(self, *args, **kwargs):
        if convert_charrefs:
            HTMLParser.__init__(self, convert_charrefs = True)
        HTMLParser.__init__(self)
        self.title = None
        self.state = 0
        self.db = {}

    def debug_print(self, *args):
        #print(args)
        pass

    def _print(self, *args):
        #print(args)
        pass

    def print_db(self, python=False):
        print("db =", json.dumps(self.db, indent=2))

    def handle_starttag(self, tag, attrs):
        self.debug_print("TAG: [{}]".format(tag))
        self.debug_print(attrs)
        if tag == "p":
            if self.state in [0, 2] and attrs[0] == ("class","sg"):
                self.state = 1
                self.debug_print("=> state", self.state)
                return
            elif self.state in [2, 3] and (attrs[0] in [
                    ("class","mb"), ("class","pb"), ("class","sb")]):
                self.state = 3
                self.debug_print("=> state", self.state)
        elif tag == "a":
            if self.state == 3:
                for a in attrs:
                    if a[0] == "title":
                        if len(a) < 2:
                            raise ValueError(f"ERROR: {a}")
                        else:
                            self._print(f"attr: {a[1]}")
                            # e.g.
                            # ('title', 'FB50')
                            # ('title', '10450-1047F')
                            # ('title', '2654-265F, 26C0-26C3')
                            for rx in [re_1, re_2, re_4]:
                                r = rx.match(a[1])
                                if r:
                                    break
                            else:
                                raise ValueError(f"ERROR: {a[1]}")
                            self.attr = [int(i,16) for i in r.groups()]
                        break
                self.state = 2
                self.debug_print("=> state", self.state)

    def handle_endtag(self, tag):
        self.debug_print("END TAG:[{}]".format(tag))

    def handle_data(self, data):
        self.debug_print("DATA:[{}]".format(data))
        data = data.encode("utf-8").decode("utf-8")
        if self.state in [1, 2]:
            data = data.strip()
            if len(data) > 2:
                if self.state == 1:
                    self._print(f"category: {data}") # e.g. European Scripts
                    self.category = data
                elif self.state == 2:
                    self._print(f"subcategory: {data}") # e.g. Shavian
                    if "MB)" in data:
                        pass
                    else:
                        d = self.db.setdefault(self.category, {})
                        d.update({data: self.attr})
                self.state = 2
                self.debug_print("=> state", self.state)

if sys.argv[1] == "-f":
    html_text = open(sys.argv[2]).read()
else:
    url = sys.argv[1]
    ret = requests.get(url)
    ret.encoding = ret.apparent_encoding
    html_text = ret.text

p = MyHTMLParser()
p.feed(html_text)
p.print_db(python=True)
p.close()
