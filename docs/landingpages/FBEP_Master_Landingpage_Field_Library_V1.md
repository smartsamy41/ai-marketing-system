# FBEP Master Landingpage Field Library V1

**Projekt:** AI Marketing System / FBEP  
**Owner:** Samy Jendoubi  
**Google-Cloud-Projekt:** `smartcontent2050`  
**Domain:** `https://freebasics.online`  
**Repository:** `smartsamy41/ai-marketing-system`  
**Version:** `1.0.0`  
**Status:** PRODUCTION STANDARD

## Übersicht

- 32 Landingpage-Abschnitte
- 665 eindeutige Felder
- Einheitliche Metadaten für Google Sheets, BigQuery, Drive, GitHub und Cloud Run
- Integrierte SEO-, Schema-, Compliance-, Accessibility-, AI-Governance- und Deployment-Kennzeichnung

## Abschnitte

| Nr. | Code | Abschnitt | Pflicht | Felder |
|---:|---|---|:---:|---:|
| 1 | `TECH` | Technische Seitendaten | Ja | 40 |
| 2 | `NAV` | Globale Navigation | Ja | 20 |
| 3 | `BCR` | Breadcrumbs | Ja | 20 |
| 4 | `ADV` | Werbekennzeichnung | Ja | 20 |
| 5 | `HERO` | Hero-Bereich | Ja | 25 |
| 6 | `PROB` | Nutzerproblem | Ja | 20 |
| 7 | `SOL` | Lösung / Produktvorstellung | Ja | 20 |
| 8 | `COMP` | Vorteile & Nachteile | Ja | 20 |
| 9 | `SPEC` | Funktionen & technische Details | Ja | 20 |
| 10 | `PRICE` | Preise, Kosten & Konditionen | Ja | 20 |
| 11 | `COMPARE` | Vergleich & Alternativen | Ja | 20 |
| 12 | `FAQ` | FAQ | Ja | 20 |
| 13 | `REVIEW` | Bewertungen & Erfahrungsberichte | Ja | 20 |
| 14 | `TRUST` | Vertrauenselemente | Ja | 20 |
| 15 | `CTA` | Call-to-Action | Ja | 20 |
| 16 | `AFF` | Affiliate-Links & Tracking | Ja | 20 |
| 17 | `LINK` | Interne Verlinkung | Ja | 20 |
| 18 | `SOURCE` | Externe Quellen & Referenzen | Ja | 20 |
| 19 | `MEDIA` | Medienverwaltung | Ja | 20 |
| 20 | `SEO` | SEO-Struktur | Ja | 20 |
| 21 | `SCHEMA` | Schema.org & strukturierte Daten | Ja | 20 |
| 22 | `A11Y` | Accessibility & WCAG | Ja | 20 |
| 23 | `LEGAL` | Rechtliches & Compliance | Ja | 20 |
| 24 | `PERF` | Performance & Core Web Vitals | Ja | 20 |
| 25 | `ANALYTICS` | Analytics & Conversion Tracking | Ja | 20 |
| 26 | `LOC` | Personalisierung & Lokalisierung | Ja | 20 |
| 27 | `AIQ` | Content-Qualität & AI-Governance | Ja | 20 |
| 28 | `PUB` | Veröffentlichung & Workflow | Ja | 20 |
| 29 | `VER` | Versionierung & Änderungsverlauf | Ja | 20 |
| 30 | `LIFE` | Archivierung & Lifecycle | Ja | 20 |
| 31 | `QA` | Qualitätsprüfung & Freigabe | Ja | 20 |
| 32 | `SYS` | System-Metadaten & Deployment | Ja | 20 |

## Vollständige Feldbibliothek

