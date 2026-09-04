# HomePantry 0.1.0-alpha.1

This is the first public alpha release of HomePantry.

HomePantry is a self-hosted household pantry, inventory, and recipe
management application designed for everyday use on desktop and mobile
devices.

## Highlights

- Household-based inventory management
- Ingredient and product catalog
- Barcode support and browser-based barcode scanning
- Open Food Facts product metadata lookup
- Hierarchical storage locations
- Inventory batches and movement history
- Low-stock rules
- Recipe management with images and tags
- Recipe availability based on current inventory
- Online recipe search and import through TheMealDB
- Optional local recipe translation with LibreTranslate
- Hungarian and English user interface
- Multi-user household support
- PostgreSQL database
- Automated Ubuntu installation
- Reverse-proxy and application-prefix support

## Installation

The recommended installation target for this release is Ubuntu 24.04 LTS.

HomePantry includes an installation script that prepares PostgreSQL,
the Python virtual environment, database migrations, reference data,
systemd service, and application configuration.

Detailed installation instructions are provided in the repository
documentation.

## Alpha status

This release is intended for self-hosters who are comfortable operating
and backing up their own services.

Although HomePantry is already used as a real household application,
this is the first public release. Installation paths, configuration,
database migrations, and documentation may continue to evolve during
the alpha releases.

Back up your database and uploaded media before upgrading.

## Third-party services

Some features integrate with external or separately deployed services:

- Open Food Facts
- TheMealDB
- LibreTranslate

Barcode scanning uses the bundled Quagga2 library.

See `THIRD_PARTY_NOTICES.md` for details.

## License

HomePantry is released under the MIT License.
