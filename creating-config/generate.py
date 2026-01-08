#!/usr/bin/env python3

import os
import re
import json

files = sorted(os.listdir('.'))

METADATA = {}
EXAMPLE_MODEL_CONFIGS = []

for file in files:
    if file == 'index.html.in':
        continue

    if file == 'index.html':
        continue

    if file == 'generate.py':
        continue

    basename = os.path.splitext(file)[0]

    with open(file, 'r', encoding='UTF-8') as fh:
        content = fh.read()

    m = re.search(r'<!--.*-->', content, re.DOTALL)
    if not m:
        print("Missing metadata comment:", file)
        continue

    comment = m[0]
    comment = comment.replace('<!--', '')
    comment = comment.replace('-->', '')
    metadata = json.loads(comment)

    METADATA[basename] = metadata

for basename, metadata in METADATA.items():
    registers = []
    methods = []

    for item, data in metadata.items():
        if data['type'] == 'register':
            registers.append(f'<b>{item}</b> ({data["mode"]})')

        if data['type'] == 'method':
            methods.append(f'<b>{item}</b> ({data["mode"]})')

    url = '%s.html' % basename.replace(' ', '%20')

    table_row = f'''\
          <tr>
            <td><a href="{url}">{basename}</a></td>
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
