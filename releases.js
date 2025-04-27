async function fetchReleases() {
    const response = await fetch('https://api.github.com/repos/nbfc-linux/nbfc-linux/releases');
    const releases = await response.json();
    return releases;
}

function compareVersions(v1, v2) {
    const a = v1.replace(/^v/, '').split('.').map(Number);
    const b = v2.replace(/^v/, '').split('.').map(Number);
    for (let i = 0; i < Math.max(a.length, b.length); i++) {
        if ((a[i] || 0) > (b[i] || 0)) return -1;
        if ((a[i] || 0) < (b[i] || 0)) return 1;
    }
    return 0;
}

function findLatestAssets(releases) {
    const latestDeb = { version: '', url: '' };
    const latestRpm = { version: '', url: '' };

    releases.sort((a, b) => compareVersions(a.tag_name, b.tag_name));

    for (const release of releases) {
        for (const asset of release.assets) {
            if (!latestDeb.url && asset.name.endsWith('.deb')) {
                latestDeb.version = release.tag_name;
                latestDeb.url = asset.browser_download_url;
            }
            if (!latestRpm.url && asset.name.endsWith('.rpm')) {
                latestRpm.version = release.tag_name;
                latestRpm.url = asset.browser_download_url;
            }
        }
        if (latestDeb.url && latestRpm.url) break;
    }

    return { latestDeb, latestRpm };
}

async function showDownloads() {
    const downloadsDiv = document.getElementById('downloads');
    try {
        const releases = await fetchReleases();
        const { latestDeb, latestRpm } = findLatestAssets(releases);

        downloadsDiv.innerHTML = '';

        if (latestDeb.url) {
            const debLink = document.createElement('a');
            debLink.href = latestDeb.url;
            debLink.textContent = `Download .deb package (Version ${latestDeb.version})`;
            downloadsDiv.appendChild(debLink);
        }

        if (latestRpm.url) {
            const rpmLink = document.createElement('a');
            rpmLink.href = latestRpm.url;
            rpmLink.textContent = `Download .rpm package (Version ${latestRpm.version})`;
            downloadsDiv.appendChild(rpmLink);
        }

        if (!latestDeb.url && !latestRpm.url) {
            downloadsDiv.textContent = 'No packages found.';
        }
    } catch (error) {
        console.error('Error loading releases:', error);
        downloadsDiv.textContent = 'Failed to load releases.';
    }
}

showDownloads();
