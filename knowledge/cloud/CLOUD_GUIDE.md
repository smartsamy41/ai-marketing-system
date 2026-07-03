# FBEP-KNOW-0008

# Cloud Infrastructure Knowledge Base

Version: 1.0.0
Status: Official
Owner: Samy Jendoubi
Project: Free Basics Enterprise Platform

## Purpose

Defines the current Google Cloud and production infrastructure for FBEP.

## Production Project

Project ID:
smartcontent2050

Project Number:
1081897051313

## Production Cloud Run URL

https://ai-marketing-system-1081897051313.europe-west1.run.app

## Production Region

europe-west1

## Important Rule

europe-west1 is the current production region.

This region contains the validated Cloud Run service, working environment variables and production configuration.

No migration to another region is allowed without a documented migration plan.

## Europe West 3

europe-west3 must not be deleted until a full audit confirms that no production service, secret, scheduler, domain mapping or environment variable depends on it.

## Domain

Primary domain:
freebasics.online

Domain status:
Cloudflare active, SSL active, Cloud Run connected.

Secondary domain:
freebasics-online.de

Status:
Registered. Cloudflare integration pending.

## Secrets

All production secrets must be stored in Google Cloud Secret Manager.

Current / required secret categories:

- Google OAuth credentials
- Google Sheets credentials
- Google Drive credentials
- YouTube credentials
- Groq API key
- Hugging Face token
- Affiliate API credentials
- Pinterest OAuth credentials
- Gemini API key

## Gemini

Gemini will be added as an additional AI partner.

Gemini is not a replacement for ChatGPT.

Both AI systems must work from the same FBEP repository documentation.

## Rule

Do not hardcode secrets.

Do not move production regions without audit.

Do not delete cloud resources without documentation.

End of Document
