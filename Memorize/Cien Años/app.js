/* Cien años paragraph course: audio, browser voice, word cards, practice boxes, progress.
   No dependencies. Data comes from data.js (window.CA), which build.py generates. */
(function () {
  "use strict";
  var CA = window.CA;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ------------------------------------------------------------ saved state */
  var KEY = "cienanos.p1.v1";
  var store = { done: {}, checks: {}, practice: {}, speed: 1, en: true, last: null };
  try {
    var saved = JSON.parse(localStorage.getItem(KEY) || "{}");
    for (var k in saved) store[k] = saved[k];
  } catch (e) { /* private mode: progress simply is not kept */ }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(store)); } catch (e) {} }

  var toastEl, toastTimer;
  function toast(msg) {
    if (!toastEl) { toastEl = document.createElement("div"); toastEl.className = "toast"; toastEl.setAttribute("role", "status"); document.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add("show");
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { toastEl.classList.remove("show"); }, 4200);
  }

  /* ------------------------------------------------------------ recording player */
  var audio = null, cur = null, raf = 0, bar = null;
  var SPEEDS = [1, 0.85, 0.75, 0.6, 0.5];

  function rangeOf(target) {
    var m;
    if (target === "all") return { a: 0, b: CA.clip, label: "The whole paragraph", s0: 1, s1: 17 };
    if ((m = /^s(\d+)$/.exec(target))) { var t = CA.sent[m[1] - 1].t; return { a: t[0], b: t[1], label: "Sentence " + m[1], s0: +m[1], s1: +m[1] }; }
    if ((m = /^r(\d+)-(\d+)$/.exec(target))) return { a: CA.sent[m[1] - 1].t[0], b: CA.sent[m[2] - 1].t[1], label: "Sentences " + m[1] + " to " + m[2], s0: +m[1], s1: +m[2] };
    if ((m = /^c(\d+)$/.exec(target))) { var c = CA.chunks[+m[1]]; if (!c || !c.t) return null; return { a: c.t[0], b: c.t[1], label: "Phrase from sentence " + c.s, s0: c.s, s1: c.s, phrase: true }; }
    return null;
  }

  function ensureAudio() {
    if (audio) return audio;
    audio = new Audio();
    audio.preload = "auto";
    audio.src = audio.canPlayType('audio/mp4; codecs="mp4a.40.2"') ? "audio/para1.m4a" : "audio/para1.mp3";
    audio.addEventListener("error", function () { toast("The recording could not be loaded. Check your connection and try again."); stop(); });
    bar = document.createElement("div");
    bar.className = "player";
    bar.innerHTML = '<div class="row"><button class="btn solid" data-p="toggle" aria-label="Pause or resume">Pause</button>' +
      '<div class="what"><span class="lbl"></span><small>audiobook recording</small></div>' +
      '<label class="fine">Speed <select data-p="speed" aria-label="Playback speed">' +
      SPEEDS.map(function (s) { return '<option value="' + s + '">' + (s === 1 ? "1× normal" : s + "×") + "</option>"; }).join("") + "</select></label>" +
      '<button class="btn" data-p="repeat" aria-pressed="false">Repeat</button><button class="btn" data-p="stop">Stop</button>' +
      '<div class="bar"><i></i></div></div>';
    document.body.appendChild(bar);
    $("[data-p=speed]", bar).value = String(store.speed);
    bar.addEventListener("click", function (e) {
      var b = e.target.closest("[data-p]"); if (!b) return;
      var p = b.getAttribute("data-p");
      if (p === "stop") stop();
      if (p === "toggle") { if (audio.paused) { audio.play(); tick(); } else audio.pause(); syncUI(); }
      if (p === "repeat" && cur) { cur.repeat = !cur.repeat; syncUI(); }
    });
    $("[data-p=speed]", bar).addEventListener("change", function () {
      store.speed = parseFloat(this.value); save(); audio.playbackRate = store.speed;
    });
    return audio;
  }

  function syncUI() {
    $$(".playing").forEach(function (b) { b.classList.remove("playing"); });
    $$(".sent.now, .rs-sent.now").forEach(function (b) { b.classList.remove("now"); });
    if (!bar) return;
    bar.classList.toggle("show", !!cur);
    if (!cur) return;
    $(".lbl", bar).textContent = cur.label;
    $("[data-p=toggle]", bar).textContent = audio.paused ? "Resume" : "Pause";
    var rep = $("[data-p=repeat]", bar); rep.setAttribute("aria-pressed", cur.repeat ? "true" : "false");
    $$('[data-play="' + cur.target + '"]').forEach(function (b) { b.classList.add("playing"); });
  }

  function highlight(time) {
    if (!cur || cur.phrase) return;
    var n = cur.s0;
    for (var i = cur.s0; i <= cur.s1; i++) if (time >= CA.sent[i - 1].t[0] - 0.05) n = i;
    if (n === cur.shown) return;
    cur.shown = n;
    $$(".sent.now, .rs-sent.now").forEach(function (b) { b.classList.remove("now"); });
    $$('.sent[data-s="' + n + '"], .rs-sent[data-s="' + n + '"]').forEach(function (b) { b.classList.add("now"); });
    if (cur.s1 > cur.s0) {
      var el = $('.sent[data-s="' + n + '"]') || $('.rs-sent[data-s="' + n + '"]');
      if (el) { var r = el.getBoundingClientRect(); if (r.top < 60 || r.bottom > window.innerHeight - 110) el.scrollIntoView({ block: "center", behavior: "smooth" }); }
    }
  }

  function tick() {
    cancelAnimationFrame(raf);
    if (!cur) return;
    var t = audio.currentTime;
    $(".bar i", bar).style.width = Math.max(0, Math.min(100, (t - cur.a) / (cur.b - cur.a) * 100)) + "%";
    highlight(t);
    if (t >= cur.b || audio.ended) {
      if (cur.repeat) { audio.currentTime = cur.a; if (audio.paused) audio.play(); }
      else { stop(); return; }
    }
    if (!audio.paused) raf = requestAnimationFrame(tick);
  }

  function stop() {
    cancelAnimationFrame(raf);
    if (audio) audio.pause();
    cur = null; syncUI();
  }

  function play(target, repeat) {
    var r = rangeOf(target); if (!r) return;
    stopVoice();
    ensureAudio();
    if (cur && cur.target === target && !audio.paused && !repeat) { stop(); return; }
    cur = { target: target, a: r.a, b: r.b, label: r.label, s0: r.s0, s1: r.s1, phrase: r.phrase, repeat: !!repeat, shown: 0 };
    var mine = cur, tries = 0;
    var canSeek = function (t) {
      var sk = audio.seekable;
      for (var i = 0; i < sk.length; i++) if (sk.start(i) <= t + 0.01 && sk.end(i) >= t) return true;
      return false;
    };
    var start = function () {
      if (cur !== mine) return;
      // Some servers send the file without byte ranges; then nothing past the start can be reached until it has downloaded.
      if (r.a > 0.5 && !canSeek(r.a) && tries++ < 12) {
        $(".lbl", bar).textContent = r.label + " (loading…)";
        setTimeout(start, 250); return;
      }
      audio.currentTime = r.a; audio.playbackRate = store.speed;
      var p = audio.play();
      if (p && p.catch) p.catch(function () { if (cur === mine) { toast("Tap the play button again to start the audio."); stop(); } });
      syncUI(); tick();
    };
    syncUI();
    if (audio.readyState >= 1) start();
    else { audio.addEventListener("loadedmetadata", start, { once: true }); audio.load(); }
  }
  document.addEventListener("visibilitychange", function () { if (cur && audio && !audio.paused) tick(); });
  setInterval(function () { if (cur && audio && !audio.paused) { if (audio.currentTime >= cur.b) tick(); } }, 120);

  /* ------------------------------------------------------------ browser voice (synthesized) */
  var voice = null, voicesReady = false;
  function pickVoice() {
    if (!("speechSynthesis" in window)) return;
    var vs = speechSynthesis.getVoices().filter(function (v) { return /^es([-_]|$)/i.test(v.lang); });
    voicesReady = speechSynthesis.getVoices().length > 0;
    var pref = ["es-CO", "es-MX", "es-US", "es-419", "es-ES"];
    vs.sort(function (a, b) {
      var ia = pref.indexOf(a.lang.replace("_", "-")), ib = pref.indexOf(b.lang.replace("_", "-"));
      return (ia < 0 ? 9 : ia) - (ib < 0 ? 9 : ib);
    });
    voice = vs[0] || null;
  }
  if ("speechSynthesis" in window) { pickVoice(); speechSynthesis.addEventListener && speechSynthesis.addEventListener("voiceschanged", pickVoice); }
  function stopVoice() { if ("speechSynthesis" in window) speechSynthesis.cancel(); }
  function sayText(text) {
    if (!("speechSynthesis" in window)) { toast("This browser has no built-in speech. Use the recording or the dictionary link instead."); return; }
    if (!voice) pickVoice();
    if (!voice && voicesReady) { toast("No Spanish voice is installed on this device. Use the recording or the dictionary link instead."); return; }
    if (cur) stop();
    speechSynthesis.cancel();
    var u = new SpeechSynthesisUtterance(text.replace(/[«»—]/g, " ").replace(/\bXV\b/, "quince").replace(/^MUCHOS/, "Muchos"));
    u.lang = voice ? voice.lang : "es-MX";
    if (voice) u.voice = voice;
    u.rate = Math.max(0.5, 0.92 * store.speed);
    speechSynthesis.speak(u);
  }

  /* ------------------------------------------------------------ word card */
  var card = null;
  function showWord(key) {
    var v = CA.vocab[key]; if (!v) return;
    if (!card) {
      card = document.createElement("div"); card.className = "wcard"; card.setAttribute("role", "dialog"); card.setAttribute("aria-label", "Word details");
      document.body.appendChild(card);
    }
    var link = "";
    if (v.u) {
      var lab = v.uk === "base" ? 'SpanishDict: base form <i lang="es">' + v.ub + "</i>" : "Hear on SpanishDict";
      link = '<a class="ext" target="_blank" rel="noopener" href="' + v.u + '">' + lab + " ↗</a>";
    }
    var base = v.b !== v.f ? ' <span class="fine">from <i lang="es">' + v.b + "</i></span>" : "";
    card.innerHTML = '<button class="x" aria-label="Close">×</button><h4 lang="es">' + v.f + "</h4>" +
      '<div class="syl" lang="es">' + v.syl + "</div>" + (v.sn.length ? '<div class="sn">' + v.sn.join("; ") + "</div>" : "") +
      '<p class="m">' + v.m + base + '</p><p class="g">' + v.g + "</p>" +
      '<div class="acts"><button class="btn say" data-say="' + (key === "XV" ? "quince" : v.f) + '">Voice</button>' + link +
      '<a class="ext" href="vocabulary.html#w-' + encodeURIComponent(key) + '">In the vocabulary list</a></div>';
    card.classList.add("show");
  }
  function hideWord() { if (card) card.classList.remove("show"); }

  /* ------------------------------------------------------------ practice boxes */
  function seeded(seed) { return function () { seed = (seed * 1664525 + 1013904223) % 4294967296; return seed / 4294967296; }; }
  var WORD = /[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+/g;
  var FRACTION = [0, 0.25, 0.5, 0.75, 1, 1];
  var HINTS = ["Level 0: the full text. Read it aloud twice before hiding anything.",
    "Level 1: one word in four is hidden. Say the whole text aloud; tap a blank only if you are stuck.",
    "Level 2: half the words are hidden.", "Level 3: three words in four are hidden.",
    "Level 4: only the first letter of each word is shown.", "Level 5: everything is hidden. Recite, then tap to check."];

  function setupCloze(box) {
    var sel = $(".cz-range", box), body = $(".cz-body", box), count = $(".cz-count", box), hint = $(".cz-hint", box);
    var st = { level: 1, seed: 7, reveals: 0 };
    function rkey() { return sel.value; }
    function render() {
      var nums = sel.value.split(",").map(Number), rnd = seeded(st.seed + nums[0] * 31 + st.level), out = [];
      st.reveals = 0;
      nums.forEach(function (n) {
        var s = CA.sent[n - 1], i = 0, phase = Math.floor(rnd() * 4);
        var htmlS = s.es.replace(WORD, function (w) {
          var hide;
          if (st.level === 0) hide = false;
          else if (st.level >= 4) hide = true;
          else if (st.level === 1) hide = (i + phase) % 4 === 0;
          else if (st.level === 2) hide = (i + phase) % 2 === 0;
          else hide = (i + phase) % 4 !== 0;
          i++;
          if (!hide) return w;
          var shown = st.level === 4 ? '<span class="fl">' + w.charAt(0) + "</span>" + w.slice(1) : w;
          return '<span class="gap" tabindex="0" role="button" aria-label="hidden word">' + shown + "</span>";
        });
        out.push('<div class="cz-sent"><span class="num">' + n + "</span>" + htmlS + '<div class="cz-en" lang="en">' + s.en + "</div></div>");
      });
      body.innerHTML = out.join("");
      $$("[data-level]", box).forEach(function (b) { b.classList.toggle("on", +b.getAttribute("data-level") === st.level); });
      hint.textContent = HINTS[st.level];
      upd();
    }
    function upd() {
      var best = store.practice[rkey()];
      count.textContent = (st.level ? "Reveals: " + st.reveals : "") + (best != null ? (st.level ? " · " : "") + "best level recorded: " + best : "");
    }
    function open(g) { if (g.classList.contains("open")) return; g.classList.add("open"); g.removeAttribute("tabindex"); st.reveals++; upd(); }
    box.addEventListener("click", function (e) {
      var g = e.target.closest(".gap"); if (g) { open(g); return; }
      var lv = e.target.closest("[data-level]"); if (lv) { st.level = +lv.getAttribute("data-level"); render(); return; }
      var a = e.target.closest("[data-cz]"); if (!a) return;
      var act = a.getAttribute("data-cz");
      if (act === "reveal") { $$(".gap", box).forEach(function (x) { x.classList.add("open"); }); }
      if (act === "reset") render();
      if (act === "shuffle") { st.seed += 13; render(); }
      if (act === "done") {
        var prev = store.practice[rkey()];
        if (prev == null || st.level > prev) { store.practice[rkey()] = st.level; save(); }
        toast("Recorded level " + st.level + (st.level && st.reveals ? " with " + st.reveals + " reveal" + (st.reveals > 1 ? "s" : "") : "") + (st.level < 5 ? ". Try level " + (st.level + 1) + " next." : ". That is the top level."));
        upd(); renderRecord();
      }
    });
    box.addEventListener("keydown", function (e) {
      if ((e.key === "Enter" || e.key === " ") && e.target.classList.contains("gap")) { e.preventDefault(); open(e.target); }
    });
    sel.addEventListener("change", render);
    $(".cz-en", box).addEventListener("change", function () { box.classList.toggle("show-en", this.checked); });
    var best = store.practice[rkey()];
    if (best != null) st.level = Math.min(5, best + 1);
    if (document.body.getAttribute("data-page") === "lesson-20.html") st.level = 5;
    render();
  }

  function renderRecord() {
    var host = $("#practice-record"); if (!host) return;
    var rows = CA.scenes.map(function (sc) {
      var nums = []; for (var i = sc.a; i <= sc.b; i++) nums.push(i);
      return [sc.name + " (" + (sc.a === sc.b ? sc.a : sc.a + "–" + sc.b) + ")", nums.join(",")];
    });
    var all = []; for (var i = 1; i <= 17; i++) all.push(i);
    rows.push(["The whole paragraph", all.join(",")]);
    host.innerHTML = '<div class="tablewrap"><table><thead><tr><th>Text</th><th>Levels 1 to 5</th><th>Best</th></tr></thead><tbody>' + rows.map(function (r) {
      var best = store.practice[r[1]], dots = "";
      for (var l = 1; l <= 5; l++) dots += '<span class="dot' + (best != null && best >= l ? " on" : "") + '"></span>';
      return "<tr><td>" + r[0] + "</td><td>" + dots + "</td><td>" + (best != null ? "level " + best : "not yet") + "</td></tr>";
    }).join("") + "</tbody></table></div>";
  }

  /* ------------------------------------------------------------ progress, checks */
  function lessonNo() { var m = /lesson-(\d+)\.html/.exec(document.body.getAttribute("data-page") || ""); return m ? +m[1] : 0; }

  function refreshScores() {
    $$(".score").forEach(function (el) {
      var p = el.getAttribute("data-prefix"), total = +el.getAttribute("data-total"), n = 0;
      for (var i = 1; i <= total; i++) if (store.checks[p + i]) n++;
      el.textContent = n ? n + " of " + total + " marked right" : "";
    });
  }
  function refreshDone() {
    var b = $("[data-done]"); if (!b) return;
    var n = b.getAttribute("data-done"), d = !!store.done[n];
    b.classList.toggle("is-done", d);
    b.textContent = d ? "Lesson " + n + " complete ✓ (tap to undo)" : "Mark lesson " + n + " complete";
  }
  function refreshIndex() {
    var cards = $$(".lcard"); if (!cards.length) return;
    var n = 0, next = 0;
    cards.forEach(function (c) {
      var id = c.getAttribute("data-lesson"), d = !!store.done[id];
      c.classList.toggle("done", d); if (d) n++; else if (!next) next = +id;
    });
    $(".pfill").style.width = (n / 20 * 100) + "%";
    $(".ptext").textContent = n + " of 20 lessons complete";
    var cont = $("#continue");
    if (n === 20) { cont.textContent = "Review the final assessment"; cont.href = "lesson-20.html"; }
    else {
      var goto = next || 1;
      cont.href = "lesson-" + (goto < 10 ? "0" : "") + goto + ".html";
      cont.textContent = (n ? "Continue with lesson " : "Start lesson ") + goto;
    }
  }

  /* ------------------------------------------------------------ vocabulary page */
  function setupVocab() {
    var q = $("#vq"); if (!q) return;
    var s = $("#vs"), rows = $$("#vt tbody tr, #xt tbody tr"), cnt = $("#vcount");
    function fold(x) { return x.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
    function apply() {
      var t = fold(q.value.trim()), sn = s.value, n = 0;
      rows.forEach(function (r) {
        var ok = (!t || r.getAttribute("data-f").indexOf(t) >= 0) && (!sn || r.getAttribute("data-s").indexOf("," + sn + ",") >= 0);
        r.hidden = !ok; if (ok) n++;
      });
      cnt.textContent = n + " of " + rows.length + " entries";
    }
    q.addEventListener("input", apply); s.addEventListener("change", apply); apply();
    function jump() {
      var id = decodeURIComponent(location.hash.slice(1)); if (!id) return;
      var el = document.getElementById(id); if (!el) return;
      $$("tr.hit").forEach(function (r) { r.classList.remove("hit"); });
      if (el.tagName === "TR") { el.hidden = false; el.classList.add("hit"); el.scrollIntoView({ block: "center" }); }
    }
    window.addEventListener("hashchange", jump); setTimeout(jump, 50);
  }

  /* ------------------------------------------------------------ wiring */
  document.addEventListener("click", function (e) {
    var t = e.target;
    var p = t.closest("[data-play]"); if (p) { e.preventDefault(); play(p.getAttribute("data-play")); return; }
    var rp = t.closest("[data-repeat]"); if (rp) { e.preventDefault(); play(rp.getAttribute("data-repeat"), true); return; }
    var sy = t.closest("[data-say]"); if (sy) { e.preventDefault(); sayText(sy.getAttribute("data-say")); return; }
    if (t.closest(".wcard .x")) { hideWord(); return; }
    var w = t.closest(".w"); if (w && !t.closest(".gap")) { showWord(w.getAttribute("data-k")); return; }
    var es = t.closest(".es"); if (es && !t.closest("a")) { sayText(es.textContent); return; }
    var d = t.closest("[data-done]");
    if (d) {
      var n = d.getAttribute("data-done");
      if (store.done[n]) delete store.done[n]; else store.done[n] = true;
      save(); refreshDone(); return;
    }
    if (t.id === "reset-progress") {
      if (confirm("Erase all saved progress for this course on this device?")) {
        store.done = {}; store.checks = {}; store.practice = {}; save(); location.reload();
      }
      return;
    }
    if (card && card.classList.contains("show") && !t.closest(".wcard")) hideWord();
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { hideWord(); } });
  document.addEventListener("change", function (e) {
    var c = e.target;
    if (c.matches && c.matches("input[data-check]")) {
      var key = c.getAttribute("data-check");
      if (c.checked) store.checks[key] = true; else delete store.checks[key];
      save(); refreshScores();
    }
    if (c.id === "toggle-en") { store.en = c.checked; save(); document.body.classList.toggle("no-en", !store.en); }
  });

  $$("input[data-check]").forEach(function (c) { c.checked = !!store.checks[c.getAttribute("data-check")]; });
  $$(".w").forEach(function (w) { w.setAttribute("tabindex", "0"); w.setAttribute("role", "button"); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && e.target.classList && e.target.classList.contains("w")) showWord(e.target.getAttribute("data-k"));
  });
  var ten = $("#toggle-en"); if (ten) { ten.checked = store.en !== false; document.body.classList.toggle("no-en", store.en === false); }
  $$("[data-cloze]").forEach(setupCloze);
  renderRecord(); refreshScores(); refreshDone(); refreshIndex(); setupVocab();
  if (lessonNo()) { store.last = lessonNo(); save(); }
  if (location.hash && /^#s\d+$/.test(location.hash)) { var tgt = $(location.hash); if (tgt) tgt.classList.add("now"); }
})();
