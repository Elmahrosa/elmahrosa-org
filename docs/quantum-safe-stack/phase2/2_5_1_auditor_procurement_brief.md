# 2.5.1 — External Reviewer Procurement Brief (DRAFT — for candidate circulation)

**Status:** DRAFT — prepared 2026-09-13 for Founder circulation. Auditor **OUTSTANDING** — must be named by the Founder. This brief does not constitute the review and names no reviewer.

**Baseline under review:** A3 baseline `qss-a3-locked-r2` @ `5816117`; Phase 0 artifacts (`a1ca8dc`); Phase 1 acceptance (`dcc65b6`, accepted under Rule 6 2026-09-13).
**Companion paperwork:** `docs/quantum-safe-stack/phase2/2_5_external_review_engagement_draft.md`; `docs/quantum-safe-stack/M2_5_EXTERNAL_REVIEW_CHECKLIST.md`.
**Governance constraints (Rule 3, Rule 6, FINAL_ORDER.md §4):** Reviewer must be a **named, independent, real person/organization** with cryptographic engineering or applied security expertise. AI-authored auditor identities are prohibited. A **signed, dated deliverable** is required.

---

## 1. Why this review exists

Phase 2 (FINAL_ORDER.md §4) requires independent validation of the Teos Quantum-Safe Stack A3 baseline before any acceptance claim and before Phase 3. Internal reports 2.1–2.4 exist as committed drafts but are **not accepted**; external review (2.5) is the authoritative gate. This brief asks an independent party to validate the design, contracts, and evidence — not to audit live cryptographic operations (none exist today; all stubs return `NOT_IMPLEMENTED`).

## 2. Scope of the review

1. Cryptographic standards alignment: FIPS 203 / 204 / 205, SP 800-90B/C, SP 800-57 Pt 3, SP 1800-38 — verify interfaces reference applicable standards correctly.
2. Interface correctness and implementability of the A2 contract (`modules/quantum-safe/COMMON-CONTRACT.md`) and the Phase 1 stub implementations (contract-only; zero live crypto).
3. Security & privacy properties: fail-closed design, constant-time comparison expectations, secret zeroization, error-model consistency (`TeosError`).
4. Compliance mapping accuracy: TESL, EU AI Act Art. 50, NIST SP 800-53, PCI DSS, HIPAA, GDPR.
5. CBOM / CycloneDX 1.6 conformance and threat-model completeness (harvest-now-decrypt-later exposure).

**Out of scope:** live cryptographic operations (none implementable in Phase 1), deployment review, production readiness, performance benchmarking, and any Phase 3+ scope.

## 3. Required qualifications (selection criteria)

- Demonstrated cryptographic engineering or applied security expertise: published work, certifications (e.g., CISSP, SSCP, SANS GIAC cryptography track), or verifiable practitioner history.
- Independence from the authoring sessions; no prior AI-builder role in this repository.
- Availability to produce a **signed, dated deliverable** and to participate in one disposition exchange (Q&A on findings).
- No conflict of interest with Elmahrosa or the DealMaker codebase.

## 4. Evidence bundle (provided by Founder on selection)

| Evidence | Path |
|---|---|
| Program charter | `FINAL_ORDER.md` (includes Rule 1–6 and §4 gate) |
| Cryptography inventory (0.1) | `docs/quantum-safe-stack/inventory/0_1_current_crypto_inventory.md` |
| CBOM (0.2, schema-valid) | `docs/quantum-safe-stack/inventory/quantum-inventory.cbom.json` |
| Threat model (0.3) | `docs/quantum-safe-stack/A3_THREAT_MODEL.md` |
| A2 common contract | `modules/quantum-safe/COMMON-CONTRACT.md` |
| Phase 1 acceptance evidence | `docs/quantum-safe-stack/phase1_acceptance.md` |
| NIST alignment (2.1) | `docs/quantum-safe-stack/validation/nist/2_1_nist_alignment_report.md` |
| CycloneDX conformance (2.2) | `docs/quantum-safe-stack/validation/cyclonedx/2_2_cyclonedx_conformance_report.md` |
| Security properties (2.3) | `docs/quantum-safe-stack/validation/security/2_3_security_properties_report.md` |
| Compliance mapping (2.4) | `docs/quantum-safe-stack/validation/compliance/2_4_compliance_mapping_report.md` |
| Review checklist | `docs/quantum-safe-stack/M2_5_EXTERNAL_REVIEW_CHECKLIST.md` |

## 5. Deliverable required

A single PDF or Markdown report containing:

```
REVIEWER NAME / ORGANIZATION: <named auditor>
SIGNATURE: <dated signature>
BASELINE REVIEWED: <commit sha (must equal 5816117 for the r2 baseline)>
SCOPE: <per §2 above>
METHOD: <tools/procedures used>
FINDINGS: FEEDBACK-ID-XXX → ACCEPTED / CONDITIONAL / REJECTED (per scope area)
EVIDENCE CHECKLIST: <each §4 item confirmed present/reviewed, or NOT FOUND>
CONCLUSION: RECOMMEND ACCEPT / CONDITIONAL / NOT READY  [RECOMMEND ACCEPT]
```

Findings are entered into `docs/quantum-safe-stack/A3_FEEDBACK_AND_RESPONSES.md` for disposition (owner + deadline). **Critical** findings block Phase 2 closure per FINAL_ORDER.md §4 exit gate.

## 6. Engagement terms (to be confirmed by Founder)

- **Contact:** Foundation contracts via Founder (Elmahrosa-Teos); no agent negotiates on the Founder's behalf.
- **Confidentiality:** NDA covering repository contents and DealMaker internals is mandatory before evidence handover.
- **Timeline:** dated deliverable expected within 30 days of engagement confirmation (adjustable by Founder).
- **Compensation:** to be agreed between Founder and Reviewer; out of scope for this repository.

## 7. How to respond

Candidates respond to the Founder with:
1. CV / org profile and relevant qualifications (§3).
2. Independence and conflict-of-interest declaration.
3. Proposed deliverable date.
4. Fee quote (optional, Founder's preference).

Founder records the selected reviewer in `docs/quantum-safe-stack/phase2/2_5_external_review_engagement_draft.md` §6 and, per Rule 6, issues a dated instruction naming reviewer, scope, and deliverable deadline before any report is filed as evidence.

---

**Status:** 🔴 AUDITOR **OUTSTANDING**. Phase 2 remains IN PROGRESS — INTERNAL ONLY; no acceptance or completion claim is authorized until a named reviewer's signed, dated deliverable is on record and dispositioned.