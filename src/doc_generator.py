"""
Swimm-Style Documentation Generator - Complete 5-Layer Architecture
Generates interactive, business-first documentation from COBOL analysis.

Layers:
  1. Repository Overview (00-SYSTEM-OVERVIEW.md)
  2. Module Documentation (modules/MODULE-NAME.md)
  3. Program Walkthroughs (programs/PROGRAM-NAME.md)
  4. Business Rules Catalog (business-rules/INDEX.md + per-rule)
  5. Screen Catalog (screens/SCREEN-ID.md)

Plus:
  - Call Graph Diagram (diagrams/call-graph.md)
  - Data Dictionary (data-dictionary.md)
  - Copybook Reference (copybook-reference.md)
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict

from jinja2 import Environment, BaseLoader, TemplateNotFound
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console(force_terminal=True, highlight=False)


# ============================================================
# Jinja2 Template Loader (inline templates)
# ============================================================

class InlineTemplateLoader(BaseLoader):
    """Loads templates from inline strings or optional template files."""

    def __init__(self, templates: Dict[str, str], templates_dir: str = None):
        self._templates = templates
        self._templates_dir = templates_dir

    def get_source(self, environment, template):
        if self._templates_dir:
            path = Path(self._templates_dir) / template
            if path.exists():
                return path.read_text(encoding="utf-8"), str(path), lambda: True
        if template in self._templates:
            return self._templates[template], template, lambda: True
        raise TemplateNotFound(template)


# ============================================================
# Templates
# ============================================================

TEMPLATES = {}

# ----- Layer 1: System Overview -----
TEMPLATES["system_overview.md.j2"] = '''\
# {{ system_name }} - System Overview

> **Auto-generated documentation** | {{ generated_date }}  
> Analyzed from {{ total_programs }} COBOL programs across {{ total_modules }} functional modules

---

## What is {{ system_name }}?

{{ system_name }} is a mainframe COBOL application that provides core business functionality
for credit card account management. The system handles customer sign-on, account inquiries,
transaction processing, credit card management, and batch operations through a combination
of CICS online screens and batch JCL jobs.

## System at a Glance

| Metric | Count |
|--------|-------|
| Programs | {{ total_programs }} |
| Functional Modules | {{ total_modules }} |
| BMS Screens | {{ total_screens }} |
| Data Items | {{ total_data_items }} |
| Inter-Program Calls | {{ total_calls }} |
| Business Rules | {{ total_rules }} |
| Copybooks | {{ total_copybooks }} |

## Architecture Overview

```mermaid
flowchart TB
    subgraph ONLINE["Online (CICS) Programs"]
{% for prog in online_programs[:12] %}
        {{ prog.program_id }}["{{ prog.program_id }}"]
{% endfor %}
    end

    subgraph BATCH["Batch Programs"]
{% for prog in batch_programs[:8] %}
        {{ prog.program_id }}["{{ prog.program_id }}"]
{% endfor %}
    end

{% for call in call_graph[:25] %}
{% if call.called_program and call.called_program != "UNKNOWN" %}
    {{ call.caller_program }} --> {{ call.called_program }}
{% endif %}
{% endfor %}

    USER([User/CSR]) --> ONLINE
    SCHEDULER([Job Scheduler]) --> BATCH
```

## Functional Modules

{% for module in modules %}
### [{{ module.business_name }}](modules/{{ module.module_name }}.md)

{{ module.business_purpose | default(module.business_name ~ " operations") }}

| Programs | Type |
|----------|------|
{% for prog in module.programs[:5] %}
| [{{ prog.program_id }}](programs/{{ prog.program_id }}.md) | {{ prog.program_type | default("BATCH") }} |
{% endfor %}
{% if module.programs | length > 5 %}
| *...{{ module.programs | length - 5 }} more* | |
{% endif %}

{% endfor %}

## Entry Points

Programs that are not called by others -- these are likely user-facing entry points:

{% for prog in entry_points %}
- [{{ prog }}](programs/{{ prog }}.md)
{% endfor %}

## Quick Navigation

| Section | Description |
|---------|-------------|
| [Program Documentation](programs/) | Detailed walkthrough for each COBOL program |
| [Linked Programs](clusters/INDEX.md) | Connected program clusters and dependency graphs |
| [Module Documentation](modules/) | Business-grouped program clusters |
| [Business Rules Catalog](business-rules/INDEX.md) | All extracted business rules |
| [Screen Catalog](screens/INDEX.md) | BMS screen definitions and layouts |
| [Call Graph](diagrams/call-graph.md) | Inter-program dependency diagram |
| [Data Dictionary](data-dictionary.md) | Complete variable listing |
| [Copybook Reference](copybook-reference.md) | Shared data structures |

---

*Generated by COBOL Documentation Pipeline*
'''

# ----- Layer 2: Module Documentation -----
TEMPLATES["module.md.j2"] = '''\
# Module: {{ business_name }}

> **Module ID:** `{{ module_name }}`  
> **Programs:** {{ programs | length }}

---

## Business Purpose

{{ business_purpose | default("This module groups related programs that handle " ~ business_name ~ " operations within the CardDemo application.") }}

## Programs in This Module

| Program | Type | Lines | Business Purpose |
|---------|------|-------|-----------------|
{% for prog in programs %}
| [{{ prog.program_id }}](../programs/{{ prog.program_id }}.md) | {{ prog.program_type | default("BATCH") }} | {{ prog.line_count | default(0) }} | {{ prog.business_purpose | default("-") | truncate(60) }} |
{% endfor %}

{% set valid_mod_calls = [] %}
{% for call in calls %}
{% if call.called_program and call.called_program != "UNKNOWN" %}
{% set _ = valid_mod_calls.append(call) %}
{% endif %}
{% endfor %}
{% if valid_mod_calls %}
## Internal Call Flow

Programs in this module interact through the following call chain:

```mermaid
flowchart LR
{% set seen = {} %}
{% for call in valid_mod_calls %}
{% set key = call.caller_program ~ "->" ~ call.called_program %}
{% if key not in seen %}
    {{ call.caller_program }}["{{ call.caller_program }}"] --> {{ call.called_program }}["{{ call.called_program }}"]
{% set _ = seen.update({key: true}) %}
{% endif %}
{% endfor %}
```

| Caller | Calls | Line |
|--------|-------|------|
{% set seen_mod_calls = {} %}
{% for call in valid_mod_calls %}
{% set key = call.caller_program ~ "->" ~ call.called_program %}
{% if key not in seen_mod_calls %}
| [{{ call.caller_program }}](../programs/{{ call.caller_program }}.md) | [{{ call.called_program }}](../programs/{{ call.called_program }}.md) | {{ call.line_number | default("-") }} |
{% set _ = seen_mod_calls.update({key: true}) %}
{% endif %}
{% endfor %}
{% endif %}

{% if screens %}
## Associated Screens

| Screen | Map | Mapset | Program |
|--------|-----|--------|---------|
{% for s in screens %}
| [{{ s.screen_name }}](../screens/{{ s.screen_name }}.md) | {{ s.map_name }} | {{ s.mapset_name }} | [{{ s.associated_program }}](../programs/{{ s.associated_program }}.md) |
{% endfor %}
{% endif %}

{% if files %}
## Data Files Used

| File | Type | Access | Program |
|------|------|--------|---------|
{% for f in files %}
| `{{ f.file_name }}` | {{ f.file_type | default("SEQUENTIAL") }} | {{ f.access_mode | default("-") }} | {{ f.program_id }} |
{% endfor %}
{% endif %}

---

*Generated {{ generated_date }}*
'''

# ----- Layer 3: Program Walkthrough -----
TEMPLATES["program.md.j2"] = '''\
# Program: {{ program_id }}

{% if business_name %}> **{{ business_name }}**{% endif %}

---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| Program ID | `{{ program_id }}` |
| Type | {{ program_type | default("BATCH") }} |
| Lines | {{ line_count | default(0) }} |
| Source | {{ file_path | code_link(1, file_path | basename) }} |
| Paragraphs | {{ paragraphs | length }} |
| Statements | {{ statements | length }} |
| Impact Risk | **{{ impact.risk | default("LOW") }}** — {{ impact.total_impact | default(0) }} programs affected |

> **View Source:** {{ file_path | code_link(1, "Open " ~ (file_path | basename)) }}

{% if business_purpose %}
## Business Purpose

{{ business_purpose }}

{% if user_role %}**Used By:** {{ user_role }}{% endif %}
{% if business_process %}  |  **Process:** {{ business_process }}{% endif %}
{% endif %}

{% if migration_complexity %}
## Migration Summary

| Attribute | Value |
|-----------|-------|
| Migration Complexity | **{{ migration_complexity }}/5** — {{ complexity_reason | default("-") }} |
| Modern Equivalent | {{ modern_equivalent | default("TBD") }} |
| Target Microservice | `{{ suggested_service | default("TBD") }}` |

{% if migration_approach %}
### How to Migrate This Program

{{ migration_approach }}
{% endif %}

{% if data_contracts %}
### Data Contracts (Input / Output)

{{ data_contracts }}
{% endif %}

{% if migration_risks %}
### Migration Risks

> ⚠️ {{ migration_risks }}
{% endif %}

{% if dependencies_to_migrate_first %}
### Migrate These First

The following programs should be migrated before this one:

{% for dep in dependencies_to_migrate_first %}
- [`{{ dep }}`]({{ dep }}.md)
{% endfor %}
{% endif %}

---
{% endif %}

## Dependency Context

> This section shows how **{{ program_id }}** connects to the rest of the system — who calls it,
> what it calls, and what data it shares. If linked programs exist, they must appear here.

### Programs That Call {{ program_id }} (Callers)

{% if dep_callers %}
| Caller | Type | Line | Why |
|--------|------|------|-----|
{% for c in dep_callers %}
| [{{ c.caller_program }}]({{ c.caller_program }}.md) | {{ c.program_type | default("-") }} | {{ c.line_number | default("-") }} | {{ c.business_purpose | default(c.business_name | default("Calls " ~ program_id)) | truncate(80) }} |
{% endfor %}
{% else %}
*No programs call {{ program_id }} — this is likely a top-level entry point or CICS transaction starter.*
{% endif %}

### Programs Called by {{ program_id }} (Callees)

{% if dep_callees %}
| Called Program | Type | Line | Why |
|----------------|------|------|-----|
{% for c in dep_callees %}
| [{{ c.called_program }}]({{ c.called_program }}.md) | {{ c.program_type | default("-") }} | {{ c.line_number | default("-") }} | {{ c.business_purpose | default(c.business_name | default("Called by " ~ program_id)) | truncate(80) }} |
{% endfor %}
{% else %}
*{{ program_id }} does not call any other programs (leaf program).*
{% endif %}

### Shared Data (Copybooks & Files)

{% if shared_copybooks %}
#### Shared Copybooks

| Copybook | Also Used By | # Co-Users |
|----------|-------------|------------|
{% for cb in shared_copybooks %}
| `{{ cb.copybook_name }}` | {{ cb.co_users[:5] | map(attribute="program_id") | join(", ") }}{% if cb.co_user_count > 5 %} (+{{ cb.co_user_count - 5 }} more){% endif %} | {{ cb.co_user_count }} |
{% endfor %}
{% else %}
*No shared copybooks.*
{% endif %}

{% if shared_files %}
#### Shared Files

| File | Type | Access | Also Used By |
|------|------|--------|-------------|
{% for f in shared_files %}
| `{{ f.file_name }}` | {{ f.file_type | default("-") }} | {{ f.access_mode | default("-") }} | {{ f.co_users[:5] | map(attribute="program_id") | join(", ") }}{% if f.co_user_count > 5 %} (+{{ f.co_user_count - 5 }} more){% endif %} |
{% endfor %}
{% endif %}

---

## Dependency Graph

```mermaid
flowchart TD
{% for c in dep_callers %}
    {{ c.caller_program | mermaid_id }}["{{ c.caller_program }}"]:::caller
{% endfor %}
    {{ program_id | mermaid_id }}["⬤ {{ program_id }}"]:::target
{% for c in dep_callees %}
    {{ c.called_program | mermaid_id }}["{{ c.called_program }}"]:::callee
{% endfor %}
{% for c in dep_callers %}
    {{ c.caller_program | mermaid_id }} --> {{ program_id | mermaid_id }}
{% endfor %}
{% for c in dep_callees %}
    {{ program_id | mermaid_id }} --> {{ c.called_program | mermaid_id }}
{% endfor %}
{% for cb in shared_copybooks[:8] %}
{% if cb.co_user_count > 0 %}
    {{ cb.copybook_name | mermaid_cb_node }}
    {{ program_id | mermaid_id }} -.- CB_{{ cb.copybook_name | mermaid_id }}
{% for u in cb.co_users[:3] %}
    {{ u.program_id | mermaid_id }}["{{ u.program_id }}"]:::coupled
    CB_{{ cb.copybook_name | mermaid_id }} -.- {{ u.program_id | mermaid_id }}
{% endfor %}
{% endif %}
{% endfor %}
{% if impact.transitive_callers %}
{% for tc in impact.transitive_callers[:5] %}
{% if tc not in dep_callers | map(attribute="caller_program") | list %}
    {{ tc | mermaid_id }}["{{ tc }}"]:::transitive
    {{ tc | mermaid_id }} -.-> {{ program_id | mermaid_id }}
{% endif %}
{% endfor %}
{% endif %}
{% if impact.transitive_callees %}
{% for tc in impact.transitive_callees[:5] %}
{% if tc not in dep_callees | map(attribute="called_program") | list %}
    {{ tc | mermaid_id }}["{{ tc }}"]:::transitive
    {{ program_id | mermaid_id }} -.-> {{ tc | mermaid_id }}
{% endif %}
{% endfor %}
{% endif %}
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

> **If you change {{ program_id }}, what else could break?**

| Impact Metric | Count |
|--------------|-------|
| Direct Callers | {{ impact.direct_callers | length }} |
| Transitive Callers (callers of callers) | {{ impact.transitive_callers | length }} |
| Direct Callees | {{ impact.direct_callees | length }} |
| Transitive Callees | {{ impact.transitive_callees | length }} |
| Copybook-Coupled Programs | {{ impact.copybook_coupling | length }} |
| **Total Impact** | **{{ impact.total_impact }}** |
| **Risk Rating** | **{{ impact.risk }}** |

{% if impact.transitive_callers %}
**Programs that would break (transitive callers):**
{% for p in impact.transitive_callers %}
- `{{ p }}`
{% endfor %}
{% endif %}

{% if impact.copybook_coupling %}
**Programs affected via shared copybooks:**
{% for p in impact.copybook_coupling %}
- `{{ p }}`
{% endfor %}
{% endif %}

---

## Statement Profile

{% if stmt_summary %}
| Statement Type | Count |
|---------------|-------|
{% for stype, count in stmt_summary.items() %}
| {{ stype }} | {{ count }} |
{% endfor %}
{% endif %}

## Control Flow

```mermaid
flowchart TD
    START([Program Entry])
{% for para in paragraphs[:15] %}
    {{ para.paragraph_name | mermaid_id }}["{{ para.paragraph_name }}"]
{% endfor %}
{% if paragraphs %}
    START --> {{ paragraphs[0].paragraph_name | mermaid_id }}
{% endif %}
{% set seen = {} %}
{% for perf in performs[:20] %}
{% set key = perf.source_paragraph ~ "->" ~ perf.target_paragraph %}
{% if key not in seen %}
    {{ perf.source_paragraph | mermaid_id }} --> {{ perf.target_paragraph | mermaid_id }}
{% set _ = seen.update({key: true}) %}
{% endif %}
{% endfor %}
```

## Paragraphs

{% for para in paragraphs %}
### {{ para.business_name if para.business_name else para.paragraph_name }}

| | |
|---|---|
| **Paragraph** | `{{ para.paragraph_name }}` |
| **Lines** | {{ para.line_start | default("?") }} - {{ para.line_end | default("?") }} |
| **View Code** | {{ file_path | code_link(para.line_start, "Jump to Line " ~ (para.line_start | string)) }} |

{% if para.narrative %}
{{ para.narrative }}
{% endif %}

{% if para.purpose %}
> **Purpose:** {{ para.purpose }}
{% endif %}

{% endfor %}

{% if jcl_jobs %}
## Executed by JCL Jobs

This program is run by the following batch JCL jobs:

| Job Name | Step | Step Comments |
|----------|------|---------------|
{% for j in jcl_jobs %}
| [{{ j.job_name }}](../jcl/{{ j.job_name }}.md) | `{{ j.step_name }}` | {{ j.step_comments | default("-") | truncate(80) }} |
{% endfor %}

{% endif %}

## Business Rules

{% if business_rules %}
{% for rule in business_rules %}
- **{{ rule.rule_name }}** `{{ rule.rule_id }}`  
  {{ rule.rule_statement }}  
  [View Rule Details](../business-rules/{{ rule.rule_id }}.md)
{% endfor %}
{% else %}
*No business rules extracted yet. Run LLM enrichment to extract rules from IF/EVALUATE logic.*
{% endif %}

## Key Data Items

{% if data_items %}
| Name | Level | Picture | Section | Business Name |
|------|-------|---------|---------|---------------|
{% for item in data_items[:40] %}
| `{{ item.name }}` | {{ item.level_number | default("-") }} | `{{ item.picture | default("-") }}` | {{ item.section | default("-") }} | {{ item.business_name | default("-") }} |
{% endfor %}
{% if data_items | length > 40 %}

*Showing 40 of {{ data_items | length }} data items. See [Data Dictionary](../data-dictionary.md).*
{% endif %}
{% else %}
*No data items found for this program.*
{% endif %}

---

*Generated {{ generated_date }}*
'''

# ----- Layer 4: Business Rules -----
TEMPLATES["business_rule.md.j2"] = '''\
# Business Rule: {{ rule_name }}

| Attribute | Value |
|-----------|-------|
| Rule ID | `{{ rule_id }}` |
| Category | {{ category | default("GENERAL") }} |
| Program | [{{ program_id }}](../programs/{{ program_id }}.md) |
| Paragraph | `{{ paragraph_name | default("-") }}` |
{% if line_start %}| Lines | {{ line_start }} - {{ line_end | default("") }} |{% endif %}

## Rule Statement

> {{ rule_statement }}

## Condition

{{ condition_text | default(condition) | default("When specific business conditions are met") }}

## Action

{{ action_text | default(action) | default("System performs the defined business action") }}

{% if source_code %}
## Source Code

```cobol
{{ source_code }}
```
{% endif %}

---

*Generated {{ generated_date }}*
'''

TEMPLATES["business_rules_index.md.j2"] = '''\
# Business Rules Catalog

> **Total Rules:** {{ rules | length }}  
> **Categories:** {{ categories | length }}

---

{% for category, cat_rules in rules_by_category.items() %}
## {{ category }} ({{ cat_rules | length }} rules)

| Rule ID | Name | Statement | Program |
|---------|------|-----------|---------|
{% for rule in cat_rules %}
| [{{ rule.rule_id }}]({{ rule.rule_id }}.md) | {{ rule.rule_name }} | {{ rule.rule_statement | truncate(60) }} | [{{ rule.program_id }}](../programs/{{ rule.program_id }}.md) |
{% endfor %}

{% endfor %}

{% if not rules %}
*No business rules have been extracted yet. Run the LLM enrichment step to extract rules from IF/EVALUATE statements.*
{% endif %}

---

*Generated {{ generated_date }}*
'''

# ----- Layer 5: Screen Documentation -----
TEMPLATES["screen.md.j2"] = '''\
# Screen: {{ screen_name }}

| Attribute | Value |
|-----------|-------|
| Map Name | `{{ map_name }}` |
| Mapset | `{{ mapset_name }}` |
{% if associated_program %}| Program | [{{ associated_program }}](../programs/{{ associated_program }}.md) |{% endif %}
{% if transaction_id %}| Transaction ID | `{{ transaction_id }}` |{% endif %}

## Screen Layout

The following fields are defined in this BMS map:

{% if input_fields %}
### Input Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
{% for f in input_fields %}
| `{{ f.field_name }}` | {{ f.row_position }} | {{ f.col_position }} | {{ f.length | default(0) }} | {{ f.attributes | default("-") }} |
{% endfor %}
{% endif %}

{% if output_fields %}
### Output / Display Fields

| Field | Row | Col | Length | Attributes |
|-------|-----|-----|--------|------------|
{% for f in output_fields %}
| `{{ f.field_name }}` | {{ f.row_position }} | {{ f.col_position }} | {{ f.length | default(0) }} | {{ f.attributes | default("-") }} |
{% endfor %}
{% endif %}

{% if label_fields %}
### Labels / Decorations

| Label Text | Row | Col |
|------------|-----|-----|
{% for f in label_fields %}
| {{ f.description | default(f.field_name) }} | {{ f.row_position }} | {{ f.col_position }} |
{% endfor %}
{% endif %}

## Visual Mockup

```
{% for row_num in range(1, max_row + 1) %}
{% set row_fields = fields_by_row.get(row_num, []) %}
{% if row_fields %}
Row {{ "%2d" | format(row_num) }}: {% for f in row_fields %}{{ f.description | default(f.field_name) | default("____") }}  {% endfor %}

{% endif %}
{% endfor %}
```

---

*Generated {{ generated_date }}*
'''

TEMPLATES["screens_index.md.j2"] = '''\
# Screen Catalog

> **Total Screens:** {{ screens | length }}

---

| Screen | Map | Mapset | Program | Fields |
|--------|-----|--------|---------|--------|
{% for s in screens %}
| [{{ s.screen_name }}]({{ s.screen_name }}.md) | `{{ s.map_name | default("-") }}` | `{{ s.mapset_name | default("-") }}` | {% if s.associated_program %}[{{ s.associated_program }}](../programs/{{ s.associated_program }}.md){% else %}-{% endif %} | {{ s.field_names | default("-") }} |
{% endfor %}

---

*Generated {{ generated_date }}*
'''

# ----- Call Graph -----
TEMPLATES["call_graph.md.j2"] = '''\
# Program Call Hierarchy

> Inter-program call relationships across the entire {{ system_name }} application.

## Visual Call Graph

```mermaid
graph LR
{% set seen = {} %}
{% for call in calls %}
{% if call.called_program and call.called_program != "UNKNOWN" %}
{% set key = call.caller_program ~ "->" ~ call.called_program %}
{% if key not in seen %}
    {{ call.caller_program }}["{{ call.caller_name if call.caller_name else call.caller_program }}"] --> {{ call.called_program }}["{{ call.called_name if call.called_name else call.called_program }}"]
{% set _ = seen.update({key: true}) %}
{% endif %}
{% endif %}
{% endfor %}
```

## Call Matrix

| Caller | Calls | Line |
|--------|-------|------|
{% for call in calls %}
{% if call.called_program and call.called_program != "UNKNOWN" %}
| [{{ call.caller_program }}](../programs/{{ call.caller_program }}.md) | [{{ call.called_program }}](../programs/{{ call.called_program }}.md) | {{ call.line_number | default("-") }} |
{% endif %}
{% endfor %}

## Entry Points

Programs not called by any other program (likely top-level entry points or CICS transaction starters):

{% for prog in entry_points %}
- [{{ prog }}](../programs/{{ prog }}.md)
{% endfor %}

## Leaf Programs

Programs that don't call any other program (utility or terminal logic):

{% for prog in leaf_programs %}
- [{{ prog }}](../programs/{{ prog }}.md)
{% endfor %}

---

*Generated {{ generated_date }}*
'''

# ----- Data Dictionary -----
TEMPLATES["data_dictionary.md.j2"] = '''\
# Data Dictionary

> **Total Data Items:** {{ total_items }}  
> **Programs:** {{ programs_count }}

---

{% for section, items in items_by_section.items() %}
## {{ section }} Section ({{ items | length }} items)

| Name | Level | Picture | Program | Business Name |
|------|-------|---------|---------|---------------|
{% for item in items[:100] %}
| `{{ item.name }}` | {{ item.level_number | default("-") }} | `{{ item.picture | default("-") }}` | [{{ item.program_id }}](programs/{{ item.program_id }}.md) | {{ item.business_name | default("-") }} |
{% endfor %}
{% if items | length > 100 %}

*Showing 100 of {{ items | length }} items in {{ section }}.*
{% endif %}

{% endfor %}

---

*Generated {{ generated_date }}*
'''

# ----- JCL Job Index -----
TEMPLATES["jcl_index.md.j2"] = '''\
# JCL Jobs Catalog

> **Total Jobs:** {{ jobs | length }}
> All batch JCL jobs found in the repository.

---

| Job Name | File | Description | Steps | Programs Called |
|----------|------|-------------|-------|----------------|
{% for job in jobs %}
| [{{ job.job_name }}]({{ job.job_name }}.md) | `{{ job.file_name }}` | {{ job.job_description | default("-") | truncate(50) }} | {{ job.step_count | default(0) }} | {{ job.programs_called | join(", ") if job.programs_called else "-" }} |
{% endfor %}

---

*Generated {{ generated_date }}*
'''

# ----- JCL Job Detail -----
TEMPLATES["jcl_job.md.j2"] = '''\
# JCL Job: {{ job_name }}

| Attribute | Value |
|-----------|-------|
| File | `{{ file_name }}` |
| Description | {{ job_description | default("-") }} |
| Job Class | {{ job_class | default("-") }} |
| Msg Class | {{ msg_class | default("-") }} |
| Steps | {{ steps | length }} |

{% if header_comments %}
## Job Description (Comments)

```
{{ header_comments }}
```
{% endif %}

## Job Steps

{% for step in steps %}
### Step {{ loop.index }}: {{ step.step_name }}

| Attribute | Value |
|-----------|-------|
| Step Name | `{{ step.step_name }}` |
| Type | {{ step.step_type | default("-") }} |
{% if step.program %}| Program | {% if step.program_is_cobol %}[{{ step.program }}](../programs/{{ step.program }}.md){% else %}`{{ step.program }}`{% endif %} |{% endif %}
{% if step.proc %}| Procedure | `{{ step.proc }}` |{% endif %}
{% if step.cond %}| COND | `{{ step.cond }}` |{% endif %}

{% if step.step_comments %}
> {{ step.step_comments | replace("\n", "  \n> ") }}
{% endif %}

{% if step.datasets %}
#### Datasets (DD Cards)

| DD Name | Dataset Name | DISP | Direction | RECFM | LRECL |
|---------|-------------|------|-----------|-------|-------|
{% for ds in step.datasets %}
{% if not ds.is_inline %}
| `{{ ds.dd_name }}` | `{{ ds.dsn | default("-") }}` | {{ ds.disp | default("-") }} | {{ ds.direction | default("-") }} | {{ ds.recfm | default("-") }} | {{ ds.lrecl | default("-") }} |
{% endif %}
{% endfor %}
{% endif %}

{% if step.sysin_data %}
#### Inline SYSIN

```
{% for line in step.sysin_data %}
{{ line }}
{% endfor %}
```
{% endif %}

---
{% endfor %}

## Summary

{% if programs_called %}
### COBOL Programs Executed

{% for prog in programs_called %}
- [{{ prog }}](../programs/{{ prog }}.md)
{% endfor %}
{% endif %}

{% if input_datasets %}
### Input Datasets

{% for dsn in input_datasets %}
- `{{ dsn }}`
{% endfor %}
{% endif %}

{% if output_datasets %}
### Output Datasets

{% for dsn in output_datasets %}
- `{{ dsn }}`
{% endfor %}
{% endif %}

---

*Generated {{ generated_date }}*
'''

# ----- Copybook Reference -----
TEMPLATES["copybook_reference.md.j2"] = '''\
# Copybook Reference

> **Total Copybooks:** {{ copybooks | length }}

Copybooks are shared data structure definitions included (COPY) by multiple programs.

---

| Copybook | Used By Programs | Business Name |
|----------|-----------------|---------------|
{% for cb in copybooks %}
| `{{ cb.copybook_name }}` | {{ cb.used_by | default("-") }} | {{ cb.business_name | default("-") }} |
{% endfor %}

---

*Generated {{ generated_date }}*
'''

# ----- Layer 6: Linked Programs (Clusters) -----
TEMPLATES["cluster.md.j2"] = '''\
# Linked Programs: Cluster {{ cluster_id }}

> **{{ size }} interconnected programs** linked through call relationships and shared copybooks.

---

## Why These Programs Are Linked

These programs form a connected cluster because they either call each other directly,
share copybook data structures, or are transitively linked through intermediate programs.
A change to any one of them has the potential to affect the others.

## Programs in This Cluster

| Program | Type | Business Name |
|---------|------|---------------|
{% for m in member_details %}
| [{{ m.program_id }}](../programs/{{ m.program_id }}.md) | {{ m.program_type | default("-") }} | {{ m.business_name | default("-") }} |
{% endfor %}

## Internal Call Flow

{% if internal_calls %}
```mermaid
graph LR
{% set seen = {} %}
{% for call in internal_calls %}
{% set key = call.caller_program ~ "->" ~ call.called_program %}
{% if key not in seen %}
    {{ call.caller_program | mermaid_id }}["{{ call.caller_program }}"] --> {{ call.called_program | mermaid_id }}["{{ call.called_program }}"]
{% set _ = seen.update({key: true}) %}
{% endif %}
{% endfor %}
```

| Caller | Calls | Line |
|--------|-------|------|
{% for call in internal_calls %}
| [{{ call.caller_program }}](../programs/{{ call.caller_program }}.md) | [{{ call.called_program }}](../programs/{{ call.called_program }}.md) | {{ call.line_number | default("-") }} |
{% endfor %}
{% else %}
*No direct call relationships between these programs — they are linked exclusively through shared copybooks.*
{% endif %}

{% if shared_copybooks %}
## Shared Copybooks (Data Coupling)

These copybooks are shared by 2+ programs in this cluster. Changing them affects multiple programs:

| Copybook | Shared By |
|----------|-----------|
{% for cb in shared_copybooks %}
| `{{ cb.copybook_name }}` | {{ cb.programs }} |
{% endfor %}
{% endif %}

---

*Generated {{ generated_date }}*
'''

TEMPLATES["clusters_index.md.j2"] = '''\
# Linked Programs Index

> **{{ clusters | length }} clusters** detected across the system.
> Programs are grouped by call relationships and shared copybook data coupling.

---

{% set connected = clusters | selectattr("is_standalone", "false") | list %}
{% set standalone = clusters | selectattr("is_standalone", "true") | list %}

## Connected Clusters ({{ connected | length }})

{% if connected %}
| Cluster | Programs | Internal Calls | Shared Copybooks |
|---------|----------|---------------|------------------|
{% for c in connected %}
| [Cluster {{ c.cluster_id }}](CLUSTER-{{ c.cluster_id }}.md) | {{ c.size }} | {{ c.internal_calls | length }} | {{ c.shared_copybooks | length }} |
{% endfor %}
{% else %}
*No multi-program clusters detected.*
{% endif %}

## Standalone Programs ({{ standalone | length }})

These programs have no call or copybook relationships with other programs:

{% for c in standalone %}
- [{{ c.members[0] }}](../programs/{{ c.members[0] }}.md)
{% endfor %}

---

*Generated {{ generated_date }}*
'''


# ============================================================
# Documentation Generator
# ============================================================

class DocGenerator:
    """Generates complete Swimm-style documentation from SQLite knowledge base."""

    def __init__(
        self,
        db_loader,
        output_dir: str = "docs",
        templates_dir: str = None,
        repo_path: str = None,
        system_name: str = "CardDemo",
    ):
        self.db = db_loader
        self.output_dir = Path(output_dir)
        self.repo_path = repo_path
        self.system_name = system_name

        self.env = Environment(
            loader=InlineTemplateLoader(TEMPLATES, templates_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Custom filters
        self.env.filters["basename"] = lambda x: Path(x).name if x else ""
        self.env.filters["truncate"] = lambda x, n: (x[:n] + "...") if x and len(str(x)) > n else (x or "")
        self.env.filters["mermaid_id"] = lambda x: (x or "UNKNOWN").replace("-", "_").replace(" ", "_")

        def mermaid_cb_node(cb_name, node_id_prefix="CB_"):
            """Generate a full Mermaid copybook node line with hexagon shape.
            Uses {{ }} which is Mermaid hexagon syntax — this filter outputs it
            as a raw string to avoid Jinja2 clash."""
            safe_id = (cb_name or "UNKNOWN").replace("-", "_").replace(" ", "_")
            node_id = f"{node_id_prefix}{safe_id}"
            # Double curly braces in Python f-string become literal { }
            return f'{node_id}{{{{"{cb_name}"}}}}:::copybook'

        self.env.filters["mermaid_cb_node"] = mermaid_cb_node
        
        # Live code link filter - generates clickable source links
        def code_link(file_path, line=None, text=None):
            """Generate a clickable link to source code.
            
            Supports:
            - VS Code: Opens file at line when clicked in VS Code markdown preview
            - GitHub: #L{line} anchors work in GitHub
            - Relative paths for portability
            """
            if not file_path:
                return text or "source"
            
            # Make path relative to docs folder for portability
            try:
                rel_path = Path(file_path).as_posix()
                # Calculate relative path from docs to repo
                if repo_path:
                    rel_path = f"../{repo_path}/{Path(file_path).name}"
            except:
                rel_path = file_path
            
            display = text or Path(file_path).name
            
            if line and int(line) > 0:
                # GitHub-style line anchor + VS Code compatible
                return f"[{display}]({rel_path}#L{line})"
            else:
                return f"[{display}]({rel_path})"
        
        self.env.filters["code_link"] = code_link
        
        # Store repo_path for the filter
        self.env.globals["repo_path"] = repo_path

    def generate_all(self):
        """Generate all 6 documentation layers plus supporting docs."""
        console.print("[cyan]Generating Swimm-style documentation...[/cyan]")

        # Create output directories
        for subdir in ["programs", "modules", "business-rules", "screens", "diagrams", "clusters", "jcl"]:
            (self.output_dir / subdir).mkdir(parents=True, exist_ok=True)

        generated = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Layer 1: System Overview
        self._generate_system_overview(generated)

        # Layer 2: Linked Programs (Clusters)
        self._generate_linked_clusters(generated)

        # Layer 3: Module Documentation
        self._generate_module_docs(generated)

        # Layer 4: Program Walkthroughs (with dependency + impact)
        self._generate_program_docs(generated)

        # Layer 5: Business Rules Catalog
        self._generate_business_rules(generated)

        # Layer 6: Screen Catalog
        self._generate_screen_docs(generated)

        # Supporting: Call Graph, Data Dictionary, Copybook Reference, JCL
        self._generate_call_graph(generated)
        self._generate_data_dictionary(generated)
        self._generate_copybook_reference(generated)
        self._generate_jcl_docs(generated)

        total = len(list(self.output_dir.rglob("*.md")))
        console.print(f"[green]OK - Generated {total} documentation files in {self.output_dir}[/green]")

    # ================================================================
    # Layer 1: System Overview
    # ================================================================

    def _generate_system_overview(self, generated_date: str):
        console.print("  [cyan]Layer 1: System Overview[/cyan]")

        programs = self.db.get_all_programs()
        call_graph = self.db.get_call_graph()
        modules = self.db.get_all_modules()
        rules = self.db.get_all_business_rules()
        screens = self.db.get_all_screens()
        copybooks = self.db.get_copybooks()

        # Compute stats
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM data_items")
        total_data_items = cursor.fetchone()[0]

        online = [p for p in programs if (p.get("program_type") or "").upper() == "ONLINE"]
        batch = [p for p in programs if (p.get("program_type") or "").upper() != "ONLINE"]

        # Entry points
        called_set = set(c["called_program"] for c in call_graph)
        all_set = set(p["program_id"] for p in programs)
        entry_points = sorted(all_set - called_set)

        template = self.env.get_template("system_overview.md.j2")
        content = template.render(
            system_name=self.system_name,
            total_programs=len(programs),
            total_modules=len(modules),
            total_screens=len(screens),
            total_data_items=total_data_items,
            total_calls=len(call_graph),
            total_rules=len(rules),
            total_copybooks=len(copybooks),
            online_programs=online,
            batch_programs=batch,
            call_graph=call_graph,
            modules=modules,
            entry_points=entry_points,
            generated_date=generated_date,
        )
        (self.output_dir / "00-SYSTEM-OVERVIEW.md").write_text(content, encoding="utf-8")

    # ================================================================
    # Layer 2: Linked Programs (Clusters)
    # ================================================================

    def _generate_linked_clusters(self, generated_date: str):
        console.print("  [cyan]Layer 2: Linked Programs (Clusters)[/cyan]")

        clusters = self.db.get_linked_clusters()

        # Generate individual cluster files
        cluster_template = self.env.get_template("cluster.md.j2")
        for cluster in clusters:
            if cluster["is_standalone"]:
                continue  # Don't generate individual files for standalone programs
            content = cluster_template.render(
                **cluster,
                generated_date=generated_date,
            )
            (self.output_dir / "clusters" / f"CLUSTER-{cluster['cluster_id']}.md").write_text(
                content, encoding="utf-8"
            )

        # Generate index
        index_template = self.env.get_template("clusters_index.md.j2")
        content = index_template.render(
            clusters=clusters,
            generated_date=generated_date,
        )
        (self.output_dir / "clusters" / "INDEX.md").write_text(content, encoding="utf-8")

        connected = [c for c in clusters if not c["is_standalone"]]
        standalone = [c for c in clusters if c["is_standalone"]]
        console.print(f"[green]OK - {len(connected)} connected clusters, "
                      f"{len(standalone)} standalone programs[/green]")

    # ================================================================
    # Layer 3: Module Documentation
    # ================================================================

    def _generate_module_docs(self, generated_date: str):
        console.print("  [cyan]Layer 2: Module Documentation[/cyan]")

        modules = self.db.get_all_modules()

        with Progress(SpinnerColumn(), TextColumn("{task.description}"),
                       BarColumn(), console=console) as progress:
            task = progress.add_task("Modules...", total=len(modules))

            for mod in modules:
                details = self.db.get_module_details(mod["id"])
                if details:
                    template = self.env.get_template("module.md.j2")
                    content = template.render(
                        **details,
                        generated_date=generated_date,
                    )
                    fname = details["module_name"].replace(" ", "_").upper()
                    (self.output_dir / "modules" / f"{fname}.md").write_text(content, encoding="utf-8")

                progress.advance(task)

    # ================================================================
    # Layer 3: Program Walkthroughs
    # ================================================================

    def _generate_program_docs(self, generated_date: str):
        console.print("  [cyan]Layer 4: Program Walkthroughs (with dependencies + impact)[/cyan]")

        programs = self.db.get_all_programs()
        template = self.env.get_template("program.md.j2")

        with Progress(SpinnerColumn(), TextColumn("{task.description}"),
                       BarColumn(), console=console) as progress:
            task = progress.add_task("Programs...", total=len(programs))

            for prog_summary in programs:
                pid = prog_summary["program_id"]
                details = self.db.get_program_details(pid)

                if details:
                    stmt_summary = self.db.get_statement_summary(pid)

                    # Fetch dependency context
                    deps = self.db.get_program_dependencies(pid)
                    shared = self.db.get_shared_data_context(pid)
                    impact = self.db.get_impact_analysis(pid)

                    # Parse JSON list field back to a Python list for the template
                    deps_raw = details.pop("dependencies_to_migrate_first", None) or "[]"
                    try:
                        deps_list = json.loads(deps_raw) if isinstance(deps_raw, str) else (deps_raw or [])
                    except Exception:
                        deps_list = []

                    jcl_jobs_for_prog = self.db.get_program_jcl_jobs(pid)

                    content = template.render(
                        **details,
                        stmt_summary=stmt_summary,
                        dep_callers=deps["callers"],
                        dep_callees=deps["callees"],
                        shared_copybooks=shared["shared_copybooks"],
                        shared_files=shared["shared_files"],
                        impact=impact,
                        dependencies_to_migrate_first=deps_list,
                        jcl_jobs=jcl_jobs_for_prog,
                        generated_date=generated_date,
                    )
                    (self.output_dir / "programs" / f"{pid}.md").write_text(content, encoding="utf-8")

                progress.advance(task)

    # ================================================================
    # Layer 4: Business Rules Catalog
    # ================================================================

    def _generate_business_rules(self, generated_date: str):
        console.print("  [cyan]Layer 4: Business Rules Catalog[/cyan]")

        rules = self.db.get_all_business_rules()

        # Generate individual rule files
        if rules:
            rule_template = self.env.get_template("business_rule.md.j2")
            for rule in rules:
                content = rule_template.render(**rule, generated_date=generated_date)
                safe_id = (rule["rule_id"] or "UNKNOWN").replace("/", "_")
                (self.output_dir / "business-rules" / f"{safe_id}.md").write_text(content, encoding="utf-8")

        # Generate index
        rules_by_category = defaultdict(list)
        for rule in rules:
            cat = rule.get("category") or "GENERAL"
            rules_by_category[cat].append(rule)

        index_template = self.env.get_template("business_rules_index.md.j2")
        content = index_template.render(
            rules=rules,
            rules_by_category=dict(rules_by_category),
            categories=dict(rules_by_category),
            generated_date=generated_date,
        )
        (self.output_dir / "business-rules" / "INDEX.md").write_text(content, encoding="utf-8")

    # ================================================================
    # Layer 5: Screen Catalog
    # ================================================================

    def _generate_screen_docs(self, generated_date: str):
        console.print("  [cyan]Layer 5: Screen Catalog[/cyan]")

        screens = self.db.get_all_screens()

        for screen_summary in screens:
            sid = screen_summary.get("id")
            details = self.db.get_screen_details(sid)
            if not details:
                continue

            fields = details.get("fields", [])

            # Separate field types
            input_fields = [f for f in fields if (f.get("field_type") or "").upper() == "INPUT"]
            output_fields = [f for f in fields if (f.get("field_type") or "").upper() == "OUTPUT"]
            label_fields = [f for f in fields if (f.get("field_type") or "").upper() == "LABEL"]

            # Group by row for visual mockup
            fields_by_row = defaultdict(list)
            max_row = 0
            for f in fields:
                row = f.get("row_position") or 0
                if row > 0:
                    fields_by_row[row].append(f)
                    max_row = max(max_row, row)

            template = self.env.get_template("screen.md.j2")
            content = template.render(
                **details,
                input_fields=input_fields,
                output_fields=output_fields,
                label_fields=label_fields,
                fields_by_row=dict(fields_by_row),
                max_row=max_row,
                generated_date=generated_date,
            )
            screen_name = details.get("screen_name") or f"SCREEN_{sid}"
            (self.output_dir / "screens" / f"{screen_name}.md").write_text(content, encoding="utf-8")

        # Index
        index_template = self.env.get_template("screens_index.md.j2")
        content = index_template.render(screens=screens, generated_date=generated_date)
        (self.output_dir / "screens" / "INDEX.md").write_text(content, encoding="utf-8")

    # ================================================================
    # Supporting: Call Graph
    # ================================================================

    def _generate_call_graph(self, generated_date: str):
        console.print("  [cyan]Diagram: Call Graph[/cyan]")

        calls = self.db.get_call_graph()
        programs = self.db.get_all_programs()

        called_set = set(c["called_program"] for c in calls)
        caller_set = set(c["caller_program"] for c in calls)
        all_set = set(p["program_id"] for p in programs)

        entry_points = sorted(all_set - called_set)
        leaf_programs = sorted(all_set - caller_set)

        template = self.env.get_template("call_graph.md.j2")
        content = template.render(
            system_name=self.system_name,
            calls=calls,
            entry_points=entry_points,
            leaf_programs=leaf_programs,
            generated_date=generated_date,
        )
        (self.output_dir / "diagrams" / "call-graph.md").write_text(content, encoding="utf-8")

    # ================================================================
    # Supporting: Data Dictionary
    # ================================================================

    def _generate_data_dictionary(self, generated_date: str):
        console.print("  [cyan]Reference: Data Dictionary[/cyan]")

        items = self.db.get_data_dictionary()
        programs = self.db.get_all_programs()

        # Group by section
        items_by_section = defaultdict(list)
        for item in items:
            section = item.get("section") or "OTHER"
            items_by_section[section].append(item)

        template = self.env.get_template("data_dictionary.md.j2")
        content = template.render(
            total_items=len(items),
            programs_count=len(programs),
            items_by_section=dict(items_by_section),
            generated_date=generated_date,
        )
        (self.output_dir / "data-dictionary.md").write_text(content, encoding="utf-8")

    # ================================================================
    # Supporting: Copybook Reference
    # ================================================================

    def _generate_copybook_reference(self, generated_date: str):
        console.print("  [cyan]Reference: Copybook Reference[/cyan]")

        copybooks = self.db.get_copybooks()

        template = self.env.get_template("copybook_reference.md.j2")
        content = template.render(
            copybooks=copybooks,
            generated_date=generated_date,
        )
        (self.output_dir / "copybook-reference.md").write_text(content, encoding="utf-8")

    # ================================================================
    # JCL Documentation
    # ================================================================

    def _generate_jcl_docs(self, generated_date: str):
        console.print("  [cyan]JCL: Job Catalog[/cyan]")

        jobs = self.db.get_all_jcl_jobs()
        if not jobs:
            console.print("  [yellow]  No JCL jobs in database — skipping JCL docs[/yellow]")
            return

        # Set of known COBOL program IDs for linking
        known_programs = {p["program_id"] for p in self.db.get_all_programs()}

        # Generate index
        idx_template = self.env.get_template("jcl_index.md.j2")
        idx_content = idx_template.render(jobs=jobs, generated_date=generated_date)
        (self.output_dir / "jcl" / "INDEX.md").write_text(idx_content, encoding="utf-8")

        # Generate one page per job
        job_template = self.env.get_template("jcl_job.md.j2")
        for job in jobs:
            details = self.db.get_jcl_job_details(job["job_name"])
            if not details:
                continue
            # Mark which step programs are known COBOL programs
            for step in details.get("steps") or []:
                step["program_is_cobol"] = (step.get("program") or "").upper() in known_programs
            content = job_template.render(**details, generated_date=generated_date)
            safe_name = details["job_name"].replace("/", "_")
            (self.output_dir / "jcl" / f"{safe_name}.md").write_text(content, encoding="utf-8")

        console.print(f"  [green]OK - Generated {len(jobs)} JCL job docs in docs/jcl/[/green]")

        # Also annotate program docs: which JCL jobs call them
        # (stored in program details page via get_program_jcl_jobs)


# ============================================================
# CLI Entry Point
# ============================================================

if __name__ == "__main__":
    import argparse
    from sqlite_loader import SQLiteLoader

    parser = argparse.ArgumentParser(description="Generate Swimm-style COBOL documentation")
    parser.add_argument("--db", default="data/cobol_knowledge.db", help="Database path")
    parser.add_argument("--output", "-o", default="docs", help="Output directory")
    parser.add_argument("--templates", help="Custom templates directory")
    parser.add_argument("--repo", help="Source repository path")
    parser.add_argument("--name", default="CardDemo", help="System name")

    args = parser.parse_args()

    loader = SQLiteLoader(args.db)
    loader.connect()

    generator = DocGenerator(
        db_loader=loader,
        output_dir=args.output,
        templates_dir=args.templates,
        repo_path=args.repo,
        system_name=args.name,
    )
    generator.generate_all()

    loader.close()
