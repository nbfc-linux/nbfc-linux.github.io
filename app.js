document.addEventListener('DOMContentLoaded', () => {
  const apiUrl = 'https://api.github.com/repos/nbfc-linux/configs/contents/1.0/configs';
  const searchInput = document.getElementById('search');
  const thresholdInput = document.getElementById('threshold');
  const thresholdValue = document.getElementById('threshold-value');
  const resultsUl = document.getElementById('results');
  let configs = [];

  // 1) Lade Config-Namen
  fetch(apiUrl, { headers: { Accept: 'application/vnd.github.v3+json' } })
    .then(res => res.json())
    .then(data => {
      configs = data.map(item => item.name.replace('.json', ''));
      renderResults();
    })
    .catch(err => {
      resultsUl.innerHTML = '<li class="error">Failed to fetch configs</li>';
      console.error(err);
    });

  // 2) Event-Listener
  searchInput.addEventListener('input', renderResults);
  thresholdInput.addEventListener('input', () => {
    thresholdValue.textContent = thresholdInput.value;
    renderResults();
  });

  // 3) Filter & Anzeige
  function renderResults() {
    const query = searchInput.value.toLowerCase();
    const threshold = Number(thresholdInput.value);
    resultsUl.innerHTML = '';

    if (!query) {
      // bei leerer Eingabe alle Configs anzeigen
      configs.forEach(name => {
        const li = document.createElement('li');
        li.textContent = name;
        resultsUl.appendChild(li);
      });
      return;
    }

    configs.forEach(name => {
      const lower = name.toLowerCase();
      const sim = str_similarity(lower, query);
      if (sim >= threshold) {
        const li = document.createElement('li');
        li.textContent = name;
        resultsUl.appendChild(li);
      }
    });

    if (resultsUl.children.length === 0) {
      resultsUl.innerHTML = '<li>No matches</li>';
    }
  }
});
