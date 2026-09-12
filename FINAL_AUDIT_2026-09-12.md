# FINAL AUDIT & VERDICT — `elmahrosa-org`

| | |
| --- | --- |
| **Audit date** | 12 September 2026 |
| **Commit audited** | `72217ed1db4fb06ca4d680b359d6caffefcd432b` (main, + working tree on `arena/01a09559-elmahrosa-org`) |
| **Scope** | Every file in this repository (10 published pages, 34 markdown governance docs, 2 JSON schemas, 1 OpenAPI spec, JSONL audit data, `.htaccess`, `robots.txt`, `sitemap.xml`, manifest, icons, CI workflow, audit tooling) **and** the live properties it advertises: `elmahrosa.org`, `elmahrosa-org.vercel.app`, `sentinel.teosegypt.com`, the Dodo Payments checkouts, and the GitHub org metadata |
| **Method** | Deterministic static analysis (new `audit-tools/site_verify.py`), full-git-history credential scan, CycloneDX/OpenAPI schema runs, WCAG contrast maths against the actual CSS tokens, plus live probes of the production host, its headers, the checkout, and the product |
| **Supersedes** | `PRODUCTION_READINESS_REPORT.md` (2026-07-15, "PASS — ready for GA") and `FINAL_GA_READINESS_REPORT.md` (2026-07-16, "NO-GO") — both are wrong in places, see §C |

---

## 1. Verdict

> **NO-GO — as published.** Do not use either July report's conclusion, and do not cite
> this site as evidence of readiness in a procurement or investor reply until the four P0
> items below are closed.

> **GO-with-conditions — as a repository.** The repo itself is in good shape: no secrets in
> 39 commits of history, balanced markup on every page, every internal link and `#fragment`
> resolves, the pinned CycloneDX 1.6 schema is byte-identical to upstream, the CBOM fixture
> validates, the OpenAPI spec validates. The problem is **not** the code; it is that the repo
> is not what the world sees, and that three claims on the public site are not true.

**The single most important finding:** `elmahrosa.org` has not been redeployed since
**22 May 2026** (HTTP `Last-Modified: Fri, 22 May 2026 05:42:47 GMT`) — 113 days and 32
commits ago. Six of eight sub-pages, the sitemap and `api/status.json` **404 on the canonical
host**, and **every security header the repo declares is absent in production**. Both prior
reports assert the opposite because they audited the files, not the deployment.

### Composite score

| Dimension | Weight | Today | After P0 | After P0+P1 |
| --- | --- | --- | --- | --- |
| Repository integrity (secrets, markup, links, data, schema governance) | 15 | **92** | 92 | 95 |
| Content accuracy vs. reality (prices, products, statuses, claims) | 20 | **45** | 75 | 88 |
| Production deployment & availability | 20 | **15** | 90 | 92 |
| HTTP security posture (declared **and** applied) | 10 | **20** | 90 | 90 |
| Accessibility & bilingual coverage | 10 | **40** | 45 | 70 |
| SEO & indexability | 10 | **55** | 80 | 85 |
| Governance & CI process | 10 | **65** | 70 | 80 |
| Commercial readiness (checkout, pricing honesty) | 5 | **55** | 85 | 90 |
| **Weighted total** | 100 | **47 / 100** | **80 / 100** | **87 / 100** |

Weighted total = Σ (`score × weight ÷ 100`) over the eight rows, so no single dimension can
carry the result. Effort: **P0 ≈ one day** (one deploy, one header check at the host, one
pricing decision, one relabelled page); **P1 ≈ one week**.

---

## 2. P0 — blocking, fix before any readiness claim

### P0-1 · Production is a stale, partial copy of the repo
**Evidence**

```
GET https://elmahrosa.org/            200  Last-Modified: Fri, 22 May 2026 05:42:47 GMT
GET https://elmahrosa.org/health      404  ("This Page Does Not Exist" — Hostinger)
GET https://elmahrosa.org/architecture 404
GET https://elmahrosa.org/api/status.json 404
GET https://elmahrosa.org/sitemap.xml 404
GET https://elmahrosa.org/trust/      200  (serves the 22-May revision, not the repo's)
GET https://elmahrosa-org.vercel.app/ 200  (serves current main, incl. pricing + GA badges)
```
The live homepage still shows the pre-GA design (4 products, `teos-sentinel-shield.vercel.app`
links, no pricing table) while `main` has the 6-product GA page. `robots.txt` points
`Sitemap:` at a URL that 404s. Meanwhile `README.md` says *"Push to `main`; the host picks up
the static files. No build step."* — **there is no deploy pipeline in this repository at all**
(the only workflow is the weekly self-audit; GitHub Pages publishes `docs/` to
`elmahrosa.github.io/elmahrosa-org/`, a different host).

**Why it blocks:** every canonical URL in every page, the sitemap and the security.txt
`Canonical:` field point at `elmahrosa.org`. Search engines are being told to index pages
that 404, and the mirrored Vercel app is the only place the real content exists — with the
GitHub repo homepage metadata also pointing at Vercel. Institutional buyers who arrive from a
Google result or a link in an advisory get a 404.

**Fix (pick one, then make it automatic):**
1. **Recommended:** add a deploy job to Actions that `rsync`s the publish set to Hostinger on
   every merge to `main`, and only then update the README. The publish set should be the 10
   pages + `icons/` + `og-image.png` + `logo.svg` + `manifest.json` + `robots.txt` +
   `sitemap.xml` + `security.txt` + `.well-known/` + `.htaccess` + `api/` + `404.html` —
   explicitly **not** `docs/`, `audits/`, `audit-data/`, `audit-tools/`, `modules/`.
