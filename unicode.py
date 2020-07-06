#!/usr/bin/env python

import sys
import unicodedata
from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
from charts import db

normalize_mode_list = ["NFC", "NFKC", "NFD", "NFKD" ]

wdb = {
    # opt.eaa_mode
    True: { "F": 2, "H": 1, "W": 2, "Na": 1, "A": 2, "N": 1 },
    False: { "F": None, "H": None, "W": None, "Na": 1, "A": 1, "N": 1 }
}

def normalize(text, mode="NFC"):
    return unicodedata.normalize(mode, text)

def find_category(category_hint):
    """find categories by category_hint, which is a whole or a part of a key."""
    ret = []
    hint = category_hint.lower()
    for c,x in db.items():
        if c.lower().find(hint) > -1:
            ret.append(c)
    if len(ret) == 0:
        raise ValueError("ERROR: not found any category containing "
                         f"the string '{keyword}'")
    return ret

def find_subc(whole_key=None, keyword=None, category=None):
    """
    find sub categories by an entire key or a keyword (a part of a key).
    return the list of (subcategory name, the range of code points).
    either whole_key or keyword, but not both, must be specified.
    XXX need to be cleaned up.
    """
    if not (bool(whole_key) ^ bool(keyword)):
        raise ValueError("ERROR: either key or keyword must be specified.")
    cp_list = []
    if keyword is not None:
        # i.e. whole_key is None
        keyword = keyword.lower()
        if category:
            for k,v in db[category].items():
                if k.lower().find(keyword) > -1:
                    cp_list.append((k,v))
        else:
            # try to search with whole items in db.
            for c,x in db.items():
                for k,v in x.items():
                    if k.lower().find(keyword) > -1:
                        cp_list.append((k,v))
        #
        if opt.strict_search == True:
            if len(cp_list) == 0:
                raise ValueError("ERROR: not found any chars coresponding "
                                 f"to the key '{keyword}' "
                                 f"in category '{category}'")
        return cp_list
    else:
        # i.e. whole_key is not None
        return [db[category][subcategory]]

def print_chars(subc, cr, opt):
    """Need to improve to show charactors using the width of each charactor.
    subc: name of the sub category.
    cr: range of the code points.
    """
    def concat_ab(a, b):
        return "{}-{}".format(hex(a)[2:].upper(),hex(b)[2:].upper())
    def add_clist(clist, v0, v1):
        for i in range(cr[0],cr[1]+1):
            w_area = unicodedata.east_asian_width(chr(i))
            width = 2 if wdb[True].get(w_area) == 1 else 1
            clist.append(f"{chr(i).ljust(width)}")
    #
    clist = []
    if len(cr) == 1:
        print(f"{subc} {hex(cr[0])[2:].upper()} {1}")
        add_clist(clist, cr[0], cr[0])
    elif len(cr) == 2:
        print("{} {} {}".format(subc, concat_ab(cr[0],cr[1]), cr[1]-cr[0]+1))
        add_clist(clist, cr[0], cr[1])
    elif len(cr) == 4:
        print("{} {} {} {}".format(subc,
                                   concat_ab(cr[0],cr[1]),
                                   concat_ab(cr[2],cr[3]),
                                   (cr[1]-cr[0]+1)+(cr[3]-cr[2]+1)))
        add_clist(clist, cr[0], cr[1])
        add_clist(clist, cr[2], cr[3])
    #
    print("    ", " ".join([f"{i:2}" for i in range(opt.nb_columns)]))
    for i,n in enumerate(range(opt.nb_columns, len(clist), opt.nb_columns)):
        print(f"{i:-4}", " ".join(clist[n:n+opt.nb_columns]))

def count_text_verbose(text):
    total_size = 0
    n = 1
    for i in text:
        total_size += 1
        w_area = unicodedata.east_asian_width(i)
        width = wdb[opt.eaa_mode].get(w_area)
        print(f"{n:-3} {i:3} {w_area:2} {width:2}")
        n += 1
    return total_size

def count_text(text):
    total_size = 0
    for i in text:
        total_size += 1
    return total_size

#
# functions
#
def func_list(opt):
    """
    if neither category nor keyword is specified, just print all categories.
    """
    if opt.category_hint is None and opt.show_all_chars:
        raise ValueError("ERROR: the option -c must be defined when you use"
                         "the -a option")
    # print all categories.
    if opt.category_hint is None and opt.keyword is None:
        for category,x in db.items():
            print(f"-c '{category}'")
        return
    #
    #
    if opt.keyword: # i.e. -k option, or plus -c option.
        cp_list = []
        if opt.category_hint:
            for c in find_category(opt.category_hint):
                cp_list.extend(find_subc(keyword=opt.keyword, category=c))
        else:
            cp_list.extend(find_subc(keyword=opt.keyword))
        for subc,cp_range in cp_list:
            print_chars(subc, cp_range, opt)
    elif opt.category_hint: # i.e. only -c option.
        xcp_list = []
        for c in find_category(opt.category_hint):
            for k,v in db[c].items():
                xcp_list.append((c,k,v))
        if opt.show_all_chars:
            for c,subc,cp_range in xcp_list:
                print_chars(subc, cp_range, opt)
        else:
            # showing the list of sub categories.
            for c,subc,cp_range in xcp_list:
                if opt.show_cp:
                    print(f"-c '{c}' -k '{subc}': {db[c][subc]}")
                else:
                    print(f"-c '{c}' -k '{subc}'")

