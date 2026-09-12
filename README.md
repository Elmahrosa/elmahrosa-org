# elmahrosa-org

Static institutional website and publishing repo for **Elmahrosa International** (elmahrosa.org).

## Stack

Pure static HTML/CSS/JS — no build step, no framework, no runtime. Served directly by the web host
(Hostinger Apache) via `index.html` per directory. `api/status.json` is served as a static status
endpoint. `.htaccess` provides clean-URL rewrites and security headers.

## Structure

| Path | Purpose |
| --- | --- |
| `index.html` | Homepage — TEOS products, pricing, approach |
| `architecture/` | Platform architecture overview |
| `health/` | Service status dashboard (static) |
| `investors/` | Investor relations |
| `government/` | Government / public-sector offering |
| `security/` | Sentinel Shield security product page |
| `security-advisory/` | Security advisories (ELM-SA-* series) |
| `partners/` | Claude Partner Network page |
| `trust/` | Trust center — compliance, disclosure, procurement |
| `referral/` | CPN affiliate referral redirect (noindex) |
| `api/status.json` | Static status payload |
| `audit-tools/` | `codex_audit.sh` repo-readiness scorer; `site_verify.py` content checker |
| `404.html` | branded error page (`ErrorDocument 404`) |
| `SECURITY.md` | disclosure policy, scope, and known hardening limitations |
| `audits/`, `docs/`, `modules/` | Governance records and architecture docs |

## Local checks

Open `index.html` directly in a browser, or serve the folder:

```bash
python -m http.server 8080
python3 audit-tools/site_verify.py      # links, meta, i18n, data files, secrets, headers config
python3 audit-tools/site_verify.py --strict   # also fail on WARN

## Content conventions

- Bilingual (English + Arabic) via `data-en` / `data-ar` attributes **on `index.html`,
  `trust/` and `security-advisory/` only**; the six sub-pages are English-only and load no
  Arabic face. Either extend the switcher or keep the copy honest about the coverage.
- Canonical host: `https://elmahrosa.org/`.
- Open Graph images reference `/og-image.png`; PWA icons live in `/icons/`.
- Keep `sitemap.xml` and `robots.txt` in sync when adding indexable pages.

## Deploy

**There is no deploy automation in this repository.** Merging to `main` publishes only the
GitHub Pages dashboard (`docs/` → `elmahrosa.github.io/elmahrosa-org/`). The public site on
`elmahrosa.org` (Hostinger) is updated by a manual upload of the publish set, which is why the
2026-09-12 audit found production 113 days behind `main` with 6 of 8 sub-pages returning 404.

Publish set: the ten `index.html` pages + `404.html`, `icons/`, `og-image.png`, `logo.svg`,
`manifest.json`, `robots.txt`, `sitemap.xml`, `security.txt`, `.well-known/`, `api/`,
`.htaccess`. **Never** publish `docs/`, `audits/`, `audit-data/`, `audit-tools/`, `modules/`
(`.htaccess` blocks them as a second line of defence, but the upload should not include them).

Verify a deploy actually happened — from a machine that can reach the host:

```bash
python3 audit-tools/site_verify.py --live        # routes, headers, staleness
curl -sI https://elmahrosa.org/ | grep -i last-modified
for u in /health /architecture /api/status.json /sitemap.xml; do
  curl -so/dev/null -w"%{http_code} $u\n" https://elmahrosa.org$u
done
```