# Unified Product Catalog Architecture

Version: 1.0.0
Status: Draft
Phase: 3.0
Owner: Samy Jendoubi

## Purpose

The Unified Product Catalog is the central product repository of FBEP.

All partner sources must be normalized into one shared catalog model before downstream processing.

## Sources

- Spreadshop
- Amazon
- CHECK24
- Tarifcheck
- Telekom

## Core Rule

There is exactly one central product model.

No engine may invent or maintain a separate permanent product structure.

## Product Identity

Every catalog product must include:

- fbep_product_id
- source
- source_product_id
- partner
- title
- category
- status
- variants
- tags

## Spreadshop Rule

For Spreadshop:

- fbep_product_id is based on the real design ID
- one real design equals one logical product group
- RSS variants remain attached to the product

## Non-Goals

The Product Catalog does not:

- publish content directly
- manage secrets
- bypass compliance checks
