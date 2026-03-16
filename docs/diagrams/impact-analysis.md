# Impact Analysis

> For each program: what happens if you change it? Who is affected?
> Covers **direct calls**, **transitive dependencies**, and **data coupling** through shared copybooks/files.

## Impact Summary

| Program | Type | Direct Callers | Transitive Callers | Direct Callees | Transitive Callees | Copybook Coupling |
|---------|------|---------------|-------------------|----------------|-------------------|-------------------|
| [00220000](../programs/00220000.md) | ONLINE | 0 | 0 | 0 | 0 | 20 |
| [CBACT01C](../programs/CBACT01C.md) | BATCH | 0 | 0 | 0 | 0 | 13 |
| [CBACT02C](../programs/CBACT02C.md) | BATCH | 0 | 0 | 0 | 0 | 9 |
| [CBACT03C](../programs/CBACT03C.md) | BATCH | 0 | 0 | 0 | 0 | 13 |
| [CBACT04C](../programs/CBACT04C.md) | BATCH | 0 | 0 | 0 | 0 | 18 |
| [CBCUS01C](../programs/CBCUS01C.md) | BATCH | 0 | 0 | 0 | 0 | 9 |
| [CBEXPORT](../programs/CBEXPORT.md) | BATCH | 0 | 0 | 0 | 0 | 24 |
| [CBIMPORT](../programs/CBIMPORT.md) | BATCH | 0 | 0 | 0 | 0 | 24 |
| [CBPAUP0C](../programs/CBPAUP0C.md) | BATCH | 0 | 0 | 0 | 0 | 7 |
| [CBSTM03A](../programs/CBSTM03A.md) | BATCH | 0 | 0 | 0 | 0 | 15 |
| [CBSTM03B](../programs/CBSTM03B.md) | BATCH | 0 | 0 | 0 | 0 | 0 |
| [CBTRN01C](../programs/CBTRN01C.md) | BATCH | 0 | 0 | 0 | 0 | 24 |
| [CBTRN02C](../programs/CBTRN02C.md) | BATCH | 0 | 0 | 0 | 0 | 18 |
| [CBTRN03C](../programs/CBTRN03C.md) | BATCH | 0 | 0 | 0 | 0 | 16 |
| [COACCT01](../programs/COACCT01.md) | ONLINE | 0 | 0 | 0 | 0 | 14 |
| [COACTUPC](../programs/COACTUPC.md) | ONLINE | 0 | 0 | 0 | 0 | 32 |
| [COACTVWC](../programs/COACTVWC.md) | ONLINE | 0 | 0 | 0 | 0 | 33 |
| [COADM01C](../programs/COADM01C.md) | ONLINE | 0 | 0 | 0 | 0 | 20 |
| [COBIL00C](../programs/COBIL00C.md) | ONLINE | 0 | 0 | 0 | 0 | 31 |
| [COBSWAIT](../programs/COBSWAIT.md) | BATCH | 0 | 0 | 0 | 0 | 0 |
| [COBTUPDT](../programs/COBTUPDT.md) | DB2 | 0 | 0 | 0 | 0 | 0 |
| [COCRDLIC](../programs/COCRDLIC.md) | ONLINE | 0 | 0 | 0 | 0 | 24 |
| [COCRDSLC](../programs/COCRDSLC.md) | ONLINE | 0 | 0 | 0 | 0 | 26 |
| [COCRDUPC](../programs/COCRDUPC.md) | ONLINE | 0 | 0 | 0 | 0 | 26 |
| [CODATE01](../programs/CODATE01.md) | ONLINE | 0 | 0 | 0 | 0 | 2 |
| [COMEN01C](../programs/COMEN01C.md) | ONLINE | 0 | 0 | 0 | 0 | 20 |
| [COPAUA0C](../programs/COPAUA0C.md) | ONLINE | 0 | 0 | 0 | 0 | 25 |
| [COPAUS0C](../programs/COPAUS0C.md) | ONLINE | 0 | 0 | 0 | 0 | 38 |
| [COPAUS1C](../programs/COPAUS1C.md) | ONLINE | 0 | 0 | 0 | 0 | 26 |
| [COPAUS2C](../programs/COPAUS2C.md) | ONLINE | 0 | 0 | 0 | 0 | 7 |
| [CORPT00C](../programs/CORPT00C.md) | ONLINE | 0 | 0 | 0 | 0 | 26 |
| [COSGN00C](../programs/COSGN00C.md) | ONLINE | 0 | 0 | 0 | 0 | 20 |
| [COTRN00C](../programs/COTRN00C.md) | ONLINE | 0 | 0 | 0 | 0 | 26 |
| [COTRN01C](../programs/COTRN01C.md) | ONLINE | 0 | 0 | 0 | 0 | 26 |
| [COTRN02C](../programs/COTRN02C.md) | ONLINE | 0 | 0 | 0 | 0 | 31 |
| [COTRTLIC](../programs/COTRTLIC.md) | ONLINE | 0 | 0 | 0 | 0 | 24 |
| [COUSR00C](../programs/COUSR00C.md) | ONLINE | 0 | 0 | 0 | 0 | 20 |
| [COUSR01C](../programs/COUSR01C.md) | ONLINE | 0 | 0 | 0 | 0 | 20 |
| [COUSR02C](../programs/COUSR02C.md) | ONLINE | 0 | 0 | 0 | 0 | 20 |
| [COUSR03C](../programs/COUSR03C.md) | ONLINE | 0 | 0 | 0 | 0 | 20 |
| [CSUTLDTC](../programs/CSUTLDTC.md) | BATCH | 0 | 0 | 0 | 0 | 0 |
| [DBUNLDGS](../programs/DBUNLDGS.md) | BATCH | 0 | 0 | 0 | 0 | 7 |
| [PAUDBLOD](../programs/PAUDBLOD.md) | BATCH | 0 | 0 | 0 | 0 | 7 |
| [PAUDBUNL](../programs/PAUDBUNL.md) | BATCH | 0 | 0 | 0 | 0 | 7 |

