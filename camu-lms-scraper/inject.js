// Runs in the page's MAIN world at document_start to capture the course
// context IDs that Camu sends with its content API requests. The IDs are
// published onto <html data-camu-ctx="..."> so the isolated-world content
// script can read them and call the same APIs directly.
(function () {
  "use strict";
  try {
    var ctx = {};
    var FIELDS = ["tCntId", "subjId", "SubjId", "PrID", "CrID", "AcYr", "DeptID", "SemID", "SecID", "InId", "staffId"];

    function publish() {
      try {
        document.documentElement.setAttribute("data-camu-ctx", JSON.stringify(ctx));
      } catch (e) { /* ignore */ }
    }

    function extract(body) {
      if (!body) return;
      var o = body;
      if (typeof body === "string") {
        try { o = JSON.parse(body); } catch (e) { return; }
      }
      if (!o || typeof o !== "object") return;
      var subject = o.subjId || o.SubjId;
      if (subject && subject !== (ctx.subjId || ctx.SubjId)) ctx = {};
      var changed = false;
      for (var i = 0; i < FIELDS.length; i++) {
        var f = FIELDS[i];
        if (o[f] && o[f] !== ctx[f]) { ctx[f] = o[f]; changed = true; }
      }
      if (changed) publish();
    }

    if (window.fetch) {
      var origFetch = window.fetch;
      window.fetch = function (input, init) {
        try { if (/teaching-content|TeachContentDefinition|lms\//.test(String(input && input.url || input)) && init && init.body) extract(init.body); } catch (e) { /* ignore */ }
        return origFetch.apply(this, arguments);
      };
    }

    var XO = XMLHttpRequest.prototype.open;
    var XS = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.open = function (method, url) {
      try { this.__camuUrl = url; } catch (e) { /* ignore */ }
      return XO.apply(this, arguments);
    };
    XMLHttpRequest.prototype.send = function (body) {
      try { if (/teaching-content|TeachContentDefinition|lms\//.test(String(this.__camuUrl)) && body) extract(body); } catch (e) { /* ignore */ }
      return XS.apply(this, arguments);
    };
  } catch (e) { /* ignore */ }
})();
