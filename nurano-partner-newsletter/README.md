# NURANO Partner & Newsletter Platform

Status: Greenfield Build
Brand: NURANO
Created: 2026-09-05

## Scope

This directory contains the new NURANO Partner & Newsletter Platform.

It is a clean greenfield implementation and does not reuse the legacy FBEP / Free Basics architecture as its production architecture.

## System Separation

### System A — NURANO GEO Knowledge Platform

The NURANO GEO Knowledge Platform is a separate system.

It must not be modified, migrated, deleted, or coupled to this platform without an explicit audited decision.

### System B — NURANO Partner & Newsletter Platform

This directory is System B.

Its scope includes:

- partners
- products
- official partner assets
- commissions
- compliance
- tracking
- routing and CTAs
- content and campaigns
- newsletters
- subscriber and DOI workflows
- consent evidence
- conversions and attribution
- provenance
- backup and restore
- handover documentation

## Active Partners

Only these partners are currently active for the clean build:

- CHECK24
- Tarifcheck
- Telekom Profis

Congstar is treated as a Telekom product or tariff area and not as a separate partner.

Amazon, Awin, FinanceAds and other legacy partners are not active unless explicitly approved later.

## Verified Partner IDs

- CHECK24: 354456
- Tarifcheck: 165274
- Telekom Profis: 100228979

## Telekom Shop

Current approved shop:

https://free-basics.telekom-profis.de

This URL must not be replaced until Telekom confirms another official partner-shop URL.

## Source-of-Truth Priority

1. Original partner email
2. Partner portal
3. Official advertising material
4. Official partner document
5. Official affiliate code
6. Provably official asset
7. Legacy data only as a hint

## Verification Statuses

- VERIFIED
- STRONG_SOURCE
- UNVERIFIED
- LEGACY
- PLACEHOLDER
- DO_NOT_USE

## Legacy Rule

Legacy files are source-extraction material only.

Legacy architecture, IDs, commissions, links, tracking formats, product records and business rules must not be copied into production unless independently verified.

The legacy file:

data/sources/Affiliate_Master_Database.csv

is classified as:

LEGACY_SOURCE / IMMUTABLE / DO_NOT_USE_FOR_PRODUCTION / EXTRACTED

## Data Safety

- No secrets in Git.
- No subscriber personal data in Git.
- No DOI evidence or consent records containing personal data in Git.
- Sensitive newsletter data requires a separate encrypted data store.
- Missing partner facts must remain missing until verified.
- No products, commissions, prices, offers, links or partner conditions may be invented.

## Migration Rule

Audit first.

Then extract verified source facts.

Then model.

Then implement.

Then test.

Then migrate.

Legacy components may only be quarantined after backup, checksum, dependency verification and restore validation.