## Highest Impact Programs

> Changing these programs has the widest ripple effect.

### COPAUS0C — N/A

- **Risk Level:** 🔴 **HIGH** (38 programs affected)
- **Type:** ONLINE
- **Copybook Coupling:** 00220000, CBACT01C, CBACT02C, CBACT03C, CBACT04C, CBCUS01C, CBEXPORT, CBIMPORT, CBPAUP0C, CBSTM03A, CBTRN01C, CBTRN02C, CBTRN03C, COACCT01, COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC, COCRDSLC, COCRDUPC, COMEN01C, COPAUA0C, COPAUS1C, COPAUS2C, CORPT00C, COSGN00C, COTRN00C, COTRN01C, COTRN02C, COTRTLIC, COUSR00C, COUSR01C, COUSR02C, COUSR03C, DBUNLDGS, PAUDBLOD, PAUDBUNL

### COACTVWC — N/A

- **Risk Level:** 🔴 **HIGH** (33 programs affected)
- **Type:** ONLINE
- **Copybook Coupling:** 00220000, CBACT01C, CBACT02C, CBACT03C, CBACT04C, CBCUS01C, CBEXPORT, CBIMPORT, CBSTM03A, CBTRN01C, CBTRN02C, CBTRN03C, COACCT01, COACTUPC, COADM01C, COBIL00C, COCRDLIC, COCRDSLC, COCRDUPC, COMEN01C, COPAUA0C, COPAUS0C, COPAUS1C, CORPT00C, COSGN00C, COTRN00C, COTRN01C, COTRN02C, COTRTLIC, COUSR00C, COUSR01C, COUSR02C, COUSR03C

### COACTUPC — N/A

- **Risk Level:** 🔴 **HIGH** (32 programs affected)
- **Type:** ONLINE
- **Copybook Coupling:** 00220000, CBACT01C, CBACT03C, CBACT04C, CBCUS01C, CBEXPORT, CBIMPORT, CBSTM03A, CBTRN01C, CBTRN02C, CBTRN03C, COACCT01, COACTVWC, COADM01C, COBIL00C, COCRDLIC, COCRDSLC, COCRDUPC, COMEN01C, COPAUA0C, COPAUS0C, COPAUS1C, CORPT00C, COSGN00C, COTRN00C, COTRN01C, COTRN02C, COTRTLIC, COUSR00C, COUSR01C, COUSR02C, COUSR03C

### COBIL00C — N/A

- **Risk Level:** 🔴 **HIGH** (31 programs affected)
- **Type:** ONLINE
- **Copybook Coupling:** 00220000, CBACT01C, CBACT03C, CBACT04C, CBEXPORT, CBIMPORT, CBSTM03A, CBTRN01C, CBTRN02C, CBTRN03C, COACCT01, COACTUPC, COACTVWC, COADM01C, COCRDLIC, COCRDSLC, COCRDUPC, COMEN01C, COPAUA0C, COPAUS0C, COPAUS1C, CORPT00C, COSGN00C, COTRN00C, COTRN01C, COTRN02C, COTRTLIC, COUSR00C, COUSR01C, COUSR02C, COUSR03C

### COTRN02C — N/A

- **Risk Level:** 🔴 **HIGH** (31 programs affected)
- **Type:** ONLINE
- **Copybook Coupling:** 00220000, CBACT01C, CBACT03C, CBACT04C, CBEXPORT, CBIMPORT, CBSTM03A, CBTRN01C, CBTRN02C, CBTRN03C, COACCT01, COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC, COCRDSLC, COCRDUPC, COMEN01C, COPAUA0C, COPAUS0C, COPAUS1C, CORPT00C, COSGN00C, COTRN00C, COTRN01C, COTRTLIC, COUSR00C, COUSR01C, COUSR02C, COUSR03C

