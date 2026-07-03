
## [1.0.0] - 2026-07-03

### Foundation Freeze

- Added CONTRIBUTING.md
- Added CODE_OF_CONDUCT.md
- Added LICENSE.md
- Removed .env from Git tracking
- Added .env protection through .gitignore
- Confirmed repository documentation as single source of truth
- Prepared FBEP Foundation v1.0 for controlled freeze

## [1.1.0] - 2026-07-03

### Added

- Added Feed Engine architecture documentation
- Added Sprint 001 Feed Engine plan
- Added FeedProduct model
- Added Feed Validator
- Added Feed Engine normalization layer
- Added Feed Sync row preparation layer

### Verified

- Feed modules compile successfully
- Valid feed records produce Google Sheets rows
- Invalid feed records produce validation error rows

## [1.1.1] - 2026-07-03

### Added

- Added generic append_rows support to GoogleSheetsConnector
- Added FeedSheetSync for valid product rows
- Added FeedSheetSync for validation error rows

### Verified

- Feed to Google Sheets sync tested with fake connector
- Valid feed products produce sync rows
- Invalid feed products produce error sync rows

## [1.1.2] - 2026-07-03

### Added

- Added Product Feed Adapter
- Connected normalized Feed Engine output to product-layer-compatible records

### Verified

- Valid feed result converts into product record format
- Existing product layer remains unchanged

## [1.1.3] - 2026-07-03

### Added

- Added Spreadshop RSS parser
- Added design-level grouping for Spreadshop products
- Documented Spreadshop design-level rule
- Documented Pinterest and YouTube future publishing rules for Spreadshop content

### Verified

- Spreadshop Google Merchant RSS feed parsed successfully
- 24,224 RSS variants grouped into 14 logical designs
- Large RSS XML sample excluded from Git through .gitignore

## [1.2.0] - 2026-07-03

### Added

- Added Unified Product Catalog core module
- Added catalog product models
- Added in-memory product repository
- Added product catalog registration and lookup
- Added product catalog sheet exporter
- Added product catalog statistics

### Verified

- Product registration works
- Product lookup works
- Sheet row export works
- Catalog statistics work
