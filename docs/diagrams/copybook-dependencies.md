# Copybook Dependency Graph

> Copybooks are shared data structures `COPY` included by multiple programs.
> They are the primary mechanism for **data coupling** in COBOL systems.

> **Total Copybooks:** 68  
> **Total COPY Statements:** 301

## Copybook Sharing Graph

```mermaid
graph LR
    03220012(("03220012<br/>(1 programs)")):::copybook
    03500000(("03500000<br/>(1 programs)")):::copybook
    CCPAUERY(("CCPAUERY<br/>(1 programs)")):::copybook
    CCPAURLY(("CCPAURLY<br/>(1 programs)")):::copybook
    CCPAURQY(("CCPAURQY<br/>(1 programs)")):::copybook
    CIPAUDTY(("CIPAUDTY<br/>(8 programs)")):::copybook
    CIPAUSMY(("CIPAUSMY<br/>(7 programs)")):::copybook
    CMQGMOV(("CMQGMOV<br/>(3 programs)")):::copybook
    CMQMDV(("CMQMDV<br/>(3 programs)")):::copybook
    CMQODV(("CMQODV<br/>(3 programs)")):::copybook
    CMQPMOV(("CMQPMOV<br/>(3 programs)")):::copybook
    CMQTML(("CMQTML<br/>(3 programs)")):::copybook
    CMQV(("CMQV<br/>(3 programs)")):::copybook
    COACTUP(("COACTUP<br/>(1 programs)")):::copybook
    COACTVW(("COACTVW<br/>(1 programs)")):::copybook
    COADM01(("COADM01<br/>(1 programs)")):::copybook
    COADM02Y(("COADM02Y<br/>(1 programs)")):::copybook
    COBIL00(("COBIL00<br/>(1 programs)")):::copybook
    COCOM01Y(("COCOM01Y<br/>(21 programs)")):::copybook
    COCRDLI(("COCRDLI<br/>(1 programs)")):::copybook
    COCRDSL(("COCRDSL<br/>(1 programs)")):::copybook
    COCRDUP(("COCRDUP<br/>(1 programs)")):::copybook
    CODATECN(("CODATECN<br/>(1 programs)")):::copybook
    COMEN01(("COMEN01<br/>(1 programs)")):::copybook
    COMEN02Y(("COMEN02Y<br/>(1 programs)")):::copybook
    COPAU00(("COPAU00<br/>(1 programs)")):::copybook
    COPAU01(("COPAU01<br/>(1 programs)")):::copybook
    CORPT00(("CORPT00<br/>(1 programs)")):::copybook
    COSGN00(("COSGN00<br/>(1 programs)")):::copybook
    COSTM01(("COSTM01<br/>(1 programs)")):::copybook
    COTRN00(("COTRN00<br/>(1 programs)")):::copybook
    COTRN01(("COTRN01<br/>(1 programs)")):::copybook
    COTRN02(("COTRN02<br/>(1 programs)")):::copybook
    COTRTLI(("COTRTLI<br/>(1 programs)")):::copybook
    COTRTUP(("COTRTUP<br/>(1 programs)")):::copybook
    COTTL01Y(("COTTL01Y<br/>(21 programs)")):::copybook
    COUSR00(("COUSR00<br/>(1 programs)")):::copybook
    COUSR01(("COUSR01<br/>(1 programs)")):::copybook
    COUSR02(("COUSR02<br/>(1 programs)")):::copybook
    COUSR03(("COUSR03<br/>(1 programs)")):::copybook
    CSDAT01Y(("CSDAT01Y<br/>(21 programs)")):::copybook
    CSLKPCDY(("CSLKPCDY<br/>(1 programs)")):::copybook
    CSMSG01Y(("CSMSG01Y<br/>(21 programs)")):::copybook
    CSMSG02Y(("CSMSG02Y<br/>(7 programs)")):::copybook
    CSSETATY(("CSSETATY<br/>(2 programs)")):::copybook
    CSUSR01Y(("CSUSR01Y<br/>(14 programs)")):::copybook
    CSUTLDPY(("CSUTLDPY<br/>(1 programs)")):::copybook
    CUSTREC(("CUSTREC<br/>(1 programs)")):::copybook
    CVACT01Y(("CVACT01Y<br/>(14 programs)")):::copybook
    CVACT02Y(("CVACT02Y<br/>(10 programs)")):::copybook
    CVACT03Y(("CVACT03Y<br/>(14 programs)")):::copybook
    CVCRD01Y(("CVCRD01Y<br/>(7 programs)")):::copybook
    CVCUS01Y(("CVCUS01Y<br/>(10 programs)")):::copybook
    CVEXPORT(("CVEXPORT<br/>(2 programs)")):::copybook
    CVTRA01Y(("CVTRA01Y<br/>(2 programs)")):::copybook
    CVTRA02Y(("CVTRA02Y<br/>(1 programs)")):::copybook
    CVTRA03Y(("CVTRA03Y<br/>(1 programs)")):::copybook
    CVTRA04Y(("CVTRA04Y<br/>(1 programs)")):::copybook
    CVTRA05Y(("CVTRA05Y<br/>(11 programs)")):::copybook
    CVTRA06Y(("CVTRA06Y<br/>(2 programs)")):::copybook
    CVTRA07Y(("CVTRA07Y<br/>(1 programs)")):::copybook
    DFHAID(("DFHAID<br/>(21 programs)")):::copybook
    DFHBMSCA(("DFHBMSCA<br/>(21 programs)")):::copybook
    IMSFUNCS(("IMSFUNCS<br/>(3 programs)")):::copybook
    PADFLPCB(("PADFLPCB<br/>(1 programs)")):::copybook
    PASFLPCB(("PASFLPCB<br/>(1 programs)")):::copybook
    PAUTBPCB(("PAUTBPCB<br/>(3 programs)")):::copybook
    REPLACING(("REPLACING<br/>(2 programs)")):::copybook
    CODATE01["CODATE01"] --> 03220012
    COACCT01["COACCT01"] --> 03500000
    COPAUA0C["COPAUA0C"] --> CCPAUERY
    COPAUA0C["COPAUA0C"] --> CCPAURLY
    COPAUA0C["COPAUA0C"] --> CCPAURQY
    CBPAUP0C["CBPAUP0C"] --> CIPAUDTY
    COPAUA0C["COPAUA0C"] --> CIPAUDTY
    COPAUS0C["COPAUS0C"] --> CIPAUDTY
    COPAUS1C["COPAUS1C"] --> CIPAUDTY
    COPAUS2C["COPAUS2C"] --> CIPAUDTY
    DBUNLDGS["DBUNLDGS"] --> CIPAUDTY
    PAUDBLOD["PAUDBLOD"] --> CIPAUDTY
    PAUDBUNL["PAUDBUNL"] --> CIPAUDTY
    CBPAUP0C["CBPAUP0C"] --> CIPAUSMY
    COPAUA0C["COPAUA0C"] --> CIPAUSMY
    COPAUS0C["COPAUS0C"] --> CIPAUSMY
    COPAUS1C["COPAUS1C"] --> CIPAUSMY
    DBUNLDGS["DBUNLDGS"] --> CIPAUSMY
    PAUDBLOD["PAUDBLOD"] --> CIPAUSMY
    PAUDBUNL["PAUDBUNL"] --> CIPAUSMY
    COPAUA0C["COPAUA0C"] --> CMQGMOV
    COACCT01["COACCT01"] --> CMQGMOV
    CODATE01["CODATE01"] --> CMQGMOV
    COPAUA0C["COPAUA0C"] --> CMQMDV
    COACCT01["COACCT01"] --> CMQMDV
    CODATE01["CODATE01"] --> CMQMDV
    COPAUA0C["COPAUA0C"] --> CMQODV
    COACCT01["COACCT01"] --> CMQODV
    CODATE01["CODATE01"] --> CMQODV
    COPAUA0C["COPAUA0C"] --> CMQPMOV
    COACCT01["COACCT01"] --> CMQPMOV
    CODATE01["CODATE01"] --> CMQPMOV
    COPAUA0C["COPAUA0C"] --> CMQTML
    COACCT01["COACCT01"] --> CMQTML
    CODATE01["CODATE01"] --> CMQTML
    COPAUA0C["COPAUA0C"] --> CMQV
    COACCT01["COACCT01"] --> CMQV
    CODATE01["CODATE01"] --> CMQV
    COACTUPC["COACTUPC"] --> COACTUP
    COACTVWC["COACTVWC"] --> COACTVW
    COADM01C["COADM01C"] --> COADM01
    COADM01C["COADM01C"] --> COADM02Y
    COBIL00C["COBIL00C"] --> COBIL00
    COPAUS0C["COPAUS0C"] --> COCOM01Y
    COPAUS1C["COPAUS1C"] --> COCOM01Y
    COTRTLIC["COTRTLIC"] --> COCOM01Y
    00220000["00220000"] --> COCOM01Y
    COACTUPC["COACTUPC"] --> COCOM01Y
    COACTVWC["COACTVWC"] --> COCOM01Y
    COADM01C["COADM01C"] --> COCOM01Y
    COBIL00C["COBIL00C"] --> COCOM01Y
    COCRDLIC["COCRDLIC"] --> COCOM01Y
    COCRDSLC["COCRDSLC"] --> COCOM01Y
    COCRDUPC["COCRDUPC"] --> COCOM01Y
    COMEN01C["COMEN01C"] --> COCOM01Y
    CORPT00C["CORPT00C"] --> COCOM01Y
    COSGN00C["COSGN00C"] --> COCOM01Y
    COTRN00C["COTRN00C"] --> COCOM01Y
    COTRN01C["COTRN01C"] --> COCOM01Y
    COTRN02C["COTRN02C"] --> COCOM01Y
    COUSR00C["COUSR00C"] --> COCOM01Y
    COUSR01C["COUSR01C"] --> COCOM01Y
    COUSR02C["COUSR02C"] --> COCOM01Y
    COUSR03C["COUSR03C"] --> COCOM01Y
    COCRDLIC["COCRDLIC"] --> COCRDLI
    COCRDSLC["COCRDSLC"] --> COCRDSL
    COCRDUPC["COCRDUPC"] --> COCRDUP
    CBACT01C["CBACT01C"] --> CODATECN
    COMEN01C["COMEN01C"] --> COMEN01
    COMEN01C["COMEN01C"] --> COMEN02Y
    COPAUS0C["COPAUS0C"] --> COPAU00
    COPAUS1C["COPAUS1C"] --> COPAU01
    CORPT00C["CORPT00C"] --> CORPT00
    COSGN00C["COSGN00C"] --> COSGN00
    CBSTM03A["CBSTM03A"] --> COSTM01
    COTRN00C["COTRN00C"] --> COTRN00
    COTRN01C["COTRN01C"] --> COTRN01
    COTRN02C["COTRN02C"] --> COTRN02
    COTRTLIC["COTRTLIC"] --> COTRTLI
    00220000["00220000"] --> COTRTUP
    COPAUS0C["COPAUS0C"] --> COTTL01Y
    COPAUS1C["COPAUS1C"] --> COTTL01Y
    COTRTLIC["COTRTLIC"] --> COTTL01Y
    00220000["00220000"] --> COTTL01Y
    COACTUPC["COACTUPC"] --> COTTL01Y
    COACTVWC["COACTVWC"] --> COTTL01Y
    COADM01C["COADM01C"] --> COTTL01Y
    COBIL00C["COBIL00C"] --> COTTL01Y
    COCRDLIC["COCRDLIC"] --> COTTL01Y
    COCRDSLC["COCRDSLC"] --> COTTL01Y
    COCRDUPC["COCRDUPC"] --> COTTL01Y
    COMEN01C["COMEN01C"] --> COTTL01Y
    CORPT00C["CORPT00C"] --> COTTL01Y
    COSGN00C["COSGN00C"] --> COTTL01Y
    COTRN00C["COTRN00C"] --> COTTL01Y
    COTRN01C["COTRN01C"] --> COTTL01Y
    COTRN02C["COTRN02C"] --> COTTL01Y
    COUSR00C["COUSR00C"] --> COTTL01Y
    COUSR01C["COUSR01C"] --> COTTL01Y
    COUSR02C["COUSR02C"] --> COTTL01Y
    COUSR03C["COUSR03C"] --> COTTL01Y
    COUSR00C["COUSR00C"] --> COUSR00
    COUSR01C["COUSR01C"] --> COUSR01
    COUSR02C["COUSR02C"] --> COUSR02
    COUSR03C["COUSR03C"] --> COUSR03
    COPAUS0C["COPAUS0C"] --> CSDAT01Y
    COPAUS1C["COPAUS1C"] --> CSDAT01Y
    COTRTLIC["COTRTLIC"] --> CSDAT01Y
    00220000["00220000"] --> CSDAT01Y
    COACTUPC["COACTUPC"] --> CSDAT01Y
    COACTVWC["COACTVWC"] --> CSDAT01Y
    COADM01C["COADM01C"] --> CSDAT01Y
    COBIL00C["COBIL00C"] --> CSDAT01Y
    COCRDLIC["COCRDLIC"] --> CSDAT01Y
    COCRDSLC["COCRDSLC"] --> CSDAT01Y
    COCRDUPC["COCRDUPC"] --> CSDAT01Y
    COMEN01C["COMEN01C"] --> CSDAT01Y
    CORPT00C["CORPT00C"] --> CSDAT01Y
    COSGN00C["COSGN00C"] --> CSDAT01Y
    COTRN00C["COTRN00C"] --> CSDAT01Y
    COTRN01C["COTRN01C"] --> CSDAT01Y
    COTRN02C["COTRN02C"] --> CSDAT01Y
    COUSR00C["COUSR00C"] --> CSDAT01Y
    COUSR01C["COUSR01C"] --> CSDAT01Y
    COUSR02C["COUSR02C"] --> CSDAT01Y
    COUSR03C["COUSR03C"] --> CSDAT01Y
    COACTUPC["COACTUPC"] --> CSLKPCDY
    COPAUS0C["COPAUS0C"] --> CSMSG01Y
    COPAUS1C["COPAUS1C"] --> CSMSG01Y
    COTRTLIC["COTRTLIC"] --> CSMSG01Y
    00220000["00220000"] --> CSMSG01Y
    COACTUPC["COACTUPC"] --> CSMSG01Y
    COACTVWC["COACTVWC"] --> CSMSG01Y
    COADM01C["COADM01C"] --> CSMSG01Y
    COBIL00C["COBIL00C"] --> CSMSG01Y
    COCRDLIC["COCRDLIC"] --> CSMSG01Y
    COCRDSLC["COCRDSLC"] --> CSMSG01Y
    COCRDUPC["COCRDUPC"] --> CSMSG01Y
    COMEN01C["COMEN01C"] --> CSMSG01Y
    CORPT00C["CORPT00C"] --> CSMSG01Y
    COSGN00C["COSGN00C"] --> CSMSG01Y
    COTRN00C["COTRN00C"] --> CSMSG01Y
    COTRN01C["COTRN01C"] --> CSMSG01Y
    COTRN02C["COTRN02C"] --> CSMSG01Y
    COUSR00C["COUSR00C"] --> CSMSG01Y
    COUSR01C["COUSR01C"] --> CSMSG01Y
    COUSR02C["COUSR02C"] --> CSMSG01Y
    COUSR03C["COUSR03C"] --> CSMSG01Y
    COPAUS0C["COPAUS0C"] --> CSMSG02Y
    COPAUS1C["COPAUS1C"] --> CSMSG02Y
    00220000["00220000"] --> CSMSG02Y
    COACTUPC["COACTUPC"] --> CSMSG02Y
    COACTVWC["COACTVWC"] --> CSMSG02Y
    COCRDSLC["COCRDSLC"] --> CSMSG02Y
    COCRDUPC["COCRDUPC"] --> CSMSG02Y
    00220000["00220000"] --> CSSETATY
    COACTUPC["COACTUPC"] --> CSSETATY
    COTRTLIC["COTRTLIC"] --> CSUSR01Y
    00220000["00220000"] --> CSUSR01Y
    COACTUPC["COACTUPC"] --> CSUSR01Y
    COACTVWC["COACTVWC"] --> CSUSR01Y
    COADM01C["COADM01C"] --> CSUSR01Y
    COCRDLIC["COCRDLIC"] --> CSUSR01Y
    COCRDSLC["COCRDSLC"] --> CSUSR01Y
    COCRDUPC["COCRDUPC"] --> CSUSR01Y
    COMEN01C["COMEN01C"] --> CSUSR01Y
    COSGN00C["COSGN00C"] --> CSUSR01Y
    COUSR00C["COUSR00C"] --> CSUSR01Y
    COUSR01C["COUSR01C"] --> CSUSR01Y
    COUSR02C["COUSR02C"] --> CSUSR01Y
    COUSR03C["COUSR03C"] --> CSUSR01Y
    COACTUPC["COACTUPC"] --> CSUTLDPY
    CBSTM03A["CBSTM03A"] --> CUSTREC
    COPAUA0C["COPAUA0C"] --> CVACT01Y
    COPAUS0C["COPAUS0C"] --> CVACT01Y
    COACCT01["COACCT01"] --> CVACT01Y
    CBACT01C["CBACT01C"] --> CVACT01Y
    CBACT04C["CBACT04C"] --> CVACT01Y
    CBEXPORT["CBEXPORT"] --> CVACT01Y
    CBIMPORT["CBIMPORT"] --> CVACT01Y
    CBSTM03A["CBSTM03A"] --> CVACT01Y
    CBTRN01C["CBTRN01C"] --> CVACT01Y
    CBTRN02C["CBTRN02C"] --> CVACT01Y
    COACTUPC["COACTUPC"] --> CVACT01Y
    COACTVWC["COACTVWC"] --> CVACT01Y
    COBIL00C["COBIL00C"] --> CVACT01Y
    COTRN02C["COTRN02C"] --> CVACT01Y
    COPAUS0C["COPAUS0C"] --> CVACT02Y
    COTRTLIC["COTRTLIC"] --> CVACT02Y
    CBACT02C["CBACT02C"] --> CVACT02Y
    CBEXPORT["CBEXPORT"] --> CVACT02Y
    CBIMPORT["CBIMPORT"] --> CVACT02Y
    CBTRN01C["CBTRN01C"] --> CVACT02Y
    COACTVWC["COACTVWC"] --> CVACT02Y
    COCRDLIC["COCRDLIC"] --> CVACT02Y
    COCRDSLC["COCRDSLC"] --> CVACT02Y
    COCRDUPC["COCRDUPC"] --> CVACT02Y
    COPAUA0C["COPAUA0C"] --> CVACT03Y
    COPAUS0C["COPAUS0C"] --> CVACT03Y
    CBACT03C["CBACT03C"] --> CVACT03Y
    CBACT04C["CBACT04C"] --> CVACT03Y
    CBEXPORT["CBEXPORT"] --> CVACT03Y
    CBIMPORT["CBIMPORT"] --> CVACT03Y
    CBSTM03A["CBSTM03A"] --> CVACT03Y
    CBTRN01C["CBTRN01C"] --> CVACT03Y
    CBTRN02C["CBTRN02C"] --> CVACT03Y
    CBTRN03C["CBTRN03C"] --> CVACT03Y
    COACTUPC["COACTUPC"] --> CVACT03Y
    COACTVWC["COACTVWC"] --> CVACT03Y
    COBIL00C["COBIL00C"] --> CVACT03Y
    COTRN02C["COTRN02C"] --> CVACT03Y
    COTRTLIC["COTRTLIC"] --> CVCRD01Y
    00220000["00220000"] --> CVCRD01Y
    COACTUPC["COACTUPC"] --> CVCRD01Y
    COACTVWC["COACTVWC"] --> CVCRD01Y
    COCRDLIC["COCRDLIC"] --> CVCRD01Y
    COCRDSLC["COCRDSLC"] --> CVCRD01Y
    COCRDUPC["COCRDUPC"] --> CVCRD01Y
    COPAUA0C["COPAUA0C"] --> CVCUS01Y
    COPAUS0C["COPAUS0C"] --> CVCUS01Y
    CBCUS01C["CBCUS01C"] --> CVCUS01Y
    CBEXPORT["CBEXPORT"] --> CVCUS01Y
    CBIMPORT["CBIMPORT"] --> CVCUS01Y
    CBTRN01C["CBTRN01C"] --> CVCUS01Y
    COACTUPC["COACTUPC"] --> CVCUS01Y
    COACTVWC["COACTVWC"] --> CVCUS01Y
    COCRDSLC["COCRDSLC"] --> CVCUS01Y
    COCRDUPC["COCRDUPC"] --> CVCUS01Y
    CBEXPORT["CBEXPORT"] --> CVEXPORT
    CBIMPORT["CBIMPORT"] --> CVEXPORT
    CBACT04C["CBACT04C"] --> CVTRA01Y
    CBTRN02C["CBTRN02C"] --> CVTRA01Y
    CBACT04C["CBACT04C"] --> CVTRA02Y
    CBTRN03C["CBTRN03C"] --> CVTRA03Y
    CBTRN03C["CBTRN03C"] --> CVTRA04Y
    CBACT04C["CBACT04C"] --> CVTRA05Y
    CBEXPORT["CBEXPORT"] --> CVTRA05Y
    CBIMPORT["CBIMPORT"] --> CVTRA05Y
    CBTRN01C["CBTRN01C"] --> CVTRA05Y
    CBTRN02C["CBTRN02C"] --> CVTRA05Y
    CBTRN03C["CBTRN03C"] --> CVTRA05Y
    COBIL00C["COBIL00C"] --> CVTRA05Y
    CORPT00C["CORPT00C"] --> CVTRA05Y
    COTRN00C["COTRN00C"] --> CVTRA05Y
    COTRN01C["COTRN01C"] --> CVTRA05Y
    COTRN02C["COTRN02C"] --> CVTRA05Y
    CBTRN01C["CBTRN01C"] --> CVTRA06Y
    CBTRN02C["CBTRN02C"] --> CVTRA06Y
    CBTRN03C["CBTRN03C"] --> CVTRA07Y
    COPAUS0C["COPAUS0C"] --> DFHAID
    COPAUS1C["COPAUS1C"] --> DFHAID
    COTRTLIC["COTRTLIC"] --> DFHAID
    00220000["00220000"] --> DFHAID
    COACTUPC["COACTUPC"] --> DFHAID
    COACTVWC["COACTVWC"] --> DFHAID
    COADM01C["COADM01C"] --> DFHAID
    COBIL00C["COBIL00C"] --> DFHAID
    COCRDLIC["COCRDLIC"] --> DFHAID
    COCRDSLC["COCRDSLC"] --> DFHAID
    COCRDUPC["COCRDUPC"] --> DFHAID
    COMEN01C["COMEN01C"] --> DFHAID
    CORPT00C["CORPT00C"] --> DFHAID
    COSGN00C["COSGN00C"] --> DFHAID
    COTRN00C["COTRN00C"] --> DFHAID
    COTRN01C["COTRN01C"] --> DFHAID
    COTRN02C["COTRN02C"] --> DFHAID
    COUSR00C["COUSR00C"] --> DFHAID
    COUSR01C["COUSR01C"] --> DFHAID
    COUSR02C["COUSR02C"] --> DFHAID
    COUSR03C["COUSR03C"] --> DFHAID
    COPAUS0C["COPAUS0C"] --> DFHBMSCA
    COPAUS1C["COPAUS1C"] --> DFHBMSCA
    COTRTLIC["COTRTLIC"] --> DFHBMSCA
    00220000["00220000"] --> DFHBMSCA
    COACTUPC["COACTUPC"] --> DFHBMSCA
    COACTVWC["COACTVWC"] --> DFHBMSCA
    COADM01C["COADM01C"] --> DFHBMSCA
    COBIL00C["COBIL00C"] --> DFHBMSCA
    COCRDLIC["COCRDLIC"] --> DFHBMSCA
    COCRDSLC["COCRDSLC"] --> DFHBMSCA
    COCRDUPC["COCRDUPC"] --> DFHBMSCA
    COMEN01C["COMEN01C"] --> DFHBMSCA
    CORPT00C["CORPT00C"] --> DFHBMSCA
    COSGN00C["COSGN00C"] --> DFHBMSCA
    COTRN00C["COTRN00C"] --> DFHBMSCA
    COTRN01C["COTRN01C"] --> DFHBMSCA
    COTRN02C["COTRN02C"] --> DFHBMSCA
    COUSR00C["COUSR00C"] --> DFHBMSCA
    COUSR01C["COUSR01C"] --> DFHBMSCA
    COUSR02C["COUSR02C"] --> DFHBMSCA
    COUSR03C["COUSR03C"] --> DFHBMSCA
    DBUNLDGS["DBUNLDGS"] --> IMSFUNCS
    PAUDBLOD["PAUDBLOD"] --> IMSFUNCS
    PAUDBUNL["PAUDBUNL"] --> IMSFUNCS
    DBUNLDGS["DBUNLDGS"] --> PADFLPCB
    DBUNLDGS["DBUNLDGS"] --> PASFLPCB
    DBUNLDGS["DBUNLDGS"] --> PAUTBPCB
    PAUDBLOD["PAUDBLOD"] --> PAUTBPCB
    PAUDBUNL["PAUDBUNL"] --> PAUTBPCB
    COACCT01["COACCT01"] --> REPLACING
    CODATE01["CODATE01"] --> REPLACING

    classDef copybook fill:#FFC107,stroke:#F57F17,color:#000
```

