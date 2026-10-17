// Presentations: intro screen, then slides with keyboard, click and swipe navigation and a progress bar.
(function () {
  var deck = document.getElementById('deck');
  if (!deck) return;
  var slides = Array.prototype.slice.call(deck.querySelectorAll('.slide'));
  var total = slides.length, i = 0;
  var bar = document.getElementById('deck-bar'), count = document.getElementById('deck-count');
  var prog = deck.querySelector('.deck-progress');
  var prev = document.getElementById('deck-prev'), next = document.getElementById('deck-next');

  function show(n) {
    i = Math.max(0, Math.min(total - 1, n));
    slides.forEach(function (s, k) { s.classList.toggle('on', k === i); s.setAttribute('aria-hidden', String(k !== i)); });
    bar.style.width = ((i + 1) / total * 100) + '%';
    prog.setAttribute('aria-valuenow', String(i + 1));
    count.textContent = (i + 1) + ' / ' + total;
    prev.disabled = i === 0;
    next.disabled = i === total - 1;
    history.replaceState(null, '', '#' + (i + 1));
  }
  function play(n) {
    deck.dataset.state = 'play';
    show(n || 0);
  }
  function stop() {
    deck.dataset.state = 'intro';
    history.replaceState(null, '', location.pathname + location.search);
    if (document.fullscreenElement) document.exitFullscreen().catch(function () {});
  }
  function full() {
    if (document.fullscreenElement) { document.exitFullscreen().catch(function () {}); return; }
    if (deck.requestFullscreen) deck.requestFullscreen().catch(function () {});
  }

  document.getElementById('deck-play').addEventListener('click', function () { play(0); });
  document.getElementById('deck-full').addEventListener('click', full);
  prev.addEventListener('click', function () { show(i - 1); });
  next.addEventListener('click', function () { show(i + 1); });

  // Click the left third to go back, anywhere else to go forward (but let links work).
  document.getElementById('deck-stage').addEventListener('click', function (e) {
    if (e.target.closest('a')) return;
    var r = this.getBoundingClientRect();
    show(e.clientX - r.left < r.width / 3 ? i - 1 : i + 1);
  });

  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if (deck.dataset.state !== 'play') {
      if (e.key === 'Enter' && document.activeElement === document.body) play(0);
      return;
    }
    switch (e.key) {
      case 'ArrowRight': case 'ArrowDown': case 'PageDown': case ' ': e.preventDefault(); show(i + 1); break;
      case 'ArrowLeft': case 'ArrowUp': case 'PageUp': e.preventDefault(); show(i - 1); break;
      case 'Home': show(0); break;
      case 'End': show(total - 1); break;
      case 'f': case 'F': full(); break;
      case 'Escape': if (!document.fullscreenElement) stop(); break;
    }
  });

  // Swipe on touch screens.
  var x0 = null;
  deck.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  deck.addEventListener('touchend', function (e) {
    if (x0 === null || deck.dataset.state !== 'play') return;
    var dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 40) show(dx < 0 ? i + 1 : i - 1);
  });

  // Open straight on a slide from a link like slides/colour-values.html#5
  var start = parseInt(location.hash.slice(1), 10);
  if (start >= 1 && start <= total) play(start - 1);
})();
