// Leest alleen de score uit de link (?s=0..30). Geen naam, geen id, niets wordt opgeslagen.
(function () {
  var m = /[?&]s=(\d{1,2})(?:&|$)/.exec(location.search);
  if (!m) return;
  var s = parseInt(m[1], 10);
  if (isNaN(s) || s < 0 || s > 30) return;
  var nl = document.getElementById('score-nl');
  var en = document.getElementById('score-en');
  if (s === 30) {
    nl.textContent = 'Je vriend haalde 30 van de 30. Foutloos. Kun jij dat ook?';
    en.textContent = 'Your friend got 30 out of 30. Flawless. Can you match it?';
  } else {
    nl.textContent = 'Je vriend haalde ' + s + ' van de 30. Doe jij het beter?';
    en.textContent = 'Your friend got ' + s + ' out of 30. Can you beat that?';
  }
})();
