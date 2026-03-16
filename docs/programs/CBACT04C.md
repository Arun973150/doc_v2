# Program: CBACT04C


---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| Program ID | `CBACT04C` |
| Type | BATCH |
| Lines | 653 |
| Source | [CBACT04C.cbl](../carddemo/CBACT04C.cbl#L1) |
| Paragraphs | 22 |
| Statements | 120 |
| Impact Risk | **HIGH** — 18 programs affected |

> **View Source:** [Open CBACT04C.cbl](../carddemo/CBACT04C.cbl#L1)



## Dependency Context

> This section shows how **CBACT04C** connects to the rest of the system — who calls it,
> what it calls, and what data it shares. If linked programs exist, they must appear here.

### Programs That Call CBACT04C (Callers)

*No programs call CBACT04C — this is likely a top-level entry point or CICS transaction starter.*

### Programs Called by CBACT04C (Callees)

| Called Program | Type | Line | Why |
|----------------|------|------|-----|
| [UNKNOWN](UNKNOWN.md) | None | 710 |  |

### Shared Data (Copybooks & Files)

#### Shared Copybooks

| Copybook | Also Used By | # Co-Users |
|----------|-------------|------------|
| `CVACT01Y` | CBACT01C, CBEXPORT, CBIMPORT, CBSTM03A, CBTRN01C (+8 more) | 13 |
| `CVACT03Y` | CBACT03C, CBEXPORT, CBIMPORT, CBSTM03A, CBTRN01C (+8 more) | 13 |
| `CVTRA01Y` | CBTRN02C | 1 |
| `CVTRA02Y` |  | 0 |
| `CVTRA05Y` | CBEXPORT, CBIMPORT, CBTRN01C, CBTRN02C, CBTRN03C (+5 more) | 10 |


---

## Dependency Graph

```mermaid
flowchart TD
    CBACT04C["⬤ CBACT04C"]:::target
    UNKNOWN["UNKNOWN"]:::callee
    CBACT04C --> UNKNOWN
    CB_CVACT01Y{{"CVACT01Y"}}:::copybook
    CBACT04C -.- CB_CVACT01Y
    CBACT01C["CBACT01C"]:::coupled
    CB_CVACT01Y -.- CBACT01C
    CBEXPORT["CBEXPORT"]:::coupled
    CB_CVACT01Y -.- CBEXPORT
    CBIMPORT["CBIMPORT"]:::coupled
    CB_CVACT01Y -.- CBIMPORT
    CB_CVACT03Y{{"CVACT03Y"}}:::copybook
    CBACT04C -.- CB_CVACT03Y
    CBACT03C["CBACT03C"]:::coupled
    CB_CVACT03Y -.- CBACT03C
    CBEXPORT["CBEXPORT"]:::coupled
    CB_CVACT03Y -.- CBEXPORT
    CBIMPORT["CBIMPORT"]:::coupled
    CB_CVACT03Y -.- CBIMPORT
    CB_CVTRA01Y{{"CVTRA01Y"}}:::copybook
    CBACT04C -.- CB_CVTRA01Y
    CBTRN02C["CBTRN02C"]:::coupled
    CB_CVTRA01Y -.- CBTRN02C
    CB_CVTRA05Y{{"CVTRA05Y"}}:::copybook
    CBACT04C -.- CB_CVTRA05Y
    CBEXPORT["CBEXPORT"]:::coupled
    CB_CVTRA05Y -.- CBEXPORT
    CBIMPORT["CBIMPORT"]:::coupled
    CB_CVTRA05Y -.- CBIMPORT
    CBTRN01C["CBTRN01C"]:::coupled
    CB_CVTRA05Y -.- CBTRN01C

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

> **If you change CBACT04C, what else could break?**

| Impact Metric | Count |
|--------------|-------|
| Direct Callers | 0 |
| Transitive Callers (callers of callers) | 0 |
| Direct Callees | 0 |
| Transitive Callees | 0 |
| Copybook-Coupled Programs | 18 |
| **Total Impact** | **18** |
| **Risk Rating** | **HIGH** |


**Programs affected via shared copybooks:**
- `CBACT01C`
- `CBACT03C`
- `CBEXPORT`
- `CBIMPORT`
- `CBSTM03A`
- `CBTRN01C`
- `CBTRN02C`
- `CBTRN03C`
- `COACCT01`
- `COACTUPC`
- `COACTVWC`
- `COBIL00C`
- `COPAUA0C`
- `COPAUS0C`
- `CORPT00C`
- `COTRN00C`
- `COTRN01C`
- `COTRN02C`

---

## Statement Profile

| Statement Type | Count |
|---------------|-------|
| MOVE | 36 |
| IF | 36 |
| EXIT | 21 |
| READ | 5 |
| OPEN | 5 |
| CLOSE | 5 |
| ARITHMETIC | 3 |
| STRING_OP | 2 |
| PERFORM | 2 |
| WRITE | 1 |
| REWRITE | 1 |
| DISPLAY | 1 |
| COMPUTE | 1 |
| CALL | 1 |

## Control Flow

```mermaid
flowchart TD
    START([Program Entry])
    0000_TCATBALF_OPEN["0000-TCATBALF-OPEN"]
    0100_XREFFILE_OPEN["0100-XREFFILE-OPEN"]
    0200_DISCGRP_OPEN["0200-DISCGRP-OPEN"]
    0300_ACCTFILE_OPEN["0300-ACCTFILE-OPEN"]
    0400_TRANFILE_OPEN["0400-TRANFILE-OPEN"]
    1000_TCATBALF_GET_NEXT["1000-TCATBALF-GET-NEXT"]
    1050_UPDATE_ACCOUNT["1050-UPDATE-ACCOUNT"]
    1100_GET_ACCT_DATA["1100-GET-ACCT-DATA"]
    1110_GET_XREF_DATA["1110-GET-XREF-DATA"]
    1200_GET_INTEREST_RATE["1200-GET-INTEREST-RATE"]
    1200_A_GET_DEFAULT_INT_RATE["1200-A-GET-DEFAULT-INT-RATE"]
    1300_COMPUTE_INTEREST["1300-COMPUTE-INTEREST"]
    1300_B_WRITE_TX["1300-B-WRITE-TX"]
    1400_COMPUTE_FEES["1400-COMPUTE-FEES"]
    9000_TCATBALF_CLOSE["9000-TCATBALF-CLOSE"]
    START --> 0000_TCATBALF_OPEN
    1300_COMPUTE_INTEREST --> INLINE
    1300_B_WRITE_TX --> INLINE
```

## Paragraphs

### 0000-TCATBALF-OPEN

| | |
|---|---|
| **Paragraph** | `0000-TCATBALF-OPEN` |
| **Lines** | 312 - 328 |
| **View Code** | [Jump to Line 312](../carddemo/CBACT04C.cbl#L312) |



### 0100-XREFFILE-OPEN

| | |
|---|---|
| **Paragraph** | `0100-XREFFILE-OPEN` |
| **Lines** | 330 - 346 |
| **View Code** | [Jump to Line 330](../carddemo/CBACT04C.cbl#L330) |



### 0200-DISCGRP-OPEN

| | |
|---|---|
| **Paragraph** | `0200-DISCGRP-OPEN` |
| **Lines** | 348 - 364 |
| **View Code** | [Jump to Line 348](../carddemo/CBACT04C.cbl#L348) |



### 0300-ACCTFILE-OPEN

| | |
|---|---|
| **Paragraph** | `0300-ACCTFILE-OPEN` |
| **Lines** | 367 - 383 |
| **View Code** | [Jump to Line 367](../carddemo/CBACT04C.cbl#L367) |



### 0400-TRANFILE-OPEN

| | |
|---|---|
| **Paragraph** | `0400-TRANFILE-OPEN` |
| **Lines** | 385 - 401 |
| **View Code** | [Jump to Line 385](../carddemo/CBACT04C.cbl#L385) |



### 1000-TCATBALF-GET-NEXT

| | |
|---|---|
| **Paragraph** | `1000-TCATBALF-GET-NEXT` |
| **Lines** | 403 - 426 |
| **View Code** | [Jump to Line 403](../carddemo/CBACT04C.cbl#L403) |



### 1050-UPDATE-ACCOUNT

| | |
|---|---|
| **Paragraph** | `1050-UPDATE-ACCOUNT` |
| **Lines** | 428 - 448 |
| **View Code** | [Jump to Line 428](../carddemo/CBACT04C.cbl#L428) |



### 1100-GET-ACCT-DATA

| | |
|---|---|
| **Paragraph** | `1100-GET-ACCT-DATA` |
| **Lines** | 450 - 469 |
| **View Code** | [Jump to Line 450](../carddemo/CBACT04C.cbl#L450) |



### 1110-GET-XREF-DATA

| | |
|---|---|
| **Paragraph** | `1110-GET-XREF-DATA` |
| **Lines** | 471 - 491 |
| **View Code** | [Jump to Line 471](../carddemo/CBACT04C.cbl#L471) |



### 1200-GET-INTEREST-RATE

| | |
|---|---|
| **Paragraph** | `1200-GET-INTEREST-RATE` |
| **Lines** | 493 - 518 |
| **View Code** | [Jump to Line 493](../carddemo/CBACT04C.cbl#L493) |



### 1200-A-GET-DEFAULT-INT-RATE

| | |
|---|---|
| **Paragraph** | `1200-A-GET-DEFAULT-INT-RATE` |
| **Lines** | 521 - 538 |
| **View Code** | [Jump to Line 521](../carddemo/CBACT04C.cbl#L521) |



### 1300-COMPUTE-INTEREST

| | |
|---|---|
| **Paragraph** | `1300-COMPUTE-INTEREST` |
| **Lines** | 540 - 548 |
| **View Code** | [Jump to Line 540](../carddemo/CBACT04C.cbl#L540) |



### 1300-B-WRITE-TX

| | |
|---|---|
| **Paragraph** | `1300-B-WRITE-TX` |
| **Lines** | 551 - 593 |
| **View Code** | [Jump to Line 551](../carddemo/CBACT04C.cbl#L551) |



### 1400-COMPUTE-FEES

| | |
|---|---|
| **Paragraph** | `1400-COMPUTE-FEES` |
| **Lines** | 596 - 598 |
| **View Code** | [Jump to Line 596](../carddemo/CBACT04C.cbl#L596) |



### 9000-TCATBALF-CLOSE

| | |
|---|---|
| **Paragraph** | `9000-TCATBALF-CLOSE` |
| **Lines** | 600 - 616 |
| **View Code** | [Jump to Line 600](../carddemo/CBACT04C.cbl#L600) |



### 9100-XREFFILE-CLOSE

| | |
|---|---|
| **Paragraph** | `9100-XREFFILE-CLOSE` |
| **Lines** | 619 - 635 |
| **View Code** | [Jump to Line 619](../carddemo/CBACT04C.cbl#L619) |



### 9200-DISCGRP-CLOSE

| | |
|---|---|
| **Paragraph** | `9200-DISCGRP-CLOSE` |
| **Lines** | 637 - 653 |
| **View Code** | [Jump to Line 637](../carddemo/CBACT04C.cbl#L637) |



### 9300-ACCTFILE-CLOSE

| | |
|---|---|
| **Paragraph** | `9300-ACCTFILE-CLOSE` |
| **Lines** | 655 - 671 |
| **View Code** | [Jump to Line 655](../carddemo/CBACT04C.cbl#L655) |



### 9400-TRANFILE-CLOSE

| | |
|---|---|
| **Paragraph** | `9400-TRANFILE-CLOSE` |
| **Lines** | 673 - 689 |
| **View Code** | [Jump to Line 673](../carddemo/CBACT04C.cbl#L673) |



### Z-GET-DB2-FORMAT-TIMESTAMP

| | |
|---|---|
| **Paragraph** | `Z-GET-DB2-FORMAT-TIMESTAMP` |
| **Lines** | 691 - 704 |
| **View Code** | [Jump to Line 691](../carddemo/CBACT04C.cbl#L691) |



### 9999-ABEND-PROGRAM

| | |
|---|---|
| **Paragraph** | `9999-ABEND-PROGRAM` |
| **Lines** | 706 - 710 |
| **View Code** | [Jump to Line 706](../carddemo/CBACT04C.cbl#L706) |



### 9910-DISPLAY-IO-STATUS

| | |
|---|---|
| **Paragraph** | `9910-DISPLAY-IO-STATUS` |
| **Lines** | 713 - 726 |
| **View Code** | [Jump to Line 713](../carddemo/CBACT04C.cbl#L713) |




## Executed by JCL Jobs

This program is run by the following batch JCL jobs:

| Job Name | Step | Step Comments |
|----------|------|---------------|
| [INTCALC](../jcl/INTCALC.md) | `STEP15` | *****************************************************************
Copyright Amaz... |


## Business Rules

- **Invalid Transaction Record** `BR-077`  
  If a transaction record is invalid, the transaction is rejected.  
  [View Rule Details](../business-rules/BR-077.md)
- **Account Not Found** `BR-078`  
  If an account cannot be found for a transaction, the transaction is rejected.  
  [View Rule Details](../business-rules/BR-078.md)
- **Cross-Reference File Open Validation** `BR-079`  
  The program must successfully open the cross-reference file to link card numbers to account IDs before processing transactions.  
  [View Rule Details](../business-rules/BR-079.md)
- **Transaction File Open Validation** `BR-080`  
  The program must successfully open the transaction file containing transaction records before processing transactions.  
  [View Rule Details](../business-rules/BR-080.md)
- **Discount Group File Open Status Check** `BR-081`  
  The program verifies that the Discount Group file has been successfully opened.  
  [View Rule Details](../business-rules/BR-081.md)
- **Interest Rate File Open Status Check** `BR-082`  
  The program verifies that the Interest Rate file has been successfully opened.  
  [View Rule Details](../business-rules/BR-082.md)
- **Transaction File Open Validation** `BR-083`  
  The transaction file must be successfully opened before processing can continue.  
  [View Rule Details](../business-rules/BR-083.md)
- **Account File Open Validation** `BR-084`  
  The account file must be successfully opened before processing can continue.  
  [View Rule Details](../business-rules/BR-084.md)
- **Transaction File Open Validation** `BR-085`  
  The transaction file must be available and successfully opened before processing can continue.  
  [View Rule Details](../business-rules/BR-085.md)
- **Account File Open Validation** `BR-086`  
  The account file must be available and successfully opened before processing can continue.  
  [View Rule Details](../business-rules/BR-086.md)
- **Invalid Transaction Handling** `BR-087`  
  If a transaction record is identified as invalid, the transaction will not be processed.  
  [View Rule Details](../business-rules/BR-087.md)
- **Account Not Found Handling** `BR-088`  
  If an account cannot be found for a given transaction, the transaction will not be processed.  
  [View Rule Details](../business-rules/BR-088.md)
- **Late Payment Fee Assessment** `BR-089`  
  If a customer's payment is received after the due date, a late payment fee is applied to their account.  
  [View Rule Details](../business-rules/BR-089.md)
- **Interest Calculation** `BR-090`  
  Interest is calculated and applied to customer accounts based on the applicable interest rate.  
  [View Rule Details](../business-rules/BR-090.md)
- **Invalid Account Handling** `BR-091`  
  If an account record cannot be found for a given transaction, the transaction is considered invalid.  
  [View Rule Details](../business-rules/BR-091.md)
- **Account Status Check** `BR-092`  
  Transactions are rejected if the associated account is not in an active status.  
  [View Rule Details](../business-rules/BR-092.md)
- **Invalid Card Number Handling** `BR-093`  
  If a card number is not found in the cross-reference file, the transaction is considered invalid.  
  [View Rule Details](../business-rules/BR-093.md)
- **Account ID Retrieval** `BR-094`  
  If a card number is found in the cross-reference file, the corresponding account ID is retrieved.  
  [View Rule Details](../business-rules/BR-094.md)
- **Apply Standard Interest Rate** `BR-095`  
  If a specific interest rate is not found for an account, apply the standard interest rate.  
  [View Rule Details](../business-rules/BR-095.md)
- **Apply Discounted Interest Rate** `BR-096`  
  If the account belongs to a discount group, apply the discounted interest rate.  
  [View Rule Details](../business-rules/BR-096.md)
- **Default Interest Rate Assignment** `BR-097`  
  If a specific interest rate is not found for an account, a default interest rate is applied.  
  [View Rule Details](../business-rules/BR-097.md)
- **Transaction Record Update** `BR-098`  
  The transaction record is updated with specific values after processing.  
  [View Rule Details](../business-rules/BR-098.md)
- **Transaction File Close Status Check** `BR-099`  
  If the transaction file did not close successfully, an error message is displayed.  
  [View Rule Details](../business-rules/BR-099.md)
- **Account Balance File Close Status Check** `BR-100`  
  If the account balance file did not close successfully, an error message is displayed.  
  [View Rule Details](../business-rules/BR-100.md)
- **Cross-Reference File Close Status Check** `BR-101`  
  If the cross-reference file (linking card numbers to account IDs) does not close successfully, the program terminates.  
  [View Rule Details](../business-rules/BR-101.md)
- **Transaction File Close Status Check** `BR-102`  
  If the transaction file does not close successfully, the program terminates.  
  [View Rule Details](../business-rules/BR-102.md)
- **Discount Group File Close Status Check** `BR-103`  
  If the discount group file is not successfully closed, an error message is displayed.  
  [View Rule Details](../business-rules/BR-103.md)
- **Discount Group File Close Error Handling** `BR-104`  
  If closing the discount group file fails, the program sets a return code to indicate the failure.  
  [View Rule Details](../business-rules/BR-104.md)
- **Transaction File Status Check** `BR-105`  
  If the transaction file processing is incomplete, an error message is displayed.  
  [View Rule Details](../business-rules/BR-105.md)
- **Account File Status Check** `BR-106`  
  If the account file processing is incomplete, an error message is displayed.  
  [View Rule Details](../business-rules/BR-106.md)
- **Transaction File Close - Record Count Validation** `BR-107`  
  Verify that the number of transaction records processed is greater than zero.  
  [View Rule Details](../business-rules/BR-107.md)
- **Transaction File Close - Update Count Validation** `BR-108`  
  Verify that the number of account records updated is greater than zero.  
  [View Rule Details](../business-rules/BR-108.md)
- **I/O Status Display** `BR-109`  
  The program displays the I/O status of file operations for debugging and monitoring purposes.  
  [View Rule Details](../business-rules/BR-109.md)

## Key Data Items

| Name | Level | Picture | Section | Business Name |
|------|-------|---------|---------|---------------|
| `TRAN-CAT-BAL-RECORD` | 1 | `None` | WORKING-STORAGE | None |
| `TRAN-CAT-KEY` | 5 | `None` | WORKING-STORAGE | None |
| `TRANCAT-ACCT-ID` | 10 | `9(11)` | WORKING-STORAGE | None |
| `TRANCAT-TYPE-CD` | 10 | `X(02)` | WORKING-STORAGE | None |
| `TRANCAT-CD` | 10 | `9(04)` | WORKING-STORAGE | None |
| `TRAN-CAT-BAL` | 5 | `S9(09)V99` | WORKING-STORAGE | None |
| `FILLER` | 5 | `X(22)` | WORKING-STORAGE | None |
| `TCATBALF-STATUS` | 1 | `None` | WORKING-STORAGE | None |
| `TCATBALF-STAT1` | 5 | `X` | WORKING-STORAGE | None |
| `TCATBALF-STAT2` | 5 | `X` | WORKING-STORAGE | None |
| `CARD-XREF-RECORD` | 1 | `None` | WORKING-STORAGE | None |
| `XREF-CARD-NUM` | 5 | `X(16)` | WORKING-STORAGE | None |
| `XREF-CUST-ID` | 5 | `9(09)` | WORKING-STORAGE | None |
| `XREF-ACCT-ID` | 5 | `9(11)` | WORKING-STORAGE | None |
| `FILLER` | 5 | `X(14)` | WORKING-STORAGE | None |
| `XREFFILE-STATUS` | 1 | `None` | WORKING-STORAGE | None |
| `XREFFILE-STAT1` | 5 | `X` | WORKING-STORAGE | None |
| `XREFFILE-STAT2` | 5 | `X` | WORKING-STORAGE | None |
| `DIS-GROUP-RECORD` | 1 | `None` | WORKING-STORAGE | None |
| `DIS-GROUP-KEY` | 5 | `None` | WORKING-STORAGE | None |
| `DIS-ACCT-GROUP-ID` | 10 | `X(10)` | WORKING-STORAGE | None |
| `DIS-TRAN-TYPE-CD` | 10 | `X(02)` | WORKING-STORAGE | None |
| `DIS-TRAN-CAT-CD` | 10 | `9(04)` | WORKING-STORAGE | None |
| `DIS-INT-RATE` | 5 | `S9(04)V99` | WORKING-STORAGE | None |
| `FILLER` | 5 | `X(28)` | WORKING-STORAGE | None |
| `DISCGRP-STATUS` | 1 | `None` | WORKING-STORAGE | None |
| `DISCGRP-STAT1` | 5 | `X` | WORKING-STORAGE | None |
| `DISCGRP-STAT2` | 5 | `X` | WORKING-STORAGE | None |
| `ACCOUNT-RECORD` | 1 | `None` | WORKING-STORAGE | None |
| `ACCT-ID` | 5 | `9(11)` | WORKING-STORAGE | None |
| `ACCT-ACTIVE-STATUS` | 5 | `X(01)` | WORKING-STORAGE | None |
| `ACCT-CURR-BAL` | 5 | `S9(10)V99` | WORKING-STORAGE | None |
| `ACCT-CREDIT-LIMIT` | 5 | `S9(10)V99` | WORKING-STORAGE | None |
| `ACCT-CASH-CREDIT-LIMIT` | 5 | `S9(10)V99` | WORKING-STORAGE | None |
| `ACCT-OPEN-DATE` | 5 | `X(10)` | WORKING-STORAGE | None |
| `ACCT-EXPIRAION-DATE` | 5 | `X(10)` | WORKING-STORAGE | None |
| `ACCT-REISSUE-DATE` | 5 | `X(10)` | WORKING-STORAGE | None |
| `ACCT-CURR-CYC-CREDIT` | 5 | `S9(10)V99` | WORKING-STORAGE | None |
| `ACCT-CURR-CYC-DEBIT` | 5 | `S9(10)V99` | WORKING-STORAGE | None |
| `ACCT-ADDR-ZIP` | 5 | `X(10)` | WORKING-STORAGE | None |

*Showing 40 of 115 data items. See [Data Dictionary](../data-dictionary.md).*

---

*Generated 2026-03-16 21:06*