#!/usr/bin/env python3
"""
site_verify.py — deterministic, dependency-free repo checks for elmahrosa-org.

Complements audit-tools/codex_audit.sh (which scores *repo metadata*) by checking
the *content* that is actually served: markup integrity, internal links, SEO/i18n
parity, data files, and credential hygiene.

Usage:
    python3 audit-tools/site_verify.py            # summary + exit code
    python3 audit-tools/site_verify.py --json     # machine-readable findings
    python3 audit-tools/site_verify.py --strict   # treat WARN as FAIL

Exit code 0 = no FAIL, 1 = at least one FAIL (or WARN with --strict).
Stdlib only, so it can run in CI without a package install step.
"""
import json
import os
import re
import sys
from collections import Counter
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STRICT = "--strict" in sys.argv
AS_JSON = "--json" in sys.argv

SITE_PAGES = ["index.html"] + [
    f"{d}/index.html" for d in (
        "architecture", "health", "investors", "government", "security",
        "partners", "trust", "security-advisory", "referral",
    )
]
REQUIRED_NAME = ["description", "robots", "viewport"]
REQUIRED_OG = ["og:type", "og:url", "og:title", "og:description", "og:image"]
REQUIRED_TW = ["twitter:card", "twitter:site", "twitter:title", "twitter:description"]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}
CANON_HOST = "https://elmahrosa.org"
I18N_ALLOW = {
    "claude", "anthropic", "elmahrosa", "teos", "sentinel", "shield", "superintelligence",
    "unitycare", "unity", "care", "hospital", "engine", "crawl", "comply", "block", "warn",
    "allow", "review", "github", "gitlab", "telegram", "vercel", "aws", "docker", "linux",
    "windows", "android", "ios", "hipaa", "gdpr", "nist", "mcp", "api", "saas", "arr",
    "strong", "code", "open", "source", "self", "hosted", "native", "alpha", "beta", "html",
    "json", "yaml", "http", "https", "href", "nbsp", "laquo", "raquo", "download", "email",
    "malwarebytes", "defender", "safebrowsing", "share", "twitter", "linkedin", "gmail",
    "mutual", "installer", "browser", "browser", "malicious",
}

findings = []


def add(cid, severity, check, detail, fix=""):
    findings.append({"id": cid, "severity": severity, "check": check,
                     "detail": detail, "fix": fix})


