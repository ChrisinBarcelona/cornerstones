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

// Timetable: tick cards off (saved in this browser), per-week progress, routine toggle, expand all
(function () {
  var board = document.querySelector('.timetable');
  if (!board) return;
  var KEY = 'cs-timetable-done';
  var done = {};
  try { done = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) {}
  function save() { try { localStorage.setItem(KEY, JSON.stringify(done)); } catch (e) {} }
  var cards = board.querySelectorAll('.tt-card');

  function progress() {
    var total = 0, ticked = 0;
    board.querySelectorAll('.tt-week').forEach(function (week) {
      var cs = week.querySelectorAll('.tt-card');
      var n = 0;
      cs.forEach(function (c) { if (done[c.dataset.id]) n++; });
      var el = week.querySelector('.tt-progress');
      el.textContent = n + ' / ' + cs.length + ' done';
      el.classList.toggle('full', n === cs.length);
      total += cs.length; ticked += n;
    });
    document.getElementById('tt-overall').textContent = ticked + ' of ' + total + ' complete';
  }
  cards.forEach(function (card) {
    var box = card.querySelector('.tt-done input');
    box.checked = !!done[card.dataset.id];
    card.classList.toggle('is-done', box.checked);
    box.addEventListener('change', function () {
      if (box.checked) done[card.dataset.id] = 1; else delete done[card.dataset.id];
      card.classList.toggle('is-done', box.checked);
      save(); progress();
    });
  });
  progress();

  var routine = document.getElementById('tt-routine');
  function setRoutine(show) {
    board.classList.toggle('hide-routine', !show);
    routine.checked = show;
    try { localStorage.setItem('cs-tt-routine', show ? '1' : '0'); } catch (e) {}
  }
  var stored = null;
  try { stored = localStorage.getItem('cs-tt-routine'); } catch (e) {}
  setRoutine(stored !== '0');
  routine.addEventListener('change', function () { setRoutine(routine.checked); });

  var weeks = board.querySelectorAll('.tt-week details');
  var expand = document.getElementById('tt-expand');
  expand.addEventListener('click', function () {
    var open = expand.textContent === 'Expand all';
    weeks.forEach(function (d) { d.open = open; });
    expand.textContent = open ? 'Collapse all' : 'Expand all';
  });
  // Jumping to a week opens it.
  function openFromHash() {
    var target = location.hash && document.querySelector(location.hash + ' details');
    if (target) target.open = true;
  }
  window.addEventListener('hashchange', openFromHash);
  openFromHash();
})();

// Course login (browser-side): sign in, show/hide password, log out
(function () {
  var form = document.getElementById('login-form');
  if (form) {
    var user = document.getElementById('login-user');
    var pass = document.getElementById('login-pass');
    var error = document.getElementById('login-error');
    var toggle = document.getElementById('pw-toggle');
    toggle.addEventListener('click', function () {
      var show = pass.type === 'password';
      pass.type = show ? 'text' : 'password';
      toggle.textContent = show ? 'Hide' : 'Show';
      toggle.setAttribute('aria-pressed', String(show));
      toggle.setAttribute('aria-label', show ? 'Hide password' : 'Show password');
    });
    function sha256(text) {
      return crypto.subtle.digest('SHA-256', new TextEncoder().encode(text)).then(function (buf) {
        return Array.prototype.map.call(new Uint8Array(buf), function (b) { return ('0' + b.toString(16)).slice(-2); }).join('');
      });
    }
    // Only return to a page on this site.
    function nextUrl() {
      var next = new URLSearchParams(location.search).get('next') || '';
      return /^\/(?!\/)/.test(next) ? next : 'index.html';
    }
    [user, pass].forEach(function (el) { el.addEventListener('input', function () { error.hidden = true; }); });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      sha256(user.value.trim().toLowerCase() + ':' + pass.value).then(function (hash) {
        if (hash === form.dataset.hash) {
          try { localStorage.setItem('cs-auth', hash); } catch (err) {}
          location.replace(nextUrl());
        } else {
          error.hidden = false;
          pass.select();
        }
      });
    });
    user.focus();
  }
  var logout = document.getElementById('logout');
  if (logout) logout.addEventListener('click', function () {
    try { localStorage.removeItem('cs-auth'); } catch (e) {}
    location.replace(logout.dataset.login);
  });
})();

