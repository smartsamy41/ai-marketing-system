# FBEP-KNOW-0001

# Spreadshop Knowledge Base

Version: 1.0.0
Status: Official
Owner: Samy Jendoubi

## Purpose

This document describes the complete Spreadshop integration inside the Free Basics Enterprise Platform.

## Shop

Name: FreeBasics

Platform:
Spreadshop

Shop ID:
1519495

Main Shop URL:
https://freebasics.myspreadshop.net/

Primary Domain:
https://freebasics.online

## Product Feed

Google Merchant Feed

https://freebasics.myspreadshop.net/1519495/products.rss?pushState=false&targetPlatform=google

Meta Feed

https://freebasics.myspreadshop.net/1519495/products.rss?pushState=false&targetPlatform=facebook

## Current Integration

Spreadshop is the primary product source for Print-on-Demand products.

The RSS feed is imported into the AI platform.

Each design is treated as one logical product.

Product variants are grouped automatically.

## Landingpage Strategy

One design = One landingpage

Variants are displayed on the landingpage.

No duplicate pages for different colors or sizes.

## Product Data

Imported fields include:

- Product ID
- Design ID
- Title
- Description
- Product URL
- Image URL
- Price
- Availability
- Category
- Color
- Size
- Gender
- Age Group
- Condition

## Future Workflow

Spreadshop Feed
↓

Feed Import
↓

Google Sheets

↓

Landingpage Generator

↓

SEO Engine

↓

Publishing Engine

↓

Analytics

## Rule

Spreadshop is the master source for Print-on-Demand products.

Manual editing of imported feed data should be avoided unless required.

End of Document

## Current Feed Engine Decision

The Spreadshop RSS feed contains product variants, not final logical products.

Current audit result:

- RSS variants: 24,224
- Logical designs after design-id grouping: 14
- One design can contain more than 1,000 product variants

## Design-Level Rule

FBEP must group Spreadshop products by real design ID.

Example:

6a17cf18d69fce2b389646ab_812
→ real design ID:
6a17cf18d69fce2b389646ab

## Platform Rule

One real Spreadshop design equals one logical FBEP product group.

The variants below that design may include:

- shirts
- hoodies
- bags
- accessories
- mugs
- stickers
- colors
- sizes
- gender variants

## SEO Rule

Do not create one landingpage per RSS item.

Create one landingpage per real design.

Variants are displayed or referenced under the design-level page.

## Pinterest / YouTube Future Rule

Pinterest boards must later be created by real category, design family or campaign logic.

AI-generated pins must be unique and must not mass-post duplicate variant content.

YouTube videos must be humanized, story-based and connected to real design themes, not generic auto-generated product spam.