### 01. Technische Seitendaten

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `TECH_001` | `page_id` | String | YES | System | Eindeutige Seiten-ID |
| `TECH_002` | `slug` | String | YES | System | URL-Slug der Landingpage |
| `TECH_003` | `canonical_url` | URL | YES | SEO Engine | Kanonische Produktions-URL |
| `TECH_004` | `page_url` | URL | YES | Publisher | Öffentliche Seiten-URL |
| `TECH_005` | `language` | String | YES | Config | Seitensprache |
| `TECH_006` | `country` | String | YES | Config | Zielland |
| `TECH_007` | `currency` | String | YES | Config | Standardwährung |
| `TECH_008` | `page_title` | String | YES | Content Engine | Interner Seitentitel |
| `TECH_009` | `meta_description` | String | YES | Content Engine | Meta-Beschreibung |
| `TECH_010` | `meta_keywords` | JSON | NO | SEO Engine | Optionale Suchbegriffe |
| `TECH_011` | `robots_index` | Boolean | YES | SEO Engine | Indexierung erlaubt |
| `TECH_012` | `robots_follow` | Boolean | YES | SEO Engine | Linkverfolgung erlaubt |
| `TECH_013` | `og_title` | String | YES | Content Engine | Open-Graph-Titel |
| `TECH_014` | `og_description` | String | YES | Content Engine | Open-Graph-Beschreibung |
| `TECH_015` | `og_image` | URL | NO | Asset Engine | Open-Graph-Bild |
| `TECH_016` | `twitter_title` | String | NO | Content Engine | Social-Titel |
| `TECH_017` | `twitter_description` | String | NO | Content Engine | Social-Beschreibung |
| `TECH_018` | `twitter_image` | URL | NO | Asset Engine | Social-Vorschaubild |
| `TECH_019` | `schema_type` | Enum | YES | Schema Engine | Primärer Schema.org-Typ |
| `TECH_020` | `schema_json` | JSON | YES | Schema Engine | Generierter JSON-LD-Block |
| `TECH_021` | `hreflang` | JSON | NO | SEO Engine | Sprach- und Länderzuordnungen |
| `TECH_022` | `sitemap_status` | Enum | YES | SEO Engine | Sitemap-Status |
| `TECH_023` | `publish_status` | Enum | YES | Workflow Engine | Veröffentlichungsstatus |
| `TECH_024` | `created_at` | Datetime | YES | System | Erstellungszeitpunkt |
| `TECH_025` | `updated_at` | Datetime | YES | System | Letzte Änderung |
| `TECH_026` | `published_at` | Datetime | NO | Publisher | Veröffentlichungszeitpunkt |
| `TECH_027` | `last_review_at` | Datetime | YES | Quality Engine | Letzte Prüfung |
| `TECH_028` | `version` | String | YES | Version Engine | Inhaltsversion |
| `TECH_029` | `template_version` | String | YES | Template Engine | Template-Version |
| `TECH_030` | `compliance_version` | String | YES | Compliance Engine | Compliance-Regelversion |
| `TECH_031` | `seo_score` | Decimal | YES | SEO Engine | Interner SEO-Wert |
| `TECH_032` | `accessibility_score` | Decimal | YES | Accessibility Engine | Accessibility-Wert |
| `TECH_033` | `quality_score` | Decimal | YES | Quality Engine | Gesamtqualitätswert |
| `TECH_034` | `author_id` | String | YES | System | Autor oder Engine |
| `TECH_035` | `reviewer_id` | String | NO | Workflow Engine | Prüfer |
| `TECH_036` | `ai_model` | String | NO | Content Engine | Verwendetes AI-Modell |
| `TECH_037` | `generation_id` | String | NO | Content Engine | Generierungs-ID |
| `TECH_038` | `source_system` | Enum | YES | System | Ursprungssystem |
| `TECH_039` | `page_status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |
| `TECH_040` | `notes` | Text | NO | Redaktion | Interne Hinweise |

### 02. Globale Navigation

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `NAV_001` | `navigation_id` | String | YES | System | Eindeutige Navigations-ID |
| `NAV_002` | `navigation_version` | String | YES | System | Version der Navigation |
| `NAV_003` | `logo_url` | URL | YES | Asset Engine | Logo-Datei |
| `NAV_004` | `logo_alt` | String | YES | Content Engine | Alternativtext des Logos |
| `NAV_005` | `home_url` | URL | YES | Config | Link zur Startseite |
| `NAV_006` | `primary_menu` | JSON | YES | Navigation Engine | Hauptmenü |
| `NAV_007` | `secondary_menu` | JSON | NO | Navigation Engine | Zusatzmenü |
| `NAV_008` | `mobile_menu` | JSON | YES | Navigation Engine | Mobile Navigation |
| `NAV_009` | `sticky_navigation` | Boolean | NO | Config | Sticky Header aktiv |
| `NAV_010` | `search_enabled` | Boolean | YES | Config | Seitensuche aktiv |
| `NAV_011` | `search_placeholder` | String | NO | Content Engine | Suchfeld-Platzhalter |
| `NAV_012` | `category_menu` | JSON | YES | Navigation Engine | Kategorienavigation |
| `NAV_013` | `footer_navigation` | JSON | YES | Navigation Engine | Footer-Menü |
| `NAV_014` | `language_switcher` | Boolean | NO | Config | Sprachumschaltung |
| `NAV_015` | `current_language` | String | YES | Config | Aktive Sprache |
| `NAV_016` | `accessibility_skiplink` | Boolean | YES | Accessibility Engine | Skip-Link vorhanden |
| `NAV_017` | `breadcrumb_enabled` | Boolean | YES | Navigation Engine | Breadcrumb aktiv |
| `NAV_018` | `breadcrumb_source` | Enum | YES | Navigation Engine | Automatisch oder manuell |
| `NAV_019` | `active_menu_item` | String | YES | Navigation Engine | Aktiver Menüpunkt |
| `NAV_020` | `navigation_status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 03. Breadcrumbs

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `BCR_001` | `breadcrumb_id` | String | YES | System | Eindeutige Breadcrumb-ID |
| `BCR_002` | `breadcrumb_enabled` | Boolean | YES | Config | Breadcrumb aktiv |
| `BCR_003` | `breadcrumb_type` | Enum | YES | Navigation Engine | Hierarchisch, Kategorie oder benutzerdefiniert |
| `BCR_004` | `breadcrumb_depth` | Integer | YES | Navigation Engine | Anzahl der Ebenen |
| `BCR_005` | `breadcrumb_items` | JSON | YES | Navigation Engine | Gesamte Breadcrumb-Struktur |
| `BCR_006` | `level_1_name` | String | YES | Navigation Engine | Name der Startseite |
| `BCR_007` | `level_1_url` | URL | YES | Config | URL der Startseite |
| `BCR_008` | `level_2_name` | String | YES | Category Engine | Hauptkategorie |
| `BCR_009` | `level_2_url` | URL | YES | Category Engine | URL der Hauptkategorie |
| `BCR_010` | `level_3_name` | String | NO | Category Engine | Unterkategorie |
| `BCR_011` | `level_3_url` | URL | NO | Category Engine | URL der Unterkategorie |
| `BCR_012` | `current_page_name` | String | YES | Landingpage Engine | Aktuelle Seite |
| `BCR_013` | `current_page_url` | URL | YES | Landingpage Engine | URL der aktuellen Seite |
| `BCR_014` | `schema_enabled` | Boolean | YES | Schema Engine | BreadcrumbList erzeugen |
| `BCR_015` | `schema_json` | JSON | YES | Schema Engine | JSON-LD BreadcrumbList |
| `BCR_016` | `visible_on_page` | Boolean | YES | Layout Engine | Sichtbar für Besucher |
| `BCR_017` | `crawl_priority` | Integer | NO | SEO Engine | Crawl-Priorität |
| `BCR_018` | `internal_link_score` | Decimal | NO | SEO Engine | Interne Linkbewertung |
| `BCR_019` | `validation_status` | Enum | YES | Quality Engine | VALID, WARNING oder ERROR |
| `BCR_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 04. Werbekennzeichnung

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `ADV_001` | `disclosure_id` | String | YES | System | Eindeutige Kennzeichnungs-ID |
| `ADV_002` | `advertising_label` | String | YES | Compliance Engine | Werbung oder Anzeige |
| `ADV_003` | `disclosure_text` | Text | YES | Compliance Engine | Standard-Hinweistext |
| `ADV_004` | `disclosure_position` | Enum | YES | Layout Engine | Position der Kennzeichnung |
| `ADV_005` | `disclosure_visible` | Boolean | YES | System | Sichtbar für Besucher |
| `ADV_006` | `disclosure_mobile` | Boolean | YES | Layout Engine | Mobil sichtbar |
| `ADV_007` | `disclosure_desktop` | Boolean | YES | Layout Engine | Desktop sichtbar |
| `ADV_008` | `affiliate_links_present` | Boolean | YES | Link Engine | Affiliate-Links vorhanden |
| `ADV_009` | `affiliate_network` | Enum | YES | Product Engine | Amazon, Check24, Tarifcheck, Telekom oder sonstige |
| `ADV_010` | `partner_notice` | Text | NO | Compliance Engine | Partnerbezogener Hinweis |
| `ADV_011` | `transparency_text` | Text | YES | Compliance Engine | Transparenz über Vergütung |
| `ADV_012` | `external_provider_notice` | Boolean | YES | Compliance Engine | Hinweis auf externen Anbieter |
| `ADV_013` | `freebasics_role` | Enum | YES | Compliance Engine | Tippgeber oder Informationsportal |
| `ADV_014` | `provider_name` | String | YES | Product Engine | Tatsächlicher Anbieter |
| `ADV_015` | `legal_basis` | String | NO | Compliance Engine | Interner Rechtsgrundlagenverweis |
| `ADV_016` | `compliance_status` | Enum | YES | Compliance Engine | VALID, WARNING oder ERROR |
| `ADV_017` | `last_compliance_check` | Datetime | YES | Compliance Engine | Letzte Prüfung |
| `ADV_018` | `compliance_version` | String | YES | Compliance Engine | Regelversion |
| `ADV_019` | `auto_generated` | Boolean | YES | System | Automatisch eingefügt |
| `ADV_020` | `locked` | Boolean | YES | System | Darf nicht entfernt werden |

### 05. Hero-Bereich

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `HERO_001` | `hero_id` | String | YES | System | Eindeutige Hero-ID |
| `HERO_002` | `hero_variant` | Enum | YES | Template Engine | Hero-Layoutvariante |
| `HERO_003` | `hero_h1` | String | YES | Content Engine | Hauptüberschrift |
| `HERO_004` | `hero_subheadline` | String | NO | Content Engine | Unterüberschrift |
| `HERO_005` | `hero_intro` | Text | YES | Content Engine | Kurze Einleitung |
| `HERO_006` | `hero_summary` | Text | YES | Content Engine | Zusammenfassung des Angebots |
| `HERO_007` | `hero_primary_cta` | String | YES | Content Engine | Primärer CTA-Text |
| `HERO_008` | `hero_primary_cta_url` | URL | YES | Link Engine | Ziel des primären CTA |
| `HERO_009` | `hero_secondary_cta` | String | NO | Content Engine | Sekundärer CTA |
| `HERO_010` | `hero_secondary_cta_url` | URL | NO | Link Engine | Ziel des sekundären CTA |
| `HERO_011` | `hero_image_url` | URL | NO | Asset Engine | Hero-Bild |
| `HERO_012` | `hero_image_alt` | String | NO | Content Engine | Alternativtext |
| `HERO_013` | `hero_image_caption` | String | NO | Content Engine | Bildbeschreibung |
| `HERO_014` | `hero_video_url` | URL | NO | Video Engine | Hero-Video |
| `HERO_015` | `hero_badges` | JSON | NO | Compliance Engine | Belegbare Vertrauenshinweise |
| `HERO_016` | `hero_partner_name` | String | YES | Product Engine | Affiliate-Partner |
| `HERO_017` | `hero_provider_name` | String | YES | Product Engine | Tatsächlicher Anbieter |
| `HERO_018` | `hero_external_notice` | Boolean | YES | Compliance Engine | Hinweis auf externe Weiterleitung |
| `HERO_019` | `hero_layout` | Enum | YES | Template Engine | Desktop- und Mobile-Layout |
| `HERO_020` | `hero_alignment` | Enum | YES | Template Engine | Textausrichtung |
| `HERO_021` | `hero_background_type` | Enum | NO | Template Engine | Farbe, Bild oder Verlauf |
| `HERO_022` | `hero_background_asset` | URL | NO | Asset Engine | Hintergrundgrafik |
| `HERO_023` | `hero_reading_time` | Integer | NO | Content Engine | Geschätzte Lesezeit |
| `HERO_024` | `hero_last_updated` | Date | YES | Quality Engine | Letzte Aktualisierung |
| `HERO_025` | `hero_status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 06. Nutzerproblem

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `PROB_001` | `problem_id` | String | YES | System | Eindeutige Problem-ID |
| `PROB_002` | `problem_category` | Enum | YES | Product Engine | Problemkategorie |
| `PROB_003` | `user_intent` | Enum | YES | SEO Engine | Suchabsicht |
| `PROB_004` | `target_audience` | Enum | YES | Product Engine | Zielgruppe |
| `PROB_005` | `problem_title` | String | YES | Content Engine | Kurzbezeichnung des Problems |
| `PROB_006` | `problem_description` | Text | YES | Content Engine | Beschreibung der Ausgangssituation |
| `PROB_007` | `pain_points` | JSON | YES | Content Engine | Zentrale Herausforderungen |
| `PROB_008` | `user_questions` | JSON | YES | Content Engine | Typische Nutzerfragen |
| `PROB_009` | `decision_factors` | JSON | YES | Content Engine | Entscheidungskriterien |
| `PROB_010` | `urgency_level` | Enum | NO | Content Engine | Niedrig, Mittel oder Hoch |
| `PROB_011` | `misconceptions` | JSON | NO | Content Engine | Häufige Missverständnisse |
| `PROB_012` | `prerequisites` | JSON | NO | Product Engine | Voraussetzungen |
| `PROB_013` | `regional_limitations` | JSON | NO | Product Engine | Regionale Einschränkungen |
| `PROB_014` | `legal_limitations` | JSON | NO | Compliance Engine | Rechtliche Einschränkungen |
| `PROB_015` | `financial_considerations` | JSON | NO | Content Engine | Kostenaspekte |
| `PROB_016` | `technical_considerations` | JSON | NO | Content Engine | Technische Voraussetzungen |
| `PROB_017` | `comparison_needed` | Boolean | YES | Content Engine | Vergleich sinnvoll |
| `PROB_018` | `expert_tip` | Text | NO | Redaktion | Neutraler Hinweis |
| `PROB_019` | `readability_level` | Enum | YES | Content Engine | Einfach, Standard oder fachlich |
| `PROB_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 07. Lösung / Produktvorstellung

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `SOL_001` | `solution_id` | String | YES | System | Eindeutige Lösungs-ID |
| `SOL_002` | `product_id` | String | YES | Product Engine | Interne Produkt-ID |
| `SOL_003` | `partner_name` | String | YES | Product Engine | Affiliate-Partner |
| `SOL_004` | `provider_name` | String | YES | Product Engine | Tatsächlicher Anbieter |
| `SOL_005` | `product_name` | String | YES | Product Engine | Produktbezeichnung |
| `SOL_006` | `product_category` | Enum | YES | Product Engine | Produktkategorie |
| `SOL_007` | `solution_headline` | String | YES | Content Engine | Abschnittsüberschrift |
| `SOL_008` | `solution_intro` | Text | YES | Content Engine | Einleitung |
| `SOL_009` | `solution_description` | Text | YES | Content Engine | Sachliche Produktbeschreibung |
| `SOL_010` | `key_features` | JSON | YES | Product Engine | Hauptmerkmale |
| `SOL_011` | `key_benefits` | JSON | YES | Content Engine | Wesentliche Vorteile |
| `SOL_012` | `limitations` | JSON | NO | Product Engine | Einschränkungen |
| `SOL_013` | `target_users` | JSON | YES | Content Engine | Geeignete Zielgruppen |
| `SOL_014` | `unsuitable_for` | JSON | NO | Content Engine | Weniger geeignete Zielgruppen |
| `SOL_015` | `requirements` | JSON | NO | Product Engine | Voraussetzungen |
| `SOL_016` | `availability` | Enum | NO | Product Engine | Regional, national oder online |
| `SOL_017` | `official_source` | URL | NO | Source Engine | Offizielle Quelle |
| `SOL_018` | `last_verified` | Date | YES | Quality Engine | Letzte Prüfung |
| `SOL_019` | `content_version` | String | YES | Version Engine | Versionsnummer |
| `SOL_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 08. Vorteile & Nachteile

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `COMP_001` | `comparison_id` | String | YES | System | Eindeutige Vergleichs-ID |
| `COMP_002` | `section_title` | String | YES | Content Engine | Abschnittsüberschrift |
| `COMP_003` | `summary` | Text | YES | Content Engine | Kurze Zusammenfassung |
| `COMP_004` | `advantages` | JSON | YES | Content Engine | Liste der Vorteile |
| `COMP_005` | `disadvantages` | JSON | YES | Content Engine | Liste der Nachteile |
| `COMP_006` | `neutral_observations` | JSON | NO | Content Engine | Neutrale Hinweise |
| `COMP_007` | `strongest_advantage` | String | YES | Content Engine | Wichtigster Vorteil |
| `COMP_008` | `biggest_limitation` | String | NO | Content Engine | Größte Einschränkung |
| `COMP_009` | `suitable_for` | JSON | YES | Content Engine | Geeignete Nutzergruppen |
| `COMP_010` | `less_suitable_for` | JSON | NO | Content Engine | Weniger geeignete Zielgruppen |
| `COMP_011` | `feature_completeness` | Enum | NO | Product Engine | Basis, Standard oder Premium |
| `COMP_012` | `usability_rating` | Decimal | NO | Quality Engine | Interne Bewertung |
| `COMP_013` | `complexity_level` | Enum | NO | Content Engine | Einfach, mittel oder komplex |
| `COMP_014` | `maintenance_required` | Boolean | NO | Product Engine | Laufende Pflege notwendig |
| `COMP_015` | `alternatives_available` | Boolean | YES | Product Engine | Alternativen vorhanden |
| `COMP_016` | `comparison_last_review` | Date | YES | Quality Engine | Letzte Prüfung |
| `COMP_017` | `reviewer` | String | NO | Redaktion | Prüfer |
| `COMP_018` | `source_reference` | JSON | NO | Source Engine | Verwendete Quellen |
| `COMP_019` | `quality_status` | Enum | YES | Quality Engine | VALID, REVIEW oder ERROR |
| `COMP_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 09. Funktionen & technische Details

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `SPEC_001` | `specification_id` | String | YES | System | Eindeutige Spezifikations-ID |
| `SPEC_002` | `product_id` | String | YES | Product Engine | Interne Produkt-ID |
| `SPEC_003` | `specification_version` | String | YES | Version Engine | Versionsnummer |
| `SPEC_004` | `feature_list` | JSON | YES | Product Engine | Vollständige Funktionsliste |
| `SPEC_005` | `technical_specifications` | JSON | YES | Product Engine | Technische Daten |
| `SPEC_006` | `supported_platforms` | JSON | NO | Product Engine | Unterstützte Plattformen |
| `SPEC_007` | `compatibility` | JSON | NO | Product Engine | Kompatibilität |
| `SPEC_008` | `minimum_requirements` | JSON | NO | Product Engine | Mindestanforderungen |
| `SPEC_009` | `maximum_capacity` | String | NO | Product Engine | Maximale Leistung oder Kapazität |
| `SPEC_010` | `performance_metrics` | JSON | NO | Product Engine | Leistungskennzahlen |
| `SPEC_011` | `supported_languages` | JSON | NO | Product Engine | Verfügbare Sprachen |
| `SPEC_012` | `regional_availability` | JSON | NO | Product Engine | Verfügbare Regionen |
| `SPEC_013` | `integration_options` | JSON | NO | Product Engine | Schnittstellen und Integrationen |
| `SPEC_014` | `update_frequency` | Enum | NO | Product Engine | Update- oder Wartungsrhythmus |
| `SPEC_015` | `documentation_url` | URL | NO | Source Engine | Offizielle Dokumentation |
| `SPEC_016` | `api_available` | Boolean | NO | Product Engine | API verfügbar |
| `SPEC_017` | `mobile_support` | Boolean | NO | Product Engine | Mobile Unterstützung |
| `SPEC_018` | `accessibility_features` | JSON | NO | Product Engine | Barrierefreiheitsfunktionen |
| `SPEC_019` | `verified_at` | Date | YES | Quality Engine | Letzte technische Prüfung |
| `SPEC_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 10. Preise, Kosten & Konditionen

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `PRICE_001` | `pricing_id` | String | YES | System | Eindeutige Preis-ID |
| `PRICE_002` | `product_id` | String | YES | Product Engine | Interne Produkt-ID |
| `PRICE_003` | `pricing_model` | Enum | YES | Product Engine | Einmalig, monatlich, jährlich oder variabel |
| `PRICE_004` | `currency` | String | YES | Config | Währung |
| `PRICE_005` | `base_price` | Decimal | NO | Product Engine | Grundpreis |
| `PRICE_006` | `recurring_price` | Decimal | NO | Product Engine | Wiederkehrender Preis |
| `PRICE_007` | `setup_fee` | Decimal | NO | Product Engine | Einrichtungsgebühr |
| `PRICE_008` | `shipping_cost` | Decimal | NO | Product Engine | Versandkosten |
| `PRICE_009` | `minimum_term` | Integer | NO | Product Engine | Mindestlaufzeit in Monaten |
| `PRICE_010` | `cancellation_period` | String | NO | Product Engine | Kündigungsfrist |
| `PRICE_011` | `payment_methods` | JSON | NO | Product Engine | Unterstützte Zahlungsarten |
| `PRICE_012` | `discounts_available` | Boolean | NO | Product Engine | Rabatte verfügbar |
| `PRICE_013` | `discount_description` | Text | NO | Product Engine | Beschreibung von Rabatten |
| `PRICE_014` | `additional_fees` | JSON | NO | Product Engine | Weitere Kosten |
| `PRICE_015` | `tax_information` | String | NO | Product Engine | Steuerhinweise |
| `PRICE_016` | `price_source` | URL | NO | Source Engine | Offizielle Preisquelle |
| `PRICE_017` | `valid_from` | Date | NO | Product Engine | Gültig ab |
| `PRICE_018` | `last_verified` | Date | YES | Quality Engine | Letzte Preisprüfung |
| `PRICE_019` | `verification_status` | Enum | YES | Quality Engine | VALID, REVIEW oder OUTDATED |
| `PRICE_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 11. Vergleich & Alternativen

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `COMPARE_001` | `comparison_id` | String | YES | System | Eindeutige Vergleichs-ID |
| `COMPARE_002` | `product_id` | String | YES | Product Engine | Interne Produkt-ID |
| `COMPARE_003` | `comparison_title` | String | YES | Content Engine | Abschnittsüberschrift |
| `COMPARE_004` | `comparison_summary` | Text | YES | Content Engine | Kurze Einleitung |
| `COMPARE_005` | `comparison_criteria` | JSON | YES | Product Engine | Vergleichskriterien |
| `COMPARE_006` | `compared_features` | JSON | YES | Product Engine | Verglichene Eigenschaften |
| `COMPARE_007` | `strengths` | JSON | YES | Content Engine | Stärken des Produkts |
| `COMPARE_008` | `limitations` | JSON | NO | Content Engine | Einschränkungen |
| `COMPARE_009` | `alternatives` | JSON | NO | Product Engine | Alternative Produkte |
| `COMPARE_010` | `alternative_categories` | JSON | NO | Product Engine | Alternative Lösungsarten |
| `COMPARE_011` | `best_for` | JSON | YES | Content Engine | Geeignet für |
| `COMPARE_012` | `not_best_for` | JSON | NO | Content Engine | Weniger geeignet für |
| `COMPARE_013` | `decision_matrix` | JSON | NO | Content Engine | Entscheidungshilfe |
| `COMPARE_014` | `recommendation_logic` | Enum | NO | System | Regelbasierte Empfehlung |
| `COMPARE_015` | `recommendation_reason` | Text | NO | Content Engine | Begründung |
| `COMPARE_016` | `source_references` | JSON | NO | Source Engine | Datengrundlagen |
| `COMPARE_017` | `last_verified` | Date | YES | Quality Engine | Letzte Prüfung |
| `COMPARE_018` | `quality_status` | Enum | YES | Quality Engine | VALID, REVIEW oder ERROR |
| `COMPARE_019` | `version` | String | YES | Version Engine | Versionsnummer |
| `COMPARE_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 12. FAQ

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `FAQ_001` | `faq_section_id` | String | YES | System | Eindeutige Abschnitts-ID |
| `FAQ_002` | `faq_title` | String | YES | Content Engine | Abschnittsüberschrift |
| `FAQ_003` | `faq_intro` | Text | NO | Content Engine | Kurze Einführung |
| `FAQ_004` | `faq_items` | JSON | YES | Content Engine | Liste aus Fragen und Antworten |
| `FAQ_005` | `question` | String | YES | Content Engine | Konkrete Nutzerfrage |
| `FAQ_006` | `answer` | Text | YES | Content Engine | Sachliche Antwort |
| `FAQ_007` | `answer_summary` | String | NO | Content Engine | Kurzantwort |
| `FAQ_008` | `answer_source` | JSON | NO | Source Engine | Belegquellen |
| `FAQ_009` | `answer_verified` | Boolean | YES | Quality Engine | Antwort geprüft |
| `FAQ_010` | `answer_verified_at` | Datetime | NO | Quality Engine | Prüfzeitpunkt |
| `FAQ_011` | `faq_category` | Enum | YES | Content Engine | FAQ-Kategorie |
| `FAQ_012` | `user_intent` | Enum | YES | SEO Engine | Suchabsicht |
| `FAQ_013` | `priority` | Integer | YES | System | Reihenfolge |
| `FAQ_014` | `visible_on_page` | Boolean | YES | Layout Engine | Sichtbarkeit |
| `FAQ_015` | `schema_eligible` | Boolean | YES | Schema Engine | Für strukturierte Daten geeignet |
| `FAQ_016` | `schema_enabled` | Boolean | YES | Schema Engine | Schema-Ausgabe aktiv |
| `FAQ_017` | `duplicate_check` | Enum | YES | Quality Engine | VALID, DUPLICATE oder REVIEW |
| `FAQ_018` | `compliance_status` | Enum | YES | Compliance Engine | VALID, WARNING oder ERROR |
| `FAQ_019` | `content_version` | String | YES | Version Engine | Version |
| `FAQ_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 13. Bewertungen & Erfahrungsberichte

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `REVIEW_001` | `review_section_id` | String | YES | System | Abschnitts-ID |
| `REVIEW_002` | `review_id` | String | YES | System | Bewertungs-ID |
| `REVIEW_003` | `review_type` | Enum | YES | System | Kunde, Redaktion oder Plattform |
| `REVIEW_004` | `reviewer_name` | String | NO | Source Engine | Anzeigename |
| `REVIEW_005` | `reviewer_verified` | Boolean | YES | Quality Engine | Identität oder Herkunft geprüft |
| `REVIEW_006` | `review_title` | String | NO | Source Engine | Überschrift |
| `REVIEW_007` | `review_text` | Text | YES | Source Engine | Erfahrungsbericht |
| `REVIEW_008` | `rating_value` | Decimal | NO | Source Engine | Bewertung |
| `REVIEW_009` | `rating_scale` | Decimal | NO | Source Engine | Maximalwert |
| `REVIEW_010` | `review_date` | Date | YES | Source Engine | Bewertungsdatum |
| `REVIEW_011` | `review_source` | String | YES | Source Engine | Herkunft |
| `REVIEW_012` | `source_url` | URL | NO | Source Engine | Originalquelle |
| `REVIEW_013` | `consent_documented` | Boolean | YES | Compliance Engine | Nutzungserlaubnis |
| `REVIEW_014` | `edited_for_length` | Boolean | YES | Redaktion | Text gekürzt |
| `REVIEW_015` | `material_changes` | Boolean | YES | Redaktion | Inhaltlich verändert |
| `REVIEW_016` | `incentivized` | Boolean | YES | Compliance Engine | Gegenleistung erfolgt |
| `REVIEW_017` | `aggregate_rating` | JSON | NO | Review Engine | Gesamtbewertung |
| `REVIEW_018` | `schema_eligible` | Boolean | YES | Schema Engine | Schema zulässig |
| `REVIEW_019` | `compliance_status` | Enum | YES | Compliance Engine | VALID, WARNING oder ERROR |
| `REVIEW_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 14. Vertrauenselemente

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `TRUST_001` | `trust_section_id` | String | YES | System | Abschnitts-ID |
| `TRUST_002` | `trust_title` | String | YES | Redaktion | Überschrift |
| `TRUST_003` | `trust_items` | JSON | YES | Trust Engine | Vertrauenselemente |
| `TRUST_004` | `trust_type` | Enum | YES | System | Sicherheit, Redaktion, Partner oder Aktualität |
| `TRUST_005` | `trust_label` | String | YES | Redaktion | Sichtbarer Text |
| `TRUST_006` | `trust_description` | Text | YES | Redaktion | Erläuterung |
| `TRUST_007` | `evidence_type` | Enum | YES | Compliance Engine | Nachweisart |
| `TRUST_008` | `evidence_reference` | String | NO | Source Engine | Nachweis |
| `TRUST_009` | `evidence_url` | URL | NO | Source Engine | Referenz |
| `TRUST_010` | `issuer_name` | String | NO | Source Engine | Herausgeber |
| `TRUST_011` | `valid_from` | Date | NO | Source Engine | Gültigkeitsbeginn |
| `TRUST_012` | `valid_until` | Date | NO | Source Engine | Gültigkeitsende |
| `TRUST_013` | `verified_at` | Datetime | YES | Quality Engine | Letzte Prüfung |
| `TRUST_014` | `verified_by` | String | YES | Quality Engine | Prüfer |
| `TRUST_015` | `logo_url` | URL | NO | Asset Engine | Freigegebenes Logo |
| `TRUST_016` | `logo_usage_authorized` | Boolean | YES | Compliance Engine | Nutzungsrecht |
| `TRUST_017` | `display_position` | Enum | YES | Layout Engine | Position |
| `TRUST_018` | `schema_relevant` | Boolean | YES | Schema Engine | Schema-Relevanz |
| `TRUST_019` | `compliance_status` | Enum | YES | Compliance Engine | VALID, WARNING oder ERROR |
| `TRUST_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 15. Call-to-Action

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `CTA_001` | `cta_id` | String | YES | System | CTA-ID |
| `CTA_002` | `cta_type` | Enum | YES | System | Primär, sekundär oder Textlink |
| `CTA_003` | `cta_text` | String | YES | Content Engine | Sichtbarer CTA |
| `CTA_004` | `cta_url` | URL | YES | Link Engine | Ziel-URL |
| `CTA_005` | `cta_target_type` | Enum | YES | Link Engine | Intern, extern oder Partner |
| `CTA_006` | `partner_name` | String | NO | Product Engine | Affiliate-Partner |
| `CTA_007` | `product_id` | String | NO | Product Engine | Produktzuordnung |
| `CTA_008` | `affiliate_link` | Boolean | YES | Link Engine | Affiliate-Link |
| `CTA_009` | `advertising_label` | String | NO | Compliance Engine | Werbung oder Anzeige |
| `CTA_010` | `disclosure_position` | Enum | YES | Compliance Engine | Position der Kennzeichnung |
| `CTA_011` | `external_redirect_notice` | String | NO | Compliance Engine | Weiterleitungshinweis |
| `CTA_012` | `open_new_tab` | Boolean | YES | System | Neues Fenster |
| `CTA_013` | `rel_attributes` | String | YES | SEO Engine | Linkattribute |
| `CTA_014` | `tracking_id` | String | NO | Tracking Engine | Tracking-Kennung |
| `CTA_015` | `campaign_id` | String | NO | Tracking Engine | Kampagne |
| `CTA_016` | `placement_id` | String | YES | Tracking Engine | CTA-Position |
| `CTA_017` | `mobile_visible` | Boolean | YES | Layout Engine | Mobil sichtbar |
| `CTA_018` | `desktop_visible` | Boolean | YES | Layout Engine | Desktop sichtbar |
| `CTA_019` | `validation_status` | Enum | YES | Quality Engine | VALID, WARNING oder ERROR |
| `CTA_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 16. Affiliate-Links & Tracking

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `AFF_001` | `affiliate_link_id` | String | YES | System | Eindeutige Link-ID |
| `AFF_002` | `product_id` | String | YES | Product Engine | Produkt-ID |
| `AFF_003` | `partner_name` | String | YES | Product Engine | Partner |
| `AFF_004` | `partner_id` | String | YES | Partner Config | Partner-ID |
| `AFF_005` | `network_name` | String | NO | Partner Config | Affiliate-Netzwerk |
| `AFF_006` | `base_url` | URL | YES | Partner Config | Ausgangs-URL |
| `AFF_007` | `destination_url` | URL | YES | Link Engine | Finale Ziel-URL |
| `AFF_008` | `deeplink` | Boolean | YES | Link Engine | Deeplink |
| `AFF_009` | `tracking_id` | String | NO | Partner Config | Tracking-ID |
| `AFF_010` | `tracking_parameter` | String | NO | Partner Config | URL-Parameter |
| `AFF_011` | `sub_id` | String | NO | Tracking Engine | Sub-ID |
| `AFF_012` | `campaign_id` | String | NO | Tracking Engine | Kampagne |
| `AFF_013` | `content_id` | String | NO | Tracking Engine | Content-Zuordnung |
| `AFF_014` | `placement_id` | String | YES | Tracking Engine | Position |
| `AFF_015` | `advertising_disclosure` | String | YES | Compliance Engine | Werbekennzeichnung |
| `AFF_016` | `link_checked_at` | Datetime | YES | Link Monitor | Letzte Prüfung |
| `AFF_017` | `http_status` | Integer | NO | Link Monitor | HTTP-Status |
| `AFF_018` | `redirect_valid` | Boolean | YES | Link Monitor | Ziel erreichbar |
| `AFF_019` | `compliance_status` | Enum | YES | Compliance Engine | VALID, WARNING oder ERROR |
| `AFF_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 17. Interne Verlinkung

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `LINK_001` | `internal_link_set_id` | String | YES | System | Eindeutige Linkstruktur-ID |
| `LINK_002` | `source_page_id` | String | YES | Landingpage Engine | Ausgangsseite |
| `LINK_003` | `target_page_id` | String | YES | Landingpage Engine | Zielseite |
| `LINK_004` | `target_url` | URL | YES | System | Interne Ziel-URL |
| `LINK_005` | `anchor_text` | String | YES | Content Engine | Sichtbarer Linktext |
| `LINK_006` | `link_context` | Text | NO | Content Engine | Textumfeld des Links |
| `LINK_007` | `link_type` | Enum | YES | System | Kategorie, Produkt, Blog oder Ratgeber |
| `LINK_008` | `cluster_id` | String | NO | SEO Engine | Themencluster |
| `LINK_009` | `pillar_page_id` | String | NO | SEO Engine | Zentrale Themenseite |
| `LINK_010` | `relationship_type` | Enum | YES | SEO Engine | Parent, Child, Related oder Alternative |
| `LINK_011` | `placement_section` | String | YES | Layout Engine | Position auf der Seite |
| `LINK_012` | `placement_priority` | Integer | YES | SEO Engine | Reihenfolge und Priorität |
| `LINK_013` | `relevance_score` | Decimal | YES | SEO Engine | Inhaltliche Relevanz |
| `LINK_014` | `link_depth` | Integer | YES | Navigation Engine | Klicktiefe ab Startseite |
| `LINK_015` | `crawl_enabled` | Boolean | YES | SEO Engine | Für Crawler erreichbar |
| `LINK_016` | `follow_enabled` | Boolean | YES | SEO Engine | Follow-Status |
| `LINK_017` | `broken_link_status` | Enum | YES | Link Monitor | VALID, REDIRECT oder BROKEN |
| `LINK_018` | `last_checked_at` | Datetime | YES | Link Monitor | Letzte Prüfung |
| `LINK_019` | `validation_status` | Enum | YES | Quality Engine | VALID, WARNING oder ERROR |
| `LINK_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 18. Externe Quellen & Referenzen

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `SOURCE_001` | `source_id` | String | YES | System | Eindeutige Quellen-ID |
| `SOURCE_002` | `source_type` | Enum | YES | Source Engine | Anbieter, Behörde, Studie oder Dokumentation |
| `SOURCE_003` | `source_title` | String | YES | Source Engine | Titel |
| `SOURCE_004` | `source_author` | String | NO | Source Engine | Autor oder Organisation |
| `SOURCE_005` | `publisher_name` | String | YES | Source Engine | Herausgeber |
| `SOURCE_006` | `source_url` | URL | NO | Source Engine | Referenz-URL |
| `SOURCE_007` | `source_document_id` | String | NO | Drive | Interne Dokument-ID |
| `SOURCE_008` | `publication_date` | Date | NO | Source Engine | Veröffentlichungsdatum |
| `SOURCE_009` | `accessed_at` | Datetime | YES | System | Abrufzeitpunkt |
| `SOURCE_010` | `last_verified_at` | Datetime | YES | Quality Engine | Letzte Quellenprüfung |
| `SOURCE_011` | `claim_ids` | JSON | YES | Content Engine | Zugeordnete Aussagen |
| `SOURCE_012` | `evidence_excerpt` | Text | NO | Redaktion | Relevanter Auszug |
| `SOURCE_013` | `evidence_location` | String | NO | Redaktion | Seite, Abschnitt oder Absatz |
| `SOURCE_014` | `source_language` | String | YES | Source Engine | Sprache |
| `SOURCE_015` | `authority_level` | Enum | YES | Quality Engine | Primär, sekundär oder ergänzend |
| `SOURCE_016` | `commercial_source` | Boolean | YES | Compliance Engine | Kommerzielle Quelle |
| `SOURCE_017` | `affiliate_partner_source` | Boolean | YES | Compliance Engine | Partnerquelle |
| `SOURCE_018` | `license_status` | Enum | YES | Compliance Engine | Zulässigkeit der Nutzung |
| `SOURCE_019` | `verification_status` | Enum | YES | Quality Engine | VALID, OUTDATED oder REJECTED |
| `SOURCE_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 19. Medienverwaltung

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `MEDIA_001` | `media_id` | String | YES | Asset Engine | Eindeutige Medien-ID |
| `MEDIA_002` | `product_id` | String | NO | Product Engine | Produktzuordnung |
| `MEDIA_003` | `media_type` | Enum | YES | Asset Engine | Bild, Video, PDF oder Grafik |
| `MEDIA_004` | `media_role` | Enum | YES | Layout Engine | Hero, Inhalt, Thumbnail oder Download |
| `MEDIA_005` | `source_type` | Enum | YES | Asset Engine | Eigene Datei, Partner oder Anbieter |
| `MEDIA_006` | `source_url` | URL | NO | Source Engine | Ursprungsquelle |
| `MEDIA_007` | `storage_path` | String | YES | Drive | Speicherort |
| `MEDIA_008` | `public_url` | URL | NO | Publisher | Veröffentlichte URL |
| `MEDIA_009` | `filename` | String | YES | Asset Engine | Dateiname |
| `MEDIA_010` | `mime_type` | String | YES | Asset Engine | Dateityp |
| `MEDIA_011` | `width` | Integer | NO | Asset Engine | Breite |
| `MEDIA_012` | `height` | Integer | NO | Asset Engine | Höhe |
| `MEDIA_013` | `file_size_bytes` | Integer | YES | Asset Engine | Dateigröße |
| `MEDIA_014` | `alt_text` | String | CONDITIONAL | Content Engine | Alternativtext |
| `MEDIA_015` | `caption` | String | NO | Content Engine | Bildunterschrift |
| `MEDIA_016` | `copyright_holder` | String | YES | Compliance Engine | Rechteinhaber |
| `MEDIA_017` | `usage_permission` | Enum | YES | Compliance Engine | Freigegeben, begrenzt oder verboten |
| `MEDIA_018` | `optimization_status` | Enum | YES | Performance Engine | OPTIMIZED, REVIEW oder ERROR |
| `MEDIA_019` | `accessibility_status` | Enum | YES | Accessibility Engine | VALID, WARNING oder ERROR |
| `MEDIA_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 20. SEO-Struktur

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `SEO_001` | `seo_record_id` | String | YES | SEO Engine | Eindeutige SEO-ID |
| `SEO_002` | `page_id` | String | YES | System | Seitenzuordnung |
| `SEO_003` | `primary_keyword` | String | YES | SEO Engine | Hauptsuchbegriff |
| `SEO_004` | `secondary_keywords` | JSON | NO | SEO Engine | Ergänzende Suchbegriffe |
| `SEO_005` | `search_intent` | Enum | YES | SEO Engine | Informational, Commercial oder Transactional |
| `SEO_006` | `seo_title` | String | YES | Content Engine | Suchergebnistitel |
| `SEO_007` | `meta_description` | String | YES | Content Engine | Meta-Beschreibung |
| `SEO_008` | `h1` | String | YES | Content Engine | Hauptüberschrift |
| `SEO_009` | `heading_structure` | JSON | YES | Content Engine | H2- bis H6-Struktur |
| `SEO_010` | `canonical_url` | URL | YES | SEO Engine | Kanonische URL |
| `SEO_011` | `robots_index` | Boolean | YES | SEO Engine | Indexierung |
| `SEO_012` | `robots_follow` | Boolean | YES | SEO Engine | Linkverfolgung |
| `SEO_013` | `sitemap_included` | Boolean | YES | SEO Engine | Sitemap-Status |
| `SEO_014` | `hreflang_entries` | JSON | NO | SEO Engine | Sprach- und Länderziele |
| `SEO_015` | `content_freshness_date` | Date | YES | Quality Engine | Aktualitätsdatum |
| `SEO_016` | `internal_link_count` | Integer | YES | SEO Engine | Interne Links |
| `SEO_017` | `external_source_count` | Integer | YES | SEO Engine | Externe Quellen |
| `SEO_018` | `seo_score` | Decimal | YES | SEO Engine | Interner Qualitätswert |
| `SEO_019` | `validation_status` | Enum | YES | Quality Engine | VALID, WARNING oder ERROR |
| `SEO_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 21. Schema.org & strukturierte Daten

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `SCHEMA_001` | `schema_record_id` | String | YES | Schema Engine | Eindeutige Schema-ID |
| `SCHEMA_002` | `page_id` | String | YES | System | Seitenzuordnung |
| `SCHEMA_003` | `primary_schema_type` | Enum | YES | Schema Engine | WebPage, Article, Product oder Service |
| `SCHEMA_004` | `additional_schema_types` | JSON | NO | Schema Engine | Ergänzende Typen |
| `SCHEMA_005` | `webpage_schema` | JSON | YES | Schema Engine | WebPage-Daten |
| `SCHEMA_006` | `organization_schema` | JSON | NO | Schema Engine | Betreiberangaben |
| `SCHEMA_007` | `breadcrumb_schema` | JSON | CONDITIONAL | Schema Engine | BreadcrumbList |
| `SCHEMA_008` | `faq_schema` | JSON | CONDITIONAL | Schema Engine | FAQPage |
| `SCHEMA_009` | `product_schema` | JSON | CONDITIONAL | Schema Engine | Product |
| `SCHEMA_010` | `service_schema` | JSON | CONDITIONAL | Schema Engine | Service |
| `SCHEMA_011` | `offer_schema` | JSON | CONDITIONAL | Schema Engine | Offer |
| `SCHEMA_012` | `review_schema` | JSON | CONDITIONAL | Schema Engine | Review |
| `SCHEMA_013` | `aggregate_rating_schema` | JSON | CONDITIONAL | Schema Engine | AggregateRating |
| `SCHEMA_014` | `image_object_schema` | JSON | NO | Schema Engine | ImageObject |
| `SCHEMA_015` | `video_object_schema` | JSON | NO | Schema Engine | VideoObject |
| `SCHEMA_016` | `publisher_reference` | String | YES | Config | Publisher-ID |
| `SCHEMA_017` | `source_consistency_valid` | Boolean | YES | Quality Engine | Übereinstimmung mit Seiteninhalt |
| `SCHEMA_018` | `schema_validation_result` | JSON | YES | Quality Engine | Prüfergebnis |
| `SCHEMA_019` | `compliance_status` | Enum | YES | Compliance Engine | VALID, WARNING oder ERROR |
| `SCHEMA_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 22. Accessibility & WCAG

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `A11Y_001` | `accessibility_record_id` | String | YES | System | Eindeutige Accessibility-ID |
| `A11Y_002` | `page_id` | String | YES | System | Seitenzuordnung |
| `A11Y_003` | `wcag_target_level` | Enum | YES | Config | A, AA oder AAA |
| `A11Y_004` | `document_language` | String | YES | Content Engine | Seitensprache |
| `A11Y_005` | `skip_link_enabled` | Boolean | YES | Template Engine | Sprunglink vorhanden |
| `A11Y_006` | `landmark_structure_valid` | Boolean | YES | Accessibility Engine | Header, Main, Nav und Footer korrekt |
| `A11Y_007` | `heading_order_valid` | Boolean | YES | Accessibility Engine | Überschriftenhierarchie |
| `A11Y_008` | `keyboard_navigation_valid` | Boolean | YES | Accessibility Engine | Tastaturbedienung |
| `A11Y_009` | `focus_visibility_valid` | Boolean | YES | Accessibility Engine | Fokus sichtbar |
| `A11Y_010` | `color_contrast_valid` | Boolean | YES | Accessibility Engine | Kontrast ausreichend |
| `A11Y_011` | `image_alt_status` | Enum | YES | Accessibility Engine | VALID, WARNING oder ERROR |
| `A11Y_012` | `form_label_status` | Enum | CONDITIONAL | Accessibility Engine | Formularbeschriftung |
| `A11Y_013` | `aria_usage_status` | Enum | YES | Accessibility Engine | ARIA-Prüfung |
| `A11Y_014` | `link_text_status` | Enum | YES | Accessibility Engine | Verständliche Linktexte |
| `A11Y_015` | `media_caption_status` | Enum | CONDITIONAL | Media Engine | Untertitel vorhanden |
| `A11Y_016` | `transcript_status` | Enum | CONDITIONAL | Media Engine | Transkript vorhanden |
| `A11Y_017` | `reduced_motion_supported` | Boolean | YES | Template Engine | Bewegungsreduktion |
| `A11Y_018` | `automated_test_result` | JSON | YES | Quality Engine | Automatisiertes Testergebnis |
| `A11Y_019` | `manual_review_status` | Enum | YES | Redaktion | VALID, REVIEW oder ERROR |
| `A11Y_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 23. Rechtliches & Compliance

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `LEGAL_001` | `legal_record_id` | String | YES | System | Eindeutige Rechts-ID |
| `LEGAL_002` | `page_id` | String | YES | System | Seitenzuordnung |
| `LEGAL_003` | `operator_name` | String | YES | Config | Seitenbetreiber |
| `LEGAL_004` | `operator_role` | Enum | YES | Compliance Engine | Tippgeber, Publisher oder Händler |
| `LEGAL_005` | `imprint_url` | URL | YES | Config | Impressum |
| `LEGAL_006` | `privacy_url` | URL | YES | Config | Datenschutz |
| `LEGAL_007` | `cookie_policy_url` | URL | CONDITIONAL | Config | Cookie-Hinweise |
| `LEGAL_008` | `affiliate_disclosure` | Text | CONDITIONAL | Compliance Engine | Affiliate-Hinweis |
| `LEGAL_009` | `advertising_label_required` | Boolean | YES | Compliance Engine | Kennzeichnungspflicht |
| `LEGAL_010` | `partner_legal_notice` | Text | CONDITIONAL | Partner Config | Partnerpflichttext |
| `LEGAL_011` | `provider_disclaimer` | Text | CONDITIONAL | Compliance Engine | Anbieterhinweis |
| `LEGAL_012` | `mediation_disclaimer` | Text | CONDITIONAL | Compliance Engine | Keine Vermittlung |
| `LEGAL_013` | `price_disclaimer` | Text | CONDITIONAL | Compliance Engine | Preisänderungshinweis |
| `LEGAL_014` | `data_processing_basis` | Enum | CONDITIONAL | Privacy Engine | Rechtsgrundlage |
| `LEGAL_015` | `consent_required` | Boolean | YES | Privacy Engine | Einwilligung erforderlich |
| `LEGAL_016` | `prohibited_terms_check` | JSON | YES | Compliance Engine | Verbotene Begriffe |
| `LEGAL_017` | `partner_rules_version` | String | YES | Compliance Engine | Regelversion |
| `LEGAL_018` | `legal_reviewed_at` | Datetime | YES | Compliance Engine | Letzte Prüfung |
| `LEGAL_019` | `compliance_status` | Enum | YES | Compliance Engine | VALID, WARNING oder ERROR |
| `LEGAL_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 24. Performance & Core Web Vitals

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `PERF_001` | `performance_record_id` | String | YES | System | Performance-ID |
| `PERF_002` | `page_id` | String | YES | System | Seitenzuordnung |
| `PERF_003` | `page_weight_bytes` | Integer | YES | Performance Engine | Gesamtgröße |
| `PERF_004` | `html_size_bytes` | Integer | YES | Performance Engine | HTML-Größe |
| `PERF_005` | `css_size_bytes` | Integer | YES | Performance Engine | CSS-Größe |
| `PERF_006` | `js_size_bytes` | Integer | YES | Performance Engine | JavaScript-Größe |
| `PERF_007` | `image_weight_bytes` | Integer | YES | Performance Engine | Bildgröße |
| `PERF_008` | `request_count` | Integer | YES | Performance Engine | Anzahl Requests |
| `PERF_009` | `lcp_ms` | Integer | YES | Performance Engine | Largest Contentful Paint |
| `PERF_010` | `inp_ms` | Integer | YES | Performance Engine | Interaction to Next Paint |
| `PERF_011` | `cls_score` | Decimal | YES | Performance Engine | Cumulative Layout Shift |
| `PERF_012` | `ttfb_ms` | Integer | YES | Performance Engine | Serverantwort |
| `PERF_013` | `lazy_loading_enabled` | Boolean | YES | Template Engine | Lazy Loading |
| `PERF_014` | `responsive_images_enabled` | Boolean | YES | Media Engine | Responsive Bilder |
| `PERF_015` | `compression_enabled` | Boolean | YES | Deployment | Komprimierung |
| `PERF_016` | `caching_enabled` | Boolean | YES | Deployment | Caching |
| `PERF_017` | `third_party_scripts` | JSON | YES | Performance Engine | Fremdskripte |
| `PERF_018` | `performance_score` | Decimal | YES | Quality Engine | Gesamtwert |
| `PERF_019` | `validation_status` | Enum | YES | Quality Engine | VALID, WARNING oder ERROR |
| `PERF_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 25. Analytics & Conversion Tracking

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `ANALYTICS_001` | `analytics_record_id` | String | YES | System | Tracking-ID |
| `ANALYTICS_002` | `page_id` | String | YES | System | Seitenzuordnung |
| `ANALYTICS_003` | `analytics_enabled` | Boolean | YES | Config | Tracking aktiv |
| `ANALYTICS_004` | `consent_required` | Boolean | YES | Privacy Engine | Einwilligung |
| `ANALYTICS_005` | `consent_category` | Enum | YES | Privacy Engine | Statistik oder Marketing |
| `ANALYTICS_006` | `page_view_event` | String | YES | Tracking Engine | Seitenereignis |
| `ANALYTICS_007` | `affiliate_click_event` | String | YES | Tracking Engine | Affiliate-Klick |
| `ANALYTICS_008` | `cta_click_event` | String | YES | Tracking Engine | CTA-Klick |
| `ANALYTICS_009` | `form_start_event` | String | CONDITIONAL | Tracking Engine | Formularstart |
| `ANALYTICS_010` | `form_complete_event` | String | CONDITIONAL | Tracking Engine | Formularabschluss |
| `ANALYTICS_011` | `outbound_click_event` | String | YES | Tracking Engine | Externer Klick |
| `ANALYTICS_012` | `campaign_parameters` | JSON | NO | Tracking Engine | UTM- oder Sub-ID |
| `ANALYTICS_013` | `partner_tracking_id` | String | NO | Partner Config | Partner-Tracking |
| `ANALYTICS_014` | `conversion_id` | String | NO | Tracking Engine | Conversion-Zuordnung |
| `ANALYTICS_015` | `revenue_value` | Decimal | NO | Attribution Engine | Vergütung |
| `ANALYTICS_016` | `revenue_currency` | String | NO | Attribution Engine | Währung |
| `ANALYTICS_017` | `anonymization_enabled` | Boolean | YES | Privacy Engine | Anonymisierung |
| `ANALYTICS_018` | `retention_days` | Integer | YES | Privacy Engine | Aufbewahrung |
| `ANALYTICS_019` | `validation_status` | Enum | YES | Quality Engine | VALID, WARNING oder ERROR |
| `ANALYTICS_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 26. Personalisierung & Lokalisierung

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `LOC_001` | `localization_record_id` | String | YES | System | Lokalisierungs-ID |
| `LOC_002` | `page_id` | String | YES | System | Seitenzuordnung |
| `LOC_003` | `default_language` | String | YES | Config | Standardsprache |
| `LOC_004` | `available_languages` | JSON | YES | Config | Sprachen |
| `LOC_005` | `default_country` | String | YES | Config | Standardland |
| `LOC_006` | `available_countries` | JSON | YES | Config | Zielländer |
| `LOC_007` | `default_currency` | String | YES | Config | Währung |
| `LOC_008` | `locale_code` | String | YES | Config | Gebietsschema |
| `LOC_009` | `translated_content` | JSON | NO | Translation Engine | Übersetzungen |
| `LOC_010` | `translation_status` | Enum | YES | Translation Engine | VALID, REVIEW oder MISSING |
| `LOC_011` | `hreflang_mapping` | JSON | NO | SEO Engine | Sprachzuordnung |
| `LOC_012` | `regional_availability` | JSON | NO | Product Engine | Regionale Verfügbarkeit |
| `LOC_013` | `regional_disclaimer` | Text | NO | Compliance Engine | Regionale Hinweise |
| `LOC_014` | `device_variant` | Enum | NO | Layout Engine | Desktop oder Mobile |
| `LOC_015` | `traffic_source_variant` | Enum | NO | Campaign Engine | Kampagnenvariante |
| `LOC_016` | `personalization_basis` | Enum | NO | Personalization Engine | Sprache, Region oder Quelle |
| `LOC_017` | `user_profile_required` | Boolean | YES | Privacy Engine | Profil nötig |
| `LOC_018` | `consent_required` | Boolean | YES | Privacy Engine | Einwilligung |
| `LOC_019` | `validation_status` | Enum | YES | Quality Engine | VALID, WARNING oder ERROR |
| `LOC_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 27. Content-Qualität & AI-Governance

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `AIQ_001` | `ai_quality_record_id` | String | YES | System | Governance-ID |
| `AIQ_002` | `page_id` | String | YES | System | Seitenzuordnung |
| `AIQ_003` | `ai_generated` | Boolean | YES | Content Engine | AI-Inhalt |
| `AIQ_004` | `ai_model` | String | CONDITIONAL | Content Engine | Modell |
| `AIQ_005` | `prompt_id` | String | CONDITIONAL | Prompt Registry | Prompt-ID |
| `AIQ_006` | `prompt_version` | String | CONDITIONAL | Prompt Registry | Prompt-Version |
| `AIQ_007` | `generation_id` | String | CONDITIONAL | Content Engine | Generierungs-ID |
| `AIQ_008` | `source_grounded` | Boolean | YES | Quality Engine | Quellengebunden |
| `AIQ_009` | `source_ids` | JSON | CONDITIONAL | Source Engine | Quellen |
| `AIQ_010` | `factual_claims` | JSON | YES | Content Engine | Faktenbehauptungen |
| `AIQ_011` | `unsupported_claims_count` | Integer | YES | Quality Engine | Unbelegte Aussagen |
| `AIQ_012` | `hallucination_risk` | Enum | YES | Quality Engine | LOW, MEDIUM oder HIGH |
| `AIQ_013` | `prohibited_terms_found` | JSON | YES | Compliance Engine | Verbotsbegriffe |
| `AIQ_014` | `duplicate_content_score` | Decimal | YES | Quality Engine | Duplikatwert |
| `AIQ_015` | `readability_score` | Decimal | YES | Quality Engine | Lesbarkeit |
| `AIQ_016` | `tone_validation` | Enum | YES | Quality Engine | VALID, REVIEW oder ERROR |
| `AIQ_017` | `human_review_required` | Boolean | YES | Governance | Prüfung nötig |
| `AIQ_018` | `human_review_status` | Enum | YES | Redaktion | PENDING, APPROVED oder REJECTED |
| `AIQ_019` | `quality_status` | Enum | YES | Quality Engine | VALID, WARNING oder ERROR |
| `AIQ_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 28. Veröffentlichung & Workflow

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `PUB_001` | `publication_record_id` | String | YES | System | Veröffentlichungs-ID |
| `PUB_002` | `page_id` | String | YES | System | Seitenzuordnung |
| `PUB_003` | `workflow_status` | Enum | YES | Workflow Engine | DRAFT, REVIEW, APPROVED oder PUBLISHED |
| `PUB_004` | `content_status` | Enum | YES | Content Engine | Inhaltsstatus |
| `PUB_005` | `seo_status` | Enum | YES | SEO Engine | SEO-Status |
| `PUB_006` | `compliance_status` | Enum | YES | Compliance Engine | Compliance-Status |
| `PUB_007` | `accessibility_status` | Enum | YES | Accessibility Engine | Accessibility-Status |
| `PUB_008` | `performance_status` | Enum | YES | Performance Engine | Performance-Status |
| `PUB_009` | `schema_status` | Enum | YES | Schema Engine | Schema-Status |
| `PUB_010` | `link_status` | Enum | YES | Link Monitor | Linkstatus |
| `PUB_011` | `reviewer_id` | String | CONDITIONAL | Redaktion | Prüfer |
| `PUB_012` | `approved_by` | String | CONDITIONAL | Workflow Engine | Freigeber |
| `PUB_013` | `approved_at` | Datetime | CONDITIONAL | Workflow Engine | Freigabezeit |
| `PUB_014` | `scheduled_publish_at` | Datetime | NO | Publisher | Planung |
| `PUB_015` | `published_at` | Datetime | NO | Publisher | Veröffentlichung |
| `PUB_016` | `publication_target` | Enum | YES | Publisher | Cloud Run oder Blogger |
| `PUB_017` | `publication_url` | URL | NO | Publisher | Öffentliche URL |
| `PUB_018` | `publication_result` | JSON | NO | Publisher | Ergebnis |
| `PUB_019` | `blocking_errors` | JSON | YES | Quality Engine | Blockierende Fehler |
| `PUB_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 29. Versionierung & Änderungsverlauf

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `VER_001` | `version_record_id` | String | YES | System | Versions-ID |
| `VER_002` | `page_id` | String | YES | System | Seitenzuordnung |
| `VER_003` | `version_number` | String | YES | Version Engine | Versionsnummer |
| `VER_004` | `previous_version` | String | NO | Version Engine | Vorgänger |
| `VER_005` | `change_type` | Enum | YES | Version Engine | CREATE, UPDATE, FIX oder ROLLBACK |
| `VER_006` | `changed_fields` | JSON | YES | Version Engine | Geänderte Felder |
| `VER_007` | `previous_values` | JSON | NO | Version Engine | Alte Werte |
| `VER_008` | `new_values` | JSON | NO | Version Engine | Neue Werte |
| `VER_009` | `change_reason` | Text | YES | System | Begründung |
| `VER_010` | `changed_by` | String | YES | System | Benutzer oder Engine |
| `VER_011` | `changed_at` | Datetime | YES | System | Zeitpunkt |
| `VER_012` | `source_commit` | String | NO | GitHub | Commit |
| `VER_013` | `source_run_id` | String | NO | Engine | Lauf-ID |
| `VER_014` | `prompt_version` | String | NO | Prompt Registry | Prompt-Version |
| `VER_015` | `compliance_version` | String | YES | Compliance Engine | Regelversion |
| `VER_016` | `rollback_available` | Boolean | YES | Version Engine | Rollback möglich |
| `VER_017` | `rollback_target` | String | NO | Version Engine | Zielversion |
| `VER_018` | `snapshot_location` | String | YES | Drive | Snapshot |
| `VER_019` | `validation_status` | Enum | YES | Quality Engine | VALID, WARNING oder ERROR |
| `VER_020` | `status` | Enum | YES | System | ACTIVE, ARCHIVED oder INVALID |

### 30. Archivierung & Lifecycle

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `LIFE_001` | `lifecycle_record_id` | String | YES | System | Lifecycle-ID |
| `LIFE_002` | `page_id` | String | YES | System | Seitenzuordnung |
| `LIFE_003` | `lifecycle_status` | Enum | YES | Lifecycle Engine | ACTIVE, EXPIRING oder ARCHIVED |
| `LIFE_004` | `activation_date` | Date | YES | System | Aktivierung |
| `LIFE_005` | `expiration_date` | Date | NO | Product Engine | Ablaufdatum |
| `LIFE_006` | `review_due_date` | Date | YES | Quality Engine | Nächste Prüfung |
| `LIFE_007` | `deactivation_reason` | Text | NO | System | Grund |
| `LIFE_008` | `product_discontinued` | Boolean | YES | Product Engine | Produkt eingestellt |
| `LIFE_009` | `partner_inactive` | Boolean | YES | Partner Engine | Partner inaktiv |
| `LIFE_010` | `affiliate_link_inactive` | Boolean | YES | Link Monitor | Link inaktiv |
| `LIFE_011` | `replacement_page_id` | String | NO | Lifecycle Engine | Ersatzseite |
| `LIFE_012` | `redirect_required` | Boolean | YES | SEO Engine | Weiterleitung |
| `LIFE_013` | `redirect_type` | Enum | NO | SEO Engine | 301, 302 oder 410 |
| `LIFE_014` | `redirect_target_url` | URL | NO | SEO Engine | Ziel |
| `LIFE_015` | `remove_from_sitemap` | Boolean | YES | SEO Engine | Sitemap-Entfernung |
| `LIFE_016` | `robots_index` | Boolean | YES | SEO Engine | Indexierung |
| `LIFE_017` | `archive_snapshot_path` | String | YES | Drive | Archivkopie |
| `LIFE_018` | `archived_at` | Datetime | NO | Lifecycle Engine | Archivzeitpunkt |
| `LIFE_019` | `validation_status` | Enum | YES | Quality Engine | VALID, WARNING oder ERROR |
| `LIFE_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 31. Qualitätsprüfung & Freigabe

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `QA_001` | `qa_record_id` | String | YES | Quality Engine | QA-ID |
| `QA_002` | `page_id` | String | YES | System | Seitenzuordnung |
| `QA_003` | `required_fields_complete` | Boolean | YES | Quality Engine | Pflichtfelder vollständig |
| `QA_004` | `factual_validation_passed` | Boolean | YES | Quality Engine | Faktenprüfung |
| `QA_005` | `source_validation_passed` | Boolean | YES | Quality Engine | Quellenprüfung |
| `QA_006` | `compliance_validation_passed` | Boolean | YES | Compliance Engine | Compliance |
| `QA_007` | `seo_validation_passed` | Boolean | YES | SEO Engine | SEO |
| `QA_008` | `schema_validation_passed` | Boolean | YES | Schema Engine | Schema |
| `QA_009` | `accessibility_validation_passed` | Boolean | YES | Accessibility Engine | Accessibility |
| `QA_010` | `performance_validation_passed` | Boolean | YES | Performance Engine | Performance |
| `QA_011` | `link_validation_passed` | Boolean | YES | Link Monitor | Links |
| `QA_012` | `media_validation_passed` | Boolean | YES | Media Engine | Medien |
| `QA_013` | `tracking_validation_passed` | Boolean | YES | Tracking Engine | Tracking |
| `QA_014` | `duplicate_validation_passed` | Boolean | YES | Quality Engine | Duplikate |
| `QA_015` | `prohibited_terms_passed` | Boolean | YES | Compliance Engine | Verbotsbegriffe |
| `QA_016` | `warning_count` | Integer | YES | Quality Engine | Warnungen |
| `QA_017` | `error_count` | Integer | YES | Quality Engine | Fehler |
| `QA_018` | `release_decision` | Enum | YES | Quality Engine | APPROVED, BLOCKED oder REVIEW |
| `QA_019` | `reviewed_at` | Datetime | YES | Quality Engine | Prüfzeitpunkt |
| `QA_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

### 32. System-Metadaten & Deployment

| Feld-ID | Feldname | Typ | Pflicht | Quelle | Beschreibung |
|---|---|---|:---:|---|---|
| `SYS_001` | `system_record_id` | String | YES | System | System-ID |
| `SYS_002` | `page_id` | String | YES | System | Seitenzuordnung |
| `SYS_003` | `project_name` | String | YES | Config | Projektname |
| `SYS_004` | `project_id` | String | YES | Config | Cloud-Projekt |
| `SYS_005` | `environment` | Enum | YES | Deployment | DEVELOPMENT, STAGING oder PRODUCTION |
| `SYS_006` | `repository` | String | YES | GitHub | Repository |
| `SYS_007` | `branch` | String | YES | GitHub | Branch |
| `SYS_008` | `commit_sha` | String | CONDITIONAL | GitHub | Commit |
| `SYS_009` | `build_id` | String | CONDITIONAL | Cloud Build | Build-ID |
| `SYS_010` | `deployment_id` | String | CONDITIONAL | Deployment | Deployment-ID |
| `SYS_011` | `service_name` | String | YES | Cloud Run | Dienst |
| `SYS_012` | `region` | String | YES | Cloud Run | Region |
| `SYS_013` | `deployment_url` | URL | NO | Cloud Run | Ziel-URL |
| `SYS_014` | `healthcheck_url` | URL | NO | Monitoring | Healthcheck |
| `SYS_015` | `deployment_status` | Enum | YES | Deployment | SUCCESS, FAILED oder PENDING |
| `SYS_016` | `deployed_at` | Datetime | NO | Deployment | Zeitpunkt |
| `SYS_017` | `log_reference` | String | NO | Logging | Log-ID |
| `SYS_018` | `monitoring_status` | Enum | YES | Monitoring | HEALTHY, DEGRADED oder DOWN |
| `SYS_019` | `rollback_version` | String | NO | Deployment | Rollback |
| `SYS_020` | `status` | Enum | YES | System | ACTIVE, REVIEW oder DISABLED |

## Verbindliche Partnerregeln

- Affiliate-Links und Werbemittel werden unmittelbar als **Werbung** oder **Anzeige** gekennzeichnet.
- Tarifcheck: Free Basics ist Tippgeber; `powered by TARIFCHECK24 GmbH` und die dokumentierten Pflichtangaben müssen sichtbar sein.
- Check24: keine Verwendung von `CHECK24` in Landingpage-URLs oder SEO-Titeln.
- Telekom: Produktabschluss ausschließlich über `https://free-basics.telekom-profis.de`; keine eigene Abschluss-Landingpage.
- Amazon: nur zulässige PartnerNet-Links und Originalbilder aus freigegebenen Quellen.
- Fehlende Preise, Leistungswerte, Bewertungen oder technische Daten bleiben leer und werden nicht erfunden.

## Release-Gate

Eine Landingpage darf nur veröffentlicht werden, wenn alle blockierenden Qualitäts-, Quellen-, Compliance-, SEO-, Schema-, Accessibility-, Link- und Medienprüfungen bestanden sind und `error_count = 0` sowie `release_decision = APPROVED` gelten.