## Copybook Details

### `03220012` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [CODATE01](../programs/CODATE01.md) | - |

### `03500000` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COACCT01](../programs/COACCT01.md) | - |

### `CCPAUERY` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COPAUA0C](../programs/COPAUA0C.md) | - |

### `CCPAURLY` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COPAUA0C](../programs/COPAUA0C.md) | - |

### `CCPAURQY` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COPAUA0C](../programs/COPAUA0C.md) | - |

### `CIPAUDTY` 

**Used by 8 programs:**

| Program | COPY Line |
|---------|-----------|
| [CBPAUP0C](../programs/CBPAUP0C.md) | - |
| [COPAUA0C](../programs/COPAUA0C.md) | - |
| [COPAUS0C](../programs/COPAUS0C.md) | - |
| [COPAUS1C](../programs/COPAUS1C.md) | - |
| [COPAUS2C](../programs/COPAUS2C.md) | - |
| [DBUNLDGS](../programs/DBUNLDGS.md) | - |
| [PAUDBLOD](../programs/PAUDBLOD.md) | - |
| [PAUDBUNL](../programs/PAUDBUNL.md) | - |

### `CIPAUSMY` 

**Used by 7 programs:**

| Program | COPY Line |
|---------|-----------|
| [CBPAUP0C](../programs/CBPAUP0C.md) | - |
| [COPAUA0C](../programs/COPAUA0C.md) | - |
| [COPAUS0C](../programs/COPAUS0C.md) | - |
| [COPAUS1C](../programs/COPAUS1C.md) | - |
| [DBUNLDGS](../programs/DBUNLDGS.md) | - |
| [PAUDBLOD](../programs/PAUDBLOD.md) | - |
| [PAUDBUNL](../programs/PAUDBUNL.md) | - |

