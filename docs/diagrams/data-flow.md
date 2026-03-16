# Data Flow Analysis

> How data flows through the CardDemo system — VSAM files, sequential files, and I/O patterns.

> **Total Files:** 0  
> **Total File Usages:** 0  
> **Programs with I/O:** 14

## Data Flow Diagram

```mermaid
graph LR

    classDef file fill:#E1BEE7,stroke:#6A1B9A,color:#000
```

## File Details

| File | Type | Organization | Programs | Access Modes |
|------|------|-------------|----------|--------------|

## I/O Statement Profile

| Program | READs | WRITEs | REWRITEs | OPENs | CLOSEs |
|---------|-------|--------|----------|-------|--------|
| [CBACT01C](../programs/CBACT01C.md) | 1 | 4 | 0 | 4 | 1 |
| [CBACT02C](../programs/CBACT02C.md) | 1 | 0 | 0 | 1 | 1 |
| [CBACT03C](../programs/CBACT03C.md) | 1 | 0 | 0 | 1 | 1 |
| [CBACT04C](../programs/CBACT04C.md) | 5 | 1 | 1 | 5 | 5 |
| [CBCUS01C](../programs/CBCUS01C.md) | 1 | 0 | 0 | 1 | 1 |
| [CBEXPORT](../programs/CBEXPORT.md) | 5 | 5 | 0 | 6 | 6 |
| [CBIMPORT](../programs/CBIMPORT.md) | 1 | 6 | 0 | 7 | 7 |
| [CBSTM03A](../programs/CBSTM03A.md) | 0 | 95 | 0 | 0 | 1 |
| [CBTRN01C](../programs/CBTRN01C.md) | 3 | 0 | 0 | 6 | 6 |
| [CBTRN02C](../programs/CBTRN02C.md) | 4 | 3 | 2 | 6 | 6 |
| [CBTRN03C](../programs/CBTRN03C.md) | 5 | 1 | 0 | 6 | 6 |
| [COBTUPDT](../programs/COBTUPDT.md) | 1 | 0 | 0 | 1 | 1 |
| [PAUDBLOD](../programs/PAUDBLOD.md) | 2 | 0 | 0 | 2 | 2 |
| [PAUDBUNL](../programs/PAUDBUNL.md) | 0 | 0 | 0 | 2 | 2 |

---

*Generated 2026-02-10 21:17*