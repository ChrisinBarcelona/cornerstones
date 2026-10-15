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
  setRoutine(stored === '1');  // hidden unless the student turns it on
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
  // Pages that moved to another section keep their ticks.
  var moved = window.CS_MOVED || {}, migrated = false;
  Object.keys(moved).forEach(function (oldKey) {
    if (done[oldKey]) { done[moved[oldKey]] = 1; delete done[oldKey]; migrated = true; }
  });
  if (migrated) write(KEY, done);

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
  function stats(track, milestone) {
    var items = TRACKS[track].items.filter(function (i) { return !milestone || i.category === milestone; }), share = 0, n = 0;
    items.forEach(function (i) { share += itemShare(i); if (itemDone(i)) n++; });
    var full = n === items.length;
    return { done: n, total: items.length, share: share, pct: percent(share, items.length, full), full: full };
  }
  // Milestones are a section's sub-sections; awards are whole sections; the certificate needs every award.
  function milestones(track) { return TRACKS[track].milestones || []; }
  function awardsEarned() { return Object.keys(TRACKS).filter(function (t) { return stats(t).full; }).length; }
  function certEarned() { return awardsEarned() === Object.keys(TRACKS).length; }
  var CERT = window.CS_CERT || {}, CERT_DATE = 'cs-cert-date';
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
      if (text) text.textContent = st.full ? 'Award won: ' + TRACKS[el.dataset.track].badge + '.'
        : (TRACKS[el.dataset.track].milestones.length ? 'Reach every milestone below to win the ' : 'Finish them all to win the ')
          + TRACKS[el.dataset.track].badge + ' award.';
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
    // Milestone badges (home, contents pages)
    document.querySelectorAll('[data-milestone]').forEach(function (el) {
      var parts = el.dataset.milestone.split(':'), st = stats(parts[0], parts.slice(1).join(':'));
      el.classList.toggle('earned', st.full);
      el.querySelector('.milestone-state').textContent = st.full ? 'Earned' : st.done + ' / ' + st.total;
    });
    // Certificate tiles and page
    var won = awardsEarned(), all = Object.keys(TRACKS).length;
    document.querySelectorAll('[data-cert]').forEach(function (el) {
      el.classList.toggle('earned', won === all);
      var s = el.querySelector('.badge-state');
      if (s) s.textContent = won === all ? 'Unlocked' : won + ' of ' + all + ' awards';
    });
    renderCertificate();
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
        (st.full ? 'award won' : st.pct + '%') + '">' + TRACKS[t].svg + '</span>';
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
      var lastCat = null;
      var items = tr.items.map(function (i) {
        var head = '';
        if (milestones(t).length && i.category !== lastCat) {
          lastCat = i.category;
          var ms = milestones(t).filter(function (m) { return m.name === i.category; })[0], mst = stats(t, i.category);
          if (ms) head = '<li class="tk-ms' + (mst.full ? ' earned' : '') + '"><span class="tk-ms-badge">' + ms.svg + '</span>' +
            '<span class="tk-ms-name">' + esc(ms.name) + '</span><span class="tk-ms-count">' + (mst.full ? 'Milestone earned' : mst.done + ' / ' + mst.total) + '</span></li>';
        }
        var row = head + check(i.key, i.title, i.url, 'tk-item' + (itemDone(i) ? ' item-complete' : ''));
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
    var won = awardsEarned(), all = Object.keys(TRACKS).length;
    html += '<a class="tk-cert' + (won === all ? ' earned' : '') + '" href="' + ROOT + 'certificate.html">' +
      '<span class="tk-badge">' + (CERT.svg || '') + '</span><span class="tk-name">Certificate' +
      '<span class="tk-count">' + (won === all ? 'Unlocked: see your certificate' : won + ' of ' + all + ' awards earned') + '</span></span></a>';
    body.innerHTML = html;
    var pct = courseStats();
    tracker.querySelector('[data-all]').textContent = pct === 100 ? 'Unmark all' : 'Mark all as complete';
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
      '<div class="tracker-actions"><button type="button" class="tracker-all" data-all></button></div>' +
      '<div class="tracker-body"></div>' +
      '<p class="tracker-note">Tick a page to mark it complete, or untick it to undo. Lectures with parts count once every part is done. Saved in this browser.</p>' +
      '</aside>';
    document.body.appendChild(tracker);
    tracker.addEventListener('click', function (e) {
      if (e.target.closest('[data-close]')) return closeTracker();
      if (e.target.closest('[data-all]')) return markAll(courseStats() !== 100);
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
  // Every page in every tracked section, parts included.
  function allKeys() {
    var keys = [];
    Object.keys(TRACKS).forEach(function (t) {
      TRACKS[t].items.forEach(function (i) { keys.push(i.key); i.children.forEach(function (c) { keys.push(c.key); }); });
    });
    return keys;
  }
  function markAll(on) {
    var msg = on ? 'Mark every UX Theory and UI Theory lecture, Figma lesson and exercise as complete?'
                 : 'Unmark everything? This clears all of your progress in this browser.';
    if (!window.confirm(msg)) return;
    allKeys().forEach(function (k) { if (on) done[k] = 1; else delete done[k]; });
    write(KEY, done);
    render();
    checkBadges();
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
    (lastOpener || opener).focus();
  }
  var lastOpener = null;
  [opener, document.getElementById('course-open')].forEach(function (btn) {
    if (btn) btn.addEventListener('click', function () { lastOpener = btn; openTracker(); });
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeTracker(); });

  // ---- Celebration: once, the moment a milestone, award or the certificate is earned (re-arms if a page is unticked) ----
  var dialog = document.getElementById('celebrate');
  function earnedNow() {
    var list = [];
    Object.keys(TRACKS).forEach(function (t) {
      milestones(t).forEach(function (m) { list.push({ key: 'ms:' + t + ':' + m.name, kind: 'milestone', track: t, m: m, full: stats(t, m.name).full }); });
      list.push({ key: t, kind: 'award', track: t, full: stats(t).full });
    });
    list.push({ key: 'cert', kind: 'cert', full: certEarned() });
    return list;
  }
  function andList(names) { return names.join(', ').replace(/, ([^,]*)$/, ' and $1'); }
  function checkBadges() {
    var seen = read(SEEN), fresh = [];
    earnedNow().forEach(function (b) {
      if (b.full && !seen[b.key]) fresh.push(b);
      if (b.full) seen[b.key] = 1; else delete seen[b.key];
    });
    write(SEEN, seen);
    if (certEarned() && !read(CERT_DATE).d) write(CERT_DATE, { d: new Date().toISOString() });
    if (!fresh.length || !dialog) return;
    closeTracker();
    var cert = fresh.filter(function (b) { return b.kind === 'cert'; }),
        awards = fresh.filter(function (b) { return b.kind === 'award'; }),
        miles = fresh.filter(function (b) { return b.kind === 'milestone'; });
    var art, eyebrow, title, text;
    if (cert.length) {
      art = CERT.svg; eyebrow = 'Certificate unlocked'; title = CERT.name;
      text = 'You\'ve earned every award. ' + CERT.school + ' awards you your certificate.';
    } else if (awards.length) {
      art = awards.map(function (b) { return TRACKS[b.track].svg; }).join('');
      eyebrow = awards.length === 1 ? 'Award unlocked' : 'Awards unlocked';
      title = andList(awards.map(function (b) { return TRACKS[b.track].badge; }));
      var left = Object.keys(TRACKS).length - awardsEarned();
      text = (awards.length === 1 ? TRACKS[awards[0].track].done + ' ' : '') +
        (left ? left + (left === 1 ? ' award' : ' awards') + ' to go until your certificate.' : '');
    } else {
      art = miles.map(function (b) { return b.m.svg; }).join('');
      eyebrow = miles.length === 1 ? 'Milestone reached' : 'Milestones reached';
      title = andList(miles.map(function (b) { return b.m.name; }));
      var tr = miles[0].track, got = milestones(tr).filter(function (m) { return stats(tr, m.name).full; }).length;
      text = miles.length === 1
        ? 'You\'ve finished every page in ' + miles[0].m.name + '. ' + got + ' of ' + milestones(tr).length + ' milestones towards the ' + TRACKS[tr].badge + ' award.'
        : 'You\'ve reached ' + miles.length + ' milestones at once.';
    }
    dialog.querySelector('.celebrate-badge').innerHTML = art;
    dialog.querySelector('.eyebrow').textContent = eyebrow;
    dialog.querySelector('#celebrate-title').textContent = title;
    dialog.querySelector('.celebrate-text').textContent = text;
    var link = dialog.querySelector('.celebrate-link');
    if (link) link.hidden = !cert.length;
    dialog.classList.toggle('is-cert', !!cert.length);
    dialog.hidden = false;
    document.getElementById('celebrate-close').focus();
  }

  // ---- Certificate page ----
  function renderCertificate() {
    var pageEl = document.querySelector('[data-cert-page]');
    if (!pageEl) return;
    var open = certEarned();
    pageEl.dataset.state = open ? 'unlocked' : 'locked';
    if (!open) return;
    var when = read(CERT_DATE).d;
    if (!when) { when = new Date().toISOString(); write(CERT_DATE, { d: when }); }
    var dateEl = pageEl.querySelector('[data-cert-date]');
    if (dateEl) dateEl.textContent = new Date(when).toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
  }
  (function () {
    var input = document.getElementById('cert-name-input'), out = document.getElementById('cert-name');
    if (!input || !out) return;
    var NAME = 'cs-cert-name';
    function show() { out.textContent = input.value.trim() || 'Your name'; out.classList.toggle('is-empty', !input.value.trim()); }
    try { input.value = localStorage.getItem(NAME) || ''; } catch (e) {}
    show();
    input.addEventListener('input', function () { try { localStorage.setItem(NAME, input.value); } catch (e) {} show(); });
    var printBtn = document.getElementById('cert-print');
    if (printBtn) printBtn.addEventListener('click', function () {
      if (!input.value.trim()) { input.focus(); input.classList.add('needs-name'); return; }
      window.print();
    });
  })();
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
  earnedNow().forEach(function (b) { if (b.full) seen[b.key] = 1; });
  write(SEEN, seen);
  if (certEarned() && !read(CERT_DATE).d) write(CERT_DATE, { d: new Date().toISOString() });
})();
