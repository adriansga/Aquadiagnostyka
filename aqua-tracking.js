(function () {
  var GA_READY = typeof window.gtag === "function";
  var STORAGE_FIRST = "aqua_first_touch";
  var STORAGE_SESSION = "aqua_session_id";
  var UTM_KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid"];

  function safeStorageGet(key) {
    try { return window.localStorage.getItem(key); } catch (e) { return null; }
  }

  function safeStorageSet(key, value) {
    try { window.localStorage.setItem(key, value); } catch (e) {}
  }

  function uuid() {
    if (window.crypto && typeof window.crypto.randomUUID === "function") {
      return window.crypto.randomUUID();
    }
    return "aqua-" + Date.now() + "-" + Math.random().toString(16).slice(2);
  }

  function hostFrom(url) {
    try { return url ? new URL(url).hostname : ""; } catch (e) { return ""; }
  }

  function classifySource(referrer, params) {
    if (params.get("gclid")) return "google_ads";
    if (params.get("utm_source")) return params.get("utm_source");
    var host = hostFrom(referrer);
    if (!host) return "direct";
    if (host.indexOf("google.") !== -1) return "google_organic";
    if (host.indexOf("facebook.") !== -1 || host.indexOf("fb.") !== -1) return "facebook";
    if (host.indexOf("instagram.") !== -1) return "instagram";
    return "referral";
  }

  function buildTouch() {
    var params = new URLSearchParams(window.location.search);
    var touch = {
      session_id: safeStorageGet(STORAGE_SESSION) || uuid(),
      source_kind: classifySource(document.referrer, params),
      referrer: document.referrer || "bezposrednio",
      referrer_host: hostFrom(document.referrer),
      landing_url: window.location.href,
      landing_path: window.location.pathname,
      query_string: window.location.search || "",
      timestamp: new Date().toISOString()
    };
    UTM_KEYS.forEach(function (key) {
      touch[key] = params.get(key) || "";
    });
    safeStorageSet(STORAGE_SESSION, touch.session_id);
    return touch;
  }

  var currentTouch = buildTouch();
  var firstTouch = safeStorageGet(STORAGE_FIRST);
  if (!firstTouch) {
    safeStorageSet(STORAGE_FIRST, JSON.stringify(currentTouch));
    firstTouch = JSON.stringify(currentTouch);
  }

  try { firstTouch = JSON.parse(firstTouch); } catch (e) { firstTouch = currentTouch; }

  function setAll(selector, value) {
    document.querySelectorAll(selector).forEach(function (el) {
      el.value = value || "";
    });
  }

  function compactSource(touch) {
    return "source: " + (touch.source_kind || "-")
      + " | ref: " + (touch.referrer || "bezposrednio")
      + " | url: " + (touch.landing_url || window.location.href)
      + " | utm_source: " + (touch.utm_source || "-")
      + " | utm_medium: " + (touch.utm_medium || "-")
      + " | utm_campaign: " + (touch.utm_campaign || "-")
      + " | gclid: " + (touch.gclid ? "tak" : "-");
  }

  function populateFields() {
    var first = firstTouch || currentTouch;
    setAll(".src-field", compactSource(currentTouch)
      + " | first_source: " + (first.source_kind || "-")
      + " | first_path: " + (first.landing_path || "-")
      + " | session: " + (currentTouch.session_id || "-"));
    setAll(".tracking-landing-url", currentTouch.landing_url);
    setAll(".tracking-landing-path", currentTouch.landing_path);
    setAll(".tracking-query-string", currentTouch.query_string);
    setAll(".tracking-referrer", currentTouch.referrer);
    setAll(".tracking-utm-source", currentTouch.utm_source);
    setAll(".tracking-utm-medium", currentTouch.utm_medium);
    setAll(".tracking-utm-campaign", currentTouch.utm_campaign);
    setAll(".tracking-gclid", currentTouch.gclid);
    setAll(".tracking-source-kind", currentTouch.source_kind);
    setAll(".tracking-first-landing-url", first.landing_url);
    setAll(".tracking-first-landing-path", first.landing_path);
    setAll(".tracking-first-source-kind", first.source_kind);
    setAll(".tracking-first-utm-source", first.utm_source);
    setAll(".tracking-first-utm-medium", first.utm_medium);
    setAll(".tracking-first-utm-campaign", first.utm_campaign);
    setAll(".tracking-session-id", currentTouch.session_id);
  }

  currentTouch.landingUrl = currentTouch.landing_url;
  currentTouch.landingPath = currentTouch.landing_path;
  currentTouch.queryString = currentTouch.query_string;
  currentTouch.utmSource = currentTouch.utm_source;
  currentTouch.utmMedium = currentTouch.utm_medium;
  currentTouch.utmCampaign = currentTouch.utm_campaign;
  currentTouch.sourceKind = currentTouch.source_kind;
  firstTouch.landingUrl = firstTouch.landing_url;
  firstTouch.landingPath = firstTouch.landing_path;
  firstTouch.utmSource = firstTouch.utm_source;
  firstTouch.utmMedium = firstTouch.utm_medium;
  firstTouch.utmCampaign = firstTouch.utm_campaign;
  firstTouch.sourceKind = firstTouch.source_kind;

  window.aquaAttribution = currentTouch;
  window.aquaFirstTouch = firstTouch;
  window.populateAquaAttributionFields = populateFields;

  function event(name, params) {
    if (!GA_READY) return;
    window.gtag("event", name, Object.assign({
      page_path: currentTouch.landing_path,
      source_kind: currentTouch.source_kind,
      referrer_host: currentTouch.referrer_host,
      utm_source: currentTouch.utm_source,
      utm_medium: currentTouch.utm_medium,
      utm_campaign: currentTouch.utm_campaign
    }, params || {}));
  }

  function appendAttributionToContactLinks() {
    document.querySelectorAll('a[href*="#kontakt"]').forEach(function (a) {
      var href = a.getAttribute("href") || "";
      if (href.indexOf("aquadiagnostyka.pl/#kontakt") === -1 && href.indexOf("/#kontakt") === -1) return;
      if (href.indexOf("utm_source=") !== -1 || !currentTouch.source_kind) return;
      var source = currentTouch.utm_source || currentTouch.source_kind || "site";
      var medium = currentTouch.utm_medium || "internal";
      var campaign = currentTouch.utm_campaign || "seo_page";
      var base = href.split("#")[0] || "/";
      var hash = "#kontakt";
      var glue = base.indexOf("?") === -1 ? "?" : "&";
      a.setAttribute("href", base + glue
        + "utm_source=" + encodeURIComponent(source)
        + "&utm_medium=" + encodeURIComponent(medium)
        + "&utm_campaign=" + encodeURIComponent(campaign)
        + hash);
    });
  }

  function bindEvents() {
    populateFields();
    appendAttributionToContactLinks();

    event("aqua_page_context", {
      page_title: document.title,
      first_source_kind: firstTouch.source_kind || "",
      session_id: currentTouch.session_id
    });

    var formStarted = {};
    document.addEventListener("focusin", function (e) {
      var form = e.target && e.target.closest ? e.target.closest("form") : null;
      if (!form || formStarted[form.id || "form"]) return;
      formStarted[form.id || "form"] = true;
      event("form_start", { event_label: form.id || "form" });
    });

    document.addEventListener("submit", function (e) {
      populateFields();
      var form = e.target;
      event("form_submit_intent", { event_label: form && form.id ? form.id : "form" });
    }, true);

    document.addEventListener("click", function (e) {
      var link = e.target && e.target.closest ? e.target.closest("a[href]") : null;
      if (!link) return;
      var href = link.getAttribute("href") || "";
      var text = (link.textContent || "").trim().slice(0, 80);
      if (href.indexOf("tel:") === 0) event("tel_click", { event_label: href });
      else if (href.indexOf("mailto:") === 0) event("email_click", { event_label: href });
      else if (href.indexOf("#kontakt") !== -1 || /zam[oó]w|kontakt/i.test(text)) event("cta_click", { event_label: text || href, link_url: href });
      else if (/^https?:\/\//.test(href) && href.indexOf(location.hostname) === -1) event("outbound_click", { event_label: hostFrom(href), link_url: href });
    });

    var sentDepth = {};
    window.addEventListener("scroll", function () {
      var doc = document.documentElement;
      var max = Math.max(1, doc.scrollHeight - window.innerHeight);
      var depth = Math.round((window.scrollY / max) * 100);
      [25, 50, 75, 90].forEach(function (mark) {
        if (depth >= mark && !sentDepth[mark]) {
          sentDepth[mark] = true;
          event("scroll_depth", { percent_scrolled: mark });
        }
      });
    }, { passive: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bindEvents);
  } else {
    bindEvents();
  }
})();
