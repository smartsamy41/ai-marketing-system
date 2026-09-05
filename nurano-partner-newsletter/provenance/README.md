# Source Provenance Rules

Status: ACTIVE
Scope: NURANO Partner & Newsletter Platform

## Purpose

Every production fact must be traceable to a source.

## Source Priority

1. original_partner_email
2. partner_portal
3. official_advertising_material
4. official_partner_document
5. official_affiliate_code
6. verified_official_asset
7. legacy_hint

## Verification Status

Allowed values:

- VERIFIED
- STRONG_SOURCE
- UNVERIFIED
- LEGACY
- PLACEHOLDER
- DO_NOT_USE

## Required Provenance Fields

Each future source record should contain:

- source_id
- partner
- source_type
- source_reference
- source_date
- extracted_at
- verification_status
- verified_fact
- notes

## Rules

- Do not invent missing values.
- Do not promote LEGACY data to VERIFIED without an independent primary source.
- Do not store secrets.
- Do not store subscriber personal data.
- Do not store DOI or consent personal evidence in Git.
- Original legacy source files must not be modified.
- Conflicting values must remain explicitly documented until resolved.