### COCRDSLC — N/A

- **Risk Level:** 🔴 **HIGH** (26 programs affected)
- **Type:** ONLINE
- **Copybook Coupling:** 00220000, CBACT02C, CBCUS01C, CBEXPORT, CBIMPORT, CBTRN01C, COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC, COCRDUPC, COMEN01C, COPAUA0C, COPAUS0C, COPAUS1C, CORPT00C, COSGN00C, COTRN00C, COTRN01C, COTRN02C, COTRTLIC, COUSR00C, COUSR01C, COUSR02C, COUSR03C

### COCRDUPC — N/A

- **Risk Level:** 🔴 **HIGH** (26 programs affected)
- **Type:** ONLINE
- **Copybook Coupling:** 00220000, CBACT02C, CBCUS01C, CBEXPORT, CBIMPORT, CBTRN01C, COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC, COCRDSLC, COMEN01C, COPAUA0C, COPAUS0C, COPAUS1C, CORPT00C, COSGN00C, COTRN00C, COTRN01C, COTRN02C, COTRTLIC, COUSR00C, COUSR01C, COUSR02C, COUSR03C

### COPAUS1C — N/A

- **Risk Level:** 🔴 **HIGH** (26 programs affected)
- **Type:** ONLINE
- **Copybook Coupling:** 00220000, CBPAUP0C, COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC, COCRDSLC, COCRDUPC, COMEN01C, COPAUA0C, COPAUS0C, COPAUS2C, CORPT00C, COSGN00C, COTRN00C, COTRN01C, COTRN02C, COTRTLIC, COUSR00C, COUSR01C, COUSR02C, COUSR03C, DBUNLDGS, PAUDBLOD, PAUDBUNL

### CORPT00C — N/A

- **Risk Level:** 🔴 **HIGH** (26 programs affected)
- **Type:** ONLINE
- **Copybook Coupling:** 00220000, CBACT04C, CBEXPORT, CBIMPORT, CBTRN01C, CBTRN02C, CBTRN03C, COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC, COCRDSLC, COCRDUPC, COMEN01C, COPAUS0C, COPAUS1C, COSGN00C, COTRN00C, COTRN01C, COTRN02C, COTRTLIC, COUSR00C, COUSR01C, COUSR02C, COUSR03C

### COTRN00C — N/A

- **Risk Level:** 🔴 **HIGH** (26 programs affected)
- **Type:** ONLINE
- **Copybook Coupling:** 00220000, CBACT04C, CBEXPORT, CBIMPORT, CBTRN01C, CBTRN02C, CBTRN03C, COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC, COCRDSLC, COCRDUPC, COMEN01C, COPAUS0C, COPAUS1C, CORPT00C, COSGN00C, COTRN01C, COTRN02C, COTRTLIC, COUSR00C, COUSR01C, COUSR02C, COUSR03C

### COTRN01C — N/A

- **Risk Level:** 🔴 **HIGH** (26 programs affected)
- **Type:** ONLINE
- **Copybook Coupling:** 00220000, CBACT04C, CBEXPORT, CBIMPORT, CBTRN01C, CBTRN02C, CBTRN03C, COACTUPC, COACTVWC, COADM01C, COBIL00C, COCRDLIC, COCRDSLC, COCRDUPC, COMEN01C, COPAUS0C, COPAUS1C, CORPT00C, COSGN00C, COTRN00C, COTRN02C, COTRTLIC, COUSR00C, COUSR01C, COUSR02C, COUSR03C

### COPAUA0C — N/A

- **Risk Level:** 🔴 **HIGH** (25 programs affected)
- **Type:** ONLINE
- **Copybook Coupling:** CBACT01C, CBACT03C, CBACT04C, CBCUS01C, CBEXPORT, CBIMPORT, CBPAUP0C, CBSTM03A, CBTRN01C, CBTRN02C, CBTRN03C, COACCT01, COACTUPC, COACTVWC, COBIL00C, COCRDSLC, COCRDUPC, CODATE01, COPAUS0C, COPAUS1C, COPAUS2C, COTRN02C, DBUNLDGS, PAUDBLOD, PAUDBUNL

### CBEXPORT — N/A

- **Risk Level:** 🔴 **HIGH** (24 programs affected)
- **Type:** BATCH
- **Copybook Coupling:** CBACT01C, CBACT02C, CBACT03C, CBACT04C, CBCUS01C, CBIMPORT, CBSTM03A, CBTRN01C, CBTRN02C, CBTRN03C, COACCT01, COACTUPC, COACTVWC, COBIL00C, COCRDLIC, COCRDSLC, COCRDUPC, COPAUA0C, COPAUS0C, CORPT00C, COTRN00C, COTRN01C, COTRN02C, COTRTLIC

