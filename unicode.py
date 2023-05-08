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

#
# functions
#
def find_subc(keyword_hint=None, category_hint=None):
    """
    get a list of code points corresponding to the specified keyword_hint and/or
    the category_hint.  The hint could be an entire name, or a part of the name,
    or the index number of the database which is showed the list command.
    return the list of (category, subcategory, the range of code points).
    """
    def _get_cp_by_category_hint(hint):
        """return code points"""
        try:
            # check if the hint is a number.
            num = int(category_hint)
        except Exception as e:
            # the hint must be a name.
            categories = []
            hint = category_hint.lower()
            for c,x in db.items():
                if c.lower().find(hint) > -1:
                    categories.append(c)
            """
            if len(categories) == 0:
                raise ValueError("ERROR: not found any category containing "
                                f"the string '{category_hint}'")
            """
            ret = {}
            for c in categories:
                ret.update({c: db[c]})
            return ret
        else:
            x = list(db.items())[num]
            return {x[0]: x[1]}
    #
    if keyword_hint is None and category_hint is None:
        raise ValueError("ERROR: either keyword_hint or category_hint, "
                         "or both hints must be specified.")
    if keyword_hint and category_hint:
        cp_list_base = _get_cp_by_category_hint(category_hint)
        try:
            # check if the hint is a number.
            num = int(keyword_hint)
        except Exception as e:
            # the hint must be a name.
            cp_list = {}
            keyword_hint = keyword_hint.lower()
            for c,x in cp_list_base.items():
                cpx = cp_list.setdefault(c, {})
                for subc,cp_range in x.items():
                    if subc.lower().find(keyword_hint) > -1:
                        cpx.update({subc:cp_range})
            return cp_list
        else:
            offset = 0
            for i,(c,x) in enumerate(cp_list_base.items()):
                for j,(subc,cp_range) in enumerate(x.items()):
                    if num == offset+j:
                        return {c: {subc: cp_range}}
                offset += len(x)
            return {}
    elif keyword_hint:
        # but, not category_hint.
        pass
    elif category_hint:
        return _get_cp_by_category_hint(category_hint)

def func_list(opt):
    """
    it shows a list of the unicoe charactors by a range of the code points
    defined by the combination of the -c option and the -k option.
    if the combination doesn't unique a single subcategory, it shows
    a list of subcategories with the indices.
    but, with the -a option (show_all_chars), it shows entire charactors.
    """
    if opt.category_hint is None and opt.keyword_hint is None:
        # show a list of entire categories.
        for i,category in enumerate(db.keys()):
            print(f"{i}: {category}")
        return
    #
    cp_list = find_subc(keyword_hint=opt.keyword_hint, category_hint=opt.category_hint)
    if opt.show_all_chars or (len(cp_list.keys()) == 1 and
                              len(cp_list[list(cp_list.keys())[0]]) == 1):
        # show entire charactors.
        for c,x in cp_list.items():
            for subc,cp_range in x.items():
                print_chars(subc, cp_range, opt)
    else:
        # show a list of sub categories spcified by the hint.
        offset = 0
        for i,(c,x) in enumerate(cp_list.items()):
            print(f"## {c}")
            for j,(subc,cp_range) in enumerate(x.items()):
                if opt.show_cp:
                    print(f"{offset+j}: '{subc}': {cp_range}")
                else:
                    print(f"{offset+j}: '{subc}'")
            offset += len(x)

def read_char(text, nb_char, ofd):
    for c in text:
        nb_char += 1
        w_area = unicodedata.east_asian_width(c)
        width = wdb[opt.eaa_mode].get(w_area)
        ucode = ord(c).to_bytes(4, "big").hex().upper()
        name = unicodedata.name(c, None)
        # this trick is for conversion the \u representation.
        if c in ["\n", "\r", "\t"]:
            c = repr(c)
        ofd.write(bytes(f"{nb_char:-3}: [{c.ljust(2)}] {w_area:2} {width:2}: {ucode} {name}\n" .encode("utf-8")))
    return nb_char

def read_normal(text, nb_char, ofd):
    for c in text:
        nb_char += 1
    ofd.write(bytes(text.encode("utf-8")))
    return nb_char

def func_read(opt):
    if opt.input_file is None:
        ifd = sys.stdin
    else:
        ifd = open(opt.input_file)
    if opt.output_file is None:
        ofd = sys.stdout.buffer
    else:
        ofd = open(opt.output_file, "wb")
    if opt.list_mode:
        func = read_char
        print("No.  Chr    EAA SZ CP   Name")
        print("==== ====== === == ==== ==========")
    else:
        func = read_normal
    #
    nb_char = 0
    try:
        for line in ifd:
            norm_line = unicodedata.normalize(opt.normalize_mode, line)
            nb_char = func(norm_line, nb_char, ofd)
    finally:
        if opt.enable_count:
            ofd.write(bytes(f"{nb_char}\n".encode("utf-8")))
        ofd.close()