// Progress: mark pages complete (saved in this browser), progress bars, badges and the tracker sidebar
(function () {
  var TRACKS = window.CS_PROGRESS;
  if (!TRACKS) return;
  var ROOT = window.CS_ROOT || '';
  var KEY = 'cs-progress', SEEN = 'cs-badges-seen', OPEN = 'cs-tracker-open';
  function read(k) { try { return JSON.parse(localStorage.getItem(k) || '{}'); } catch (e) { return {}; } }
  function write(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var done = read(KEY);

  // A page with parts is complete only when it and all of its parts are done…
  function partsDone(item) { return item.children.filter(function (c) { return done[c.key]; }).length; }
  function itemDone(item) { return !!done[item.key] && partsDone(item) === item.children.length; }
  // …but every ticked page still moves the bar along.
  function itemShare(item) { return ((done[item.key] ? 1 : 0) + partsDone(item)) / (1 + item.children.length); }
  // 100% only when everything is done; any progress at all shows at least 1%.
  function percent(part, whole, full) {
    if (full) return 100;
    if (!part) return 0;
    return Math.max(1, Math.min(99, Math.round(part / whole * 100)));
  }
  function stats(track) {
    var items = TRACKS[track].items, share = 0, n = 0;
    items.forEach(function (i) { share += itemShare(i); if (itemDone(i)) n++; });
    var full = n === items.length;
    return { done: n, total: items.length, share: share, pct: percent(share, items.length, full), full: full };
  }
  function courseStats() {
    var share = 0, all = 0, full = true;
    Object.keys(TRACKS).forEach(function (t) { var st = stats(t); share += st.share; all += st.total; full = full && st.full; });
    return percent(share, all, full);
  }
  function findItem(key) {
    var items = (TRACKS[key.split('/')[0]] || {}).items || [];
    for (var i = 0; i < items.length; i++) {
      if (items[i].key === key || items[i].children.some(function (c) { return c.key === key; })) return items[i];
    }
    return null;
  }
  function toggle(key, on) {
    if (on === undefined) on = !done[key];
    if (on) done[key] = 1; else delete done[key];
    write(KEY, done);
    render();
    checkBadges();
  }

  function render() {
    // Section panels (contents pages) and section cards (home)
    document.querySelectorAll('.progress[data-track]').forEach(function (el) {
      var st = stats(el.dataset.track);
      el.querySelector('.progress-count').textContent = el.classList.contains('compact')
        ? st.done + ' / ' + st.total + ' · ' + st.pct + '%'
        : st.done + ' of ' + st.total + ' complete · ' + st.pct + '%';
      el.querySelector('.progress-bar span').style.width = st.pct + '%';
      el.querySelector('.progress-bar').setAttribute('aria-valuenow', st.pct);
      el.classList.toggle('is-complete', st.full);
      var text = el.querySelector('.progress-badge-text');
      if (text) text.textContent = st.full ? 'Badge earned: ' + TRACKS[el.dataset.track].badge + '.'
        : 'Finish them all to earn the ' + TRACKS[el.dataset.track].badge + ' badge.';
    });
    // Rows on contents pages
    document.querySelectorAll('.row[data-key]').forEach(function (row) {
      var item = findItem(row.dataset.key);
      if (!item) return;
      row.classList.toggle('is-complete', itemDone(item));
      var pill = row.querySelector('[data-parts-of]');
      if (pill) {
        var n = partsDone(item);
        pill.textContent = n ? n + ' / ' + item.children.length + ' parts' : item.children.length + ' parts';
      }
    });
    // Badge shelf (home)
    document.querySelectorAll('.badge-item[data-track]').forEach(function (el) {
      var st = stats(el.dataset.track);
      el.classList.toggle('earned', st.full);
      el.querySelector('.badge-state').textContent = st.full ? 'Earned' : st.pct + '%';
    });
    // This page's buttons, beside the title and at the end
    document.querySelectorAll('[data-complete]').forEach(function (btn) {
      var on = !!done[btn.dataset.complete];
      btn.classList.toggle('is-complete', on);
      btn.setAttribute('aria-pressed', String(on));
    });
    var box = document.querySelector('.complete[data-key]');
    if (box) {
      box.classList.toggle('is-complete', !!done[box.dataset.key]);
      var parts = box.querySelector('[data-parts]');
      if (parts) parts.textContent = partsDone(findItem(box.dataset.key));
    }
    // Header: whole-course bar, breakdown and mini badges
    var detail = Object.keys(TRACKS).map(function (t) { var st = stats(t); return TRACKS[t].badge + ' ' + st.done + '/' + st.total; });
    var pct = courseStats();
    var bar = document.querySelector('.course-bar');
    if (bar) {
      bar.querySelector('span').style.width = pct + '%';
      bar.setAttribute('aria-valuenow', pct);
      document.getElementById('course-pct').textContent = pct + '%';
      document.getElementById('course-detail').textContent = ' · ' + detail.join(' · ');
    }
    var minis = document.getElementById('mini-badges');
    if (minis) minis.innerHTML = Object.keys(TRACKS).map(function (t) {
      var st = stats(t);
      return '<span class="mini-badge' + (st.full ? ' earned' : '') + '" title="' + esc(TRACKS[t].badge) + ': ' +
        (st.full ? 'badge earned' : st.pct + '%') + '">' + TRACKS[t].svg + '</span>';
    }).join('');
    renderTracker();
  }

  // ---- Tracker sidebar ----
  var opener = document.getElementById('tracker-open');
  var tracker = null, openSections = read(OPEN);
  var currentKey = (document.querySelector('main[data-key]') || {}).dataset ? document.querySelector('main[data-key]').dataset.key : '';
  function check(key, title, url, cls) {
    var current = key === currentKey ? ' aria-current="page"' : '';
    return '<li class="' + cls + (done[key] ? ' is-done' : '') + '"' + current + '>' +
      '<input type="checkbox" id="tk-' + esc(key) + '" data-key="' + esc(key) + '"' + (done[key] ? ' checked' : '') +
      ' aria-label="Mark ' + esc(title) + ' as complete">' +
      '<a href="' + ROOT + url + '">' + esc(title) + '</a></li>';
  }
  function renderTracker() {
    if (!tracker) return;
    var body = tracker.querySelector('.tracker-body');
    var html = Object.keys(TRACKS).map(function (t) {
      var tr = TRACKS[t], st = stats(t);
      var isOpen = openSections[t] !== undefined ? !!openSections[t] : (currentKey ? currentKey.indexOf(t + '/') === 0 : t === 'ux');
      var items = tr.items.map(function (i) {
        var row = check(i.key, i.title, i.url, 'tk-item' + (itemDone(i) ? ' item-complete' : ''));
        if (!i.children.length) return row;
        return row.replace('</li>', '<span class="tk-parts">' + partsDone(i) + ' / ' + i.children.length + ' parts</span>' +
          '<ol class="tk-children">' + i.children.map(function (c) { return check(c.key, c.title, c.url, 'tk-child'); }).join('') + '</ol></li>');
      }).join('');
      return '<section class="tk-section' + (st.full ? ' earned' : '') + '">' +
        '<button type="button" class="tk-head" data-track="' + t + '" aria-expanded="' + isOpen + '">' +
        '<span class="tk-badge">' + tr.svg + '</span><span class="tk-name">' + esc(tr.label) +
        '<span class="tk-count">' + st.done + ' / ' + st.total + ' complete · ' + st.pct + '%</span>' +
        '<span class="tk-bar"><span style="width:' + st.pct + '%"></span></span></span><span class="tk-caret" aria-hidden="true"></span></button>' +
        '<ol class="tk-items"' + (isOpen ? '' : ' hidden') + '>' + items + '</ol></section>';
    }).join('');
    body.innerHTML = html;
    var pct = courseStats();
    tracker.querySelector('.tracker-total b').textContent = pct + '%';
    tracker.querySelector('.tracker-bar span').style.width = pct + '%';
  }
  function buildTracker() {
    tracker = document.createElement('div');
    tracker.className = 'tracker';
    tracker.id = 'tracker';
    tracker.hidden = true;
    tracker.innerHTML =
      '<div class="tracker-scrim" data-close></div>' +
      '<aside class="tracker-panel" role="dialog" aria-modal="true" aria-labelledby="tracker-title">' +
      '<div class="tracker-top"><div><div class="eyebrow">Your progress</div><h2 id="tracker-title">Course tracker</h2></div>' +
      '<button type="button" class="icon-btn" data-close aria-label="Close the tracker">✕</button></div>' +
      '<div class="tracker-total">Course progress · <b>0%</b> complete</div><div class="tracker-bar"><span></span></div>' +
      '<div class="tracker-body"></div>' +
      '<p class="tracker-note">Tick a page to mark it complete, or untick it to undo. Lectures with parts count once every part is done. Saved in this browser.</p>' +
      '</aside>';
    document.body.appendChild(tracker);
    tracker.addEventListener('click', function (e) {
      if (e.target.closest('[data-close]')) return closeTracker();
      var head = e.target.closest('.tk-head');
      if (head) {
        var list = head.nextElementSibling, open = list.hidden;
        list.hidden = !open;
        head.setAttribute('aria-expanded', String(open));
        openSections[head.dataset.track] = open ? 1 : 0;
        write(OPEN, openSections);
      }
    });
    tracker.addEventListener('change', function (e) {
      if (e.target.matches('input[data-key]')) {
        var y = tracker.querySelector('.tracker-body').scrollTop;
        toggle(e.target.dataset.key, e.target.checked);
        tracker.querySelector('.tracker-body').scrollTop = y;
        var again = tracker.querySelector('input[data-key="' + e.target.dataset.key + '"]');
        if (again) again.focus();
      }
    });
  }
  function openTracker() {
    if (!tracker) buildTracker();
    renderTracker();
    tracker.classList.add('entering');
    tracker.hidden = false;
    setTimeout(function () { tracker.classList.remove('entering'); }, 20);
    document.documentElement.classList.add('tracker-is-open');
    opener.setAttribute('aria-expanded', 'true');
    var here = tracker.querySelector('[aria-current="page"]');
    if (here) here.scrollIntoView({ block: 'center' });
    tracker.querySelector('[data-close].icon-btn').focus();
  }
  function closeTracker() {
    if (!tracker || tracker.hidden) return;
    tracker.hidden = true;
    document.documentElement.classList.remove('tracker-is-open');
    opener.setAttribute('aria-expanded', 'false');
    opener.focus();
  }
  if (opener) opener.addEventListener('click', openTracker);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeTracker(); });

  // ---- Badge celebration: once, the moment a section is finished (re-arms if a page is unticked) ----
  var dialog = document.getElementById('celebrate');
  function checkBadges() {
    var seen = read(SEEN);
    Object.keys(TRACKS).forEach(function (track) {
      var full = stats(track).full;
      if (full && !seen[track] && dialog) {
        closeTracker();
        dialog.querySelector('.celebrate-badge').innerHTML = TRACKS[track].svg;
        dialog.querySelector('#celebrate-title').textContent = TRACKS[track].badge;
        dialog.querySelector('.celebrate-text').textContent = TRACKS[track].done;
        dialog.hidden = false;
        document.getElementById('celebrate-close').focus();
      }
      if (full) seen[track] = 1; else delete seen[track];
    });
    write(SEEN, seen);
  }
  if (dialog) {
    var closeDialog = function () { dialog.hidden = true; };
    document.getElementById('celebrate-close').addEventListener('click', closeDialog);
    dialog.addEventListener('click', function (e) { if (e.target === dialog) closeDialog(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeDialog(); });
  }

  document.querySelectorAll('[data-complete]').forEach(function (btn) {
    btn.addEventListener('click', function () { toggle(btn.dataset.complete); });
  });
  render();
  // Badges already earned before this page loaded shouldn't pop up on load.
  var seen = read(SEEN);
  Object.keys(TRACKS).forEach(function (t) { if (stats(t).full) seen[t] = 1; });
  write(SEEN, seen);
})();