### CBIMPORT — N/A

- **Risk Level:** 🔴 **HIGH** (24 programs affected)
- **Type:** BATCH
- **Copybook Coupling:** CBACT01C, CBACT02C, CBACT03C, CBACT04C, CBCUS01C, CBEXPORT, CBSTM03A, CBTRN01C, CBTRN02C, CBTRN03C, COACCT01, COACTUPC, COACTVWC, COBIL00C, COCRDLIC, COCRDSLC, COCRDUPC, COPAUA0C, COPAUS0C, CORPT00C, COTRN00C, COTRN01C, COTRN02C, COTRTLIC

### CBTRN01C — N/A

- **Risk Level:** 🔴 **HIGH** (24 programs affected)
- **Type:** BATCH
- **Copybook Coupling:** CBACT01C, CBACT02C, CBACT03C, CBACT04C, CBCUS01C, CBEXPORT, CBIMPORT, CBSTM03A, CBTRN02C, CBTRN03C, COACCT01, COACTUPC, COACTVWC, COBIL00C, COCRDLIC, COCRDSLC, COCRDUPC, COPAUA0C, COPAUS0C, CORPT00C, COTRN00C, COTRN01C, COTRN02C, COTRTLIC


## Per-Program Impact Details

### [00220000](../programs/00220000.md)

- **Data-coupled via copybooks** (`COCOM01Y`, `COTRTUP`, `COTTL01Y`, `CSDAT01Y`, `CSMSG01Y`, `CSMSG02Y`, `CSSETATY`, `CSUSR01Y`, `CVCRD01Y`, `DFHAID`, `DFHBMSCA`): [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)

### [CBACT01C](../programs/CBACT01C.md)

