#!/usr/bin/env python3

import os
import sys
import json
import requests

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class GitHubAsset:
    def __init__(self, data):
        self.name = data['name']
        self.size = str(int(data['size'] / 1024))
        self.url  = data['browser_download_url']

class GitHubLatestReleasesQuery:
    def __init__(self, owner, repo):
        url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        self.tag = data['tag_name']
        self.assets = [GitHubAsset(i) for i in data['assets']]

def replace_asset_data(content, owner, repo, placeholder):
    releases = GitHubLatestReleasesQuery(owner, repo)
    assets   = {k: None for k in ['DEBIAN', 'FEDORA', 'OPENSUSE', 'ARCHLINUX']}

    for asset in releases.assets:
        if asset.name.endswith('.deb'):
            assets['DEBIAN'] = asset

        elif asset.name.startswith('fedora-'):
            assets['FEDORA'] = asset

        elif asset.name.startswith('opensuse-'):
            assets['OPENSUSE'] = asset

        elif asset.name.endswith('pkg.tar.zst'):
            assets['ARCHLINUX'] = asset

    content = content.replace(f'%{placeholder}_TAG%', releases.tag)

    for os, asset in assets.items():
        content = content.replace(f'%{placeholder}_{os}_PACKAGE%', asset.name)
        content = content.replace(f'%{placeholder}_{os}_URL%',     asset.url)
        content = content.replace(f'%{placeholder}_{os}_KB%',      asset.size)

    return content

def make_index_html():
    with open('index.in.html', 'r', encoding='UTF-8') as fh:
        content = fh.read()

    content = replace_asset_data(content, 'nbfc-linux', 'nbfc-linux', 'NBFC_LINUX')
    content = replace_asset_data(content, 'nbfc-linux', 'nbfc-gtk',   'NBFC_GTK')
    content = replace_asset_data(content, 'nbfc-linux', 'nbfc-qt',    'NBFC_QT')

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

make_index_html()
make_config_data_js()