2. Or move the origin to Vercel (where main already builds), keep `elmahrosa.org` as a
   custom domain, and delete the half-deployed Hostinger copy. Then `.htaccess` becomes
   `_headers`/`vercel.json` — do not lose the header block in the move.

**Done when** `curl -sI https://elmahrosa.org/` shows a `Last-Modified` within one hour of the
merge, `for u in /health /architecture /api/status.json /sitemap.xml; do curl -so/dev/null -w'%{http_code} '$u'\n' https://elmahrosa.org$u; done`
returns `200 200 200 200`, and the Pages dashboard's `Audited …` timestamp equals the last
merge time.

### P0-2 · The security headers that both July reports marked "PASS" are not being served
**Evidence** — raw response for `https://elmahrosa.org/` (securityheaders.com, 12 Sep 2026,
grade **D**):

```
HTTP/2 200
content-security-policy: upgrade-insecure-requests   ← the only CSP present, injected by the host
server: hcdn / platform: hostinger
(no Strict-Transport-Security)  (no X-Frame-Options) (no X-Content-Type-Options)
(no Referrer-Policy)            (no Permissions-Policy) (no COOP/CORP)
```
`FINAL_GA_READINESS_REPORT.md` §Website Status and `PRODUCTION_READINESS_REPORT.md` §3 both
list HSTS, CSP, X-Frame-Options DENY, nosniff, Referrer-Policy, Permissions-Policy as ✓.
That is true of the file, not of the site. The most likely causes, in order: the current
`.htaccess` is not the one deployed (see P0-1); `mod_headers` is unavailable and the whole
block sits inside `<IfModule mod_headers.c>` so it **fails silently**; or `Header set` (which
this repo used) is being applied only to 2xx responses while the CDN serves a cached variant.

**Why it blocks:** the product being sold is *pre-execution security enforcement*, and the
Trust Center's §01 promise is that credentials and data never leave the customer's perimeter.
A marketing site for that company that is frameable, MIME-sniffable and reachable over plain
HTTP is the single most quotable line an adversary or a procurement reviewer can write.

**Fix:** the `.htaccess` in this branch is already rewritten for this (`Header always set`,
commented failure mode, dot-segment deny, `-Indexes`, 404 handler, compression, CSP with
`base-uri`/`form-action`/`upgrade-insecure-requests`). Deploy it, then verify from outside:

