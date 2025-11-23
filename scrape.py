import time
import requests
import re
import json

w = []

for n in range(ord("a"), ord("z") + 1):
    char = chr(n) 
    res = requests.get(f"https://www.merriam-webster.com/wordfinder/classic/begins/common/5/{char}/1")
    content = res.text.replace("\n", "")

    pattern = re.compile(r'<a href="/dictionary/[a-zA-Z]+"')
    
    for match in pattern.findall(content):
        w.append(match[-6:-1])

    time.sleep(1.5)

with open("known.json", "w+", encoding="utf-8") as ofile:
    json.dump(w, ofile)