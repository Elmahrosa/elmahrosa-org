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
| `audit-tools/` | `codex_audit.sh` repo-readiness scorer |
| `audits/`, `docs/`, `modules/` | Governance records and architecture docs |

## Local checks

Open `index.html` directly in a browser, or serve the folder:

```bash
python -m http.server 8080
```

## Content conventions

- Pages are bilingual (English + Arabic) via `data-en` / `data-ar` attributes.
- Canonical host: `https://elmahrosa.org/`.
- Open Graph images reference `/og-image.png`; PWA icons live in `/icons/`.
- Keep `sitemap.xml` and `robots.txt` in sync when adding indexable pages.

## Deploy

Push to `main`; the host picks up the static files. No build step.