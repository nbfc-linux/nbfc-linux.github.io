async function fetchReleases() {
  const response = await fetch('https://api.github.com/repos/nbfc-linux/nbfc-linux/releases/latest');
  const releases = await response.json();
  return releases;
}

function findLatestAssets(releases) {
  const latestArchLinux = { version: '', url: '', os: 'Arch Linux'            };
  const latestDebian    = { version: '', url: '', os: 'Debian (Bookworm)'     };
  const latestFedora    = { version: '', url: '', os: 'Fedora 42 (Adams)'     };
  const latestOpenSuse  = { version: '', url: '', os: 'OpenSuse (Tumbleweed)' };

  const tagName = releases.tag_name;

  for (const asset of releases.assets) {
    if (asset.name.endsWith('.deb')) {
      latestDebian.version = tagName;
      latestDebian.url = asset.browser_download_url;
    }
    else if (asset.name.endsWith('pkg.tar.zst')) {
      latestArchLinux.version = tagName;
      latestArchLinux.url = asset.browser_download_url;
    }
    else if (asset.name.startsWith('fedora-')) {
      latestFedora.version = tagName;
      latestFedora.url = asset.browser_download_url;
    }
    else if (asset.name.startsWith('opensuse-')) {
      latestOpenSuse.version = tagName;
      latestOpenSuse.url = asset.browser_download_url;
    }
  }

  return [ latestArchLinux, latestDebian, latestFedora, latestOpenSuse ];
}

async function showDownloads() {
  const downloadsDiv = document.getElementById('downloads');
  try {
    const releases = await fetchReleases();
    const assets   = findLatestAssets(releases);

    downloadsDiv.innerHTML = '';

    if (assets.length === 0) {
      downloadsDiv.textContent = 'No packages found.';
      return;
    }

    for (const asset of assets) {
      const link = document.createElement('a');
      link.href = asset.url;
      link.textContent = `Download ${asset.os} package (Version ${asset.version})`;
      downloadsDiv.appendChild(link);
    }
  } catch (error) {
    console.error('Error loading releases:', error);
    downloadsDiv.textContent = 'Failed to load releases.';
  }
}

showDownloads();
