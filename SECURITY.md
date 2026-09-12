# Security Policy — Elmahrosa International

This repository (`elmahrosa-org`) holds the **static institutional site** for Elmahrosa
International: marketing pages, the Trust Center, security advisories, and governance
documents. It ships no executable service — the products it describes live in other
repositories.

## Reporting a vulnerability

- **Email:** [ayman@elmahrosa.org](mailto:ayman@elmahrosa.org) — subject
  `Responsible Disclosure — [Product Name]`
- **Machine-readable contact:** [`/.well-known/security.txt`](https://elmahrosa.org/.well-known/security.txt)
- **Policy, response targets and safe-harbour statement:** [Trust Center §Vulnerability
  Reporting](https://elmahrosa.org/trust/#disclosure)

| Step | Commitment |
| --- | --- |
| Acknowledgement | within 48 hours |
| Initial severity assessment | within 7 business days |
| Confirmed critical fix | within 30 days where technically feasible |
| Public disclosure | affected customers within 72 hours of confirmation; public advisory within 7 days |

Do not open a public issue for anything exploitable. Use email; we will coordinate the
advisory and credit you in it if you want it.

## Scope

**In scope**

- `elmahrosa.org` and every page published from this repository.
- The TEOS products described here — Sentinel Shield, TEOS AI Engine, UCH Sovereign Core,
  TEOS Comply-Crawl, Agent Code Risk MCP — including their hosted demos and Telegram bot.

**Out of scope**

- Third-party services we do not operate (Dodo Payments checkout, Anthropic API, GitHub
  Actions runners, Hostinger or Vercel infrastructure).
- Social engineering of end users. See
  [ELM-SA-2026-001](https://elmahrosa.org/security-advisory/) for an example and how we
  handle it.

## Known limitations of this repo's hardening

Stated plainly, because the Trust Center promises honest disclosure:

- The site is static and has **no server-side input**, so injection classes do not apply,
  but the CSP still allows `'unsafe-inline'` for scripts and styles because pages carry
  inline blocks. Nonces or extracted files would remove that allowance.
- Security headers are declared in [`.htaccess`](.htaccess) and **are not verified in CI**.
  A Hostinger-side change or a disabled `mod_headers` silently removes all of them, which is
  exactly what the 2026-09-12 audit found in production. Check with
  `python3 audit-tools/site_verify.py --live` or `curl -sI https://elmahrosa.org/`.
- Deployment is manual. A commit to `main` does **not** publish the site; see
  [`FINAL_AUDIT_2026-09-12.md`](FINAL_AUDIT_2026-09-12.md) §P0-1.

## Publishing hygiene for this repository

Never commit secrets, tokens, webhooks, or customer data — including in governance
documents, audit logs, screenshots, and JSON fixtures. `api/status.json` and
`audit-data/*.jsonl` are generated artefacts; keep them free of credentials and internal
hostnames. Pre-commit check:

```bash
python3 audit-tools/site_verify.py          # includes a secret scanner
```

## Advisories

Published advisories for the wider ecosystem live at
[elmahrosa.org/security-advisory/](https://elmahrosa.org/security-advisory/) and use the
`ELM-SA-YYYY-NNN` identifier scheme.