```bash
curl -sI https://elmahrosa.org/ | tr -d '\r' | grep -iE 'strict|content-security|x-frame|x-content|referrer|permissions'
python3 audit-tools/site_verify.py --live     # fails if any of the six headers is missing
```
If the host still strips them, set the headers in hPanel → *CDN / Security* (or disable the
CDN's header override) — `.htaccess` cannot win a fight with an edge that rewrites responses.

**Also:** HSTS is currently declared with `preload` while the site is not on the preload list
and subdomains may not be HTTPS-only. Keep `includeSubDomains` only after checking
`teosegypt.com`-style subdomains you do not control, and submit to preload only once the
redirect is proven.

### P0-3 · The advertised launch discount is not the discount the checkout applies
**Evidence** — the "Buy Now" buttons were followed to the live merchant of record:

| Site (before this audit) | Price on page | Checkout link resolves to | Live price |
| --- | --- | --- | --- |
| ~~Starter~~ Pro (monthly) | $69/mo | `dodo.pe/teos-starter-monthly-730161` → **TEOS SENTINEL — PRO (Monthly)**, `pdt_0NiubmCxvCi9MJbVfnJAT` | **$69.00/mo** ✓ |
| ~~Starter~~ Pro (annual) | ~~$690/yr~~ **$690/yr** + "Founding 10 · 50% Off First Year" | `dodo.pe/teos-starter-annual-730161` → **TEOS SENTINEL — PRO (Annual)** | **$690.00/yr** ✗ no 50 % applied |
| Team (monthly) | $199/mo | `dodo.pe/teos-sentinel-shield-team-monthly` | not verified in this audit |
| Team (annual) | ~~$1,990/yr~~ **$1,990/yr** + "Standard GA Pricing" | `dodo.pe/teos-team-annual-730161` | not verified in this audit |
| Enterprise | $45,000/yr | `mailto:sales@elmahrosa.org` | n/a |

Three separate defects in one card: the strikethrough "original" price **equals** the price
below it (so the row renders "50 % off" as `$690 → $690`); the tier is called "Starter" in the
hero and one card while the button's own product is "PRO"; and the only launch offer Dodo
actually applies is *"first 100 paid users get +200 bonus credits"*, not 50 % off the first
year for 10 customers.

**Two pages describe the same promotion incompatibly.** `index.html` sells it twice as
*"Founding 10: 50% OFF Annual Plans"* (hero ticker, ×2) and *"Founding 10 · 50% Off First Year"*
(the annual card), while `/investors` — line 222 — sells *"Founding 10: First 10 paying
customers receive custom onboarding and priority support. Annual plans (Pro Annual $690/yr, Team
Annual $1,990/yr) **save up to 17%** compared to monthly billing."* The 17 % figure is the one
the arithmetic supports ($69×12 = $828 vs $690 = 16.7 %; $199×12 = $2,388 vs $1,990 = 16.7 %),
and it is what the checkout actually charges. So the outlier is the homepage's "50%", not the
price list.

**Why it blocks:** this is the one class of finding that turns into chargebacks and, in the
EU/GCC consumer context, advertising complaints. It is also self-inflicted: `site_verify.py`
flags it in one second (`PROMO-NOT-APPLIED`).

**Fix (choose one, then verify at the checkout, not in the HTML):**
Either:
* honour the promo → create a 50 %-off first-year coupon/period in Dodo and show `$345/yr`
  under `$690/yr`; or
* describe what is actually true → *"Founding 10 · priority onboarding + ~17 % annual saving"*,
  delete both strikethroughs, and align `/investors` wording with it. If Dodo's "+200 bonus
  credits for the first 100 paid users" is the real launch offer, say that instead — it is a
  better offer than a phantom discount, and it is verifiable.
Either way: rename the two legacy `teos-starter-*` product slugs or add the `*-pro-*` links so
the slug, the card label, the Dodo product name and the JSON-LD all say **Pro**. Also verify
the Team links resolve to products at $199/$1,990 — they are the only unverified ones left.

### P0-4 · `/health` publishes operational numbers that no system produces
**Evidence:** `/health` says *"Real-time status of the Elmahrosa Open Stack"*,
`uptime 99.95%`, `avg latency 23ms`, per-service `100.00% / 99.97% / 99.99%`, deployment
versions (`3.2.0`, `2.8.3`, `1.6.1`, `1.2.0`, `2.4.0`), and *"Last incident: AI Engine
analytics delay — resolved 2026-07-10"*. The file contains **zero `<script>` tags**, no
`fetch()`, no data source. The only endpoint it could read, `api/status.json`, is a
hand-edited static file (`"updated": "2026-09-12T00:00:00Z"`, 3 services vs the 6 the page
lists) and is not deployed at all (P0-1). The July audit for the same date found 4 of 6
services failing their health checks — so the page reads "all systems operational" on the day
the org's own audit said the opposite.

**Why it blocks:** for a vendor whose differentiator is *"every AI verdict is logged,
timestamped and explainable — no black boxes"*, a fabricated status page is a direct
contradiction of the Trust Center, and it is the kind of thing a due-diligence engineer
notices first. Uptime and latency figures are also quasi-contractual: buyers quote status
pages back at you in SLA disputes.

**Fix, cheapest first:**
1. Relabel honestly today: *"Platform status — snapshot dated 2026-09-12, self-reported, not
   monitored"*, drop the invented uptime/latency/version rows or mark them `—`, and tag each
   line with your own capability tags (`Verified` / `Inferred` / `Speculative`).
2. Make it real: a 20-line scheduled workflow (`status.yml`) that probes each service's
   `/health` or `/live`, writes `api/status.json` + a 90-day history, and commits; the page
   then renders that file (your CSP's `connect-src 'self'` already allows it).
3. Add a status badge to the workflow so the page cannot silently go stale.

**Done when** every number on `/health` is either derived from the file it fetches or absent,
and `api/status.json` returns 200 with an `updated` timestamp < 15 minutes old.

---

## 3. P1 — accuracy and credibility (this week)

| # | Finding | Evidence | Recommended fix |
| --- | --- | --- | --- |
| P1-1 | The site describes a different product than the one you run | Site: *"25 deterministic rules across three scan engines, BLOCK/WARN/ALLOW, Sentinel Shield v5.0.0 GA"*. Product (`sentinel.teosegypt.com`): **121 governance controls, 6 engines, 4 verdicts** (Block/Warn/**Review**/Allow), `v4.0.0-rc1`, "RC Now Available · limited testers". Product Hunt says **27 rules**. Naming also drifts: "TEOS Sentinel Shield" vs "TEOS Sovereign Sentinel" | One canonical spec block, generated from the engine's own rule count, used by all pages + the bot + PH. Either say RC (and stop selling "GA"), or ship GA and update the product page. "GA" + "RC" in the same market week is the worst of both |
| P1-2 | A ghost product was advertised as Live | `/investors` listed **"Cloud Console — Live"** and `/architecture` twice, although `GA_RELEASE_NOTES.md` records it as *replaced*; `PRODUCTION_READINESS_REPORT.md` §5 claims "Zero fake product references" | **Applied in this branch:** ghost card replaced with the real TEOS Comply-Crawl; architecture node demoted to `Planned — Q1 2027`. Decide whether Cloud Console belongs on the roadmap at all |
| P1-3 | Text corrupted by an old global find/replace | `/investors`: "document **startercessing**", "**Starterfessional** Services" (from `Pro`→`Starter`) | **Applied** (restored "processing" / "Professional Services"). Then grep for the same rename damage elsewhere: `grep -rn -o -E "[a-z]starter[a-z]+|Starter[a-z]{3,}" --include=*.html .` |
| P1-4 | Product count contradicts itself page to page | `index.html`: "Live products **04**"; `/health`: "6 Products, **5 Live**, 1 Private Alpha"; `/government` and `/security` omit Comply-Crawl entirely; nav is 9 links on the homepage vs 7 on sub-pages | Publish a single "product roster" truth table (name, tier, status, GA date, link) and let it drive every page. **Needs your decision** — I did not guess which 4 or 5 are GA |
| P1-5 | Homepage links to GitHub repos that are not publicly resolvable | `teos-superintelligence`, `agent-code-risk-mcp`, `teoslinker-bot`, `safe-ingestion-engine`, `UCH-Backend`, `Unity-Care-Hospital` → 404 for anonymous visitors (org shows 24 public repos). `UnityCare-Platform`, `teos-ai-guard`, `teos-ai-engine`, `teos-compliance-kit` resolve | For each: rename the link to the live repo, or drop it. A security vendor whose "auditable, open source" links 404 is a self-inflicted wound. If they are private, remove "Open-source, auditable" from that card |
| P1-6 | Unverifiable scale claims in front of procurement reviewers | "71 repositories" (24 public, rest unprovable); "75+ **nations**" is Telegram-community reach presented as market reach (`index.html:1216` label says exactly that); `/partners` says "**certified partner** … combined ecosystem value exceeding $100M+" where the $100M+ is **Anthropic's** committed partner-programme fund from the homepage ticker | Apply your own §02 tagging: `Verified` = countable public evidence. Recount repos live (`gh api orgs/Elmahrosa/repos --jq length`), restate reach as "community in N countries", and move "$100M+" off the partners page or attribute it in the sentence |
| P1-7 | Membership wording differs | Homepage/topbar/JSON-LD: "Registered Member" / `memberOf`; `/partners`: "certified partner" | Use Anthropic's exact program wording in all four places, or drop the claim from `/partners` |
| P1-8 | Three contradictory readiness documents in-tree | `PRODUCTION_READINESS_REPORT.md`: 9/9 PASS, Pro $49/$490, `pdt_0NdjovMrD2e79VHGXwncS`. `FINAL_GA_READINESS_REPORT.md`: NO-GO, demands $49/$490. `RELEASE_NOTES_v5.0.0.md`: $49/mo, "$45,000 Enterprise", "Platform: Vercel Edge (auto-deploy from main)". Live checkout: **$69/$690**. All three reference `vercel.json`, which does not exist in this repo | **Applied in this branch:** each of the three now carries a `⚠ Historical record — superseded` banner plus a `site_verify:ignore PRICING-DIVERGENCE` marker, so the checker stops reporting corrected history as live drift while leaving the original text untouched. Move them to `audits/` if you want the repo root to hold only current documents. Note the $49 figure was *itself* the error: correcting the site to it would have broken pricing. **`site_verify.py` now enforces this** (`PRICING-DIVERGENCE`) |
| P1-9 | "Bilingual" is true for 3 of 10 pages | `data-en`/`data-ar` counts: `index.html` 139/139, `trust` 136/136, `security-advisory` 99/99 — the other 7 pages have **0**, don't load the Arabic font, and have no language switcher, while `README.md` states "Pages are bilingual" | Either ship the switcher on the 6 sub-pages (they share one CSS block — copy the `setLang` function + Noto Naskh font link) or state "English, with Arabic on the homepage, Trust Center and advisories" |
| P1-10 | A3 quantum-safe package: mechanically sound, but the docs overclaim two things | Verified ✓: `bom-1.6.schema.json`/`spdx`/`jsf-0.82` are **byte-identical to upstream** (git blob SHA-1 match against `CycloneDX/specification`); `A3_CBOM_EXAMPLE.cyclonedx-valid.json` is **VALID**; flat fixture fails on `properties` exactly as documented; OpenAPI 3.1 validates (`openapi-spec-validator`, 3 ops, unique ids). Overclaims: (a) `A3_TEOS_CBOM_EXTENSION.schema.json` validates 4/4 *flat* maps but **0/4** in the CycloneDX-conformant file — because CycloneDX property values must be strings, so `"256"` fails `type: integer`. Any CI that validates the conformant fixture against the extension schema will always fail. (b) `A3_VALIDATION_REPORT.md` §2 says "NOT_IMPLEMENTED maps to HTTP 501" — the spec declares only `200/400/401/403/500`; no 501 and no error→status mapping table exists | (a) give each extension property a `oneOf` that also accepts the stringified form (or declare the transform's coercion rules in `A3_CBOM_SCHEMA_SPEC.md` §Schema Validation). (b) add explicit `'501'` response objects with `ErrorResponse.code: NOT_IMPLEMENTED`, or downgrade the sentence to "not yet mapped". Both are 15-minute fixes; do them **before** the founder signs |
| P1-11 | Governance state is unsigned and the branch topology is confusing | `A3_FOUNDER_SIGN_OFF.md`: *"Status: DRAFT — awaiting founder signature"*, signature line blank; `A3_READINESS_REVIEW.md`: M2.5 external review, MAPI.6 idempotency, rate-limit headers all open, reviewer table empty. PR **#1** (open, `develop` → `main`, 17 files/+349, "mergeable: UNKNOWN") duplicates content already on `main`; branches `develop` and `feature/quantum-safe-stack-phase2` both live | Close or rebase PR #1 with a note, delete `feature/quantum-safe-stack-phase2`, and either sign off or record an explicit "deferred until M2.5" date. An unsigned "sign-off" file that is referenced as an assurance artefact is worse than no file |

---

## 4. P2 — quality (this month)

**Accessibility — WCAG 2.2 AA gaps on the three flagship pages.** Measured from the actual CSS
tokens against `--bg: #0a0d12`: `--text-muted: rgba(232,230,225,0.3)` = **2.34 : 1** (needs
4.5:1) and it is applied at `font-size: 0.58–0.68rem` ≈ **9.3–10.9 px** (`.product-status` pills, ticker and meta labels sit at 0.58–0.68rem); `--text-dim` = 5.22:1
(OK). The other pages' `#7a8299` = 5.08:1 (OK). `:focus-visible` styling exists on only 3 of
12 HTML files; no page has a skip link; 6 sub-pages put `role="menubar"`/`menuitem` on plain
nav links (the pattern requires arrow-key roving tabindex, so it currently *removes* native
semantics); emoji are used as badge icons without `aria-hidden`. Recommendation: raise the dim
token to `rgba(232,230,225,.62)` (≈4.6:1), floor body text at 0.78rem and any pill/label at 0.72rem, add one
`a:focus-visible{outline:2px solid var(--teal);outline-offset:2px}` rule to every page, delete
the `role=menubar` attributes (they buy nothing here), and add `<a class="skip" href="#main">`.
For a page whose stated audience is "institutional procurement review", EN-301-549/Section-508
equivalence is a stated expectation in many MENA tenders — this is cheap insurance.

**SEO / structured data.** `trust/` and `security-advisory/` lack `twitter:creator` and
`twitter:image` (the other pages have them). The `SoftwareApplication` JSON-LD offered
`"price": "0"` against a page selling $69/mo — **fixed to 69 with a `#pricing` URL**; consider
`OfferCatalog` with all five plans, and drop `"operatingSystem": "Telegram"` (it will not match
the rich-result category you want). `sitemap.xml` and `robots.txt` are consistent with the repo
(9 URLs, `/referral/` correctly excluded and `noindex`) — they are simply not deployed
(P0-1). Canonical tags correctly point at `elmahrosa.org` on the Vercel mirror, so duplicate
content is mitigated, but add `X-Robots-Tag: noindex` to the Vercel response if you keep both
hosts. `Cross-Origin-Resource-Policy: same-origin` on `og-image.png` is fine for crawlers
(server-side) but will break `<img>` embeds of your OG image from other sites — if that
matters, serve `og-image.png`/`icons/*` with `Cross-Origin-Resource-Policy: cross-origin`.

**`/referral` route.** JS-only redirect (no server 302), `console.log` of the affiliate id, and
`.htaccess` rewrites only `^referral$` (not `^referral/$`) — a trailing-slash share link
therefore depends on the directory index. `sessionStorage` attribution is written but nothing on
this site reads it. If CPN attribution is commercially live, it needs a first-party cookie
(with a consent note, since you serve no consent UI) or a server-side redirect, and the
`console.log` should go. Verified: it does not appear in the sitemap and is `noindex, nofollow` ✓.

**Performance.** Single-file pages, no build step: homepage 82 KB HTML + 9 Google-Font faces
(render-blocking `stylesheets`; `display=swap` is set ✓) + a Product Hunt iframe + an
`api.producthunt.com` badge image whose `post_id=teos-sovereign-sentinel` is a *slug* where the
embed API expects a numeric post id (`1151244`) — check that badge renders, it likely 404s.
`og-image.png` is 1200×630 as declared ✓, icons are 192/512 as the manifest says ✓, favicon
64×64 ✓. Add `preconnect` (present) plus `<link rel="preload" as="style">` for the font CSS,
self-host the two WOFF2 families to drop a third-party dependency (also removes
`fonts.googleapis.com` from your CSP), and gzip + `Expires` — **the compression/caching block
is now in `.htaccess`** since shared hosts won't do it unless asked.

**CI & the audit pipeline.** Fixed in this branch: `actions/checkout@v4` used its default
`fetch-depth: 1`, so `git rev-list --count --since="90 days ago"` could only ever see one commit
— `commits_90d: 1` in every archived record, `active_commits` permanently false, the 12-week
trajectory permanently flat, and the Pages dashboard's "Commits 90d" understating reality by
32× (verified: the true count today is **32**). Also fixed: `codex_audit.sh` never emitted
`generated_epoch`, although `docs/script.js` reads it, so "Audited …" was really "last pushed
…"; `has_security`/`has_contributing` were computed and then dropped (now reported, still
unscored); and the score counts "license ✓" from a file's existence while GitHub reports the
TESL custom license as `NOASSERTION` — an org-wide "licensed" score that treats a
source-available proprietary license identically to MIT is misleading, so the tier definition
should split `license: standard / custom / none`. Remaining: the workflow still `curl`s its own
script from `main` instead of running the checked-out copy (a truncated fetch can therefore run
a *different* auditor), the push token is inlined into the URL (documented trade-off in the
workflow comment), and `audit-self` runs only on a Monday cron — the data is up to 7 days stale
while the dashboard shows it as current; add `push: paths: [audit-tools/**]` plus a stale-data
warning in the UI.

**Repo hygiene.** Added in this branch: `SECURITY.md` (including the honest "known
limitations" section, because a security vendor with no SECURITY.md at repo root is a scoring
item in most questionnaires), `404.html`, and `audit-tools/site_verify.py`. Still worth adding:
`.github/CODEOWNERS`, an issue/PR template (the org-level `.github` repo may already supply
them — verify), and `audits/README.md` explaining the record format so future reports land in
one place. `manifest.json` `display: browser` → `standalone` if you want an installable PWA
(`.nojekyll`, icons and manifest are otherwise correct).

---

## 5. P3 — polish / backlog

1. `--text-dim`/`--text-muted`/`--muted` naming differs between page families (3 token sets, 2
   palettes: `#e8e6e1` vs `#d4d8e0`) → extract one shared `theme.css`; today the 6 sub-pages
   cannot be re-themed in one commit.
2. `.gitignore` lists `dist/` twice; `robots.txt`/`security.txt` lack trailing newlines
   (cosmetic, but `.well-known/security.txt` and root `security.txt` are byte-duplicates —
   generate one from the other so the `Expires: 2027-05-21` can't drift).
3. `docs/script.js`: `repoNameFromUrl()` is dead code; `error`/`empty` states never hide
   again after a successful retry; no `aria-live` on the status text.
4. `audit-tools/site_verify.py` currently reports `LIVE-UNREACHABLE` as INFO from this sandbox
   (no egress). Give it a GitHub-API-based fallback, or run the `--live` step from a self-hosted
   runner / a scheduled external probe (UptimeRobot-style) that opens an issue on drift — that
   single job would have caught P0-1 and P0-2 on 16 July.
5. `LICENSE` is non-standard (`TESL`, `NOASSERTION` on GitHub). Add
   `License-Identifier: TEOS-Egypt-Sovereign-1.0`-style text at the top plus the canonical URL
   (already present) so automated scanners can classify it, and add a short
   `LICENSE.faq.md` for procurement.
6. The A1/A2/A3 docs live both in `docs/quantum-safe-stack/` and `modules/quantum-safe/*/`;
   `COMMON-CONTRACT.md` is duplicated in spirit — pick one home and symlink in prose.

---

## 6. Verified clean — what this audit did *not* find

These were all run as explicit tests, so they are defensible in a questionnaire:

| Check | Result |
| --- | --- |
| Credential scan of the **full git history** (39 commits, every blob) — AWS/GitHub/Slack/OpenAI/Google/Telegram/JWT/PEM/URL-credential patterns + `*SECRET|TOKEN|PASSWORD|KEY|SALT =` assignments | **0 hits.** No `.env`, key or credential file has *ever* been committed here. The July secret findings concern other repos (bot/ingestion services), not this one |
| Working-tree secret scan (all text files, including the audit tooling itself) | 1 benign match: `AUTH="Authorization: …"` in `codex_audit.sh`, an env-var reference |
| HTML well-formedness, 12 pages | no unclosed/stray tags, no duplicate ids (post-fix), `<div>` balance verified on every touched file |
| Internal link integrity | every root path (`/health`, `/trust`, `/security-advisory`, …) and **every `#fragment`** — including 25 cross-page ones — resolves to an existing file and id |
| Canonical / OG / twitter metadata | canonical + `og:url` agree on all 9 indexable pages; `referral` intentionally `noindex, nofollow`, absent from the sitemap |
| `sitemap.xml` ↔ pages ↔ `robots.txt` | 9 URLs, exactly the indexable set; `/api/` disallowed |
| JSON / JSONL validity | `audit-data/latest.jsonl`, `docs/data/latest.jsonl` (identical to each other), `api/status.json`, `manifest.json`, both CBOM fixtures, `logo.svg` all parse |
| CycloneDX governance | all three pinned schemas **byte-identical to upstream** (`bom-1.6` blob `b6c096a9…` = upstream `b6c096a9…`); `A3_CBOM_EXAMPLE.cyclonedx-valid.json` **VALID** against official 1.6 (reproduced independently, not just trusted from the report); the flat fixture's 4 documented `properties` errors are exactly as described |
| OpenAPI | `A3_CBOM_API_OPENAPI.yaml`: 3.1.0, **valid**, 3 operations, unique `operationId`s, `mTLS`+`oauth2` schemes, no secret-returning endpoint; the "example.com server URLs" warnings are as documented |
| Placeholder / fake-product sweep | no `TODO`/`FIXME`/`Lorem ipsum`/`Coming Soon`/`TBD` anywhere (the "Cloud Console" issue was a *stale product*, not a placeholder — now fixed) |
| PWA + social assets | `manifest.json` icons 192/512 present at the declared sizes, `og-image.png` 1200×630 as declared in markup, favicon 64×64 |
| Mixed content | no `http://` resource references anywhere; the only `http://` strings are SVG/XML namespaces and a schema `$id` |
| Third-party surface | exactly 3 external origins (`fonts.googleapis.com`/`fonts.gstatic.com`, `cards.producthunt.com`/`api.producthunt.com`, `cdn.jsdelivr.net` on the internal dashboard) — none on the public pages beyond fonts/PH, no analytics, no trackers, no cookies (the doubleclick noise in the live 404 screenshots comes from the *auditor's* browser, not your site) |
| GitHub repo state | `open_issues: 0` (the 1 in `open_issues_count` is the PR), not archived, default branch `main`, Pages publishing healthy (last run success, ~2 h ago) |

---

## 7. Applied in this audit

Content and config fixes that were **unambiguous defects** (each verified by re-running the
checker; nothing here changes a price, a promotion or a product-status claim):

| File | Change |
| --- | --- |
| `.htaccess` | rewritten: `Header always set` (headers survive 404/5xx), `Options -Indexes -MultiViews`, dot-segment deny with `/.well-known/` re-opened, 404s for `/audit-data/`, `/audit-tools/`, `/audits/`, `/docs/`, `ErrorDocument 404 /404.html`, `mod_deflate` + `mod_expires`, CSP extended with `base-uri 'self'`, `form-action 'self'`, `upgrade-insecure-requests`, `X-XSS-Protection` removed (deprecated, re-enables legacy filters), rewrites added for `/trust` and `/security-advisory`, and a comment block explaining the silent-`IfModule` failure mode with the verification command |
| `index.html` | Arabic hero price `٤٩$` → `٦٩$` (it contradicted the English `$69` and the real checkout); `Starter` → `Pro` in the hero CTA, card 2's tier and its copy (the button's own product is "TEOS SENTINEL — PRO"); broken Arabic `"-alpha خاصة"` → `"ألفا خاصة"`; untranslated `validate` in the hero sub → `التحقق من`; added the `#trust-badges-heading` that `aria-labelledby` referenced but that did not exist; JSON-LD `offers.price` `0` → `69` with `category`/`url` |
| `investors/index.html` | repaired `document startercessing` → `processing` and `Starterfessional Services` → `Professional Services`; ghost "Cloud Console — Live" card → the real TEOS Comply-Crawl card; `Starter` → `Pro` in the ACV stat, SaaS list, promo sentence and ARR path |
| `architecture/index.html` | "Elmahrosa Cloud Console" demoted `Live` → `Planned — Q1 2027`; the "Agent Code Risk MCP → Cloud Console" card rewritten to describe the audit trail and say the console is not offered today |
| `security/index.html` | CTA tier `Starter` → `Pro` (prices untouched) |
| `docs/index.html` | Chart.js moved out of `<head>` to the end of `<body>`, `<noscript>` fallback, SRI command documented inline |
| `audit-tools/site_verify.py` | **new** — 12 HTML files, 30+ deterministic checks, stdlib-only, `--json` / `--strict` / `--live` |
| `audit-tools/codex_audit.sh` | emits `generated_epoch`; reports `has_security_policy` + `has_contributing`; documents the `fetch-depth` dependency in the header |
| `.github/workflows/audit.yml` | `fetch-depth: 0`, `concurrency`, `timeout-minutes: 10`, advisory `site_verify.py` step whose tail lands in the run summary, and a warning when `main`'s script differs from the checked-out copy |
| `SECURITY.md`, `404.html` | **new** |
| `audits/2026-09-12-final-audit.json` | **new** — machine-readable findings + the external evidence (live route matrix, checkout receipts, header list, schema hashes) for this audit |

Deliberately **not** changed, because they are decisions rather than defects: the plan prices and
the 50 %-off/`Founding 10` promo wording; the "Live products 04" vs "5 Live" count; the
"GA RELEASE — JULY 2026" badges; the 25-rules / 3-engines / GA-vs-RC product wording;
`audit-data/*.jsonl` (left for CI — a local run could not reach `api.github.com` from this
sandbox and would have written a degraded record); and the two superseded July reports and the July release
notes (kept verbatim as history; annotated with a superseded banner and a
`site_verify:ignore PRICING-DIVERGENCE` marker so the checker treats them as records).

Re-run everything with:

```bash
python3 audit-tools/site_verify.py            # 3 FAIL, 5 WARN remain — all listed in §3–§4
python3 audit-tools/site_verify.py --strict    # also fail on WARN
python3 audit-tools/site_verify.py --json | jq '.findings[] | select(.severity=="FAIL")'
python3 audit-tools/site_verify.py --live      # run from a network that can reach the host
```

---

## 8. Recommended plan

**Today (blocking, ~1 day total)**
1. Deploy `main` to the canonical host and prove it: `Last-Modified` fresh, `/health`,
   `/architecture`, `/api/status.json`, `/sitemap.xml` all 200. *(30 min, deploy access)*
2. Confirm the six security headers actually appear on `elmahrosa.org` and on a **404**
   response; if the edge strips them, set them in hPanel. *(30 min)*
3. Choose the promo answer — honour 50 % at Dodo or fix the copy — and verify by opening the
   checkout, not the HTML. Verify the two Team links while you are there. *(15 min + Dodo)*
4. Relabel `/health` honestly today (snapshot + capability tags, no invented uptime); open a
   follow-up issue for the real status job. *(1 h)*

**This week**
5. Sync the product spec: one source for rules/engines/verdicts/version/GA-vs-RC, then
   propagate to `index.html`, `security`, `health`, the bot, and the PH copy. *(2 h)*
6. Fix the GitHub links that 404 and the scale claims (§3 P1-5, P1-6); add the repo-count
   command to the checklist so it stays true. *(1 h)*
7. Supersede the two July reports with a banner; keep this file as the single current one.
   *(20 min)*
8. A3 before signature: extension-schema `oneOf` for stringified CycloneDX values, explicit
   `501` responses (or drop the mapping claim), then founder signature + a date for M2.5. *(2 h)*
9. Close/rebase PR #1, delete the stale `feature/quantum-safe-stack-phase2` branch. *(15 min)*

**This month**
10. Accessibility pass (contrast token, 0.78rem floor, focus-visible, drop `role=menubar`,
    skip links). *(0.5 day)*
11. Bilingual coverage decision for the 6 sub-pages. *(0.5 day)*
12. Real status pipeline (`status.yml` → `api/status.json` + history) and an external
    `site_verify.py --live` probe that opens an issue on drift. *(1 day)*

**Acceptance criteria for "GO"** — all of these, run by a third party, not self-attested:
```
[ ] curl -sI https://elmahrosa.org/ | grep -i last-modified     → < 1 h old
[ ] every canonical URL in the sitemap returns 200 on the canonical host
[ ] all six headers present on both / and a deliberately missing path (404)
[ ] python3 audit-tools/site_verify.py --live → 0 FAIL
[ ] each visible price == the price rendered by its own checkout page (screenshot in audits/)
[ ] /health numbers derived from api/status.json; status.json updated < 15 min ago
[ ] "Verified/Probable/Inferred/Speculative" tag applied to every countable claim on index,
    partners, government — and each Verified one has a public link
[ ] no readiness document in-tree disagrees with another about price, roster or status
```

---

## Appendix A — external evidence collected

| Probe | Result |
| --- | --- |
| `GET elmahrosa.org/` | 200, `last-modified: Fri, 22 May 2026 05:42:47 GMT`, `platform: hostinger`, `server: hcdn`, `x-hcdn-cache-status: DYNAMIC`, only `content-security-policy: upgrade-insecure-requests` |
| `GET elmahrosa.org/health`, `/architecture`, `/api/status.json`, `/sitemap.xml` | **404** (Hostinger "This Page Does Not Exist") |
| `GET elmahrosa.org/.htaccess` | 403 — good, host-protected |
| `GET elmahrosa.org/audit-data/latest.jsonl` | 404 (repo scaffolding not exposed today) |
| `GET elmahrosa.org/trust/`, `/security-advisory/` | 200, but 22-May revisions (trust page shows "Last updated: 22 May 2026" and a 10-section set that differs from the repo's) |
| `GET elmahrosa-org.vercel.app/` | 200, **matches current `main`** incl. pricing table + GA badges (this is why the mirror looks fine and the canonical host does not) |
| `securityheaders.com` scan | grade **D**; missing HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy |
| `dodo.pe/teos-starter-monthly-730161` | → `checkout.dodopayments.com/session/…` "TEOS SENTINEL — PRO (Monthly)" **$69.00/mo**, product `pdt_0NiubmCxvCi9MJbVfnJAT`, "+200 bonus credits, first 100 paid users" |
| `dodo.pe/teos-starter-annual-730161` | → "TEOS SENTINEL — PRO (Annual)" **$690.00/yr**, `pdt_0NiubmDStYOWzNVUkcFC8` — **no discount applied** |
| `sentinel.teosegypt.com/` | 200: "v4.0.0-rc1 · Sentinel Engine v4.0.0", **121 Active Governance Controls**, **6 scan engines**, **4 verdicts** (Block/Warn/Review/Allow), "596/596 tests passing", "RC Now Available · Limited testers" |
| Product Hunt `teos-sovereign-sentinel` | exists, 2 followers, copy says **27 rules**, 142 scans, 19 blocked |
| `gh api orgs/Elmahrosa/repos` | **24 public repos**; 6 homepage repo links not publicly resolvable |
| GitHub Pages | `elmahrosa.github.io/elmahrosa-org/data/latest.jsonl` 200, served by the `docs/` source, last build ~2 h ago |
| Audit history | `audit-data/archive/*.jsonl`: score 75 → 85 after the LICENSE commit; **`commits_90d` is 1 in every single record** → confirms the shallow-checkout bug |

## Appendix B — methodology & limitations

Static analysis ran in the sandbox against this working tree: `site_verify.py` (markup, ids,
links/fragments, meta/i18n parity, sitemap, JSONL, secret regexes, `.htaccess` assertions,
price/promo/status cross-file consistency), a full-history blob scan (39 commits),
`jsonschema` (Draft-07) runs for the CBOM and the Teos extension, `openapi-spec-validator` for
the A3 API, WCAG relative-luminance maths on the real CSS custom properties, and `git`/`gh api`
for repo and org metadata.

Limitations, stated because this report is meant to be quotable: **(1)** the sandbox had no
direct egress to `elmahrosa.org`/`dodo.pe`/`sentinel.teosegypt.com`, so live checks were made
through the page-fetch path and a public header-scanning service rather than raw `curl`;
the header finding rests on the scanner's raw-header dump, which is worth re-confirming with
`curl -sI` from your own terminal. **(2)** Private GitHub repos are indistinguishable from
deleted ones for an unauthenticated visitor — that is precisely what a buyer sees, but it means
"not publicly resolvable" ≠ "does not exist". **(3)** The Team-plan checkouts and the Product
Hunt embed were not opened in this pass; they are listed as unverified rather than assumed OK.
**(4)** No service-side health of the TEOS products was probed from here, so §P0-4 relies on the
site's own contradiction and the July audit, not on a fresh probe. **(5)** `api.github.com`
returned 401 for the unauthenticated path used by `codex_audit.sh` in this sandbox, which is
why no audit data was regenerated.

## Appendix C — how this report reconciles the two July reports

`PRODUCTION_READINESS_REPORT.md` (15 Jul) and `FINAL_GA_READINESS_REPORT.md` (16 Jul) disagree
with each other on the launch decision, and each disagrees with today's tree:

* **Both right:** this repo carries no secrets; the July secret exposure was in the bot /
  ingestion / activation services. That remains an open item *there*, and until a rotation
  receipt exists for those `BOT_TOKEN` / `*_WEBHOOK_SECRET` / `*_SALT` values, the Trust Center
  §03 disclosure promise is the place to record it.
* **Both wrong:** the security-headers "PASS" (P0-2) and "7 pages / consistent nav" (nav is
  9 links on the homepage vs 7 on sub-pages, and 3 more pages exist since).
* **Wrong in a way that mattered:** the July NO-GO demanded pricing be changed from $69/$690 to
  $49/$490. The live merchant of record charges **$69/$690**, so that instruction would have
  broken the price shown to buyers. `RELEASE_NOTES_v5.0.0.md` still contains the $49/$490
  table and the "Vercel Edge (auto-deploy from main)" deployment note — neither is true.
* **Still outstanding from the July NO-GO:** the two service-level items (health endpoints
  returning 404/502; missing lint scripts; test timeouts) belong to other repositories and
  were not re-checked here — carry them into that repo's own audit rather than closing them on
  the strength of this one.

---

*Machine-readable findings: [`audits/2026-09-12-final-audit.json`](audits/2026-09-12-final-audit.json) —
3 open FAIL, 5 WARN, plus the evidence above. Re-verify with
`python3 audit-tools/site_verify.py --json`.*
