# TEOS SENTINEL SHIELD v5.0.0 — GA RELEASE NOTES

**Release Date:** July 15, 2026
**Tag:** `ecosystem-v5.0.0-ga`
**Status:** General Availability

---

## What's New

### Founding 10 Launch Promotion
First 10 paying customers receive **50% OFF** annual plans:
- **Pro Annual:** $245/yr (was $490/yr)
- **Team Annual:** $995/yr (was $1,990/yr)
- **Enterprise:** Contact Sales for Founding Partner Terms

### Sentinel Shield — GA Launch
TEOS Sentinel Shield is now **generally available**. Pre-execution AI security gateway enforcing 25 deterministic rules across three scan engines.

### Pricing via Dodo Payments
Self-serve checkout with 5 plans:
| Plan | Price | Billing |
|------|-------|---------|
| Pro Monthly | $49/mo | Monthly |
| Pro Annual | $245/yr (Founding 10) | Annual |
| Team Monthly | $199/mo | Monthly |
| Team Annual | $995/yr (Founding 10) | Annual |
| Enterprise | $45,000/yr | Annual |

### Website — 7 Production Pages
- **Homepage:** Hero, products, pricing, trust badges, GA badge
- **/architecture:** TEOS ecosystem diagram, product relationships
- **/health:** 6 product status cards with uptime bars
- **/investors:** Business model, ARR expansion path, Founding 10 note
- **/government:** TEOS for government deployment
- **/security:** 25 deterministic rules, 10 HTTP security headers
- **/partners:** 6 partner types (Implementation, Security, Government, Healthcare, Reseller, Enterprise)

### Bot — GA Pricing Update
- 9 commands: /start, /scan, /deps, /ci, /credits, /plans, /upgrade, /status, /help
- Plans display shows Founding 10 prices
- All Dodo Payments checkout links updated
- 50-credit gate removed from /deps and /ci (all paid plans access)

### Security Hardening
- 25 named MCP rules (SS-001 to SS-025)
- 10 HTTP security headers in vercel.json
- HMAC-signed audit trail
- Rate limiting and throttling
- Deterministic BLOCK/WARN/ALLOW verdicts

### Trust & Credibility
- Registered Member of Anthropic Claude Partner Network
- Sovereign AI Infrastructure badge
- MENA & Africa Focused badge
- Enterprise & Government Ready badge

---

## Bug Fixes
- Health dashboard: replaced "Cloud Console" with "TEOS Comply-Crawl" (6th product)
- Health dashboard: updated meta descriptions to list all 6 products
- All Railway references removed from teos-sentinel-stack (13 refs across 10 files)
- Repository references updated to canonical: `https://github.com/Elmahrosa/teos-sovereign-security-stack`

---

## Breaking Changes
None.

## Upgrade Path
N/A — this is the initial GA release.

---

## Repository

**Canonical:** `https://github.com/Elmahrosa/teos-sovereign-security-stack`
**Website:** `https://elmahrosa.org`
**Bot:** `https://t.me/teoslinker_bot`

## Tags
- `ecosystem-v5.0.0` — GA release
- `ecosystem-v5.0.0-ga` — Final launch tag

## Commits Included
- `b6441b6` — feat: Founding 10 launch promotion + health dashboard fix
- `9b8f5fc` — chore: update bot pricing to GA plans, remove all Railway links
- `bd0fa01` — release: ecosystem v5.0.0 GA
