# Free Basics FastAPI Application Router

## Purpose

Central routing documentation layer for the
FREE BASICS AI MARKETING SYSTEM.

## Router Areas

health:
- system status
- availability checks

landingpages:
- product landingpage routing
- product_id based access

blog:
- article access
- content distribution

data:
- public datasets
- knowledge resources


## Architecture

Cloud Run
    |
    |
FastAPI Application
    |
    ├── Health Router
    ├── Landingpage Router
    ├── Blog Router
    └── Data Router


## Public API

Base:
https://freebasics.online

Documentation:
OpenAPI 3.0