### `CMQGMOV` 

**Used by 3 programs:**

| Program | COPY Line |
|---------|-----------|
| [COACCT01](../programs/COACCT01.md) | - |
| [CODATE01](../programs/CODATE01.md) | - |
| [COPAUA0C](../programs/COPAUA0C.md) | - |

### `CMQMDV` 

**Used by 3 programs:**

| Program | COPY Line |
|---------|-----------|
| [COACCT01](../programs/COACCT01.md) | - |
| [CODATE01](../programs/CODATE01.md) | - |
| [COPAUA0C](../programs/COPAUA0C.md) | - |

### `CMQODV` 

**Used by 3 programs:**

| Program | COPY Line |
|---------|-----------|
| [COACCT01](../programs/COACCT01.md) | - |
| [CODATE01](../programs/CODATE01.md) | - |
| [COPAUA0C](../programs/COPAUA0C.md) | - |

### `CMQPMOV` 

**Used by 3 programs:**

| Program | COPY Line |
|---------|-----------|
| [COACCT01](../programs/COACCT01.md) | - |
| [CODATE01](../programs/CODATE01.md) | - |
| [COPAUA0C](../programs/COPAUA0C.md) | - |

### `CMQTML` 

**Used by 3 programs:**

| Program | COPY Line |
|---------|-----------|
| [COACCT01](../programs/COACCT01.md) | - |
| [CODATE01](../programs/CODATE01.md) | - |
| [COPAUA0C](../programs/COPAUA0C.md) | - |

