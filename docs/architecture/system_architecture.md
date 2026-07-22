# FREE BASICS AI MARKETING SYSTEM / FBEP

## System Architecture

Owner:
Samy Jendoubi

Repository:
smartsamy41/ai-marketing-system

Cloud:
Google Cloud Run

Project:
smartcontent2050

Domain:
https://freebasics.online


## Architecture Principle

Das System wird nicht neu aufgebaut.
Bestehende Produktionskomponenten bilden die Basis.

FREE-BASICS-PRODUCTION-MASTER dient als Governance- und Dokumentationsschicht.


## Core Components

### Application Layer

app/

- main.py
- schema_generator.py
- product_templates.py
- geo/


### GEO Engine

app/geo/

- Entity Registry
- Fact Registry
- GEO Service
- JSON-LD Pipeline
- Schema Validation


### Knowledge Layer

knowledge/

- entities
- facts
- sources
- legal


### Engine Layer

engine/

- Content Engine
- Affiliate Engine
- Automation Engine
- Learning Engine
- Performance Engine


### Data Layer

- Google Sheets
- BigQuery
- Tracking Daten


### Infrastructure

- Docker
- Cloud Run
- Python Runtime


### Validation

- audits/
- compliance checks
- GEO validation


## Data Flow

Product Data
→ Knowledge Layer
→ Content Engine
→ GEO Schema
→ Landingpages
→ Publishing
→ Tracking
→ Learning


## Governance Rule

Änderungen erfolgen nach:

Audit
→ Analyse
→ Backup
→ Integration
→ Test
→ Commit + Push