def func_read(opt):
    if opt.input_file == "-":
        fd = sys.stdin
    else:
        fd = open(opt.input_file)
    if opt.count_mode:
        if opt.verbose:
            func = count_text_verbose
        else:
            func = count_text
        nb_char = 0
        for line in fd:
            nb_char += func(unicodedata.normalize("NFC", line))
        print(nb_char)
    else:
        for line in fd:
            # this trick is for conversion the \u representation.
            line = line.encode("utf-8").decode("utf-8")
            print(normalize(line, opt.normalize_mode), end="")

def func_show(opt):
    base = 16
    if opt.integer:
        base = 10
    if opt.series:
        if len(opt.code_point) != 2:
            raise ValueError("ERROR: two code_points must be specified "
                             "with the option -s.")
        n_start = int(opt.code_point[0], base)
        n_end = int(opt.code_point[1], base)
        #
        if opt.virtical_node:
            if opt.verbose:
                for n in range(n_start, n_end+1):
                    c = chr(n)
                    print(f"{n:6X}: {c} : {unicodedata.name(c)}")
            else:
                for i in range(n_start, n_end+1):
                    print(f"{chr(i)}")
        else:
            for i in range(n_start, n_end+1):
                print(f"{chr(i)}", end="")
    else:
        if opt.virtical_node:
            if opt.verbose:
                for i in opt.code_point:
                    n = int(i,base)
                    c = chr(n)
                    print(f"{n:6X}: {c} : {unicodedata.name(c)}")
            else:
                for i in opt.code_point:
                    print(f"{chr(int(i,base))}")
        else:
            for i in opt.code_point:
                print(f"{chr(int(i,base))}", end="")
    if opt.newline:
        print("")

#
# main
#
ap = ArgumentParser(
        description="a unicode tool.",
        formatter_class=ArgumentDefaultsHelpFormatter)
subp = ap.add_subparsers(dest="parser_name", help="sub-command help")
# list
sap0 = subp.add_parser("list", aliases=["l"],
                       help="""showing unicode chars. It just shows the list
                       of the categories if you don't specify any arguments.""")
sap0.add_argument("-c", action="store", dest="category_hint",
                  help="specify a category or a part of category name.")
sap0.add_argument("-a", action="store_true", dest="show_all_chars",
                  help="show all chars under the category specified.")
sap0.add_argument("--show-code-point", action="store_true", dest="show_cp",
                  help="show the range of code point.")
sap0.add_argument("-k", action="store", dest="keyword",
                  help="specify a keyword of the unicode sub category name.")
sap0.add_argument("--strict", action="store_true", dest="strict_search",
                  help="specify to search strictly.")
sap0.add_argument("--columns", action="store", dest="nb_columns",
                  type=int, default=20,
                  help="specify the number of the columns to show.")
sap0.set_defaults(func=func_list)
# read
sap1 = subp.add_parser("read", aliases=["r"],
                       help="read text and do something.")
sap1.add_argument("-f", action="store", dest="input_file",
                  help="specify the filename. '-' can be used as stdin.")
sap1.add_argument("-c", action="store_true", dest="count_mode",
                  help="enable to count chars")
sap1.add_argument("-E", action="store_false", dest="eaa_mode",
                  help="disable to handle the input text as EAA.")
sap1.add_argument("--normalize-mode", action="store", dest="normalize_mode",
                  default="NFC",
                  help=f"""specify a mode to normalize. valid mode is:
                  {normalize_mode_list}""")
sap1.add_argument("-v", action="store_true", dest="verbose",
                  help="enable verbose mode.")
sap1.set_defaults(func=func_read)
# show
sap2 = subp.add_parser("show", aliases=["s"],
                       help="show a single char specified by a code point")
sap2.add_argument("code_point", nargs="+",
                  help="a list of code points.")
sap2.add_argument("-s", action="store_true", dest="series",
                  help="indicate to show a list of code points "
                  "from the 1st to the 2nd.")
sap2.add_argument("-l", action="store_true", dest="virtical_node",
                  help="specify to show the chars in virtical.")
sap2.add_argument("-i", action="store_true", dest="integer",
                  help="specify that the code points are in integer.")
sap2.add_argument("-v", action="store_true", dest="verbose",
                  help="enable verbose mode, valid in the virtical mode.")
sap2.add_argument("-N", "--no-newline", action="store_false", dest="newline",
                  help="disable to add a newline at the end of the list.")
sap2.set_defaults(func=func_show)
#
opt = ap.parse_args()
if opt.parser_name is None:
    ap.print_help()
    exit(0)

opt.func(opt)
