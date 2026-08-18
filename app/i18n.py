from flask_login import current_user


TRANSLATIONS = {
    "hu": {
        "product_field_images": "Termékképek",
        "product_images_help": (
            "Több JPG, PNG vagy WEBP kép is "
            "feltölthető. A képek automatikusan "
            "átméretezésre és tömörítésre kerülnek."
        ),
        "product_images_existing": (
            "Feltöltött képek"
        ),
        "product_image_cover": "Borítókép",
        "product_image_set_cover": (
            "Beállítás borítóképként"
        ),
        "product_image_delete": "Kép törlése",
        "product_image_invalid": (
            "A feltöltött kép nem érvényes "
            "vagy nem támogatott formátumú."
        ),
        "product_image_cover_updated": (
            "A borítókép módosítva."
        ),
        "product_image_deleted": (
            "A kép törölve."
        ),
        "search": "Keresés",
        "clear": "Törlés",
        "admin_dashboard_title": (
            "Adminisztráció"
        ),
        "admin_dashboard_description": (
            "A HomePantry törzsadatainak és "
            "felhasználóinak karbantartása."
        ),
        "admin_total": "összesen",

        "pagination_previous": "Előző",
        "pagination_next": "Következő",
        "dashboard_title": "Áttekintés",
        "dashboard_welcome": "Szia",
        "dashboard_household": "Háztartás",

        "dashboard_inventory": "Készlet",
        "dashboard_batches": "készlettétel",
        "dashboard_expiring": "Hamarosan lejár",
        "dashboard_expired": "Lejárt",
        "dashboard_low_stock": "Minimum alatt",
        "dashboard_ingredients": "alapanyag",
        "dashboard_next_three_days": (
            "A következő 3 napban"
        ),
        "dashboard_needs_attention": (
            "Figyelmet igényel"
        ),

        "dashboard_attention": (
            "Lejáratok"
        ),
        "dashboard_attention_help": (
            "Lejárt és hamarosan lejáró készlettételek."
        ),
        "dashboard_view_inventory": (
            "Teljes készlet"
        ),
        "dashboard_no_expiration_alerts": (
            "Nincs lejárt vagy hamarosan lejáró tétel."
        ),

        "dashboard_low_stock_help": (
            "A beállított minimumkészlet alá került alapanyagok."
        ),
        "dashboard_current": "Jelenleg",
        "dashboard_stock_ok": (
            "Minden beállított minimumkészlet rendben van."
        ),

        "dashboard_recent_movements": (
            "Legutóbbi készletmozgások"
        ),
        "dashboard_recent_movements_help": (
            "A legfrissebb készletváltozások."
        ),

        "dashboard_quick_actions": (
            "Gyors műveletek"
        ),
        "dashboard_quick_actions_help": (
            "A leggyakrabban használt funkciók."
        ),
        "dashboard_quick_inventory_help": (
            "Vonalkód vagy kézi bevitel"
        ),
        "dashboard_quick_products_help": (
            "Terméktörzs és vonalkódok"
        ),
        "dashboard_quick_locations_help": (
            "Tárhelyek karbantartása"
        ),
        "dashboard_quick_movements_help": (
            "Készletváltozások előzményei"
        ),

        "dashboard_no_household": (
            "Nincs aktív háztartás a felhasználóhoz rendelve."
        ),
        "unit_dimension_mass": "Tömeg",
        "unit_dimension_volume": "Térfogat",
        "unit_dimension_count": "Darabszám",
        "product_add_ingredient": (
            "+ Új alapanyag"
        ),
        "nav_ingredients_admin": "Alapanyagok",

        "ingredient_admin_title": "Alapanyagok",
        "ingredient_admin_description": (
            "Az alapanyagtörzs karbantartása."
        ),
        "ingredient_admin_new": "Új alapanyag",
        "ingredient_admin_edit": (
            "Alapanyag szerkesztése"
        ),

        "ingredient_admin_name_hu": (
            "Magyar név"
        ),
        "ingredient_admin_name_en": (
            "Angol név"
        ),
        "ingredient_admin_category": (
            "Kategória"
        ),
        "ingredient_admin_no_category": (
            "— Nincs kategória —"
        ),
        "ingredient_admin_default_unit": (
            "Alapértelmezett mértékegység"
        ),
        "ingredient_admin_allowed_units": (
            "Engedélyezett mértékegységek"
        ),
        "ingredient_admin_aliases_hu": (
            "Magyar alternatív nevek"
        ),
        "ingredient_admin_aliases_en": (
            "Angol alternatív nevek"
        ),

        "ingredient_admin_alias_help": (
            "Soronként vagy vesszővel elválasztva "
            "több név is megadható."
        ),

        "ingredient_admin_default_must_be_allowed": (
            "Az alapértelmezett mértékegységet "
            "az engedélyezett egységek között is "
            "ki kell választani."
        ),
        "ingredient_admin_exists": (
            "Ilyen alapanyag már létezik."
        ),
        "ingredient_admin_created": (
            "Az alapanyag létrejött."
        ),
        "ingredient_admin_updated": (
            "Az alapanyag módosítva."
        ),
        "nav_movements": "Készletmozgások",

        "movements_title": "Készletmozgások",
        "movements_description": (
            "A készlet változásainak teljes története."
        ),
        "movements_search_placeholder": (
            "Keresés alapanyag, termék, típus "
            "vagy megjegyzés alapján..."
        ),

        "movement_type_opening_balance": (
            "Készletre vétel"
        ),
        "movement_type_consume": "Fogyasztás",
        "movement_type_discard": "Selejt",
        "movement_type_adjustment": "Korrekció",
        "movement_type_transfer": "Áthelyezés",

        "movement_col_time": "Időpont",
        "movement_col_ingredient": "Alapanyag",
        "movement_col_product": "Termék",
        "movement_col_type": "Mozgás",
        "movement_col_change": "Változás",
        "movement_col_before_after": (
            "Előtte → utána"
        ),
        "movement_col_user": "Felhasználó",
        "movement_col_note": "Megjegyzés",

        "movements_empty": (
            "Még nincs rögzített készletmozgás."
        ),
        "nav_stock_rules": "Minimumkészlet",

        "stock_rule_title": "Minimumkészlet",
        "stock_rule_description": (
            "Alapanyagonkénti minimum készletszintek kezelése."
        ),
        "stock_rule_add": "Új minimumkészlet szabály",
        "stock_rule_new_title": (
            "Új minimumkészlet szabály"
        ),
        "stock_rule_edit_title": (
            "Minimumkészlet szabály szerkesztése"
        ),
        "stock_rule_minimum_quantity": (
            "Minimum mennyiség"
        ),
        "stock_rule_exists": (
            "Ehhez az alapanyaghoz már létezik szabály."
        ),
        "stock_rule_created": (
            "A minimumkészlet szabály létrejött."
        ),
        "stock_rule_updated": (
            "A minimumkészlet szabály módosítva."
        ),
        "stock_rule_deactivated": (
            "A minimumkészlet szabály inaktiválva."
        ),
        "stock_rule_reactivated": (
            "A minimumkészlet szabály visszaaktiválva."
        ),
        "movement_actions": "Műveletek",
        "movement_consume": "Fogyasztás",
        "movement_discard": "Selejt",
        "movement_adjust": "Korrekció",
        "movement_transfer": "Áthelyezés",

        "movement_quantity": "Mennyiség",
        "movement_actual_quantity": (
            "Tényleges készlet"
        ),

        "movement_consume_title": (
            "Készlet fogyasztása"
        ),
        "movement_discard_title": (
            "Készlet selejtezése"
        ),
        "movement_adjust_title": (
            "Készlet korrekciója"
        ),
        "movement_transfer_title": (
            "Készlet áthelyezése"
        ),

        "movement_current_quantity": (
            "Jelenlegi mennyiség"
        ),

        "movement_too_much": (
            "A megadott mennyiség nagyobb "
            "a rendelkezésre álló készletnél."
        ),

        "movement_consumed": (
            "A fogyasztás rögzítve."
        ),
        "movement_discarded": (
            "A selejt rögzítve."
        ),
        "movement_adjusted": (
            "A készlet korrigálva."
        ),
        "movement_transferred": (
            "A készlettétel áthelyezve."
        ),
        "inventory_filter_all": "Minden",
        "inventory_filter_low": (
            "Minimumkészlet alatt"
        ),
        "inventory_filter_expiring": (
            "Hamarosan lejár"
        ),
        "inventory_filter_expired": (
            "Lejárt"
        ),

        "inventory_status_low": (
            "Minimumkészlet alatt"
        ),
        "inventory_status_expiring": (
            "Hamarosan lejár"
        ),
        "inventory_status_expired": (
            "Lejárt"
        ),

        "inventory_minimum_stock": (
            "Minimum készlet"
        ),
        "inventory_search_placeholder": (
            "Keresés alapanyag, termék, márka, "
            "vonalkód vagy tárhely alapján..."
        ),
        "inventory_batches": "Készlettételek",
        "inventory_col_purchase": "Vásárlás",
        "inventory_no_expiration": "Nincs megadva",
        "inventory_batch_count": "tétel",
        "barcode_create_product": (
            "Új termék rögzítése ehhez a vonalkódhoz"
        ),
        "barcode_new_product_name": "Terméknév",
        "barcode_new_product_brand": "Márka",
        "barcode_new_product_name_required": (
            "Ismeretlen vonalkódnál add meg a termék nevét."
        ),
        "barcode_product_created_with_stock": (
            "Az új termék és a készlettétel létrejött."
        ),
        "barcode_scan": "Vonalkód beolvasása",
        "barcode_stop_scan": "Kamera bezárása",
        "barcode_lookup": "Vonalkód keresése",
        "barcode_lookup_placeholder": (
            "Írd be vagy olvasd be a vonalkódot..."
        ),
        "barcode_product_found": (
            "Termék megtalálva."
        ),
        "barcode_product_not_found": (
            "Ehhez a vonalkódhoz még nincs termék."
        ),
        "barcode_camera_error": (
            "A kamera nem indítható."
        ),
        "nav_products": "Termékek",

        "product_title": "Termékek",
        "product_description": (
            "Csomagolt és ömlesztett termékek kezelése."
        ),
        "product_search_placeholder": (
            "Keresés terméknév, márka, alapanyag "
            "vagy vonalkód alapján..."
        ),
        "product_new_title": "Új termék",
        "product_edit_title": "Termék szerkesztése",

        "product_field_ingredient": "Alapanyag",
        "ingredient_select_placeholder": (
            "— Kezdd el gépelni az alapanyagot —"
        ),
        "product_field_name": "Terméknév",
        "product_field_brand": "Márka",
        "product_field_package_quantity": (
            "Csomag mennyisége"
        ),
        "product_field_package_unit": (
            "Csomag mértékegysége"
        ),
        "product_field_barcode": "Vonalkód",
        "product_field_barcode_type": (
            "Vonalkód típusa"
        ),

        "product_no_package_unit": (
            "— Nincs megadva —"
        ),
        "product_no_barcode": (
            "Nincs vonalkód"
        ),

        "product_add": "Új termék",
        "product_edit": "Szerkesztés",
        "product_deactivate": "Inaktiválás",
        "product_reactivate": "Visszaaktiválás",

        "product_created": (
            "A termék létrejött."
        ),
        "product_updated": (
            "A termék módosítva."
        ),
        "product_deactivated": (
            "A termék inaktiválva."
        ),
        "product_reactivated": (
            "A termék visszaaktiválva."
        ),
        "product_barcode_exists": (
            "Ez a vonalkód már egy másik "
            "termékhez tartozik."
        ),
        "admin_add_user": "Új felhasználó",
        "admin_password": "Kezdeti jelszó",
        "admin_user_created": (
            "A felhasználó létrejött."
        ),
        "nav_profile": "Profil",
        "nav_admin": "Admin",

        "profile_title": "Profil",
        "profile_description": (
            "Saját felhasználói beállítások."
        ),
        "profile_display_name": "Megjelenített név",
        "profile_username": "Felhasználónév",
        "profile_email": "E-mail cím",
        "profile_language": "Felület nyelve",
        "profile_measurement_system": (
            "Mértékegység-rendszer"
        ),
        "profile_updated": (
            "A profil módosítva."
        ),
        "profile_identity_exists": (
            "Ez az e-mail cím vagy "
            "felhasználónév már használatban van."
        ),

        "admin_users_title": (
            "Felhasználók"
        ),
        "admin_users_description": (
            "A háztartás felhasználóinak kezelése."
        ),
        "admin_user": "Felhasználó",
        "admin_role": "Szerepkör",
        "admin_active": "Aktív",
        "admin_language": "Nyelv",
        "admin_measurement": (
            "Mértékegységek"
        ),
        "admin_edit": "Szerkesztés",
        "admin_yes": "Igen",
        "admin_no": "Nem",
        "admin_user_edit_title": (
            "Felhasználó szerkesztése"
        ),
        "admin_user_updated": (
            "A felhasználó módosítva."
        ),
        "app_name": "HomePantry",

        "nav_inventory": "Készlet",
        "nav_storage": "Tárhelyek",
        "nav_logout": "Kijelentkezés",

        "storage_title": "Tárhelyek",
        "storage_description": (
            "Helyiségek, hűtők, fagyasztók, "
            "polcok és egyéb tárhelyek kezelése."
        ),
        "storage_add": "Új tárhely",
        "storage_active": "Aktív tárhelyek",
        "storage_inactive": "Inaktív tárhelyek",
        "storage_empty": "Még nincs felvett tárhely.",
        "storage_edit": "Szerkesztés",
        "storage_deactivate": "Inaktiválás",
        "storage_reactivate": "Visszaaktiválás",
        "storage_inactive_label": "Inaktív",

        "storage_new_title": "Új tárhely",
        "storage_edit_title": "Tárhely szerkesztése",

        "field_name": "Név",
        "field_type": "Típus",
        "field_parent": "Szülő tárhely",
        "field_sort_order": "Sorrend",

        "save": "Mentés",
        "cancel": "Mégse",

        "no_parent": "— Nincs szülő —",

        "location_type_room": "Helyiség",
        "location_type_cabinet": "Szekrény",
        "location_type_shelf": "Polc",
        "location_type_fridge": "Hűtő",
        "location_type_freezer": "Fagyasztó",
        "location_type_drawer": "Fiók",
        "location_type_box": "Doboz",
        "location_type_storage": "Egyéb tárhely",

        "storage_created": "A tárhely létrejött.",
        "storage_updated": "A tárhely módosítva.",
        "storage_deactivated": "A tárhely inaktiválva.",
        "storage_reactivated": "A tárhely visszaaktiválva.",
        "storage_has_children": (
            "A tárhelynek még vannak aktív "
            "gyermek tárhelyei."
        ),
        "storage_parent_inactive": (
            "Előbb a szülő tárhelyet kell "
            "visszaaktiválni."
        ),

        "inventory_title": "Készlet",
        "inventory_add": "Új készlettétel",
        "inventory_description": (
            "Az aktuális készlettételek."
        ),
        "inventory_empty": (
            "A készlet jelenleg üres."
        ),

        "inventory_field_ingredient": "Alapanyag",
        "inventory_field_product": "Termék",
        "inventory_field_location": "Tárhely",
        "inventory_field_quantity": "Mennyiség",
        "inventory_field_unit": "Mértékegység",
        "inventory_field_purchase_date": (
            "Vásárlás dátuma"
        ),
        "inventory_field_expiration_date": (
            "Lejárati dátum"
        ),
        "inventory_field_note": "Megjegyzés",

        "inventory_bulk_product": (
            "— Ömlesztett / nincs konkrét termék —"
        ),
        "inventory_bulk_help": (
            "Ömlesztett vagy vonalkód nélküli "
            "alapanyagnál ezt hagyd kiválasztva."
        ),

        "inventory_add_submit": (
            "Készlethez adás"
        ),
        "inventory_added": (
            "A készlettétel hozzáadva."
        ),

        "inventory_col_ingredient": "Alapanyag",
        "inventory_col_product": "Termék",
        "inventory_col_quantity": "Mennyiség",
        "inventory_col_location": "Tárhely",
        "inventory_col_expiration": "Lejárat",

        "inventory_bulk_label": "Ömlesztett",
    },

    "en": {
        "product_field_images": "Product images",
        "product_images_help": (
            "Multiple JPG, PNG or WEBP images may "
            "be uploaded. Images are automatically "
            "resized and compressed."
        ),
        "product_images_existing": (
            "Uploaded images"
        ),
        "product_image_cover": "Cover image",
        "product_image_set_cover": (
            "Set as cover image"
        ),
        "product_image_delete": "Delete image",
        "product_image_invalid": (
            "The uploaded image is invalid "
            "or uses an unsupported format."
        ),
        "product_image_cover_updated": (
            "Cover image updated."
        ),
        "product_image_deleted": (
            "Image deleted."
        ),
        "search": "Search",
        "clear": "Clear",
        "admin_dashboard_title": (
            "Administration"
        ),
        "admin_dashboard_description": (
            "Manage HomePantry users and master data."
        ),
        "admin_total": "total",

        "pagination_previous": "Previous",
        "pagination_next": "Next",
        "dashboard_title": "Overview",
        "dashboard_welcome": "Hello",
        "dashboard_household": "Household",

        "dashboard_inventory": "Inventory",
        "dashboard_batches": "batches",
        "dashboard_expiring": "Expiring soon",
        "dashboard_expired": "Expired",
        "dashboard_low_stock": "Below minimum",
        "dashboard_ingredients": "ingredients",
        "dashboard_next_three_days": (
            "Within the next 3 days"
        ),
        "dashboard_needs_attention": (
            "Needs attention"
        ),

        "dashboard_attention": "Expiration",
        "dashboard_attention_help": (
            "Expired and soon-to-expire inventory batches."
        ),
        "dashboard_view_inventory": (
            "View inventory"
        ),
        "dashboard_no_expiration_alerts": (
            "No expired or soon-to-expire items."
        ),

        "dashboard_low_stock_help": (
            "Ingredients below their configured minimum stock."
        ),
        "dashboard_current": "Current",
        "dashboard_stock_ok": (
            "All configured minimum stock levels are healthy."
        ),

        "dashboard_recent_movements": (
            "Recent inventory movements"
        ),
        "dashboard_recent_movements_help": (
            "The latest inventory changes."
        ),

        "dashboard_quick_actions": (
            "Quick actions"
        ),
        "dashboard_quick_actions_help": (
            "Frequently used HomePantry functions."
        ),
        "dashboard_quick_inventory_help": (
            "Barcode or manual entry"
        ),
        "dashboard_quick_products_help": (
            "Products and barcodes"
        ),
        "dashboard_quick_locations_help": (
            "Manage storage locations"
        ),
        "dashboard_quick_movements_help": (
            "Inventory movement history"
        ),

        "dashboard_no_household": (
            "No active household is assigned to this user."
        ),
        "unit_dimension_mass": "Mass",
        "unit_dimension_volume": "Volume",
        "unit_dimension_count": "Count",
        "product_add_ingredient": (
            "+ New ingredient"
        ),
        "nav_ingredients_admin": "Ingredients",

        "ingredient_admin_title": "Ingredients",
        "ingredient_admin_description": (
            "Manage the ingredient master data."
        ),
        "ingredient_admin_new": "New ingredient",
        "ingredient_admin_edit": (
            "Edit ingredient"
        ),

        "ingredient_admin_name_hu": (
            "Hungarian name"
        ),
        "ingredient_admin_name_en": (
            "English name"
        ),
        "ingredient_admin_category": (
            "Category"
        ),
        "ingredient_admin_no_category": (
            "— No category —"
        ),
        "ingredient_admin_default_unit": (
            "Default unit"
        ),
        "ingredient_admin_allowed_units": (
            "Allowed units"
        ),
        "ingredient_admin_aliases_hu": (
            "Hungarian aliases"
        ),
        "ingredient_admin_aliases_en": (
            "English aliases"
        ),

        "ingredient_admin_alias_help": (
            "Enter one alias per line or separate "
            "multiple aliases with commas."
        ),

        "ingredient_admin_default_must_be_allowed": (
            "The default unit must also be selected "
            "as an allowed unit."
        ),
        "ingredient_admin_exists": (
            "This ingredient already exists."
        ),
        "ingredient_admin_created": (
            "Ingredient created."
        ),
        "ingredient_admin_updated": (
            "Ingredient updated."
        ),
        "nav_movements": "Inventory movements",

        "movements_title": "Inventory movements",
        "movements_description": (
            "Complete history of inventory changes."
        ),
        "movements_search_placeholder": (
            "Search by ingredient, product, "
            "movement type or note..."
        ),

        "movement_type_opening_balance": (
            "Stock entry"
        ),
        "movement_type_consume": "Consumption",
        "movement_type_discard": "Discard",
        "movement_type_adjustment": "Adjustment",
        "movement_type_transfer": "Transfer",

        "movement_col_time": "Time",
        "movement_col_ingredient": "Ingredient",
        "movement_col_product": "Product",
        "movement_col_type": "Movement",
        "movement_col_change": "Change",
        "movement_col_before_after": (
            "Before → after"
        ),
        "movement_col_user": "User",
        "movement_col_note": "Note",

        "movements_empty": (
            "No inventory movements recorded yet."
        ),
        "nav_stock_rules": "Minimum stock",

        "stock_rule_title": "Minimum stock",
        "stock_rule_description": (
            "Manage minimum inventory levels by ingredient."
        ),
        "stock_rule_add": "Add minimum stock rule",
        "stock_rule_new_title": (
            "New minimum stock rule"
        ),
        "stock_rule_edit_title": (
            "Edit minimum stock rule"
        ),
        "stock_rule_minimum_quantity": (
            "Minimum quantity"
        ),
        "stock_rule_exists": (
            "A rule already exists for this ingredient."
        ),
        "stock_rule_created": (
            "Minimum stock rule created."
        ),
        "stock_rule_updated": (
            "Minimum stock rule updated."
        ),
        "stock_rule_deactivated": (
            "Minimum stock rule deactivated."
        ),
        "stock_rule_reactivated": (
            "Minimum stock rule reactivated."
        ),
        "movement_actions": "Actions",
        "movement_consume": "Consume",
        "movement_discard": "Discard",
        "movement_adjust": "Adjust",
        "movement_transfer": "Transfer",

        "movement_quantity": "Quantity",
        "movement_actual_quantity": (
            "Actual quantity"
        ),

        "movement_consume_title": (
            "Consume inventory"
        ),
        "movement_discard_title": (
            "Discard inventory"
        ),
        "movement_adjust_title": (
            "Adjust inventory"
        ),
        "movement_transfer_title": (
            "Transfer inventory"
        ),

        "movement_current_quantity": (
            "Current quantity"
        ),

        "movement_too_much": (
            "The entered quantity exceeds "
            "the available inventory."
        ),

        "movement_consumed": (
            "Consumption recorded."
        ),
        "movement_discarded": (
            "Discard recorded."
        ),
        "movement_adjusted": (
            "Inventory adjusted."
        ),
        "movement_transferred": (
            "Inventory batch transferred."
        ),
        "inventory_filter_all": "All",
        "inventory_filter_low": (
            "Below minimum stock"
        ),
        "inventory_filter_expiring": (
            "Expiring soon"
        ),
        "inventory_filter_expired": (
            "Expired"
        ),

        "inventory_status_low": (
            "Below minimum stock"
        ),
        "inventory_status_expiring": (
            "Expiring soon"
        ),
        "inventory_status_expired": (
            "Expired"
        ),

        "inventory_minimum_stock": (
            "Minimum stock"
        ),
        "inventory_search_placeholder": (
            "Search by ingredient, product, brand, "
            "barcode or storage location..."
        ),
        "inventory_batches": "Inventory batches",
        "inventory_col_purchase": "Purchase",
        "inventory_no_expiration": "Not specified",
        "inventory_batch_count": "batch",
        "barcode_create_product": (
            "Create a product for this barcode"
        ),
        "barcode_new_product_name": "Product name",
        "barcode_new_product_brand": "Brand",
        "barcode_new_product_name_required": (
            "Enter a product name for an unknown barcode."
        ),
        "barcode_product_created_with_stock": (
            "The new product and inventory item were created."
        ),
        "barcode_scan": "Scan barcode",
        "barcode_stop_scan": "Close camera",
        "barcode_lookup": "Find barcode",
        "barcode_lookup_placeholder": (
            "Enter or scan a barcode..."
        ),
        "barcode_product_found": (
            "Product found."
        ),
        "barcode_product_not_found": (
            "No product exists for this barcode yet."
        ),
        "barcode_camera_error": (
            "Camera could not be started."
        ),
        "nav_products": "Products",

        "product_title": "Products",
        "product_description": (
            "Manage packaged and bulk products."
        ),
        "product_search_placeholder": (
            "Search by product, brand, ingredient "
            "or barcode..."
        ),
        "product_new_title": "New product",
        "product_edit_title": "Edit product",

        "product_field_ingredient": "Ingredient",

        "product_field_name": "Product name",
        "product_field_brand": "Brand",
        "product_field_package_quantity": (
            "Package quantity"
        ),
        "product_field_package_unit": (
            "Package unit"
        ),
        "product_field_barcode": "Barcode",
        "product_field_barcode_type": (
            "Barcode type"
        ),

        "product_no_package_unit": (
            "— Not specified —"
        ),
        "product_no_barcode": (
            "No barcode"
        ),

        "product_add": "Add product",
        "product_edit": "Edit",
        "product_deactivate": "Deactivate",
        "product_reactivate": "Reactivate",

        "product_created": "Product created.",
        "product_updated": "Product updated.",
        "product_deactivated": (
            "Product deactivated."
        ),
        "product_reactivated": (
            "Product reactivated."
        ),
        "product_barcode_exists": (
            "This barcode already belongs "
            "to another product."
        ),
        "admin_add_user": "Add user",
        "admin_password": "Initial password",
        "admin_user_created": (
            "User created."
        ),
        "nav_profile": "Profile",
        "nav_admin": "Admin",

        "profile_title": "Profile",
        "profile_description": (
            "Your user preferences."
        ),
        "profile_display_name": "Display name",
        "profile_username": "Username",
        "profile_email": "Email",
        "profile_language": "Interface language",
        "profile_measurement_system": (
            "Measurement system"
        ),
        "profile_updated": (
            "Profile updated."
        ),
        "profile_identity_exists": (
            "This email address or username "
            "is already in use."
        ),

        "admin_users_title": "Users",
        "admin_users_description": (
            "Manage users in this household."
        ),
        "admin_user": "User",
        "admin_role": "Role",
        "admin_active": "Active",
        "admin_language": "Language",
        "admin_measurement": (
            "Measurement system"
        ),
        "admin_edit": "Edit",
        "admin_yes": "Yes",
        "admin_no": "No",
        "admin_user_edit_title": (
            "Edit user"
        ),
        "admin_user_updated": (
            "User updated."
        ),
        "app_name": "HomePantry",

        "nav_inventory": "Inventory",
        "nav_storage": "Storage",
        "nav_logout": "Logout",

        "storage_title": "Storage locations",
        "storage_description": (
            "Manage rooms, fridges, freezers, "
            "shelves and other storage locations."
        ),
        "storage_add": "Add location",
        "storage_active": "Active locations",
        "storage_inactive": "Inactive locations",
        "storage_empty": "No storage locations yet.",
        "storage_edit": "Edit",
        "storage_deactivate": "Deactivate",
        "storage_reactivate": "Reactivate",
        "storage_inactive_label": "Inactive",

        "storage_new_title": "New storage location",
        "storage_edit_title": "Edit storage location",

        "field_name": "Name",
        "field_type": "Type",
        "field_parent": "Parent location",
        "field_sort_order": "Sort order",

        "save": "Save",
        "cancel": "Cancel",

        "no_parent": "— No parent —",

        "location_type_room": "Room",
        "location_type_cabinet": "Cabinet",
        "location_type_shelf": "Shelf",
        "location_type_fridge": "Fridge",
        "location_type_freezer": "Freezer",
        "location_type_drawer": "Drawer",
        "location_type_box": "Box",
        "location_type_storage": "Other storage",

        "storage_created": "Storage location created.",
        "storage_updated": "Storage location updated.",
        "storage_deactivated": "Storage location deactivated.",
        "storage_reactivated": "Storage location reactivated.",
        "storage_has_children": (
            "This location still has active "
            "child locations."
        ),
        "storage_parent_inactive": (
            "Reactivate the parent location first."
        ),

        "inventory_title": "Inventory",
        "inventory_add": "Add inventory item",
        "inventory_description": (
            "Current inventory batches."
        ),
        "inventory_empty": (
            "Inventory is empty."
        ),

        "inventory_field_ingredient": "Ingredient",
        "ingredient_select_placeholder": (
            "— Start typing an ingredient —"
        ),
        "inventory_field_product": "Product",
        "inventory_field_location": (
            "Storage location"
        ),
        "inventory_field_quantity": "Quantity",
        "inventory_field_unit": "Unit",
        "inventory_field_purchase_date": (
            "Purchase date"
        ),
        "inventory_field_expiration_date": (
            "Expiration date"
        ),
        "inventory_field_note": "Note",

        "inventory_bulk_product": (
            "— Bulk / no specific product —"
        ),
        "inventory_bulk_help": (
            "Leave this selected for loose or "
            "non-barcoded ingredients."
        ),

        "inventory_add_submit": (
            "Add to inventory"
        ),
        "inventory_added": (
            "Inventory item added."
        ),

        "inventory_col_ingredient": "Ingredient",
        "inventory_col_product": "Product",
        "inventory_col_quantity": "Quantity",
        "inventory_col_location": "Location",
        "inventory_col_expiration": "Expiration",

        "inventory_bulk_label": "Bulk",
    },
}


def get_language():
    if current_user.is_authenticated:
        language = (
            current_user.preferred_language
            or "hu"
        )

        if language in TRANSLATIONS:
            return language

    return "hu"


def translate(key):
    language = get_language()

    return (
        TRANSLATIONS
        .get(language, TRANSLATIONS["hu"])
        .get(
            key,
            TRANSLATIONS["en"].get(
                key,
                key,
            ),
        )
    )