### `CMQV` 

**Used by 3 programs:**

| Program | COPY Line |
|---------|-----------|
| [COACCT01](../programs/COACCT01.md) | - |
| [CODATE01](../programs/CODATE01.md) | - |
| [COPAUA0C](../programs/COPAUA0C.md) | - |

### `COACTUP` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COACTUPC](../programs/COACTUPC.md) | - |

### `COACTVW` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COACTVWC](../programs/COACTVWC.md) | - |

### `COADM01` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COADM01C](../programs/COADM01C.md) | - |

### `COADM02Y` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COADM01C](../programs/COADM01C.md) | - |

### `COBIL00` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COBIL00C](../programs/COBIL00C.md) | - |

### `COCOM01Y` 

**Used by 21 programs:**

| Program | COPY Line |
|---------|-----------|
| [00220000](../programs/00220000.md) | - |
| [COACTUPC](../programs/COACTUPC.md) | - |
| [COACTVWC](../programs/COACTVWC.md) | - |
| [COADM01C](../programs/COADM01C.md) | - |
| [COBIL00C](../programs/COBIL00C.md) | - |
| [COCRDLIC](../programs/COCRDLIC.md) | - |
| [COCRDSLC](../programs/COCRDSLC.md) | - |
| [COCRDUPC](../programs/COCRDUPC.md) | - |
| [COMEN01C](../programs/COMEN01C.md) | - |
| [COPAUS0C](../programs/COPAUS0C.md) | - |
| [COPAUS1C](../programs/COPAUS1C.md) | - |
| [CORPT00C](../programs/CORPT00C.md) | - |
| [COSGN00C](../programs/COSGN00C.md) | - |
| [COTRN00C](../programs/COTRN00C.md) | - |
| [COTRN01C](../programs/COTRN01C.md) | - |
| [COTRN02C](../programs/COTRN02C.md) | - |
| [COTRTLIC](../programs/COTRTLIC.md) | - |
| [COUSR00C](../programs/COUSR00C.md) | - |
| [COUSR01C](../programs/COUSR01C.md) | - |
| [COUSR02C](../programs/COUSR02C.md) | - |
| [COUSR03C](../programs/COUSR03C.md) | - |

