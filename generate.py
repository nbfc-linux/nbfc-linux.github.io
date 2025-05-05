#!/usr/bin/env python3

import os
import sys
import json
import requests

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def make_index_html():
    with open('index.in.html', 'r', encoding='UTF-8') as fh:
        content = fh.read()

    content = replace_nbfc_linux_download_vars(content)

    with open('index.html', 'w', encoding='UTF-8') as fh:
        fh.write(content)

def make_config_data_js():
    url = 'https://api.github.com/repos/nbfc-linux/configs/contents/1.0/configs';
    response = requests.get(url)
    response.raise_for_status()
    files = response.json()

    config_data = []
    for file in files:
        config_data.append(file['name'].replace('.json', ''))

    with open('configs/data.js', 'w', encoding='UTF-8') as fh:
        fh.write('const configs = ')
        json.dump(config_data, fh, indent=1)
        fh.write(';')

def replace_nbfc_linux_download_vars(content):
    url = "https://api.github.com/repos/nbfc-linux/nbfc-linux/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    releases = response.json()

    TAG = releases['tag_name']
    DEBIAN = None
    FEDORA = None
    ARCHLINUX = None
    OPENSUSE = None

    for release in releases['assets']:
        name = release['name']
        size = str(int(release['size'] / 1024))
        url  = release['browser_download_url']

        if name.endswith('.deb'):
            DEBIAN = (name, url, size)

        elif name.startswith('fedora-'):
            FEDORA = (name, url, size)

        elif name.startswith('opensuse-'):
            OPENSUSE = (name, url, size)

        elif name.endswith('pkg.tar.zst'):
            ARCHLINUX = (name, url, size)

    content = content.replace('%NBFC_LINUX_TAG%', TAG)

    content = content.replace('%NBFC_LINUX_ARCHLINUX_PACKAGE%', ARCHLINUX[0])
    content = content.replace('%NBFC_LINUX_ARCHLINUX_URL%',     ARCHLINUX[1])
    content = content.replace('%NBFC_LINUX_ARCHLINUX_KB%',      ARCHLINUX[2])

    content = content.replace('%NBFC_LINUX_DEBIAN_PACKAGE%',    DEBIAN[0])
    content = content.replace('%NBFC_LINUX_DEBIAN_URL%',        DEBIAN[1])
    content = content.replace('%NBFC_LINUX_DEBIAN_KB%',         DEBIAN[2])

    content = content.replace('%NBFC_LINUX_FEDORA_PACKAGE%',    FEDORA[0])
    content = content.replace('%NBFC_LINUX_FEDORA_URL%',        FEDORA[1])
    content = content.replace('%NBFC_LINUX_FEDORA_KB%',         FEDORA[2])

    content = content.replace('%NBFC_LINUX_OPENSUSE_PACKAGE%',  OPENSUSE[0])
    content = content.replace('%NBFC_LINUX_OPENSUSE_URL%',      OPENSUSE[1])
    content = content.replace('%NBFC_LINUX_OPENSUSE_KB%',       OPENSUSE[2])

    return content

make_index_html()
make_config_data_js()
