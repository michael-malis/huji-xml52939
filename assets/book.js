/* ==========================================================================
   book.js — общий скрипт книги.

   Заменяет продублированную в 12 файлах настройку MathJax и выносит из
   глобальной области константы Plotly: прежние top-level `const CFG` и
   `const AXIS` конфликтовали между главами и ломали сборку всех тем в один
   документ (см. docs/legacy/revision_log.md, строки 259–288).

   Классический скрипт, не модуль: книга должна открываться двойным щелчком
   по файлу, а ES-модули и fetch() под file:// заблокированы.

   Подключается СИНХРОННО в <head>, и это существенно. Три вещи обязаны
   произойти до того, как страница начнёт отрисовываться и выполняться:
     * установка темы — иначе вспышка светлого фона на тёмной теме;
     * объявление window.MathJax — иначе конфигурация опоздает к загрузке
       самого MathJax;
     * объявление XAI.rng / XAI.CFG / XAI.AXIS — инлайновый скрипт с фигурами
       стоит в конце <body> и выполняется во время разбора документа, то есть
       РАНЬШЕ любого defer-скрипта.
   Работа с DOM отложена до DOMContentLoaded в самом низу файла.
   ========================================================================== */

/* --------------------------------------------------------------------------
   0. Настройка MathJax. Объявляется немедленно, до подключения MathJax с CDN.
   -------------------------------------------------------------------------- */
window.MathJax = {
  tex: { inlineMath: [["$", "$"]], displayMath: [["$$", "$$"]] },
  options: { skipHtmlTags: ["script", "noscript", "style", "textarea", "pre", "code"] }
};

