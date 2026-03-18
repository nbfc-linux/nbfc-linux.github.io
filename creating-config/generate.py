#!/usr/bin/env python3

import os
import re
import json
from urllib.parse import quote

FILES = sorted(os.listdir('.'))
IGNORE = ('index.html', 'index.html.in', 'generate.py', 'analyze_alternative.html')
EXAMPLE_MODEL_CONFIGS = []

def extract_metadata_comment(file):
    with open(file, 'r', encoding='UTF-8') as fh:
        content = fh.read()

    m = re.search(r'<!--.*-->', content, re.DOTALL)
    if not m:
        raise Exception("Missing metadata comment: %s" % file)

    comment = m[0]
    comment = comment.replace('<!--', '')
    comment = comment.replace('-->', '')
    return json.loads(comment)

for file in FILES:
    if file in IGNORE:
        continue

    basename = os.path.splitext(file)[0]
    metadata = extract_metadata_comment(file)
    methods = []
    registers = []

    for item, data in metadata.items():
        if data['type'] == 'register':
            registers.append(f'<b>{item}</b> ({data["mode"]})')

        if data['type'] == 'method':
            methods.append(f'<b>{item}</b> ({data["mode"]})')

    table_row = f'''\
          <tr>
            <td><a href="{quote(file)}">{basename}</a></td>
            <td>{', '.join(registers)}</td>
            <td>{', '.join(methods)}</td>
          </tr>'''

    EXAMPLE_MODEL_CONFIGS.append(table_row)

EXAMPLE_MODEL_CONFIGS = '\n'.join(EXAMPLE_MODEL_CONFIGS)

with open('index.html.in', 'r', encoding='UTF-8') as fh:
    content = fh.read()

content = content.replace("%EXAMPLE_MODEL_CONFIGS%", EXAMPLE_MODEL_CONFIGS)

with open('index.html', 'w', encoding='UTF-8') as fh:
    fh.write(content)
