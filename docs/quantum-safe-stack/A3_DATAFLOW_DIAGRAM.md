# Quantum-Safe Cryptographic Data Flow Diagram

This diagram illustrates the data flow between the quantum-safe security stack components as defined in the validated A2 interfaces.

```mermaid
flowchart TD
    %% QRNG Flow
    subgraph QRNG["Quantum Random Number Generation (Teos-QRNG)"]
        direction TB
        QRNG_Start[Noise Source] --> QRNG_Cond[Conditioning Function<br/>(SHA-256/HMAC/CMAC/Hash_df)]
        QRNG_Cond --> QRNG_DRBG[SP 800-90A DRBG<br/>(Optional)]
        QRNG_DRBG --> QRNG_Output[Conditioned Entropy Output]
        QRNG_Start -->|Health Tests (≥1024 samples)| QRNG_Health[RCT/APT Tests]
        QRNG_Health -->|Pass/Fail| QRNG_State[Entropy Source State<br/>(ACTIVE/ERROR)]
        QRNG_State -->|Reset Required| QRNG_Start
    end

    %% PQC Key Generation
    subgraph PQC["Post-Quantum Cryptography (Teos-PQC)"]
        direction TB
        PQC_Input[Entropy Input<br/>(from QRNG_DRBG or QRNG_Output)] --> PQC_KeyGen[Key Generation<br/>(keypair() function)]
        PQC_KeyGen --> PQC_Output[Key Pair Output<br/>(public_key, private_key)]
        PQC_KeyGen --> PQC_Encap[Encapsulation<br/>(encapsulate() function)]
        PQC_Encap --> PQC_Encap_Output[Ciphertext + Shared Secret]
        PQC_KeyGen --> PQC_Decap[Decapsulation<br/>(decapsulate() function)]
        PQC_Decap_Input[Ciphertext + Private Key] --> PQC_Decap
        PQC_Decap --> PQC_Decap_Output[Shared Secret]
        PQC_KeyGen --> PQC_Sign[Signing<br/>(sign() function)]
        PQC_Sign_Input[Message + Private Key] --> PQC_Sign
        PQC_Sign --> PQC_Sign_Output[Signature]
        PQC_Sign_Verif[Verification<br/>(verify() function)] --> PQC_Sign
        PQC_Sign_Verif_Input[Message + Public Key + Signature] --> PQC_Sign_Verif
        PQC_Sign_Verif --> PQC_Sign_Verif_Output[Boolean Result]
    end

    %% QKD Flow
    subgraph QKD["Quantum Key Distribution (Teos-QKD)"]
        direction TB
        QKD_Start[Quantum Channel<br/>(Single-Photon Exchange)] --> QKD_Raw[Raw Key Material]
        QKD_Raw --> QKD_Error_Correction[Error Correction<br/>(Classical Channel)]
        QKD_Error_Correction --> QKD_Privacy_Amplification[Privacy Amplification<br/>(Classical Channel)]
        QKD_Privacy_Amplification --> QKD_Auth[Authentication<br/>(authenticate_channel() function)]
        QKD_Auth_Input[Peer Public Key + Local Secret Key] --> QKD_Auth
        QKD_Auth --> QKD_Auth_Output[Auth Token<br/>(Contains Session ID)]
        QKD_Auth_Output --> QKD_Exchange[Key Exchange<br/>(exchange_key() function)]
        QKD_Exchange --> QKD_Key_Output[Shared Key + Key ID + Metadata]
        QKD_Auth -->|Requires| QKD_PQC_Auth[ML-DSA (FIPS 204)<br/>Classical Channel Auth]
        QKD_PQC_Auth -->|Provides| QKD_PQC_Keys[PQC Key Pair<br/>(from Teos-PQC)]
    end

    %% Key Storage
    subgraph KeyStore["Key Storage & Management"]
        direction TB
        PQC_Output --> KeyStore_PQC[Store PQC Keys]
        QKD_Key_Output --> KeyStore_QKD[Store QKD Keys]
        KeyStore_PQC --> KeyStore_Index[Key Index<br/>(Handle-based lookup)]
        KeyStore_QKD --> KeyStore_Index
    end

    %% Orchestration Layer & CBOM Generation
    subgraph Orchestration["Teos-Orchestration-Layer"]
        direction TB
        Orchestration_Input[Key Material<br/>(from KeyStore)] --> Orchestration_CBOM[CBOM Generation<br/>(cbom_snapshot() function)]
        Orchestration_CBOM --> Orchestration_Output[CBOM Document<br/>(CycloneDX 1.6 compliant)]
        Orchestration_Reg[Algorithm Registration<br/>(register_algorithm() function)] --> Orchestration_Reg_Output[Algorithm Handle]
        Orchestration_Rotate[Key Rotation<br/>(rotate_key() function)] --> Orchestration_Rotate_Output[New Key ID]
        Orchestration_Reg --> Orchestration_Input
        Orchestration_Rotate --> KeyStore_Index
    end

    %% Styling
    classDef quantum fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef pqc fill:#fff3e0,stroke:#ef6c00,stroke-width:2px;
    classDef qkd fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px;
    classDef storage fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px;
    classDef orchestration fill:#fffde7,stroke:#f9a825,stroke-width:2px;

    class QRNG_Start,QRNG_Cond,QRNG_DRBG,QRNG_Output,QRNG_Health,QRNG_State quantum;
    class PQC_Input,PQC_KeyGen,PQC_Output,PQC_Encap,PQC_Encap_Output,PQC_Decap,PQC_Decap_Input,PQC_Decap_Output,PQC_Sign,PQC_Sign_Input,PQC_Sign_Output,PQC_Sign_Verif,PQC_Sign_Verif_Input,PQC_Sign_Verif_Output pqc;
    class QKD_Start,QKD_Raw,QKD_Error_Correction,QKD_Privacy_Amplification,QKD_Auth,QKD_Auth_Input,QKD_Auth_Output,QKD_Exchange,QKD_Key_Output,QKD_PQC_Auth,QKD_PQC_Keys qkd;
    class KeyStore_PQC,KeyStore_QKD,KeyStore_Index storage;
    class Orchestration_Input,Orchestration_CBOM,Orchestration_Output,Orchestration_Reg,Orchestration_Reg_Output,Orchestration_Rotate,Orchestration_Rotate_Output orchestration;

    %% Cross-connections
    QRNG_Output -->|Entropy Input| PQC_Input
    QRNG_DRBG -->|Entropy Input| PQC_Input
    QKD_PQC_Auth -.->|Uses| PQC_KeyGen
    QKD_PQC_Auth -.->|Uses| PQC_Sign
    Orchestration_CBOM -.->|Reads| KeyStore_Index
    Orchestration_Reg -.->|Registers| PQC_KeyGen
    Orchestration_Rotate -.->|Requests| KeyStore_Index
    Orchestration_Output -.->|Exported via| API[/cbom/snapshot Endpoint]

    %% Notes
    classDef note fill:#fafafa,stroke:#ccc,stroke-dasharray: 5 5,color:#666;
    class Note1,Note2,Note3 note;
    Note1["Note: All functions return Result<T, TeosError><br/>Stubs return NOT_IMPLEMENTED"]:::Note1
    Note2["Note: Error handling via shared COMMON-CONTRACT.md conventions"]:::Note2
    Note3["Note: No live cryptography - interface/stub only"]:::Note3
```

