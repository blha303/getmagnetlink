#!/usr/bin/env python
from __future__ import print_function
import argparse
import os
import shutil
import sys
import types

try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode

from bs4 import BeautifulSoup as Soup
from prettytable import PrettyTable, NONE
import requests
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

input = raw_input if hasattr(__builtins__, 'raw_input') else input

magnet_template = "magnet:?xt=urn:btih:{}"
trackers = ["http://9.rarbg.com:2710/announce","http://announce.torrentsmd.com:6969/announce","http://bt.careland.com.cn:6969/announce","http://explodie.org:6969/announce","http://mgtracker.org:2710/announce","http://tracker.best-torrents.net:6969/announce","http://tracker.tfile.me/announce","http://tracker.torrenty.org:6969/announce","http://tracker1.wasabii.com.tw:6969/announce","udp://9.rarbg.com:2710/announce","udp://9.rarbg.me:2710/announce","udp://coppersurfer.tk:6969/announce","udp://exodus.desync.com:6969/announce","udp://open.demonii.com:1337/announce","udp://tracker.btzoo.eu:80/announce","udp://tracker.istole.it:80/announce","udp://tracker.openbittorrent.com:80/announce","udp://tracker.prq.to/announce","udp://tracker.publicbt.com:80/announce"]

class TorrentResult():
    def __init__(self, name, torrenthash):
        self.name = name
        self.torrenthash = torrenthash

def print_multicolumn(alist):
    """Formats a list into columns to fit on screen. Similar to `ls`. From http://is.gd/6dwsuA (daniweb snippet, search for func name)

    :param alist: list of data to print into columns

    >>> print_multicolumn(["a", "aa", "aaa", "aaaa"])
      a   aa   aaa   aaaa
    """
    try:
        ncols = shutil.get_terminal_size((80, 20)).columns // max(len(a) for a in alist)
    except AttributeError:
        ncols = 80 // max(len(a) for a in alist)
    try:
        nrows = - ((-len(alist)) // ncols)
        ncols = - ((-len(alist)) // nrows)
    except ZeroDivisionError:
        print("\n".join(alist), file=sys.stderr)
        return
    t = PrettyTable([str(x) for x in range(ncols)])
    t.header = False
    t.align = 'l'
    t.hrules = NONE
    t.vrules = NONE
    chunks = [alist[i:i+nrows] for i in range(0, len(alist), nrows)]
    chunks[-1].extend('' for i in range(nrows - len(chunks[-1])))
    chunks = zip(*chunks)
    for c in chunks:
        t.add_row(c)
    print(t, file=sys.stderr)

def choice(options, q="Enter your selection: "):
    if hasattr(options,'__iter__') and not hasattr(options,'__len__'):
        options = [o for o in options]
    if len(options) == 1:
        if type(options[0]) is tuple:
            print("Selecting {}...".format(options[0][1]), file=sys.stderr)
        else:
            print("Selecting {}...".format(options[0]), file=sys.stderr)
        return options[0][0] if type(options[0]) is tuple else options[0]
    if type(options[0]) is tuple:
        choices = ["{}: {}".format(a, b) for a,b in options]
    else:
        choices = options
    print_multicolumn(choices)
    if os.isatty(sys.stdout.fileno()):
        return prompt(q)

def prompt(*objs):
    old_stdout = sys.stdout
    try:
        sys.stdout = sys.stderr
        return input(*objs)
    finally:
        sys.stdout = old_stdout

def get_torrents(term):
    """ Gets a list of TorrentResults """
    data = Soup(requests.get("https://torrentz.eu/search?" + urlencode({"q": term})).text, "html.parser")
    output = []
    for dt in data.findAll('dt'):
        torhash = dt.find('a')["href"][1:]
        name = dt.text.split(" \xbb")[0]
        output.append(TorrentResult(name, torhash))
    return output

def get_magnet_link(torrent, trackers=trackers):
    """ Converts a TorrentResult into a magnet link using a predefined list of trackers """
    magnet_link = magnet_template.format(torrent.torrenthash)
    if torrent.name:
        magnet_link += "&{}".format(urlencode({"dn": torrent.name}))
    if trackers:
        magnet_link += "".join(["&tr={}".format(tr) for tr in trackers])
    return magnet_link

def main():
    parser = argparse.ArgumentParser(prog="getmagnetlink")
    parser.add_argument("term", help="Search term")
    args = parser.parse_args()
    try:
        torrents = get_torrents(args.term)
        picked = choice(enumerate([t.name for t in torrents]))
        if picked == "*":
            print("\n".join(get_magnet_link(torrent) for torrent in torrents))
        else:
            print(get_magnet_link(torrents[int(picked)]))
    except ValueError:
        print("Invalid input provided. Please use the numbers to the left of the torrent names.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        return 130

if __name__ == "__main__":
    sys.exit(main())
