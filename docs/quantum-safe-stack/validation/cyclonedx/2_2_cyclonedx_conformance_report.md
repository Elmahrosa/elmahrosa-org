# Milestone 2.2: CycloneDX 1.6 Conformance Validation Report

## Executive Summary

The Teos Quantum-Safe Stack CBOM schema has been validated for conformance with CycloneDX 1.6 specification. The validation confirms that the Teos CBOM mapping document (A3_CBOM_SCHEMA_SPEC.md) correctly maps Teos-specific fields to CycloneDX 1.6 standard fields while preserving the ability to extend with Teos-specific properties under a properly defined namespace. The sample CBOM documents demonstrate that when transformed to the CycloneDX 1.6 required property array format, the resulting CBOM is fully valid against the official CycloneDX 1.6 JSON schema. The hybrid algorithm representation approach uses CycloneDX's composition mechanism and extension properties as specified, maintaining schema validity.

## Validation of A3_CBOM_SCHEMA_SPEC.md against CycloneDX 1.6

The mapping document A3_CBOM_SCHEMA_SPEC.md provides a comprehensive mapping from Teos CBOM fields to CycloneDX 1.6 elements. Key observations:

- **Baseline**: The document correctly identifies CycloneDX 1.6 JSON as the baseline format, leveraging the `cryptographic-asset` component type.
- **Extension Mechanism**: The document specifies a proper extension namespace (`http://schemas.teos.example.com/cbom/1.0`) with prefix `teos` to maintain CycloneDX 1.6 validity.
- **Field Mapping**: All Teos CBOM root-level fields, assets array fields, gap analysis fields, and compliance references are mapped to appropriate CycloneDX 1.6 constructs (metadata, component properties, or standard fields).
- **Schema Validation Note**: The document explicitly states that the internal flat representation (used for Teos internal processing) is not valid as-is against CycloneDX 1.6 due to the `properties` field requiring an array of `{name, value}` objects. However, the documented transformation to the array form yields a valid CycloneDX 1.6 document.

## Check of Required Fields Mapping

CycloneDX 1.6 requires the following top-level fields:
- `bomFormat`: Mapped implicitly (hardcoded as "CycloneDX" in examples).
- `specVersion`: Mapped implicitly (hardcoded as "1.6").
- `version`: Mapped from `cbom_version` (mapped to `metadata.component.version` in the spec, though note: the examples show a separate `version` field at root; the spec could clarify this mapping).
- `metadata.timestamp`: Mapped from `generated_at`.
- `metadata.component`: Mapped from `scope.repo` (group), `scope.component` (name), and implicitly sets type and version.
- `components`: Mapped from the `assets` array, each as a `cryptographic-asset` type.

All required fields are accounted for in the mapping document or the example CBOMs. The spec's table for root-level fields shows mapping for `cbom_version` and `generated_at`, and `scope.repo` and `scope.component`. The `metadata.component.type` is not explicitly mapped in the root-level table but is present in the examples as "application". The spec notes that a fix was applied to add `metadata.component.type = "application"` to the example, and this should be reflected in the mapping guidance.

## Teos Extension Namespace Verification

The Teos extension namespace is properly defined and used:
- **Namespace URI**: `http://schemas.teos.example.com/cbom/1.0`
- **Prefix**: `teos`
- **Usage**: All Teos-specific fields appear under this namespace in the XML format or as prefixed properties in JSON (in the array form, as `{"name": "teos:<field>", "value": "..."}`).
- **Validation**: The extension schema `A3_TEOS_CBOM_EXTENSION.schema.json` validates the Teos-specific properties, confirming appropriate types and allowed values.

## Sample CBOM Validation Results

Two sample CBOM documents were validated:

1. **A3_CBOM_EXAMPLE.json** (internal Teos flat representation):
   - Format: Uses a flat map for `properties` (e.g., `"properties": { "teos:location": "value", ... }`).
   - Validation Result: **INVALID** against CycloneDX 1.6 schema (`bom-1.6.schema.json`) because CycloneDX 1.6 requires `properties` to be an array of objects with `name` and `value` fields.
   - Error: Validation fails on the `properties` field structure.