### `COCRDLI` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COCRDLIC](../programs/COCRDLIC.md) | - |

### `COCRDSL` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COCRDSLC](../programs/COCRDSLC.md) | - |

### `COCRDUP` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COCRDUPC](../programs/COCRDUPC.md) | - |

### `CODATECN` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [CBACT01C](../programs/CBACT01C.md) | - |

### `COMEN01` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COMEN01C](../programs/COMEN01C.md) | - |

### `COMEN02Y` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COMEN01C](../programs/COMEN01C.md) | - |

### `COPAU00` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COPAUS0C](../programs/COPAUS0C.md) | - |

### `COPAU01` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COPAUS1C](../programs/COPAUS1C.md) | - |

### `CORPT00` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [CORPT00C](../programs/CORPT00C.md) | - |

### `COSGN00` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COSGN00C](../programs/COSGN00C.md) | - |

### `COSTM01` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [CBSTM03A](../programs/CBSTM03A.md) | - |

### `COTRN00` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COTRN00C](../programs/COTRN00C.md) | - |

### `COTRN01` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COTRN01C](../programs/COTRN01C.md) | - |

### `COTRN02` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COTRN02C](../programs/COTRN02C.md) | - |

### `COTRTLI` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COTRTLIC](../programs/COTRTLIC.md) | - |

