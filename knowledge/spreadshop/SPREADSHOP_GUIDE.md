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