2. **A3_CBOM_EXAMPLE.cyclonedx-valid.json** (CycloneDX 1.6 compliant transformation):
   - Format: Transforms the flat `properties` map to the required array format (e.g., `"properties": [ {"name": "teos:location", "value": "value"}, ... ]`).
   - Validation Result: **VALID** against `bom-1.6.schema.json` (as confirmed by A3_VALIDATION_REPORT.md section 3).
   - Additional checks: All `bom-ref` values are unique, dependency/composition references resolve, and no cryptographic secrets are included.

The validation was performed using `ajv-cli` v5.0.0 against the official CycloneDX 1.6 JSON schema (locally pinned as `bom-1.6.schema.json`).

## Hybrid Representation Approach Validation

The hybrid algorithm representation approach, as specified in section "Quantum-Specific Extensions → Hybrid Algorithm Representation" of A3_CBOM_SCHEMA_SPEC.md, is validated as follows:

- **Composition Linkage**: Uses CycloneDX's `components` relationship mechanism via the `bom-ref` field to link assets.
- **Extension Property**: Represents hybrid relationships via the namespaced extension property `teos:hybridComponents`, which contains an array of subordinate asset `bom-ref` values.
- **Validation**: The validation report (A3_VALIDATION_REPORT.md section 3) confirms that all `hybridComponents` references point to existing `bom-ref` values in the sample CBOM, ensuring referential integrity.
- **Schema Validity**: The approach does not introduce any properties that violate CycloneDX 1.6 schema; the `teos:hybridComponents` property is validated as part of the Teos extension schema.

The example in the spec (lines 96-116) demonstrates a hybrid asset (TLS 1.3 Hybrid Key Exchange) with two subcomponents (X25519 and ML-KEM-768 key exchanges), correctly linked via `teos:hybridComponents`.

## Overall Assessment

Based on the validation evidence:

- The Teos CBOM mapping document correctly specifies how to map Teos CBOM to CycloneDX 1.6.
- All required CycloneDX 1.6 fields are present or properly mapped.
- The Teos extension namespace is properly defined and used, ensuring that extension fields do not conflict with standard fields.
- Sample CBOM documents, when transformed to the CycloneDX 1.6 required property array format, validate successfully against the official CycloneDX 1.6 schema.
- The hybrid algorithm representation approach maintains schema validity and uses CycloneDX mechanisms appropriately.

**Gate Status: PASS**

## Blocking Issues (if any)

None. The mapping document and sample CBOMs are conformant when the documented transformation to the CycloneDX 1.6 property array format is applied.

## Minor Issues (if any)

1. **Root-level `version` field mapping**: The mapping document maps `cbom_version` to `metadata.component.version`, but CycloneDX 1.6 also requires a root-level `version` field (as seen in the examples). The mapping document should explicitly note that the root-level `version` field is set to the CBOM version (or a fixed value like 1) and is distinct from the component version. However, the examples show a root-level `version` of 1, and the spec's example snippet includes it. This is a minor documentation clarification opportunity.

2. **Explicit `metadata.component.type` mapping**: The root-level mapping table does not include a mapping for `metadata.component.type`. The examples set this to "application", and the validation report notes that a fix was applied to add this field. The mapping document could add a row for setting the component type (perhaps from a fixed Teos context or via an extension property).

These minor issues do not affect the validity of the generated CBOMs when following the examples and the documented transformation.

## Recommendations

1. **Update the mapping document**: Clarify the root-level `version` field mapping and add explicit guidance for setting `metadata.component.type` (either as a fixed value or derivable from Teos context).
2. **Consider providing a transformation tool**: To assist users in converting the internal Teos flat representation to the CycloneDX 1.6 compliant array format, a simple transformation script or utility could be provided.
3. **Automate validation in CI**: Integrate the CBOM schema validation (using the CycloneDX 1.6 schema and the Teos extension schema) into the Teos Quantum-Safe Stack CI pipeline to ensure ongoing conformance.

---
*Validation completed as part of Milestone 2.2 for the Teos Quantum-Safe Stack.*