### `COTRTUP` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [00220000](../programs/00220000.md) | - |

### `COTTL01Y` 

**Used by 21 programs:**

| Program | COPY Line |
|---------|-----------|
| [00220000](../programs/00220000.md) | - |
| [COACTUPC](../programs/COACTUPC.md) | - |
| [COACTVWC](../programs/COACTVWC.md) | - |
| [COADM01C](../programs/COADM01C.md) | - |
| [COBIL00C](../programs/COBIL00C.md) | - |
| [COCRDLIC](../programs/COCRDLIC.md) | - |
| [COCRDSLC](../programs/COCRDSLC.md) | - |
| [COCRDUPC](../programs/COCRDUPC.md) | - |
| [COMEN01C](../programs/COMEN01C.md) | - |
| [COPAUS0C](../programs/COPAUS0C.md) | - |
| [COPAUS1C](../programs/COPAUS1C.md) | - |
| [CORPT00C](../programs/CORPT00C.md) | - |
| [COSGN00C](../programs/COSGN00C.md) | - |
| [COTRN00C](../programs/COTRN00C.md) | - |
| [COTRN01C](../programs/COTRN01C.md) | - |
| [COTRN02C](../programs/COTRN02C.md) | - |
| [COTRTLIC](../programs/COTRTLIC.md) | - |
| [COUSR00C](../programs/COUSR00C.md) | - |
| [COUSR01C](../programs/COUSR01C.md) | - |
| [COUSR02C](../programs/COUSR02C.md) | - |
| [COUSR03C](../programs/COUSR03C.md) | - |

### `COUSR00` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COUSR00C](../programs/COUSR00C.md) | - |

### `COUSR01` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COUSR01C](../programs/COUSR01C.md) | - |

### `COUSR02` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COUSR02C](../programs/COUSR02C.md) | - |

### `COUSR03` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COUSR03C](../programs/COUSR03C.md) | - |

### `CSDAT01Y` 

**Used by 21 programs:**

| Program | COPY Line |
|---------|-----------|
| [00220000](../programs/00220000.md) | - |
| [COACTUPC](../programs/COACTUPC.md) | - |
| [COACTVWC](../programs/COACTVWC.md) | - |
| [COADM01C](../programs/COADM01C.md) | - |
| [COBIL00C](../programs/COBIL00C.md) | - |
| [COCRDLIC](../programs/COCRDLIC.md) | - |
| [COCRDSLC](../programs/COCRDSLC.md) | - |
| [COCRDUPC](../programs/COCRDUPC.md) | - |
| [COMEN01C](../programs/COMEN01C.md) | - |
| [COPAUS0C](../programs/COPAUS0C.md) | - |
| [COPAUS1C](../programs/COPAUS1C.md) | - |
| [CORPT00C](../programs/CORPT00C.md) | - |
| [COSGN00C](../programs/COSGN00C.md) | - |
| [COTRN00C](../programs/COTRN00C.md) | - |
| [COTRN01C](../programs/COTRN01C.md) | - |
| [COTRN02C](../programs/COTRN02C.md) | - |
| [COTRTLIC](../programs/COTRTLIC.md) | - |
| [COUSR00C](../programs/COUSR00C.md) | - |
| [COUSR01C](../programs/COUSR01C.md) | - |
| [COUSR02C](../programs/COUSR02C.md) | - |
| [COUSR03C](../programs/COUSR03C.md) | - |

### `CSLKPCDY` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COACTUPC](../programs/COACTUPC.md) | - |

### `CSMSG01Y` 

**Used by 21 programs:**

| Program | COPY Line |
|---------|-----------|
| [00220000](../programs/00220000.md) | - |
| [COACTUPC](../programs/COACTUPC.md) | - |
| [COACTVWC](../programs/COACTVWC.md) | - |
| [COADM01C](../programs/COADM01C.md) | - |
| [COBIL00C](../programs/COBIL00C.md) | - |
| [COCRDLIC](../programs/COCRDLIC.md) | - |
| [COCRDSLC](../programs/COCRDSLC.md) | - |
| [COCRDUPC](../programs/COCRDUPC.md) | - |
| [COMEN01C](../programs/COMEN01C.md) | - |
| [COPAUS0C](../programs/COPAUS0C.md) | - |
| [COPAUS1C](../programs/COPAUS1C.md) | - |
| [CORPT00C](../programs/CORPT00C.md) | - |
| [COSGN00C](../programs/COSGN00C.md) | - |
| [COTRN00C](../programs/COTRN00C.md) | - |
| [COTRN01C](../programs/COTRN01C.md) | - |
| [COTRN02C](../programs/COTRN02C.md) | - |
| [COTRTLIC](../programs/COTRTLIC.md) | - |
| [COUSR00C](../programs/COUSR00C.md) | - |
| [COUSR01C](../programs/COUSR01C.md) | - |
| [COUSR02C](../programs/COUSR02C.md) | - |
| [COUSR03C](../programs/COUSR03C.md) | - |

