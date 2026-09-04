# Changelog

All notable changes to HomePantry will be documented in this file.

## [0.1.0-alpha.1] - 2026-09-04

### Added

- Household-based user and member management.
- Bilingual Hungarian and English user interface.
- Ingredient master data with categories, aliases, units, and substitutions.
- Product management with multiple barcodes and product images.
- Open Food Facts integration for product metadata.
- Storage location hierarchy with location images.
- Inventory batches, stock rules, and inventory movement history.
- Barcode scanning from supported browser cameras using Quagga2.
- Recipe management with ingredients, tags, and images.
- Online recipe search and import using TheMealDB.
- Measurement normalization for imported recipes.
- Optional English-to-Hungarian recipe translation using LibreTranslate.
- Recipe availability calculations based on household inventory.
- PostgreSQL database with Alembic migrations.
- Gunicorn and systemd deployment support.
- Application-prefix support for reverse-proxy deployments.
- Health-check endpoint.
- Automated Ubuntu installation script.
- Reference-data seeding for clean installations.

### Changed

- Prepared deployment configuration for reproducible public installation.
- Made the application session cookie HomePantry-specific.
- Improved inventory filtering, movement display, and entry workflows.
- Improved ingredient autocomplete and storage-location navigation.
- Improved recipe availability handling for water.

### Security

- Application secrets and database credentials are kept outside version control.
- CSRF protection is enabled for forms.
- Authentication is handled with Flask-Login.
- Production configuration uses a dedicated environment file.

### Notes

This is the first public alpha release of HomePantry.

The project is functional and actively used, but the public installation
and upgrade experience should still be considered alpha quality.
