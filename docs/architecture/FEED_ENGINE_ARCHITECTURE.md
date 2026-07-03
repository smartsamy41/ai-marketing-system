# Feed Engine Architecture

Version: 1.0.0
Status: Draft
Phase: 2.1
Owner: Samy Jendoubi

## Purpose

The Feed Engine collects, normalizes, validates and synchronizes product feed data for FBEP.

## Scope

Supported sources:

- Spreadshop
- Amazon
- CHECK24
- Tarifcheck
- Telekom

## Core Rule

The Feed Engine does not publish content directly.

It only prepares validated product data for downstream systems.

## Data Flow

External Feed Source -> Feed Connector -> Feed Engine -> Feed Validator -> Normalized Product Model -> Google Sheets -> Landingpages / Pinterest / YouTube / Analytics

## Normalized Product Model

Required fields:

- product_id
- source
- partner
- title
- description
- category
- price
- currency
- product_url
- affiliate_url
- image_url
- status
- created_at
- updated_at

## Planned Modules

- engine/feed_models.py
- engine/feed_validator.py
- engine/feed_engine.py
- engine/feed_sync.py

## Non-Goals

The Feed Engine does not:

- publish Pinterest pins
- upload YouTube videos
- generate final landingpage HTML
- manage secrets directly
- bypass compliance validation