### `CSMSG02Y` 

**Used by 7 programs:**

| Program | COPY Line |
|---------|-----------|
| [00220000](../programs/00220000.md) | - |
| [COACTUPC](../programs/COACTUPC.md) | - |
| [COACTVWC](../programs/COACTVWC.md) | - |
| [COCRDSLC](../programs/COCRDSLC.md) | - |
| [COCRDUPC](../programs/COCRDUPC.md) | - |
| [COPAUS0C](../programs/COPAUS0C.md) | - |
| [COPAUS1C](../programs/COPAUS1C.md) | - |

### `CSSETATY` 

**Used by 2 programs:**

| Program | COPY Line |
|---------|-----------|
| [00220000](../programs/00220000.md) | - |
| [COACTUPC](../programs/COACTUPC.md) | - |

### `CSUSR01Y` 

**Used by 14 programs:**

| Program | COPY Line |
|---------|-----------|
| [00220000](../programs/00220000.md) | - |
| [COACTUPC](../programs/COACTUPC.md) | - |
| [COACTVWC](../programs/COACTVWC.md) | - |
| [COADM01C](../programs/COADM01C.md) | - |
| [COCRDLIC](../programs/COCRDLIC.md) | - |
| [COCRDSLC](../programs/COCRDSLC.md) | - |
| [COCRDUPC](../programs/COCRDUPC.md) | - |
| [COMEN01C](../programs/COMEN01C.md) | - |
| [COSGN00C](../programs/COSGN00C.md) | - |
| [COTRTLIC](../programs/COTRTLIC.md) | - |
| [COUSR00C](../programs/COUSR00C.md) | - |
| [COUSR01C](../programs/COUSR01C.md) | - |
| [COUSR02C](../programs/COUSR02C.md) | - |
| [COUSR03C](../programs/COUSR03C.md) | - |

### `CSUTLDPY` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [COACTUPC](../programs/COACTUPC.md) | - |

### `CUSTREC` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [CBSTM03A](../programs/CBSTM03A.md) | - |

### `CVACT01Y` 

**Used by 14 programs:**

| Program | COPY Line |
|---------|-----------|
| [CBACT01C](../programs/CBACT01C.md) | - |
| [CBACT04C](../programs/CBACT04C.md) | - |
| [CBEXPORT](../programs/CBEXPORT.md) | - |
| [CBIMPORT](../programs/CBIMPORT.md) | - |
| [CBSTM03A](../programs/CBSTM03A.md) | - |
| [CBTRN01C](../programs/CBTRN01C.md) | - |
| [CBTRN02C](../programs/CBTRN02C.md) | - |
| [COACCT01](../programs/COACCT01.md) | - |
| [COACTUPC](../programs/COACTUPC.md) | - |
| [COACTVWC](../programs/COACTVWC.md) | - |
| [COBIL00C](../programs/COBIL00C.md) | - |
| [COPAUA0C](../programs/COPAUA0C.md) | - |
| [COPAUS0C](../programs/COPAUS0C.md) | - |
| [COTRN02C](../programs/COTRN02C.md) | - |

### `CVACT02Y` 

**Used by 10 programs:**

| Program | COPY Line |
|---------|-----------|
| [CBACT02C](../programs/CBACT02C.md) | - |
| [CBEXPORT](../programs/CBEXPORT.md) | - |
| [CBIMPORT](../programs/CBIMPORT.md) | - |
| [CBTRN01C](../programs/CBTRN01C.md) | - |
| [COACTVWC](../programs/COACTVWC.md) | - |
| [COCRDLIC](../programs/COCRDLIC.md) | - |
| [COCRDSLC](../programs/COCRDSLC.md) | - |
| [COCRDUPC](../programs/COCRDUPC.md) | - |
| [COPAUS0C](../programs/COPAUS0C.md) | - |
| [COTRTLIC](../programs/COTRTLIC.md) | - |

### `CVACT03Y` 

**Used by 14 programs:**

| Program | COPY Line |
|---------|-----------|
| [CBACT03C](../programs/CBACT03C.md) | - |
| [CBACT04C](../programs/CBACT04C.md) | - |
| [CBEXPORT](../programs/CBEXPORT.md) | - |
| [CBIMPORT](../programs/CBIMPORT.md) | - |
| [CBSTM03A](../programs/CBSTM03A.md) | - |
| [CBTRN01C](../programs/CBTRN01C.md) | - |
| [CBTRN02C](../programs/CBTRN02C.md) | - |
| [CBTRN03C](../programs/CBTRN03C.md) | - |
| [COACTUPC](../programs/COACTUPC.md) | - |
| [COACTVWC](../programs/COACTVWC.md) | - |
| [COBIL00C](../programs/COBIL00C.md) | - |
| [COPAUA0C](../programs/COPAUA0C.md) | - |
| [COPAUS0C](../programs/COPAUS0C.md) | - |
| [COTRN02C](../programs/COTRN02C.md) | - |

### `CVCRD01Y` 

**Used by 7 programs:**

| Program | COPY Line |
|---------|-----------|
| [00220000](../programs/00220000.md) | - |
| [COACTUPC](../programs/COACTUPC.md) | - |
| [COACTVWC](../programs/COACTVWC.md) | - |
| [COCRDLIC](../programs/COCRDLIC.md) | - |
| [COCRDSLC](../programs/COCRDSLC.md) | - |
| [COCRDUPC](../programs/COCRDUPC.md) | - |
| [COTRTLIC](../programs/COTRTLIC.md) | - |

### `CVCUS01Y` 

**Used by 10 programs:**

| Program | COPY Line |
|---------|-----------|
| [CBCUS01C](../programs/CBCUS01C.md) | - |
| [CBEXPORT](../programs/CBEXPORT.md) | - |
| [CBIMPORT](../programs/CBIMPORT.md) | - |
| [CBTRN01C](../programs/CBTRN01C.md) | - |
| [COACTUPC](../programs/COACTUPC.md) | - |
| [COACTVWC](../programs/COACTVWC.md) | - |
| [COCRDSLC](../programs/COCRDSLC.md) | - |
| [COCRDUPC](../programs/COCRDUPC.md) | - |
| [COPAUA0C](../programs/COPAUA0C.md) | - |
| [COPAUS0C](../programs/COPAUS0C.md) | - |

