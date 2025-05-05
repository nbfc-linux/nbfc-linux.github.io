/**
 * Berechnet mittels Levenshtein-Algorithmus die Ähnlichkeit (0–100) zweier Strings.
 * @param {string} a
 * @param {string} b
 * @returns {number} similarity in percent
 */
function str_similarity(a, b) {
  const n = a.length, m = b.length;
  if (n === 0 && m === 0) return 100;
  // matrix (n+1)x(m+1)
  const dp = Array.from({ length: n + 1 }, () => Array(m + 1));
  for (let i = 0; i <= n; i++) dp[i][0] = i;
  for (let j = 0; j <= m; j++) dp[0][j] = j;
  for (let i = 1; i <= n; i++) {
    for (let j = 1; j <= m; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      dp[i][j] = Math.min(
        dp[i - 1][j] + 1,
        dp[i][j - 1] + 1,
        dp[i - 1][j - 1] + cost
      );
    }
  }
  const dist = dp[n][m];
  const maxLen = Math.max(n, m);
  return ((maxLen - dist) / maxLen) * 100;
}
