#!/usr/bin/env python3

import sys

target_list = ["mmx","popcnt","sse","sse2","sse3","ssse3","sse4.1","sse4.2",
               "avx","avx2","sse4a","fma4","xop","fma","avx512f","bmi","bmi2",
               "aes","pclmul","avx512vl","avx512bw","avx512dq","avx512cd",
               "avx512vbmi","avx512ifma","avx512vpopcntdq","avx512vbmi2","gfni",
               "vpclmulqdq","avx512vnni","avx512bitalg","avx512bf16",
               "avx512vp2intersect","3dnow","adx","abm","cldemote","clflushopt",
               "clwb","clzero","cx16","enqcmd","f16c","fsgsbase","fxsr","hle",
               "sahf","lwp","lzcnt","movbe","movdir64b","movdiri","mwaitx",
               "pconfig","pku","prfchw","ptwrite","rdpid","rdrnd","rdseed",
               "rtm","serialize","sgx","sha","shstk","tbm","tsxldtrk","vaes",
               "waitpkg","wbnoinvd","xsave","xsavec","xsaveopt","xsaves",
               "amx-tile","amx-int8","amx-bf16","uintr","hreset","kl","widekl",
               "avxvnni","avx512fp16","avxifma","avxvnniint8","avxneconvert",
               "cmpccxadd","amx-fp16","prefetchi","raoint","amx-complex",
               "avxvnniint16","sm3","sha512","sm4","apxf","usermsr","avx10.1",
               "avx10.2","amx-avx512","amx-tf32","amx-transpose","amx-fp8",
               "movrs","amx-movrs"]

ignore_title = set(["PTA_64BIT"])

rev_mapping = {"PTA_NO_SAHF": "sahf"}

def covert_title(name):
    if name.startswith("PTA_"):
        name = name[4:]
    name = name.lower()
    if name.startswith("amx_"):
        name = name.replace("amx_", "amx-")
    if name.startswith("sse4_"):
        name = name.replace("sse4_", "sse4.")
    if name.startswith("avx10_"):
        name = name.replace("avx10_", "avx10.")
    if name == "user_msr":
        name = "usermsr"
    if name == "apx_f":
        name = "apxf"
    if name in rev_mapping:
        name = rev_mapping[name]
    return name

if __name__ == "__main__":
    i386_h_path = sys.argv[1]
    with open(i386_h_path, 'r') as f:
        lines = f.readlines()
    name = ""
    buf = ""
    PTA_dict = dict()
    name_seq = []
    def add_to_dict(add_item):
        if add_item in PTA_dict:
            cur_set.update(PTA_dict[add_item])
        else:
            cur_set.add(add_item)
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
    print(",".join(["target"] + target_list))
    for name in name_seq:
        cur_vec = [0] * len(target_list)
        for item in PTA_dict[name]:
            if item in ignore_title:
                continue
            if item in rev_mapping:
                continue
            cur_vec[target_list.index(covert_title(item))] = 1
        for item in rev_mapping:
            cur_vec[target_list.index(rev_mapping[item])] = int(item not in PTA_dict[name])
        print(",".join([name.replace("PTA_", "").lower()] + list(map(str, cur_vec))))