class Parser(HTMLParser):
    """Collects what we need without any third-party HTML library."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.unclosed = [], []
        self.hrefs, self.ids, self.imgs = [], [], []
        self.names, self.props = {}, {}
        self.ldjson, self._buf = [], None
        self.headings = []
        self.i18n = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag not in VOID:
            self.stack.append(tag)
        if tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "img":
            self.imgs.append((a.get("src", ""), a.get("alt", "")))
        if tag == "meta":
            if a.get("name"):
                self.names[a["name"]] = a.get("content", "")
            if a.get("property"):
                self.props[a["property"]] = a.get("content", "")
        if tag == "script" and a.get("type") == "application/ld+json":
            self._buf = []
        if re.fullmatch(r"h[1-6]", tag):
            self.headings.append(tag)
        if "data-en" in a or "data-ar" in a:
            self.i18n.append((a.get("data-en"), a.get("data-ar")))

    def handle_endtag(self, tag):
        if tag == "script" and self._buf is not None:
            self.ldjson.append("".join(self._buf))
            self._buf = None
        if tag in VOID:
            return
        if tag in self.stack:
            while self.stack and self.stack.pop() != tag:
                pass
        else:
            self.unclosed.append(tag)

    def handle_data(self, data):
        if self._buf is not None:
            self._buf.append(data)

    def close(self):
        super().close()
        self.unclosed.extend(self.stack)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as fh:
        return fh.read()


tracked = []
for dp, dn, fn in os.walk(ROOT):
    if ".git" in dp.split(os.sep):
        continue
    for f in fn:
        rel = os.path.relpath(os.path.join(dp, f), ROOT)
        tracked.append(rel)
html_files = [p for p in tracked if p.endswith((".html", ".htm"))]
parsed = {}

# ---------------------------------------------------------------- markup
for rel in html_files:
    p = Parser()
    p.feed(read(rel))
    p.close()
    parsed[rel] = p
    stray = [t for t in p.unclosed if t not in ("html", "body")]
    if stray:
        add("HTML-UNCLOSED", "FAIL", f"{rel}: unbalanced tags",
            f"unclosed/stray: {sorted(set(stray))[:6]}", "close every element")
    dup = [k for k, v in Counter(p.ids).items() if v > 1]
    if dup:
        add("HTML-DUP-ID", "FAIL", f"{rel}: duplicate id attributes", str(sorted(dup)),
            "ids must be unique per document")
    for attr in ("aria-labelledby", "aria-describedby", "aria-controls", "for"):
        for val in re.findall(rf'{attr}="([^"]+)"', read(rel)):
            for tok in val.split():
                if tok not in set(p.ids):
                    add("ARIA-DANGLING", "WARN", f"{rel}: {attr}=\"{tok}\"",
                        "references an id that does not exist in this document",
                        "add the id or drop the attribute")
    noalt = [s for s, alt in p.imgs if not alt.strip()]
    if noalt:
        add("IMG-ALT", "WARN", f"{rel}: images without alt", str(noalt), "add alt text")

# ---------------------------------------------------------------- links
missing_file, broken_frag = [], []
for rel, p in parsed.items():
    docs = {"": "index.html"}
    for d in os.listdir(ROOT):
        if os.path.isdir(os.path.join(ROOT, d)) and not d.startswith("."):
            if os.path.exists(os.path.join(ROOT, d, "index.html")):
                docs[d] = f"{d}/index.html"
    for href in p.hrefs:
        if href.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
            if href.startswith("#") and len(href) > 1 and href[1:] not in set(p.ids):
                broken_frag.append(f"{rel} -> {href}")
            continue
        if re.match(r"^https?://", href):
            continue
        path, _, frag = href.lstrip("/").partition("#")
        path = path or "index.html"
        cand = os.path.join(ROOT, path)
        if os.path.isdir(cand):
            cand = os.path.join(cand, "index.html")
        if not os.path.exists(cand):
            missing_file.append(f"{rel} -> /{path}")
            continue
        if frag:
            tgt = os.path.relpath(cand, ROOT)
            if tgt in parsed and frag not in set(parsed[tgt].ids):
                broken_frag.append(f"{rel} -> {href}")
if missing_file:
    add("LINK-MISSING", "FAIL", "internal links to non-existent files",
        "; ".join(sorted(set(missing_file))), "create the target or fix the href")
if broken_frag:
    add("LINK-ANCHOR", "FAIL", "links whose #fragment has no target id",
        "; ".join(sorted(set(broken_frag))), "add the id or drop the fragment")

# ---------------------------------------------------------------- SEO / i18n
for rel in SITE_PAGES:
    p = parsed[rel]
    skip = rel == "referral/index.html"          # intentionally noindex, no meta
    if not skip:
        for m in REQUIRED_NAME:
            if m not in p.names:
                add("SEO-META", "FAIL", f"{rel}: missing <meta name={m}>", "", "add it")
        for m in REQUIRED_OG:
            if m not in p.props:
                add("SEO-OG", "FAIL", f"{rel}: missing {m}", "", "add it")
        for m in REQUIRED_TW:
            if m not in p.names:
                add("SEO-TW", "WARN", f"{rel}: missing {m}", "", "add it")
        canon = re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]*)"', read(rel))
        if not canon:
            add("SEO-CANON", "FAIL", f"{rel}: no canonical link", "", "add it")
        elif not canon.group(1).startswith(CANON_HOST):
            add("SEO-CANON", "FAIL", f"{rel}: canonical off the agreed host",
                canon.group(1), f"canonical must start with {CANON_HOST}")
        elif canon.group(1) != p.props.get("og:url"):
            add("SEO-CANON-OG", "WARN", f"{rel}: canonical != og:url",
                f"{canon.group(1)} vs {p.props.get('og:url')}", "align them")
    for en, ar in p.i18n:
        if (en is None) != (ar is None):
            add("I18N-PARTIAL", "WARN", f"{rel}: element has only one language attribute",
                f"en={bool(en)} ar={bool(ar)}", "give every switchable element both")
    if p.i18n:
        for _, ar in p.i18n:
            if not ar or "<" in ar or "&" in ar:
                continue
            if ar.strip().startswith(("-", "–", "—")) or ar.strip().endswith(("-", "–", "—")):
                add("I18N-MALFORMED", "WARN", f"{rel}: Arabic string has a dangling joiner",
                    ar[:64], "rewrite the phrase — partial translation of a compound term")
                continue
            words = [w for w in re.findall(r"(?<![\w.-])[a-z][a-z-]{3,}(?![\w.-])", ar)]
            stray = [w for w in words if w not in I18N_ALLOW and "-" not in w]
            if stray:
                add("I18N-UNTRANSLATED", "WARN", f"{rel}: Arabic string keeps untranslated Latin word",
                    f"{stray} in: {ar[:64]}", "translate it or add the term to the allowlist")

# ---------------------------------------------------------------- data files
for rel in ("audit-data/latest.jsonl", "docs/data/latest.jsonl", "api/status.json"):
    body = read(rel)
    try:
        if rel.endswith(".jsonl"):
            for line in body.splitlines():
                if line.strip():
                    json.loads(line)
        else:
            json.loads(body)
    except Exception as exc:
        add("DATA-JSON", "FAIL", f"{rel} is not valid JSON/JSONL", str(exc), "repair the file")
if read("audit-data/latest.jsonl").strip() != read("docs/data/latest.jsonl").strip():
    add("DATA-DRIFT", "FAIL", "audit-data/latest.jsonl != docs/data/latest.jsonl",
        "the Pages copy and the repo copy disagree", "re-run codex_audit.sh")

urls = set(re.findall(r"<loc>https://elmahrosa\.org(/[^<]*)</loc>", read("sitemap.xml")))
sitemap_norm = {u.rstrip("/") or "/" for u in urls}
page_norm = {("/" if p == "index.html" else "/" + p.split("/")[0]).rstrip("/") or "/"
             for p in SITE_PAGES if "referral" not in p}
for missing in sorted(page_norm - sitemap_norm):
    add("SITEMAP-MISS", "WARN", "indexable page absent from sitemap.xml", missing,
        "add the URL to sitemap.xml")
for ghost in sorted(sitemap_norm - page_norm):
    add("SITEMAP-STALE", "WARN", "sitemap URL with no page in the repo", ghost,
        "remove the URL or restore the page")

for tag, val in re.findall(r'<url>\s*<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>',
                           read("sitemap.xml")):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", val.strip()):
        add("SITEMAP-LASTMOD", "WARN", f"{tag}: lastmod is not ISO-8601", val, "fix format")

# ---------------------------------------------------------------- security
SECRET_PATTERNS = {
    "aws-access-key": r"AKIA[0-9A-Z]{16}",
    "github-token": r"gh[pousr]_[0-9A-Za-z]{36}|github_pat_[0-9A-Za-z_]{22,}",
    "slack-token": r"xox[baprs]-[0-9A-Za-z-]{10,}",
    "openai-key": r"sk-[0-9A-Za-z]{32,}",
    "google-api-key": r"AIza[0-9A-Za-z_\-]{35}",
    "telegram-bot-token": r"\b\d{8,10}:AA[0-9A-Za-z_\-]{30,}",
    "jwt": r"eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}",
    "private-key-block": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "url-with-credentials": r"[a-z]+://[^/\s'\"]+:[^@/\s'\"]{6,}@",
}
def ignored(rel, check):
    """A file opts out of one check with  <!-- site_verify:ignore CHECK-ID -->  (historical
    records quote prices that were superseded the same day; the marker keeps that from being
    reported as drift while leaving the file itself unedited)."""
    return ("site_verify:ignore " + check) in read(rel)

for rel in tracked:
    if rel.endswith((".png", ".jpg", ".gif", ".ico", ".woff2")):
        continue
    if rel.startswith("audits/") and rel.endswith(".json"):
        continue
    body = read(rel)
    for label, pat in SECRET_PATTERNS.items():
        for m in re.finditer(pat, body):
            hit = m.group(0)
            if "${" in hit or "process.env" in hit or "os.environ" in hit:
                add("SECRET-TEMPLATE", "WARN", f"{rel}: credential placeholder interpolated into a URL",
                    hit[:60], "prefer an Authorization header or `git push` via a credential helper")
                continue
            add("SECRET", "FAIL", f"{rel}: possible {label}", hit[:60],
                "rotate immediately and remove from git history")
htaccess = read(".htaccess")
for header in ("Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options",
               "X-Content-Type-Options", "Referrer-Policy", "Permissions-Policy"):
    if header not in htaccess:
        add("HDR-MISSING", "FAIL", f".htaccess: {header} not set", "", "set it in <IfModule mod_headers.c>")
if "Header always set" not in htaccess:
    add("HDR-SCOPE", "WARN", ".htaccess uses 'Header set' only",
        "headers are absent from error responses (404/500)", "use 'Header always set'")
if "mod_headers.c>" in htaccess:
    add("HDR-FAILSILENT", "WARN", "header block is wrapped in <IfModule mod_headers.c>",
        "if the module is off, every header silently disappears",
        "keep IfModule but fail loudly: also assert headers with a smoke test")
if "Options -Indexes" not in htaccess:
    add("DIR-LISTING", "WARN", ".htaccess does not disable directory indexes",
        "directories without index.html (audit-data/, audits/, docs/) can be listed",
        "add 'Options -Indexes' and RedirectMatch 404 for internal paths")
if not re.search(r"RewriteCond.*HTTPS.*off", htaccess, re.S):
    add("NO-HTTPS-REDIRECT", "WARN", ".htaccess has no http→https redirect",
        "plain-HTTP requests are served unencrypted (and HSTS preload then breaks)",
        "add a front-end https redirect for the Hostinger CDN")
for rel in SITE_PAGES:
    body = read(rel)
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.S):
        try:
            json.loads(blk)
        except Exception as exc:
            add("JSONLD", "FAIL", f"{rel}: JSON-LD does not parse", str(exc), "fix the JSON")
        else:
            doc = json.loads(blk)
            for node in doc.get("@graph", [doc]):
                if isinstance(node, dict) and node.get("@type") == "SoftwareApplication":
                    offers = node.get("offers") or {}
                    price = str(offers.get("price", ""))
                    visible = re.findall(r"\$(\d[\d,]*)\s*/\s*mo", body)
                    if visible and price and price not in visible and price != "0":
                        add("JSONLD-PRICE", "WARN", f"{rel}: JSON-LD price != page price",
                            f"ld+json={price} page={visible}", "keep structured data in sync")
                    if price == "0" and visible:
                        add("JSONLD-PRICE", "FAIL",
                            f"{rel}: JSON-LD advertises price 0 but the page sells {visible}",
                            "set offers.price to the real lowest plan price or remove offers",
                            "Google uses this for rich results and free-product signals")
for rel in tracked:
    if rel.endswith(".js"):
        body = read(rel)
        if "cdn.jsdelivr.net" in body or "cdnjs" in body or "unpkg.com" in body:
            add("CDN-DOC", "WARN", f"{rel}: third-party CDN dependency",
                "not covered by the site CSP; no SRI hash", "self-host and pin with integrity")
for rel in html_files:
    body = read(rel)
    for m in re.finditer(r'<script[^>]+src="(https://[^"]+)"[^>]*>', body):
        if "integrity=" not in m.group(0):
            add("CDN-SRI", "WARN", f"{rel}: external script without SRI", m.group(1),
                "add integrity= and crossorigin=")

# ---------------------------------------------------------------- commercial copy
UNIT = {"mo": "mo", "month": "mo", "yr": "yr", "year": "yr"}


def prices_of(text):
    """(amount, unit) pairs. Tags are stripped first so '$199<span>/mo</span>' counts.

    Units are normalised, so '$69/month' and '$69/mo' are the same price point.
    """
    plain = re.sub(r"<[^>]+>", "", text)
    return {(n.replace(",", ""), UNIT[u.lower()])
            for n, u in re.findall(r"\$\s?([\d][\d,]{1,7})\s*/\s*(mo|month|yr|year)\b", plain, re.I)}

home = read("index.html")
home_prices = prices_of(home)
for rel in ("GA_RELEASE_NOTES.md", "RELEASE_NOTES_v5.0.0.md", "PRODUCTION_READINESS_REPORT.md",
            "FINAL_GA_READINESS_REPORT.md", "investors/index.html", "security/index.html"):
    if ignored(rel, "PRICING-DIVERGENCE"):
        continue
    other = prices_of(read(rel))
    if not other:
        continue
    only_doc = other - home_prices
    if only_doc:
        doc_side = ", ".join("$" + n + "/" + u for n, u in sorted(only_doc))
        home_side = ", ".join("$" + n + "/" + u for n, u in sorted(home_prices))
        add("PRICING-DIVERGENCE", "FAIL", f"{rel} lists prices the homepage does not offer",
            "document: " + doc_side + "  |  homepage: " + home_side,
            "make one file authoritative and regenerate the others")

# price shown in two languages must agree
for m in re.finditer(r'data-en="([^"]*\$([\d,]+)[^"]*)"[^>]*data-ar="([^"]*)"', home):
    en_num = int(m.group(2).replace(",", ""))
    ar_digits = {"٠": "0", "١": "1", "٢": "2", "٣": "3", "٤": "4",
                 "٥": "5", "٦": "6", "٧": "7", "٨": "8", "٩": "9"}
    ar = "".join(ar_digits.get(c, c) for c in m.group(3))
    nums = [int(x.replace(",", "")) for x in re.findall(r"\d{2,7}(?:,\d{3})*", ar)]
    if nums and en_num not in nums:
        add("I18N-PRICE", "FAIL", "index.html: Arabic and English advertise different prices",
            f"en ${en_num} vs ar ${nums} in: {m.group(1)[:48]}",
            "prices must match in both locales")

# strikethrough original must differ from the discounted amount
for m in re.finditer(r'<div class="pricing-original">([^<]+)</div>\s*<div class="pricing-amount">([^<]+)<', home):
    orig, now = re.findall(r"[\d,]+", m.group(1)), re.findall(r"[\d,]+", m.group(2))
    if orig and now and orig[0] == now[0]:
        add("PROMO-NOT-APPLIED", "FAIL", "index.html: discounted price equals the original price",
            f"original {m.group(1).strip()} == amount {m.group(2).strip()}",
            "show the real discounted figure or drop the strikethrough/promo label")

if re.search(r"Founding 10.{0,40}50%\s*Off", home, re.S | re.I):
    add("PROMO-UNVERIFIED", "WARN",
        "index.html advertises a 50%-off promotion",
        "the promotion only holds if the merchant-of-record checkout applies the same discount — verify the live product price",
        "re-check each dodo.pe link and keep the copy in sync with the checkout product")

# "real-time" claims need a data source
for rel in SITE_PAGES:
    body = read(rel)
    if (re.search(r"(real-?time|live)\s+(operational\s+)?status", body, re.I)
            and re.search(r"uptime", body, re.I) and "<script" not in body):
        add("STATIC-REALTIME", "FAIL", f"{rel}: advertises real-time status but ships no script or data source",
            "no <script>, no fetch of /api/status.json — the numbers are hardcoded",
            "either render from api/status.json at runtime or relabel as a snapshot with a date")

# launch-date badges expire
today = __import__("datetime").date.today()
for rel in html_files:
    for m in re.finditer(r"GA RELEASE\s*[—-]\s*([A-Z][a-z]+)\s+(20\d\d)", read(rel)):
        mon, yr = m.group(1), int(m.group(2))
        month = {v: i for i, v in enumerate(
            ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"], 1)}.get(mon)
        if month:
            deadline = __import__("datetime").date(yr, month, 28)
            if today > deadline + __import__("datetime").timedelta(days=45):
                add("STALE-LAUNCH-BADGE", "WARN", f"{rel}: launch badge reads '{m.group(0).strip()}'",
                    f"more than 45 days past ({today})", "update the badge/copy to the actual GA date")

# ---------------------------------------------------------------- optional live probe
# Off by default so the repo checks stay offline and deterministic:
#     python3 audit-tools/site_verify.py --live
LIVE_PATHS = ["/", "/architecture", "/health", "/investors", "/government", "/security",
              "/partners", "/trust/", "/security-advisory/", "/sitemap.xml", "/robots.txt",
              "/api/status.json", "/.well-known/security.txt"]
LIVE_HEADERS = ["Strict-Transport-Security", "Content-Security-Policy", "X-Frame-Options",
                "X-Content-Type-Options", "Referrer-Policy", "Permissions-Policy"]

if "--live" in sys.argv:
    origin = CANON_HOST
    for i, a in enumerate(sys.argv):
        if a == "--live-origin" and i + 1 < len(sys.argv):
            origin = sys.argv[i + 1]
    import urllib.error
    import urllib.request

    req = urllib.request.Request(origin + "/", headers={"User-Agent": "elmahrosa-site-verify"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            hdrs, last_mod = resp.headers, resp.headers.get("Last-Modified", "")
            for h in LIVE_HEADERS:
                if h.lower() not in {k.lower() for k in hdrs}:
                    add("LIVE-HEADER", "FAIL", f"{origin}: {h} not returned by the server",
                        "the .htaccess header block is not in effect in production",
                        "enable mod_headers / set headers at the host, then re-check with curl -I")
            if last_mod:
                import datetime
                import email.utils
                try:
                    stamped = email.utils.parsedate_to_datetime(last_mod).date()
                    age = (datetime.date.today() - stamped).days
                    if age > 14:
                        add("LIVE-STALE", "FAIL", f"{origin}: last deployed build is {age} days old",
                            f"Last-Modified: {last_mod}", "re-deploy main; a git push does not deploy this site")
                except Exception:
                    pass
        for path in LIVE_PATHS:
            r = urllib.request.Request(origin + path, headers={"User-Agent": "elmahrosa-site-verify"})
            try:
                with urllib.request.urlopen(r, timeout=15) as resp:
                    code = resp.status
            except urllib.error.HTTPError as exc:
                code = exc.code
            except Exception:
                code = 0
            if code != 200:
                add("LIVE-ROUTE", "FAIL", f"{origin}{path} returned {code or 'no response'}",
                    "route is not served in production", "deploy the page or fix the rewrite rule")
    except Exception as exc:
        add("LIVE-UNREACHABLE", "INFO", f"{origin} could not be probed from here",
            f"{type(exc).__name__}: {str(exc)[:80]}",
            "run this check from a network that can reach the host")

# ---------------------------------------------------------------- report
order = {"FAIL": 0, "WARN": 1, "INFO": 2}
findings.sort(key=lambda f: (order[f["severity"]], f["id"]))
fails = [f for f in findings if f["severity"] == "FAIL"]
warns = [f for f in findings if f["severity"] == "WARN"]

if AS_JSON:
    print(json.dumps({"root": ROOT, "fails": len(fails), "warns": len(warns),
                      "findings": findings}, indent=2))
else:
    cur = None
    for f in findings:
        if f["severity"] != cur:
            cur = f["severity"]
            print(f"\n### {cur}")
        print(f"  [{f['id']}] {f['check']}")
        if f["detail"]:
            print(f"        {f['detail']}")
        if f["fix"]:
            print(f"        fix: {f['fix']}")
    print(f"\nsummary: {len(fails)} FAIL, {len(warns)} WARN across {len(html_files)} HTML files")

bad = len(fails) + (len(warns) if STRICT else 0)
sys.exit(1 if bad else 0)