def func_show(opt):
    base = 16
    if opt.arg_integer:
        base = 10
    cp_list = []    # a list of code points in integer.
    # make a list of code points.
    if opt.series:
        if opt.arg_name:
            raise ValueError("ERROR: using both the options of -s and -n "
                             "in same time is not valid.")
        if len(opt.arg) != 2:
            raise ValueError("ERROR: two arg must be specified "
                             "with the option -s.")
        n_start = int(opt.arg[0], base)
        n_end = int(opt.arg[1], base)
        cp_list = [n for n in range(n_start, n_end+1)]
    elif opt.arg_name:
        if opt.arg_integer:
            raise ValueError("ERROR: using both the options of -i and -n "
                             "in same time is not valid.")
        if len(opt.arg) != 1:
            raise ValueError("ERROR: only one arg is allowed "
                             "for the option -n.")
        for i in range(0xfffff):
            if opt.arg[0] in unicodedata.name(chr(i), ""):
                cp_list.append(i)
    else:
        cp_list = [int(i, base) for i in opt.arg]
    # print the list.
    if opt.list_mode:
        if opt.with_name:
            for n in cp_list:
                c = chr(n)
                print(f"{n:6X}: {c} : {unicodedata.name(c)}")
        else:
            for i in cp_list:
                print(f"{chr(i)}")
    else:
        for i in cp_list:
            print(f"{chr(i)}", end="")
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
                       help="shows the list of the categories and charactors.")
sap0.add_argument("-c", action="store", dest="category_hint",
                  help="specify a unicode category, "
                    "which is case-insensitive, can be a part of the name, "
                  "can be a number in the list.")
sap0.add_argument("-a", action="store_true", dest="show_all_chars",
                  help="show all chars under the category specified.")
sap0.add_argument("--show-code-point", action="store_true", dest="show_cp",
                  help="show the range of code point.")
sap0.add_argument("-k", action="store", dest="keyword_hint",
                  help="specify a unicode sub category name, "
                    "which is case-insensitive, can be a part of the name, "
                  "can be a number in the list.")
sap0.add_argument("--columns", action="store", dest="nb_columns",
                  type=int, default=20,
                  help="specify the number of the columns to show.")
sap0.set_defaults(func=func_list)
# read
sap1 = subp.add_parser("read", aliases=["r"],
                       help="reads and converts text.")
sap1.add_argument("-f", action="store", dest="input_file",
                  help="specify the filename for input."
                  "default is stdin.")
sap1.add_argument("-o", action="store", dest="output_file",
                  help="specify the filename for output."
                  "default is stdout.")
sap1.add_argument("-l", action="store_true", dest="list_mode",
                  help="show the unicode name for each charactor.")
sap1.add_argument("-c", action="store_true", dest="enable_count",
                  help="add the number of charactors to the tail.")
sap1.add_argument("-E", action="store_false", dest="eaa_mode",
                  help="disable to handle the input text as EAA.")
sap1.add_argument("-n", "--normalize-mode",
                  action="store", dest="normalize_mode", default="NFC",
                  help=f"""specify a mode to normalize. valid mode is:
                  {normalize_mode_list}""")
#sap1.add_argument("-v", action="store_true", dest="verbose",
#                  help="enable verbose mode.")
sap1.set_defaults(func=func_read)
# show
sap2 = subp.add_parser("show", aliases=["s"],
                       help="shows a single char specified by the string. "
                       " it must be a code point in hex.")
sap2.add_argument("arg", nargs="+",
                  help="a code point in hex.")
sap2.add_argument("-s", action="store_true", dest="series",
                  help="indicate to show a series of the chars "
                  "specified by the two code points.")
sap2.add_argument("-l", action="store_true", dest="list_mode",
                  help="show the chars in virtical with the unicode name.")
sap2.add_argument("-i", action="store_true", dest="arg_integer",
                  help="specify that the arg is a code point in integer.")
sap2.add_argument("-n", action="store_true", dest="arg_name",
                  help="specify that the arg is a part of a unicode name.")
sap2.add_argument("-x", action="store_false", dest="with_name",
                  help="disable to show a unicode name of the option -l.")
sap2.add_argument("-N", "--no-newline", action="store_false", dest="newline",
                  help="disable to add a newline.")
sap2.set_defaults(func=func_show)
#
opt = ap.parse_args()
if opt.parser_name is None:
    ap.print_help()
    exit(0)

opt.func(opt)