### `CVEXPORT` 

**Used by 2 programs:**

| Program | COPY Line |
|---------|-----------|
| [CBEXPORT](../programs/CBEXPORT.md) | - |
| [CBIMPORT](../programs/CBIMPORT.md) | - |

### `CVTRA01Y` 

**Used by 2 programs:**

| Program | COPY Line |
|---------|-----------|
| [CBACT04C](../programs/CBACT04C.md) | - |
| [CBTRN02C](../programs/CBTRN02C.md) | - |

### `CVTRA02Y` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [CBACT04C](../programs/CBACT04C.md) | - |

### `CVTRA03Y` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [CBTRN03C](../programs/CBTRN03C.md) | - |

### `CVTRA04Y` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [CBTRN03C](../programs/CBTRN03C.md) | - |

### `CVTRA05Y` 

**Used by 11 programs:**

| Program | COPY Line |
|---------|-----------|
| [CBACT04C](../programs/CBACT04C.md) | - |
| [CBEXPORT](../programs/CBEXPORT.md) | - |
| [CBIMPORT](../programs/CBIMPORT.md) | - |
| [CBTRN01C](../programs/CBTRN01C.md) | - |
| [CBTRN02C](../programs/CBTRN02C.md) | - |
| [CBTRN03C](../programs/CBTRN03C.md) | - |
| [COBIL00C](../programs/COBIL00C.md) | - |
| [CORPT00C](../programs/CORPT00C.md) | - |
| [COTRN00C](../programs/COTRN00C.md) | - |
| [COTRN01C](../programs/COTRN01C.md) | - |
| [COTRN02C](../programs/COTRN02C.md) | - |

### `CVTRA06Y` 

**Used by 2 programs:**

| Program | COPY Line |
|---------|-----------|
| [CBTRN01C](../programs/CBTRN01C.md) | - |
| [CBTRN02C](../programs/CBTRN02C.md) | - |

### `CVTRA07Y` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [CBTRN03C](../programs/CBTRN03C.md) | - |

### `DFHAID` 

**Used by 21 programs:**

| Program | COPY Line |
|---------|-----------|
| [00220000](../programs/00220000.md) | - |
| [COACTUPC](../programs/COACTUPC.md) | - |
| [COACTVWC](../programs/COACTVWC.md) | - |
| [COADM01C](../programs/COADM01C.md) | - |
| [COBIL00C](../programs/COBIL00C.md) | - |
| [COCRDLIC](../programs/COCRDLIC.md) | - |
| [COCRDSLC](../programs/COCRDSLC.md) | - |
| [COCRDUPC](../programs/COCRDUPC.md) | - |
| [COMEN01C](../programs/COMEN01C.md) | - |
| [COPAUS0C](../programs/COPAUS0C.md) | - |
| [COPAUS1C](../programs/COPAUS1C.md) | - |
| [CORPT00C](../programs/CORPT00C.md) | - |
| [COSGN00C](../programs/COSGN00C.md) | - |
| [COTRN00C](../programs/COTRN00C.md) | - |
| [COTRN01C](../programs/COTRN01C.md) | - |
| [COTRN02C](../programs/COTRN02C.md) | - |
| [COTRTLIC](../programs/COTRTLIC.md) | - |
| [COUSR00C](../programs/COUSR00C.md) | - |
| [COUSR01C](../programs/COUSR01C.md) | - |
| [COUSR02C](../programs/COUSR02C.md) | - |
| [COUSR03C](../programs/COUSR03C.md) | - |

### `DFHBMSCA` 

**Used by 21 programs:**

| Program | COPY Line |
|---------|-----------|
| [00220000](../programs/00220000.md) | - |
| [COACTUPC](../programs/COACTUPC.md) | - |
| [COACTVWC](../programs/COACTVWC.md) | - |
| [COADM01C](../programs/COADM01C.md) | - |
| [COBIL00C](../programs/COBIL00C.md) | - |
| [COCRDLIC](../programs/COCRDLIC.md) | - |
| [COCRDSLC](../programs/COCRDSLC.md) | - |
| [COCRDUPC](../programs/COCRDUPC.md) | - |
| [COMEN01C](../programs/COMEN01C.md) | - |
| [COPAUS0C](../programs/COPAUS0C.md) | - |
| [COPAUS1C](../programs/COPAUS1C.md) | - |
| [CORPT00C](../programs/CORPT00C.md) | - |
| [COSGN00C](../programs/COSGN00C.md) | - |
| [COTRN00C](../programs/COTRN00C.md) | - |
| [COTRN01C](../programs/COTRN01C.md) | - |
| [COTRN02C](../programs/COTRN02C.md) | - |
| [COTRTLIC](../programs/COTRTLIC.md) | - |
| [COUSR00C](../programs/COUSR00C.md) | - |
| [COUSR01C](../programs/COUSR01C.md) | - |
| [COUSR02C](../programs/COUSR02C.md) | - |
| [COUSR03C](../programs/COUSR03C.md) | - |

### `IMSFUNCS` 

**Used by 3 programs:**

| Program | COPY Line |
|---------|-----------|
| [DBUNLDGS](../programs/DBUNLDGS.md) | - |
| [PAUDBLOD](../programs/PAUDBLOD.md) | - |
| [PAUDBUNL](../programs/PAUDBUNL.md) | - |

### `PADFLPCB` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [DBUNLDGS](../programs/DBUNLDGS.md) | - |

### `PASFLPCB` 

**Used by 1 programs:**

| Program | COPY Line |
|---------|-----------|
| [DBUNLDGS](../programs/DBUNLDGS.md) | - |

### `PAUTBPCB` 

**Used by 3 programs:**

| Program | COPY Line |
|---------|-----------|
| [DBUNLDGS](../programs/DBUNLDGS.md) | - |
| [PAUDBLOD](../programs/PAUDBLOD.md) | - |
| [PAUDBUNL](../programs/PAUDBUNL.md) | - |

### `REPLACING` 

**Used by 2 programs:**

| Program | COPY Line |
|---------|-----------|
| [COACCT01](../programs/COACCT01.md) | - |
| [CODATE01](../programs/CODATE01.md) | - |

---

*Generated 2026-02-10 21:17*