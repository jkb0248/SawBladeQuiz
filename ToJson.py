import json
import sys
import re
import os
print(os.getcwd())
with open(sys.argv[1]) as q_fid:
    jobj = []
    obj = {}
    for line in q_fid:
        if re.match("^\s", line): # new line, new question
            jobj.append(obj)
            obj = None

        elif re.match("(\d)+\.(\d)+\.(\w)#(.*)$", line): # if this is the definition line
            match = re.search("(\d)\.(\d)\.(\w)#(.*)$", line)
            obj = {
                "type":"ratio",
                "header":match[4],
                "answer":ord(match[3].upper())-ord('A'),
                "data":[]
            }
        elif re.match("^[a-z]\.(.*)$", line) and obj is not None: # if this is a question line
            match = re.search("^[a-z]\.(.*)$", line)
            obj["data"].append(match[1])


    with open(os.path.splitext(sys.argv[1])[0] + ".json", 'w') as fout:
        json.dump(jobj, fout, indent=4)