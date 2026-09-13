# A3 SIGN-OFF — Quantum-Safe Stack CBOM API & Schema

> **Status: SIGNED — decisions D1–D3 ratified on 2026-09-13.**
> **Status (Phase 0 completion): RE-SIGNED 2026-09-13 after artifact commit `a1ca8dc`.** The original lightweight tag `qss-a3-locked` is retained per §7; it is superseded by the annotated tag `qss-a3-locked-r2` created on the sign-off commit.

Reviewed artifacts:
  A3_CBOM_API_OPENAPI.yaml          (OpenAPI 3.1, Redocly-validated)
  A3_CBOM_SCHEMA_SPEC.md            (CycloneDX 1.6 + Teos extension)
  A3_CBOM_EXAMPLE.json              (fixture; CycloneDX 1.6 schema run complete — valid via documented transform, see A3_VALIDATION_REPORT.md §3)
  A3_TEOS_CBOM_EXTENSION.schema.json (extension JSON Schema)
  A3_DATAFLOW_DIAGRAM.md            (Mermaid, cross-checked vs A2)
  A3_AUDIT_TRAIL_SPEC.md            (hash-chained, SP 800-57 Pt 3)
  A3_ACCESS_CONTROL_POLICY.md       (mTLS/OAuth2, RBAC, redaction)
  A3_IMPLEMENTATION_ROADMAP.md      (interface-only, 6-month phased)
  A3_VALIDATION_REPORT.md           (mechanical validation results)
  inventory/0_1_current_crypto_inventory.md   (evidence-based current-crypto inventory; commit `a1ca8dc`)
  inventory/quantum-inventory.cbom.json       (CycloneDX 1.6 CBOM of 0.1, schema-validated; commit `a1ca8dc`)
  A3_THREAT_MODEL.md                (quantum-capable adversary model T1–T8; commit `a1ca8dc`)

Reviewed commit (Phase 0 lock target):
  `a1ca8dc` — docs(qss): add Phase 0 artifacts 0.1-0.3 (crypto inventory, CBOM, threat model)

Founder decisions (ratified):
  D1  CycloneDX 1.6 native baseline          ✓
  D2  Hybrid via composition linkage          ✓
  D3  Append-only SP 800-57 audit events      ✓

A2 contract integrity: UNCHANGED
Live crypto: NONE
Open items: Rate-limit headers (post-sign-off enhancement); deployment TLS zone/cipher profile (Phase 3.3/3.4)

Signed: Elmahrosa-Teos    Date: 2026-09-13    Reviewed commit: a1ca8dc