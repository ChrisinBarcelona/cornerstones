(function () {
  var root = document.documentElement;
  function store(key, value) { try { localStorage.setItem(key, value); } catch (e) {} }
  function read(key) { try { return localStorage.getItem(key); } catch (e) { return null; } }

  // Theme
  var toggle = document.getElementById('theme-toggle');
  if (toggle) toggle.addEventListener('click', function () {
    var next = root.dataset.theme === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    store('cs-theme', next);
  });

  // Index: category filter, search, list/grid
  var rows = document.getElementById('rows');
  if (rows) {
    var items = Array.prototype.slice.call(rows.querySelectorAll('.row'));
    var heads = Array.prototype.slice.call(rows.querySelectorAll('.chapter'));
    var q = document.getElementById('q');
    var showing = document.getElementById('showing');
    var empty = document.getElementById('empty');
    var catButtons = document.querySelectorAll('.cats button');
    var cat = '';

    function apply() {
      var term = q.value.trim().toLowerCase();
      var shown = 0;
      function inCat(li) { return !cat || li.dataset.cat === cat || li.dataset.parent === cat; }
      items.forEach(function (li) {
        var ok = inCat(li) && (!term || li.dataset.search.indexOf(term) !== -1);
        li.hidden = !ok;
        if (ok) shown++;
      });
      // Chapter headings show while browsing, not while searching.
      heads.forEach(function (li) { li.hidden = !!term || !inCat(li); });
      catButtons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.cat === cat)); });
      showing.textContent = 'Showing ' + shown + ' of ' + items.length;
      empty.hidden = shown !== 0;
    }
    function fromHash() {
      var m = location.hash.match(/category=([^&]+)/);
      cat = m ? decodeURIComponent(m[1]) : '';
      apply();
    }
    catButtons.forEach(function (b) {
      b.addEventListener('click', function () {
        history.replaceState(null, '', b.dataset.cat ? '#category=' + encodeURIComponent(b.dataset.cat) : location.pathname);
        cat = b.dataset.cat;
        apply();
      });
    });
    q.addEventListener('input', apply);
    window.addEventListener('hashchange', fromHash);
    fromHash();

    var viewButtons = document.querySelectorAll('.view-toggle button');
    function setView(v) {
      rows.classList.toggle('grid', v === 'grid');
      viewButtons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.view === v)); });
      store('cs-view', v);
    }
    viewButtons.forEach(function (b) { b.addEventListener('click', function () { setView(b.dataset.view); }); });
    setView(read('cs-view') || 'list');
  }

  // Lecture: highlight current section in the rail
  var tocLinks = document.querySelectorAll('.toc:not(.family) a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[decodeURIComponent(a.hash.slice(1))] = a; });
    var current;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting && map[e.target.id]) {
          if (current) current.classList.remove('active');
          current = map[e.target.id];
          current.classList.add('active');
        }
      });
    }, { rootMargin: '-70px 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { var el = document.getElementById(id); if (el) io.observe(el); });
  }

  // Lecture: click an image to enlarge
  var box = document.getElementById('lightbox');
  if (box) {
    var big = box.querySelector('img');
    document.querySelectorAll('.prose figure.media img').forEach(function (img) {
      img.addEventListener('click', function () { big.src = img.currentSrc || img.src; big.alt = img.alt; box.hidden = false; });
    });
    box.addEventListener('click', function () { box.hidden = true; });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') box.hidden = true; });
  }
})();

// Home: search every page in the site
(function () {
  var input = document.getElementById('q-all');
  var data = document.getElementById('search-index');
  if (!input || !data) return;
  var pages = JSON.parse(data.textContent);
  var results = document.getElementById('results');
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  input.addEventListener('input', function () {
    var term = input.value.trim().toLowerCase();
    if (!term) { results.hidden = true; results.innerHTML = ''; return; }
    var hits = pages.filter(function (p) { return (p.t + ' ' + p.d).toLowerCase().indexOf(term) !== -1; })
      .sort(function (a, b) { return (b.t.toLowerCase().indexOf(term) !== -1) - (a.t.toLowerCase().indexOf(term) !== -1); })
      .slice(0, 12);
    results.innerHTML = hits.length ? hits.map(function (p) {
      return '<li><a class="card" href="' + p.u + '"><span class="card-title">' + esc(p.t) + '</span>' +
        '<span class="card-desc">' + esc(p.s) + (p.d ? ' · ' + esc(p.d) : '') + '</span><span class="card-go">→</span></a></li>';
    }).join('') : '<li class="empty">Nothing matches that search.</li>';
    results.hidden = false;
  });
})();