## Flow Descriptions

### 1. QRNG → DRBG → PQC Key Generation
- Quantum noise is harvested by the Teos-QRNG module
- Output passes through a vetted conditioning function (SP 800-90B compliant)
- Conditioned entropy feeds an SP 800-90A DRBG (optional but recommended)
- DRBG output is consumed by Teos-PQC for key generation operations
- Health tests (≥1024 samples via RCT/APT) run continuously per SP 800-90B
- Any test failure puts the entropy source in ERROR state

### 2. QKD → ML-DSA-Authenticated Channel → Key Store
- Quantum key exchange occurs via single-photon transmission
- Raw key material undergoes classical post-processing (error correction, privacy amplification)
- Classical channel must be authenticated using ML-DSA (FIPS 204) signatures
- Authentication requires local ML-DSA secret key and peer's ML-DSA public key
- Successful authentication enables secure key exchange via exchange_key() function
- Output is a shared key with identifier and metadata for storage

### 3. Orchestration → CBOM Generation
- Orchestration layer manages the complete lifecycle:
  - Algorithm registration via register_algorithm() function
  - Key rotation via rotate_key() function
  - CBOM generation via cbom_snapshot() function
- CBOM output follows CycloneDX 1.6 format with Teos extensions
- Generated CBOM includes gap analysis and compliance references
- Output is available via the /cbom/snapshot API endpoint

## Interface Contract References

All flows reference the validated A2 interface contracts:

- **Teos-QRNG**: `health_test()`, `get_entropy()`, `continuous_validation()`
- **Teos-PQC**: `keypair()`, `encapsulate()`, `decapsulate()`, `sign()`, `verify()`
- **Teos-QKD**: `authenticate_channel()`, `exchange_key()`
- **Teos-Orchestration-Layer**: `register_algorithm()`, `rotate_key()`, `cbom_snapshot()`

All functions follow the Result<T, TeosError> error model with TeosError including NOT_IMPLEMENTED for stub implementations.