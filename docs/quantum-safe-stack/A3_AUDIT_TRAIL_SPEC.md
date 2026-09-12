# Tamper-Evident Audit Trail Specification

## Overview

This document specifies the tamper-evident audit trail format for the Teos Quantum-Safe Orchestration Layer. The audit trail implements an append-only, hash-chained event log aligned with NIST SP 800-57 Part 3 key management lifecycle states to ensure integrity and non-repudiation of cryptographic asset management operations.

## Design Principles

1. **Append-Only**: Events are only added; never modified or deleted
2. **Hash Chaining**: Each event includes a hash of the previous event
3. **Event Sequencing**: Monotonically increasing sequence numbers prevent replay attacks
4. **Lifecycle Alignment**: Events map to NIST SP 800-57 Part 3 key states
5. **Tamper Evidence**: Any modification breaks the hash chain
6. **Auditability**: Complete history of all cryptographic asset operations

## Event Structure

Each audit event follows this structure:

```json
{
  "event_id": "string (UUIDv4)",
  "sequence_number": "integer (monotonically increasing)",
  "timestamp": "string (ISO 8601)",
  "previous_event_hash": "string (hex-encoded SHA-256, null for genesis event)",
  "event_hash": "string (hex-encoded SHA-256 of this event excluding event_hash field)",
  "actor": {
    "user_id": "string",
    "session_id": "string",
    "ip_address": "string (optional)",
    "tenant_id": "string"
  },
  "event_type": "string (from enum)",
  "asset_id": "string (references cryptographic-asset bom-ref)",
  "asset_type": "string (algorithm|key|certificate|library|protocol)",
  "operation": "string (specific operation performed)",
  "payload": "object (operation-specific data)",
  "lifecycle_state": "string (NIST SP 800-57 Part 3 key state)",
  "tenant_context": {
    "isolation_level": "string (shared|dedicated|isolated)",
    "data_classification": "string (public|internal|confidential|restricted)",
    "purpose": "string (business justification)",
    "compliance_tags": "string[] (e.g., [\"PCI_DSS\", \"NIST_SP_1800_38\"])"
  }
}
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `event_id` | string (UUIDv4) | Unique identifier for the event |
| `sequence_number` | integer | Monotonically increasing counter starting at 1 |
| `timestamp` | string (ISO 8601) | When the event occurred |
| `previous_event_hash` | string (hex) | SHA-256 hash of the previous event's serialized form |
| `event_hash` | string (hex) | SHA-256 hash of this event (excluding this field) |
| `actor.user_id` | string | Identifier of the user/service performing the operation |
| `actor.session_id` | string | Session identifier for the operation |
| `actor.ip_address` | string (optional) | IP address of the actor |
| `actor.tenant_id` | string | Tenant identifier for multi-tenancy |
| `event_type` | string (enum) | Type of audit event |
| `asset_id` | string | Reference to the cryptographic asset involved |
| `asset_type` | string | Type of cryptographic asset |
| `operation` | string | Specific operation that was performed |
| `payload` | object | Operation-specific data (see event types below) |
| `lifecycle_state` | string | Current NIST SP 800-57 Part 3 key state |
| `tenant_context.isolation_level` | string | Tenant isolation level |
| `tenant_context.data_classification` | string | Sensitivity of data protected by the asset |
| `tenant_context.purpose` | string | Business justification for the operation |
| `tenant_context.compliance_tags` | string[] | Applicable compliance frameworks |

## Event Types and Payloads

### 1. Algorithm Registration
- **event_type**: `ALGORITHM_REGISTERED`
- **lifecycle_state**: `PRE-ACTIVATION` (NIST SP 800-57 Part 3)
- **payload**:
  ```json
  {
    "fips_id": "string (ML-KEM-768, ML-DSA-65, etc.)",
    "implementation": "string (implementation identifier)",
    "handle": "string (opaque reference for future use)",
    "algorithm_properties": {
      "security_level": "integer (1, 2, 3, 4, or 5)",
      "key_size_bits": "integer",
      "operation_types": "string[] (e.g., [\"KEY_GENERATION\", \"ENCAPSULATION\"])"
    }
  }
  ```

### 2. Key Registration (Import/Generation)
- **event_type**: `KEY_REGISTERED`
- **lifecycle_state**: `PRE-ACTIVATION`
- **payload**:
  ```json
  {
    "key_origin": "string (GENERATED|IMPORTED|DERIVED)",
    "generation_method": "string (optional, if GENERATED)",
    "import_source": "string (optional, if IMPORTED)",
    "key_attributes": {
      "algorithm": "string (FIPS identifier)",
      "key_size_bits": "integer",
      "key_usage": "string[] (e.g., [\"SIGNING\", \"KEY_AGREEMENT\"])"
    },
    "key_handle": "string (reference in key management system)"
  }
  ```

### 3. Key Activation
- **event_type**: `KEY_ACTIVATED`
- **lifecycle_state**: `ACTIVE`
- **payload**:
  ```json
  {
    "activation_time": "string (ISO 8601)",
    "activation_reason": "string (e.g., \"SCHEDULED\", \"ON_DEMAND\")",
    "activation_authority": "string (who/what authorized activation)"
  }
  ```

### 4. Key Rotation Initiation
- **event_type**: `KEY_ROTATION_INITIATED`
- **lifecycle_state**: `ACTIVE` (source key)
- **payload**:
  ```json
  {
    "rotation_reason": "string (e.g., \"SCHEDULED\", \"COMPROMISE_SUSPECTED\", \"ALGORITHM_DEPRECATION\")",
    "target_algorithm": "string (FIPS identifier for replacement)",
    "rotation_window_start": "string (ISO 8601)",
    "rotation_window_end": "string (ISO 8601, optional)"
  }
  ```

### 5. Key Rotation Completion
- **event_type**: `KEY_ROTATION_COMPLETED`
- **lifecycle_state**: 
  - Source key: `DEACTIVATED`
  - Target key: `ACTIVE`
- **payload**:
  ```json
  {
    "source_key_id": "string (original key identifier)",
    "target_key_id": "string (new key identifier)",
    "rotation_time": "string (ISO 8601)",
    "verification_method": "string (how rotation was verified)",
    "rollback_available": "boolean (whether rollback to source key is possible)"
  }
  ```

### 6. Key Deactivation
- **event_type**: `KEY_DEACTIVATED`
- **lifecycle_state**: `DEACTIVATED`
- **payload**:
  ```json
  {
    "deactivation_reason": "string (e.g., \"END_OF_LIFE\", \"SUPERSEDED\", \"COMPROMISED\")",
    "deactivation_time": "string (ISO 8601)",
    "grace_period_end": "string (ISO 8601, optional)",
    "destruction_scheduled": "string (ISO 8601, optional)"
  }
  ```

### 7. Key Destruction
- **event_type**: `KEY_DESTROYED`
- **lifecycle_state**: `DESTROYED`
- **payload**:
  ```json
  {
    "destruction_method": "string (e.g., \"ZEROIZATION\", \"SHREDDING\", \"INCINERATION\")",
    "destruction_time": "string (ISO 8601)",
    "verification_method": "string (how destruction was verified)",
    "witnesses": "string[] (optional, for physical destruction)"
  }
  ```

### 8. Key Compromise
- **event_type**: `KEY_COMPROMISED`
- **lifecycle_state**: `COMPROMISED`
- **payload**:
  ```json
  {
    "compromise_time": "string (ISO 8601, estimated if unknown)",
    "compromise_type": "string (e.g., \"KEY_EXFILTRATION\", \"WEAK_KEY_DETECTED\", \"SIDE_CHANNEL_LEAKAGE\")",
    "compromise_scope": "string (POSSIBLE|PROBABLE|CONFIRMED)",
    "impact_assessment": "string (description of potential impact)",
    "mitigation_actions": "string[] (actions taken in response)"
  }
  ```

### 9. CBOM Snapshot Generation
- **event_type**: `CBOM_GENERATED`
- **lifecycle_state**: `N/A` (CBOM is metadata, not a key)
- **payload**:
  ```json
  {
    "cbom_version": "string",
    "scope": {
      "repo": "string",
      "component": "string",
      "environment": "string (dev|staging|production)"
    },
    "asset_count": "integer",
    "quantum_vulnerable_count": "integer",
    "migration_ready_count": "integer",
    "generation_purpose": "string (e.g., \"COMPLIANCE_AUDIT\", \"RISK_ASSESSMENT\", \"MIGRATION_PLANNING\")",
    "retention_period": "string (ISO 8601 duration, optional)"
  }
  ```

### 10. CBOM Access
- **event_type**: `CBOM_ACCESSED`
- **lifecycle_state**: `N/A`
- **payload**:
  ```json
  {
    "access_reason": "string (e.g., \"AUDIT_REVIEW\", \"EXTERNAL_SHARE\", \"INTERNAL_REPORTING\")",
    "accessed_by": {
      "user_id": "string",
      "tenant_id": "string"
    },
    "access_method": "string (e.g., \"API\", \"UI\", \"EXPORT\")",
    "redaction_applied": "boolean (whether sensitive fields were redacted)",
    "redaction_level": "string (none|partial|full, if applied)",
    "access_duration_ms": "integer (optional)"
  }
  ```

### 11. Access Denied
- **event_type**: `ACCESS_DENIED`
- **lifecycle_state**: `N/A`
- **payload**:
  ```json
  {
    "attempted_operation": "string (what operation was attempted)",
    "reason": "string (e.g., \"INSUFFICIENT_PERMISSIONS\", \"INVALID_TENANT\", \"MFA_REQUIRED\")",
    "requested_by": {
      "user_id": "string",
      "tenant_id": "string"
    },
    "required_permissions": "string[] (what permissions were needed)",
    "timestamp": "string (ISO 8601)"
  }
  ```

## Hash Chain Implementation

### Hash Calculation
The `event_hash` is calculated as the SHA-256 hash of the event's JSON representation with the `event_hash` field omitted or set to null.

### Genesis Event
The first event in the chain (sequence_number = 1) has:
- `previous_event_hash`: `null`
- `event_hash`: Hash of the event with `previous_event_hash` as null and `event_hash` omitted

### Verification Process
To verify the integrity of the audit trail:
1. Start with the genesis event (sequence_number = 1)
2. Verify its `event_hash` matches the computed hash
3. For each subsequent event:
   - Verify `previous_event_hash` matches the `event_hash` of the previous event
   - Verify `sequence_number` is exactly one greater than the previous event
   - Verify the event's `event_hash` matches the computed hash
4. If any check fails, the trail is tampered with from that point forward

## Storage and Retention

### Storage Requirements
- **Immutability**: Events must be stored in write-once storage or append-only logs
- **Availability**: Audit trail must be available for the entire retention period
- **Backup**: Secure, encrypted backups must be maintained
- **Access Controls**: Strict access controls on both the audit trail and backup systems

### Retention Policy
- **Minimum Retention**: 7 years for financial and healthcare data (per common regulations)
- **Key Lifetime + 7 Years**: Retain events for the lifetime of the associated key plus 7 years
- **Legal Hold**: Events subject to legal hold must be retained until hold is released
- **Secure Disposal**: When retention expires, events must be destroyed using approved methods

## Integration with NIST SP 800-57 Part 3

The audit trail directly supports NIST SP 800-57 Part 3 key lifecycle management:

| NIST SP 800-57 Part 3 State | Corresponding Audit Events |
|-----------------------------|----------------------------|
| **PRE-ACTIVATION** | `ALGORITHM_REGISTERED`, `KEY_REGISTERED` |
| **ACTIVE** | `KEY_ACTIVATED`, `KEY_ROTATION_INITIATED` |
| **DEACTIVATED** | `KEY_ROTATION_COMPLETED` (source), `KEY_DEACTIVATED` |
| **DESTROYED** | `KEY_DESTROYED` |
| **COMPROMISED** | `KEY_COMPROMISED` |

## Implementation Notes

### Performance Considerations
- Hash computation adds minimal overhead (SHA-256 is fast)
- Append-only storage optimizes write performance
- Sequence number generation requires atomic operations or a centralized service

### Security Considerations
- Protect audit trail integrity with the same rigor as the cryptographic keys themselves
- Limit access to audit trail to authorized auditors and security personnel
- Consider transmitting audit events to a secure, centralized SIEM system
- Implement alerts for hash chain verification failures

### Compliance Mapping
This audit trail design supports:
- NIST SP 800-57 Part 3: Key management lifecycle tracking
- NIST SP 800-92: Security event logging guidance
- ISO 27001 A.12.4: Logging and monitoring
- PCI DSS Requirement 10: Track and monitor access to network resources and cardholder data
- HIPAA § 164.308(a)(1)(ii)(D): Audit controls
- GDPR Article 30: Records of processing activities

## Example Event Sequence

Here is an example of a complete key lifecycle:

```json
// Genesis Event (sequence_number: 1)
{
  "event_id": "00000000-0000-0000-0000-000000000000",
  "sequence_number": 1,
  "timestamp": "2026-09-12T00:00:00Z",
  "previous_event_hash": null,
  "event_hash": "a3f5c2e8b1d4f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
  "actor": { /* system initialization */ },
  "event_type": "SYSTEM_INITIALIZED",
  "asset_id": null,
  "asset_type": null,
  "operation": "system_startup",
  "payload": {},
  "lifecycle_state": null,
  "tenant_context": { /* system context */ }
}