- **Data-coupled via copybooks** (`CODATECN`, `CVACT01Y`): [CBACT04C](../programs/CBACT04C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBSTM03A](../programs/CBSTM03A.md), [CBTRN01C](../programs/CBTRN01C.md), [CBTRN02C](../programs/CBTRN02C.md), [COACCT01](../programs/COACCT01.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COBIL00C](../programs/COBIL00C.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [COTRN02C](../programs/COTRN02C.md)

### [CBACT02C](../programs/CBACT02C.md)

- **Data-coupled via copybooks** (`CVACT02Y`): [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBTRN01C](../programs/CBTRN01C.md), [COACTVWC](../programs/COACTVWC.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COPAUS0C](../programs/COPAUS0C.md), [COTRTLIC](../programs/COTRTLIC.md)

### [CBACT03C](../programs/CBACT03C.md)

- **Data-coupled via copybooks** (`CVACT03Y`): [CBACT04C](../programs/CBACT04C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBSTM03A](../programs/CBSTM03A.md), [CBTRN01C](../programs/CBTRN01C.md), [CBTRN02C](../programs/CBTRN02C.md), [CBTRN03C](../programs/CBTRN03C.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COBIL00C](../programs/COBIL00C.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [COTRN02C](../programs/COTRN02C.md)

### [CBACT04C](../programs/CBACT04C.md)

- **Data-coupled via copybooks** (`CVACT01Y`, `CVACT03Y`, `CVTRA01Y`, `CVTRA02Y`, `CVTRA05Y`): [CBACT01C](../programs/CBACT01C.md), [CBACT03C](../programs/CBACT03C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBSTM03A](../programs/CBSTM03A.md), [CBTRN01C](../programs/CBTRN01C.md), [CBTRN02C](../programs/CBTRN02C.md), [CBTRN03C](../programs/CBTRN03C.md), [COACCT01](../programs/COACCT01.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COBIL00C](../programs/COBIL00C.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [CORPT00C](../programs/CORPT00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md)

### [CBCUS01C](../programs/CBCUS01C.md)

- **Data-coupled via copybooks** (`CVCUS01Y`): [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBTRN01C](../programs/CBTRN01C.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md)

### [CBEXPORT](../programs/CBEXPORT.md)

- **Data-coupled via copybooks** (`CVACT01Y`, `CVACT02Y`, `CVACT03Y`, `CVCUS01Y`, `CVEXPORT`, `CVTRA05Y`): [CBACT01C](../programs/CBACT01C.md), [CBACT02C](../programs/CBACT02C.md), [CBACT03C](../programs/CBACT03C.md), [CBACT04C](../programs/CBACT04C.md), [CBCUS01C](../programs/CBCUS01C.md), [CBIMPORT](../programs/CBIMPORT.md), [CBSTM03A](../programs/CBSTM03A.md), [CBTRN01C](../programs/CBTRN01C.md), [CBTRN02C](../programs/CBTRN02C.md), [CBTRN03C](../programs/CBTRN03C.md), [COACCT01](../programs/COACCT01.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [CORPT00C](../programs/CORPT00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md)

### [CBIMPORT](../programs/CBIMPORT.md)

- **Data-coupled via copybooks** (`CVACT01Y`, `CVACT02Y`, `CVACT03Y`, `CVCUS01Y`, `CVEXPORT`, `CVTRA05Y`): [CBACT01C](../programs/CBACT01C.md), [CBACT02C](../programs/CBACT02C.md), [CBACT03C](../programs/CBACT03C.md), [CBACT04C](../programs/CBACT04C.md), [CBCUS01C](../programs/CBCUS01C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBSTM03A](../programs/CBSTM03A.md), [CBTRN01C](../programs/CBTRN01C.md), [CBTRN02C](../programs/CBTRN02C.md), [CBTRN03C](../programs/CBTRN03C.md), [COACCT01](../programs/COACCT01.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [CORPT00C](../programs/CORPT00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md)

### [CBPAUP0C](../programs/CBPAUP0C.md)

- **Data-coupled via copybooks** (`CIPAUDTY`, `CIPAUSMY`): [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [COPAUS2C](../programs/COPAUS2C.md), [DBUNLDGS](../programs/DBUNLDGS.md), [PAUDBLOD](../programs/PAUDBLOD.md), [PAUDBUNL](../programs/PAUDBUNL.md)

### [CBSTM03A](../programs/CBSTM03A.md)

- **Data-coupled via copybooks** (`COSTM01`, `CUSTREC`, `CVACT01Y`, `CVACT03Y`): [CBACT01C](../programs/CBACT01C.md), [CBACT03C](../programs/CBACT03C.md), [CBACT04C](../programs/CBACT04C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBTRN01C](../programs/CBTRN01C.md), [CBTRN02C](../programs/CBTRN02C.md), [CBTRN03C](../programs/CBTRN03C.md), [COACCT01](../programs/COACCT01.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COBIL00C](../programs/COBIL00C.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [COTRN02C](../programs/COTRN02C.md)

### [CBTRN01C](../programs/CBTRN01C.md)

- **Data-coupled via copybooks** (`CVACT01Y`, `CVACT02Y`, `CVACT03Y`, `CVCUS01Y`, `CVTRA05Y`, `CVTRA06Y`): [CBACT01C](../programs/CBACT01C.md), [CBACT02C](../programs/CBACT02C.md), [CBACT03C](../programs/CBACT03C.md), [CBACT04C](../programs/CBACT04C.md), [CBCUS01C](../programs/CBCUS01C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBSTM03A](../programs/CBSTM03A.md), [CBTRN02C](../programs/CBTRN02C.md), [CBTRN03C](../programs/CBTRN03C.md), [COACCT01](../programs/COACCT01.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [CORPT00C](../programs/CORPT00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md)

### [CBTRN02C](../programs/CBTRN02C.md)

- **Data-coupled via copybooks** (`CVACT01Y`, `CVACT03Y`, `CVTRA01Y`, `CVTRA05Y`, `CVTRA06Y`): [CBACT01C](../programs/CBACT01C.md), [CBACT03C](../programs/CBACT03C.md), [CBACT04C](../programs/CBACT04C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBSTM03A](../programs/CBSTM03A.md), [CBTRN01C](../programs/CBTRN01C.md), [CBTRN03C](../programs/CBTRN03C.md), [COACCT01](../programs/COACCT01.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COBIL00C](../programs/COBIL00C.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [CORPT00C](../programs/CORPT00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md)

### [CBTRN03C](../programs/CBTRN03C.md)

- **Data-coupled via copybooks** (`CVACT03Y`, `CVTRA03Y`, `CVTRA04Y`, `CVTRA05Y`, `CVTRA07Y`): [CBACT03C](../programs/CBACT03C.md), [CBACT04C](../programs/CBACT04C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBSTM03A](../programs/CBSTM03A.md), [CBTRN01C](../programs/CBTRN01C.md), [CBTRN02C](../programs/CBTRN02C.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COBIL00C](../programs/COBIL00C.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [CORPT00C](../programs/CORPT00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md)

### [COACCT01](../programs/COACCT01.md)

- **Data-coupled via copybooks** (`03500000`, `CMQGMOV`, `CMQMDV`, `CMQODV`, `CMQPMOV`, `CMQTML`, `CMQV`, `CVACT01Y`, `REPLACING`): [CBACT01C](../programs/CBACT01C.md), [CBACT04C](../programs/CBACT04C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBSTM03A](../programs/CBSTM03A.md), [CBTRN01C](../programs/CBTRN01C.md), [CBTRN02C](../programs/CBTRN02C.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COBIL00C](../programs/COBIL00C.md), [CODATE01](../programs/CODATE01.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [COTRN02C](../programs/COTRN02C.md)

### [COACTUPC](../programs/COACTUPC.md)

- **Data-coupled via copybooks** (`COACTUP`, `COCOM01Y`, `COTTL01Y`, `CSDAT01Y`, `CSLKPCDY`, `CSMSG01Y`, `CSMSG02Y`, `CSSETATY`, `CSUSR01Y`, `CSUTLDPY`, `CVACT01Y`, `CVACT03Y`, `CVCRD01Y`, `CVCUS01Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [CBACT01C](../programs/CBACT01C.md), [CBACT03C](../programs/CBACT03C.md), [CBACT04C](../programs/CBACT04C.md), [CBCUS01C](../programs/CBCUS01C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBSTM03A](../programs/CBSTM03A.md), [CBTRN01C](../programs/CBTRN01C.md), [CBTRN02C](../programs/CBTRN02C.md), [CBTRN03C](../programs/CBTRN03C.md), [COACCT01](../programs/COACCT01.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)

### [COACTVWC](../programs/COACTVWC.md)

- **Data-coupled via copybooks** (`COACTVW`, `COCOM01Y`, `COTTL01Y`, `CSDAT01Y`, `CSMSG01Y`, `CSMSG02Y`, `CSUSR01Y`, `CVACT01Y`, `CVACT02Y`, `CVACT03Y`, `CVCRD01Y`, `CVCUS01Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [CBACT01C](../programs/CBACT01C.md), [CBACT02C](../programs/CBACT02C.md), [CBACT03C](../programs/CBACT03C.md), [CBACT04C](../programs/CBACT04C.md), [CBCUS01C](../programs/CBCUS01C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBSTM03A](../programs/CBSTM03A.md), [CBTRN01C](../programs/CBTRN01C.md), [CBTRN02C](../programs/CBTRN02C.md), [CBTRN03C](../programs/CBTRN03C.md), [COACCT01](../programs/COACCT01.md), [COACTUPC](../programs/COACTUPC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)

### [COADM01C](../programs/COADM01C.md)

- **Data-coupled via copybooks** (`COADM01`, `COADM02Y`, `COCOM01Y`, `COTTL01Y`, `CSDAT01Y`, `CSMSG01Y`, `CSUSR01Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)

### [COBIL00C](../programs/COBIL00C.md)

- **Data-coupled via copybooks** (`COBIL00`, `COCOM01Y`, `COTTL01Y`, `CSDAT01Y`, `CSMSG01Y`, `CVACT01Y`, `CVACT03Y`, `CVTRA05Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [CBACT01C](../programs/CBACT01C.md), [CBACT03C](../programs/CBACT03C.md), [CBACT04C](../programs/CBACT04C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBSTM03A](../programs/CBSTM03A.md), [CBTRN01C](../programs/CBTRN01C.md), [CBTRN02C](../programs/CBTRN02C.md), [CBTRN03C](../programs/CBTRN03C.md), [COACCT01](../programs/COACCT01.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)

### [COCRDLIC](../programs/COCRDLIC.md)

- **Data-coupled via copybooks** (`COCOM01Y`, `COCRDLI`, `COTTL01Y`, `CSDAT01Y`, `CSMSG01Y`, `CSUSR01Y`, `CVACT02Y`, `CVCRD01Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [CBACT02C](../programs/CBACT02C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBTRN01C](../programs/CBTRN01C.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)

### [COCRDSLC](../programs/COCRDSLC.md)

- **Data-coupled via copybooks** (`COCOM01Y`, `COCRDSL`, `COTTL01Y`, `CSDAT01Y`, `CSMSG01Y`, `CSMSG02Y`, `CSUSR01Y`, `CVACT02Y`, `CVCRD01Y`, `CVCUS01Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [CBACT02C](../programs/CBACT02C.md), [CBCUS01C](../programs/CBCUS01C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBTRN01C](../programs/CBTRN01C.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)

### [COCRDUPC](../programs/COCRDUPC.md)

- **Data-coupled via copybooks** (`COCOM01Y`, `COCRDUP`, `COTTL01Y`, `CSDAT01Y`, `CSMSG01Y`, `CSMSG02Y`, `CSUSR01Y`, `CVACT02Y`, `CVCRD01Y`, `CVCUS01Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [CBACT02C](../programs/CBACT02C.md), [CBCUS01C](../programs/CBCUS01C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBTRN01C](../programs/CBTRN01C.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)

### [CODATE01](../programs/CODATE01.md)

- **Data-coupled via copybooks** (`03220012`, `CMQGMOV`, `CMQMDV`, `CMQODV`, `CMQPMOV`, `CMQTML`, `CMQV`, `REPLACING`): [COACCT01](../programs/COACCT01.md), [COPAUA0C](../programs/COPAUA0C.md)

### [COMEN01C](../programs/COMEN01C.md)

- **Data-coupled via copybooks** (`COCOM01Y`, `COMEN01`, `COMEN02Y`, `COTTL01Y`, `CSDAT01Y`, `CSMSG01Y`, `CSUSR01Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)

### [COPAUA0C](../programs/COPAUA0C.md)

- **Data-coupled via copybooks** (`CCPAUERY`, `CCPAURLY`, `CCPAURQY`, `CIPAUDTY`, `CIPAUSMY`, `CMQGMOV`, `CMQMDV`, `CMQODV`, `CMQPMOV`, `CMQTML`, `CMQV`, `CVACT01Y`, `CVACT03Y`, `CVCUS01Y`): [CBACT01C](../programs/CBACT01C.md), [CBACT03C](../programs/CBACT03C.md), [CBACT04C](../programs/CBACT04C.md), [CBCUS01C](../programs/CBCUS01C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBPAUP0C](../programs/CBPAUP0C.md), [CBSTM03A](../programs/CBSTM03A.md), [CBTRN01C](../programs/CBTRN01C.md), [CBTRN02C](../programs/CBTRN02C.md), [CBTRN03C](../programs/CBTRN03C.md), [COACCT01](../programs/COACCT01.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COBIL00C](../programs/COBIL00C.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [CODATE01](../programs/CODATE01.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [COPAUS2C](../programs/COPAUS2C.md), [COTRN02C](../programs/COTRN02C.md), [DBUNLDGS](../programs/DBUNLDGS.md), [PAUDBLOD](../programs/PAUDBLOD.md), [PAUDBUNL](../programs/PAUDBUNL.md)

### [COPAUS0C](../programs/COPAUS0C.md)

- **Data-coupled via copybooks** (`CIPAUDTY`, `CIPAUSMY`, `COCOM01Y`, `COPAU00`, `COTTL01Y`, `CSDAT01Y`, `CSMSG01Y`, `CSMSG02Y`, `CVACT01Y`, `CVACT02Y`, `CVACT03Y`, `CVCUS01Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [CBACT01C](../programs/CBACT01C.md), [CBACT02C](../programs/CBACT02C.md), [CBACT03C](../programs/CBACT03C.md), [CBACT04C](../programs/CBACT04C.md), [CBCUS01C](../programs/CBCUS01C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBPAUP0C](../programs/CBPAUP0C.md), [CBSTM03A](../programs/CBSTM03A.md), [CBTRN01C](../programs/CBTRN01C.md), [CBTRN02C](../programs/CBTRN02C.md), [CBTRN03C](../programs/CBTRN03C.md), [COACCT01](../programs/COACCT01.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS1C](../programs/COPAUS1C.md), [COPAUS2C](../programs/COPAUS2C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md), [DBUNLDGS](../programs/DBUNLDGS.md), [PAUDBLOD](../programs/PAUDBLOD.md), [PAUDBUNL](../programs/PAUDBUNL.md)

### [COPAUS1C](../programs/COPAUS1C.md)

- **Data-coupled via copybooks** (`CIPAUDTY`, `CIPAUSMY`, `COCOM01Y`, `COPAU01`, `COTTL01Y`, `CSDAT01Y`, `CSMSG01Y`, `CSMSG02Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [CBPAUP0C](../programs/CBPAUP0C.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS2C](../programs/COPAUS2C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md), [DBUNLDGS](../programs/DBUNLDGS.md), [PAUDBLOD](../programs/PAUDBLOD.md), [PAUDBUNL](../programs/PAUDBUNL.md)

### [COPAUS2C](../programs/COPAUS2C.md)

- **Data-coupled via copybooks** (`CIPAUDTY`): [CBPAUP0C](../programs/CBPAUP0C.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [DBUNLDGS](../programs/DBUNLDGS.md), [PAUDBLOD](../programs/PAUDBLOD.md), [PAUDBUNL](../programs/PAUDBUNL.md)

### [CORPT00C](../programs/CORPT00C.md)

- **Data-coupled via copybooks** (`COCOM01Y`, `CORPT00`, `COTTL01Y`, `CSDAT01Y`, `CSMSG01Y`, `CVTRA05Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [CBACT04C](../programs/CBACT04C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBTRN01C](../programs/CBTRN01C.md), [CBTRN02C](../programs/CBTRN02C.md), [CBTRN03C](../programs/CBTRN03C.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)

### [COSGN00C](../programs/COSGN00C.md)

- **Data-coupled via copybooks** (`COCOM01Y`, `COSGN00`, `COTTL01Y`, `CSDAT01Y`, `CSMSG01Y`, `CSUSR01Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [CORPT00C](../programs/CORPT00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)

### [COTRN00C](../programs/COTRN00C.md)

- **Data-coupled via copybooks** (`COCOM01Y`, `COTRN00`, `COTTL01Y`, `CSDAT01Y`, `CSMSG01Y`, `CVTRA05Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [CBACT04C](../programs/CBACT04C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBTRN01C](../programs/CBTRN01C.md), [CBTRN02C](../programs/CBTRN02C.md), [CBTRN03C](../programs/CBTRN03C.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)

### [COTRN01C](../programs/COTRN01C.md)

- **Data-coupled via copybooks** (`COCOM01Y`, `COTRN01`, `COTTL01Y`, `CSDAT01Y`, `CSMSG01Y`, `CVTRA05Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [CBACT04C](../programs/CBACT04C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBTRN01C](../programs/CBTRN01C.md), [CBTRN02C](../programs/CBTRN02C.md), [CBTRN03C](../programs/CBTRN03C.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)

### [COTRN02C](../programs/COTRN02C.md)

- **Data-coupled via copybooks** (`COCOM01Y`, `COTRN02`, `COTTL01Y`, `CSDAT01Y`, `CSMSG01Y`, `CVACT01Y`, `CVACT03Y`, `CVTRA05Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [CBACT01C](../programs/CBACT01C.md), [CBACT03C](../programs/CBACT03C.md), [CBACT04C](../programs/CBACT04C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBSTM03A](../programs/CBSTM03A.md), [CBTRN01C](../programs/CBTRN01C.md), [CBTRN02C](../programs/CBTRN02C.md), [CBTRN03C](../programs/CBTRN03C.md), [COACCT01](../programs/COACCT01.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)

### [COTRTLIC](../programs/COTRTLIC.md)

- **Data-coupled via copybooks** (`COCOM01Y`, `COTRTLI`, `COTTL01Y`, `CSDAT01Y`, `CSMSG01Y`, `CSUSR01Y`, `CVACT02Y`, `CVCRD01Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [CBACT02C](../programs/CBACT02C.md), [CBEXPORT](../programs/CBEXPORT.md), [CBIMPORT](../programs/CBIMPORT.md), [CBTRN01C](../programs/CBTRN01C.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)

### [COUSR00C](../programs/COUSR00C.md)

- **Data-coupled via copybooks** (`COCOM01Y`, `COTTL01Y`, `COUSR00`, `CSDAT01Y`, `CSMSG01Y`, `CSUSR01Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)

### [COUSR01C](../programs/COUSR01C.md)

- **Data-coupled via copybooks** (`COCOM01Y`, `COTTL01Y`, `COUSR01`, `CSDAT01Y`, `CSMSG01Y`, `CSUSR01Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)

### [COUSR02C](../programs/COUSR02C.md)

- **Data-coupled via copybooks** (`COCOM01Y`, `COTTL01Y`, `COUSR02`, `CSDAT01Y`, `CSMSG01Y`, `CSUSR01Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR03C](../programs/COUSR03C.md)

### [COUSR03C](../programs/COUSR03C.md)

- **Data-coupled via copybooks** (`COCOM01Y`, `COTTL01Y`, `COUSR03`, `CSDAT01Y`, `CSMSG01Y`, `CSUSR01Y`, `DFHAID`, `DFHBMSCA`): [00220000](../programs/00220000.md), [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COTRTLIC](../programs/COTRTLIC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md)

### [DBUNLDGS](../programs/DBUNLDGS.md)

- **Data-coupled via copybooks** (`CIPAUDTY`, `CIPAUSMY`, `IMSFUNCS`, `PADFLPCB`, `PASFLPCB`, `PAUTBPCB`): [CBPAUP0C](../programs/CBPAUP0C.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [COPAUS2C](../programs/COPAUS2C.md), [PAUDBLOD](../programs/PAUDBLOD.md), [PAUDBUNL](../programs/PAUDBUNL.md)

### [PAUDBLOD](../programs/PAUDBLOD.md)

- **Data-coupled via copybooks** (`CIPAUDTY`, `CIPAUSMY`, `IMSFUNCS`, `PAUTBPCB`): [CBPAUP0C](../programs/CBPAUP0C.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [COPAUS2C](../programs/COPAUS2C.md), [DBUNLDGS](../programs/DBUNLDGS.md), [PAUDBUNL](../programs/PAUDBUNL.md)

### [PAUDBUNL](../programs/PAUDBUNL.md)

- **Data-coupled via copybooks** (`CIPAUDTY`, `CIPAUSMY`, `IMSFUNCS`, `PAUTBPCB`): [CBPAUP0C](../programs/CBPAUP0C.md), [COPAUA0C](../programs/COPAUA0C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [COPAUS2C](../programs/COPAUS2C.md), [DBUNLDGS](../programs/DBUNLDGS.md), [PAUDBLOD](../programs/PAUDBLOD.md)

---

*Generated 2026-02-10 21:17*