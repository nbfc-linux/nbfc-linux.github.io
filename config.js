document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('search');
  const thresholdInput = document.getElementById('threshold');
  const thresholdValue = document.getElementById('threshold-value');
  const resultsUl = document.getElementById('results');

  searchInput.addEventListener('input', renderResults);
  thresholdInput.addEventListener('input', () => {
    thresholdValue.textContent = thresholdInput.value;
    renderResults();
  });

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

  renderResults();
});