// Key Registration (sequence_number: 2)
{
  "event_id": "11111111-1111-1111-1111-111111111111",
  "sequence_number": 2,
  "timestamp": "2026-09-12T10:00:00Z",
  "previous_event_hash": "a3f5c2e8b1d4f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
  "event_hash": "b4g6d3f9c2e5g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2",
  "actor": { /* admin user */ },
  "event_type": "KEY_REGISTERED",
  "asset_id": "tls-sign-key-001",
  "asset_type": "key",
  "operation": "key_generation",
  "payload": {
    "key_origin": "GENERATED",
    "generation_method": "ML-DSA-65 via SP 800-90A DRBG",
    "key_attributes": {
      "algorithm": "ML-DSA-65",
      "key_size_bits": 32256,
      "key_usage": ["SIGNING"]
    },
    "key_handle": "key_handle_tls_sign_001"
  },
  "lifecycle_state": "PRE-ACTIVATION",
  "tenant_context": { /* production tenant context */ }
}

// Key Activation (sequence_number: 3)
{
  "event_id": "22222222-2222-2222-2222-222222222222",
  "sequence_number": 3,
  "timestamp": "2026-09-12T10:05:00Z",
  "previous_event_hash": "b4g6d3f9c2e5g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2",
  "event_hash": "c5h7e4g0d3f6h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3",
  "actor": { /* automated system */ },
  "event_type": "KEY_ACTIVATED",
  "asset_id": "tls-sign-key-001",
  "asset_type": "key",
  "operation": "key_activation",
  "payload": {
    "activation_time": "2026-09-12T10:05:00Z",
    "activation_reason": "SCHEDULED",
    "activation_authority": "AUTOMATED_POLICY"
  },
  "lifecycle_state": "ACTIVE",
  "tenant_context": { /* production tenant context */ }
  }
```

## Validation Requirements

An audit trail is considered valid if and only if:
1. The genesis event exists with sequence_number = 1
2. For every event with sequence_number > 1:
   - `previous_event_hash` matches the `event_hash` of the event with sequence_number - 1
   - `sequence_number` is exactly one greater than the previous event's sequence number
3. For every event:
   - The `event_hash` matches the computed SHA-256 hash of the event (excluding the `event_hash` field)
4. All timestamps are in valid ISO 8601 format
5. All enumeration values are from the permitted sets
6. All required fields are present and non-null (where applicable)