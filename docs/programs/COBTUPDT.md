# Program: COBTUPDT


---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| Program ID | `COBTUPDT` |
| Type | DB2 |
| Lines | 238 |
| Source | [COBTUPDT.cbl](../carddemo/COBTUPDT.cbl#L1) |
| Paragraphs | 9 |
| Statements | 30 |
| Impact Risk | **LOW** — 0 programs affected |

> **View Source:** [Open COBTUPDT.cbl](../carddemo/COBTUPDT.cbl#L1)



## Dependency Context

> This section shows how **COBTUPDT** connects to the rest of the system — who calls it,
> what it calls, and what data it shares. If linked programs exist, they must appear here.

### Programs That Call COBTUPDT (Callers)

*No programs call COBTUPDT — this is likely a top-level entry point or CICS transaction starter.*

### Programs Called by COBTUPDT (Callees)

*COBTUPDT does not call any other programs (leaf program).*

### Shared Data (Copybooks & Files)

*No shared copybooks.*


---

## Dependency Graph

```mermaid
flowchart TD
    COBTUPDT["⬤ COBTUPDT"]:::target

    classDef target fill:#f85149,stroke:#da3633,color:#fff,stroke-width:3px
    classDef caller fill:#58a6ff,stroke:#1f6feb,color:#fff
    classDef callee fill:#3fb950,stroke:#238636,color:#fff
    classDef copybook fill:#d29922,stroke:#9e6a03,color:#fff
    classDef coupled fill:#d29922,stroke:#9e6a03,color:#fff,stroke-dasharray:5
    classDef transitive fill:#484f58,stroke:#8b949e,color:#c9d1d9,stroke-dasharray:5
```

> **Legend:** 🔴 Target program · 🔵 Direct callers · 🟢 Direct callees · 🟡 Copybook-coupled · ⚫ Transitive (indirect)

---

## Impact Ripple View

> **If you change COBTUPDT, what else could break?**

| Impact Metric | Count |
|--------------|-------|
| Direct Callers | 0 |
| Transitive Callers (callers of callers) | 0 |
| Direct Callees | 0 |
| Transitive Callees | 0 |
| Copybook-Coupled Programs | 0 |
| **Total Impact** | **0** |
| **Risk Rating** | **LOW** |



---

## Statement Profile

| Statement Type | Count |
|---------------|-------|
| EXIT | 9 |
| MOVE | 4 |
| EVALUATE | 4 |
| PERFORM | 3 |
| EXECSQL | 3 |
| IF | 2 |
| STOP | 1 |
| READ | 1 |
| OPEN | 1 |
| DISPLAY | 1 |
| CLOSE | 1 |

## Control Flow

```mermaid
flowchart TD
    START([Program Entry])
    0001_OPEN_FILES["0001-OPEN-FILES"]
    1001_READ_NEXT_RECORDS["1001-READ-NEXT-RECORDS"]
    1002_READ_RECORDS["1002-READ-RECORDS"]
    1003_TREAT_RECORD["1003-TREAT-RECORD"]
    10031_INSERT_DB["10031-INSERT-DB"]
    10032_UPDATE_DB["10032-UPDATE-DB"]
    10033_DELETE_DB["10033-DELETE-DB"]
    9999_ABEND["9999-ABEND"]
    2001_CLOSE_STOP["2001-CLOSE-STOP"]
    START --> 0001_OPEN_FILES
    1001_READ_NEXT_RECORDS --> INLINE
```

## Paragraphs

### 0001-OPEN-FILES

| | |
|---|---|
| **Paragraph** | `0001-OPEN-FILES` |
| **Lines** | 82 - 89 |
| **View Code** | [Jump to Line 82](../carddemo/COBTUPDT.cbl#L82) |



### 1001-READ-NEXT-RECORDS

| | |
|---|---|
| **Paragraph** | `1001-READ-NEXT-RECORDS` |
| **Lines** | 91 - 99 |
| **View Code** | [Jump to Line 91](../carddemo/COBTUPDT.cbl#L91) |



### 1002-READ-RECORDS

| | |
|---|---|
| **Paragraph** | `1002-READ-RECORDS` |
| **Lines** | 100 - 107 |
| **View Code** | [Jump to Line 100](../carddemo/COBTUPDT.cbl#L100) |



### 1003-TREAT-RECORD

| | |
|---|---|
| **Paragraph** | `1003-TREAT-RECORD` |
| **Lines** | 109 - 130 |
| **View Code** | [Jump to Line 109](../carddemo/COBTUPDT.cbl#L109) |



### 10031-INSERT-DB

| | |
|---|---|
| **Paragraph** | `10031-INSERT-DB` |
| **Lines** | 132 - 164 |
| **View Code** | [Jump to Line 132](../carddemo/COBTUPDT.cbl#L132) |



### 10032-UPDATE-DB

| | |
|---|---|
| **Paragraph** | `10032-UPDATE-DB` |
| **Lines** | 166 - 195 |
| **View Code** | [Jump to Line 166](../carddemo/COBTUPDT.cbl#L166) |



### 10033-DELETE-DB

| | |
|---|---|
| **Paragraph** | `10033-DELETE-DB` |
| **Lines** | 196 - 226 |
| **View Code** | [Jump to Line 196](../carddemo/COBTUPDT.cbl#L196) |



### 9999-ABEND

| | |
|---|---|
| **Paragraph** | `9999-ABEND` |
| **Lines** | 230 - 233 |
| **View Code** | [Jump to Line 230](../carddemo/COBTUPDT.cbl#L230) |



### 2001-CLOSE-STOP

| | |
|---|---|
| **Paragraph** | `2001-CLOSE-STOP` |
| **Lines** | 234 - 236 |
| **View Code** | [Jump to Line 234](../carddemo/COBTUPDT.cbl#L234) |





## Business Rules

- **Transaction File Open Success** `BR-031`  
  The transaction file must open successfully for the update process to continue.  
  [View Rule Details](../business-rules/BR-031.md)
- **Database Connection Success** `BR-032`  
  A successful connection to the DB2 database is required to perform updates.  
  [View Rule Details](../business-rules/BR-032.md)
- **Process Insert Record** `BR-033`  
  When a transaction record indicates an insert operation, a new record should be created in the database.  
  [View Rule Details](../business-rules/BR-033.md)
- **Process Update Record** `BR-034`  
  When a transaction record indicates an update operation, an existing record in the database should be modified.  
  [View Rule Details](../business-rules/BR-034.md)
- **Process Delete Record** `BR-035`  
  When a transaction record indicates a delete operation, an existing record in the database should be removed.  
  [View Rule Details](../business-rules/BR-035.md)
- **Process Insert Record** `BR-036`  
  When a transaction record indicates an insert operation, add a new record to the database.  
  [View Rule Details](../business-rules/BR-036.md)
- **Process Update Record** `BR-037`  
  When a transaction record indicates an update operation, modify an existing record in the database.  
  [View Rule Details](../business-rules/BR-037.md)
- **Process Delete Record** `BR-038`  
  When a transaction record indicates a delete operation, remove an existing record from the database.  
  [View Rule Details](../business-rules/BR-038.md)
- **Record Type Validation** `BR-039`  
  The system determines the type of database update (insert, update, or delete) based on a record type code within the transaction record.  
  [View Rule Details](../business-rules/BR-039.md)
- **Transaction Type Validation** `BR-040`  
  The system determines the type of database update (insert, update, or delete) based on a record type code within the transaction record.  
  [View Rule Details](../business-rules/BR-040.md)
- **Delete Record Validation** `BR-041`  
  If the database delete operation fails, set the DB2 delete status code to 'DB2-DELETE-ERROR'.  
  [View Rule Details](../business-rules/BR-041.md)
- **Delete Record Failure Handling** `BR-042`  
  If the database delete operation fails, set the overall program return code to 8.  
  [View Rule Details](../business-rules/BR-042.md)

## Key Data Items

| Name | Level | Picture | Section | Business Name |
|------|-------|---------|---------|---------------|
| `FLAGS` | 1 | `None` | WORKING-STORAGE | None |
| `LASTREC` | 5 | `X(1)` | WORKING-STORAGE | None |
| `WORKING-VARIABLES` | 1 | `None` | WORKING-STORAGE | None |
| `WS-RETURN-MSG` | 5 | `X(80)` | WORKING-STORAGE | None |
| `WS-MISC-VARS` | 1 | `None` | WORKING-STORAGE | None |
| `WS-VAR-SQLCODE` | 5 | `----9` | WORKING-STORAGE | None |
| `WS-INF-STATUS` | 1 | `None` | WORKING-STORAGE | None |
| `WS-INF-STAT1` | 5 | `X` | WORKING-STORAGE | None |
| `WS-INF-STAT2` | 5 | `X` | WORKING-STORAGE | None |
| `WS-INPUT-REC` | 1 | `None` | WORKING-STORAGE | None |
| `INPUT-REC-TYPE` | 5 | `X(1)` | WORKING-STORAGE | None |
| `INPUT-REC-NUMBER` | 5 | `X(2)` | WORKING-STORAGE | None |
| `INPUT-REC-DESC` | 5 | `X(50)` | WORKING-STORAGE | None |

---

*Generated 2026-03-16 21:06*