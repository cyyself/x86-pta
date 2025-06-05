#!/usr/bin/env python3

import sys

if __name__ == "__main__":
    i386_h_path = sys.argv[1]
    with open(i386_h_path, 'r') as f:
        lines = f.readlines()
    name = ""
    buf = ""
    PTA_dict = dict()
    PTA_number = dict()
    name_seq = []
    def PTA_number_add(name):
        if name not in PTA_number:
            PTA_number[name] = len(PTA_number)
    def add_to_dict(add_item):
        if add_item in PTA_dict:
            cur_set.update(PTA_dict[add_item])
        else:
            cur_set.add(add_item)
            PTA_number_add(add_item)
    for line in lines:
        first_line = False
        if line.startswith("constexpr wide_int_bitmask PTA_"):
            line = line.replace("constexpr wide_int_bitmask ", "")
            # find the name of the PTA
            first_line = True
            if line.startswith("PTA_"):
                name = line.split("=")[0].strip()
                line = line.split("=")[1].strip()
        line = line.replace(" ", "")
        line = line.replace("\t", "")
        if first_line or buf != "":
            buf += line.strip()
            if buf.endswith(";"):
                buf = buf[:-1]
                CNF = buf.replace("(","").replace(")","").split("|")
                cur_set = set()
                remove_set = set()
                for each_cnf in CNF:
                    if '&~' in each_cnf:
                        each_cnf = each_cnf.split('&~')
                        add_to_dict(each_cnf[0])
                        remove_set.add(each_cnf[1])
                    else:
                        add_to_dict(each_cnf)
                PTA_dict[name] = cur_set - remove_set
                name_seq.append(name)
                name = ""
                buf = ""
    title = list(sorted(PTA_number.keys(), key=lambda x: PTA_number[x]))
    print(",".join(["target"] + title))
    for name in name_seq:
        cur_vec = [0] * len(title)
        for item in PTA_dict[name]:
            cur_vec[PTA_number[item]] = 1
        print(",".join([name] + list(map(str, cur_vec))))