(function () {
  "use strict";

  var XAI = (window.XAI = window.XAI || {});

  /* ------------------------------------------------------------------------
     0b. Тема — до первой отрисовки.
     localStorage может бросать исключение (приватное окно, запрет на данные
     сайтов), поэтому любой доступ к нему обёрнут.
     ------------------------------------------------------------------------ */
  try {
    var saved = localStorage.getItem("xai-theme");
    if (saved === "dark" || saved === "light") {
      document.documentElement.setAttribute("data-theme", saved);
    }
  } catch (e) {
    /* нет доступа к хранилищу — остаётся системная тема */
  }

  /* ------------------------------------------------------------------------
     1. Манифест книги — единственный источник правды о порядке глав.
     Хлебные крошки и переходы «предыдущая/следующая» строятся отсюда, поэтому
     перенумерация главы не требует правки навигации в самих файлах.
     ------------------------------------------------------------------------ */
  var PARTS = [
    {
      n: "I",
      title: "Модели, интерпретируемые по построению",
      chapters: [
        { id: "01", file: "01-linear-models.html",         short: "Линейная модель" },
        { id: "02", file: "02-glm-gam-interactions.html",  short: "GLM, сплайны, GAM" },
        { id: "03", file: "03-trees-ensembles-gini.html",  short: "Деревья и Gini" }
      ]
    },
    {
      n: "II",
      title: "Эффект признака: глобальные агностические методы",
      chapters: [
        { id: "04", file: "04-pd-mplot-ale-fanova.html",   short: "PD, M-plot, ALE" },
        { id: "05", file: "05-feature-importance.html",    short: "Важность признака" }
      ]
    },
    {
      n: "III",
      title: "Локальные объяснения и атрибуция",
      chapters: [
        { id: "06", file: "06-shapley-shap.html",          short: "Shapley и SHAP" },
        { id: "07", file: "07-local-surrogates.html",      short: "LIME, RISE, контрфактуалы" }
      ]
    },
    {
      n: "IV",
      title: "Глубокие модели: от пикселей к концептам",
      chapters: [
        { id: "08", file: "08-saliency-maps.html",         short: "Saliency maps" },
        { id: "09", file: "09-concept-explanations.html",  short: "Концепты" }
      ]
    },
    {
      n: "V",
      title: "Данные как единица объяснения",
      chapters: [
        { id: "10", file: "10-example-based.html",         short: "Пространство примеров" }
      ]
    },
    {
      n: "VI",
      title: "Оценка объяснений",
      chapters: [
        { id: "11", file: "11-evaluation.html",            short: "Оценка объяснений" }
      ]
    }
  ];

  var FLAT = [];
  PARTS.forEach(function (part) {
    part.chapters.forEach(function (ch) {
      FLAT.push({ id: ch.id, file: ch.file, short: ch.short, part: part });
    });
  });

  XAI.PARTS = PARTS;
  XAI.CHAPTERS = FLAT;

  /* ------------------------------------------------------------------------
     2. Детерминированный ГПСЧ.
     28 мест в книге рисовали данные через Math.random(), из-за чего графики
     меняли значения при каждой перезагрузке. Справочник так вести себя не
     должен: у каждой фигуры теперь свой литеральный seed.
     ------------------------------------------------------------------------ */
  XAI.rng = function (seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6d2b79f5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  };

  /* Нормальная величина из равномерного потока (Box–Muller).
     Принимает функцию rand, чтобы наследовать её seed. */
  XAI.randn = function (rand) {
    var u = 0, v = 0;
    while (u === 0) u = rand();
    while (v === 0) v = rand();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  };

  /* ------------------------------------------------------------------------
     3. Общие настройки Plotly
     ------------------------------------------------------------------------ */
  XAI.CFG = { displayModeBar: false, scrollZoom: false, doubleClick: false, responsive: true };
  XAI.AXIS = { zeroline: false, gridcolor: "#EEEDE7" };

  /* ------------------------------------------------------------------------
     4. Навигация: хлебные крошки и переходы между главами.
     Страница объявляет себя через <body data-chapter="04">.
     ------------------------------------------------------------------------ */
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function currentIndex() {
    var id = document.body.getAttribute("data-chapter");
    if (!id) return -1;
    for (var i = 0; i < FLAT.length; i++) if (FLAT[i].id === id) return i;
    return -1;
  }

  function buildBreadcrumb(i) {
    var ch = FLAT[i];
    var nav = el("nav", "breadcrumb");
    nav.setAttribute("aria-label", "Навигация по книге");

    var home = el("a", null, "Оглавление");
    home.href = "index.html";
    nav.appendChild(home);

    nav.appendChild(el("span", "sep", "›"));
    nav.appendChild(el("span", null, "Часть " + ch.part.n + " · " + ch.part.title));
    nav.appendChild(el("span", "sep", "›"));
    nav.appendChild(el("span", null, "Глава " + Number(ch.id)));
    return nav;
  }

  function buildChapterNav(i) {
    var nav = el("nav", "chapter-nav");
    nav.setAttribute("aria-label", "Переход между главами");

    function link(target, dirLabel, cls) {
      var a = el("a", cls);
      a.href = target.file;
      a.appendChild(el("span", "dir", dirLabel));
      a.appendChild(el("span", "name", "Глава " + Number(target.id) + ". " + target.short));
      return a;
    }

    if (i > 0) nav.appendChild(link(FLAT[i - 1], "← Предыдущая глава", "prev"));

    var toc = el("a", "toc-link");
    toc.href = "index.html";
    toc.appendChild(el("span", "dir", "↑"));
    toc.appendChild(el("span", "name", "Оглавление"));
    nav.appendChild(toc);

    if (i < FLAT.length - 1) nav.appendChild(link(FLAT[i + 1], "Следующая глава →", "next"));
    return nav;
  }

  /* ------------------------------------------------------------------------
     5. Подсветка текущего раздела в оглавлении главы
     ------------------------------------------------------------------------ */
  function scrollSpy() {
    var toc = document.querySelector("nav.toc");
    if (!toc || !("IntersectionObserver" in window)) return;

    var links = {};
    Array.prototype.forEach.call(toc.querySelectorAll('a[href^="#"]'), function (a) {
      links[decodeURIComponent(a.getAttribute("href").slice(1))] = a;
    });

    var targets = Object.keys(links)
      .map(function (id) { return document.getElementById(id); })
      .filter(Boolean);
    if (!targets.length) return;

    var visible = {};
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { visible[e.target.id] = e.isIntersecting; });
      var current = null;
      for (var i = 0; i < targets.length; i++) {
        if (visible[targets[i].id]) { current = targets[i].id; break; }
      }
      Object.keys(links).forEach(function (id) {
        if (id === current) links[id].setAttribute("aria-current", "true");
        else links[id].removeAttribute("aria-current");
      });
    }, { rootMargin: "-10% 0px -70% 0px" });

    targets.forEach(function (t) { obs.observe(t); });
  }

  /* ------------------------------------------------------------------------
     6. Обёртки прокрутки для широких таблиц.
     Ставятся скриптом, чтобы не править разметку 123 таблиц вручную.
     ------------------------------------------------------------------------ */
  function wrapTables() {
    Array.prototype.forEach.call(
      document.querySelectorAll("table.plain, table.contrast"),
      function (table) {
        if (table.parentElement && table.parentElement.classList.contains("table-wrap")) return;
        var wrap = el("div", "table-wrap");
        wrap.setAttribute("role", "region");
        wrap.setAttribute("tabindex", "0");
        var cap = table.getAttribute("data-label") ||
          (table.querySelector("th") ? table.querySelector("th").textContent.trim() : "Таблица");
        wrap.setAttribute("aria-label", "Таблица: " + cap);
        table.parentNode.insertBefore(wrap, table);
        wrap.appendChild(table);
      }
    );
  }

  /* ------------------------------------------------------------------------
     7. Кнопки: наверх и переключение темы
     ------------------------------------------------------------------------ */
  function backToTop() {
    var btn = el("button", "to-top", "↑");
    btn.type = "button";
    btn.setAttribute("aria-label", "Наверх страницы");
    btn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
    document.body.appendChild(btn);

    var ticking = false;
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        btn.classList.toggle("visible", window.scrollY > 600);
        ticking = false;
      });
    }, { passive: true });
  }

  function themeToggle() {
    var btn = el("button", "theme-toggle");
    btn.type = "button";

    function label() {
      var explicit = document.documentElement.getAttribute("data-theme");
      var dark = explicit
        ? explicit === "dark"
        : window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
      btn.textContent = dark ? "☀" : "☾";
      btn.setAttribute("aria-label", dark ? "Светлая тема" : "Тёмная тема");
    }

    btn.addEventListener("click", function () {
      var explicit = document.documentElement.getAttribute("data-theme");
      var dark = explicit
        ? explicit === "dark"
        : window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
      var next = dark ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      try { localStorage.setItem("xai-theme", next); } catch (e) { /* нет хранилища */ }
      label();
    });

    label();
    document.body.appendChild(btn);
  }

  /* ------------------------------------------------------------------------
     8. Запуск
     ------------------------------------------------------------------------ */
  function init() {
    wrapTables();

    var i = currentIndex();
    if (i >= 0) {
      var back = document.querySelector("a.back-link");
      var crumb = buildBreadcrumb(i);
      if (back) back.parentNode.replaceChild(crumb, back);
      else document.body.insertBefore(crumb, document.body.firstChild);

      var footer = document.querySelector("footer");
      var chNav = buildChapterNav(i);
      if (footer) footer.parentNode.insertBefore(chNav, footer);
      else document.body.appendChild(chNav);
    }

    scrollSpy();
    backToTop();
    themeToggle();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
