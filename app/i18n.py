from flask_login import current_user


TRANSLATIONS = {
    "hu": {
"movement_col_location": "Tárhely",
"inventory_location_filter_all": (
    "Összes tárhely"
),
"inventory_filter_clear": (
    "Szűrés törlése"
),
"inventory_product_search_placeholder": (
    "Keress vagy írj be új terméknevet..."
),
"recipe_delete_action": "Recept törlése",
"recipe_delete_confirm": (
    "Biztosan törlöd ezt a receptet?"
),
"recipe_deleted": (
    "A recept törölve."
),
"recipe_edit_action": "Szerkesztés",
"recipe_print": "Nyomtatás / PDF",
"recipe_image_cover_updated": (
    "A recept borítóképe frissítve."
),
"recipe_image_deleted": (
    "A receptkép törölve."
),
"recipe_image_cover": "Borítókép",
"recipe_image_set_cover": (
    "Beállítás borítóképként"
),
"recipe_image_delete": "Kép törlése",
"recipe_images_existing": (
    "Mentett képek"
),
"recipe_images_title": "Képek",
"recipe_images_choose_files": (
    "Képek kiválasztása"
),
"recipe_images_take_photo": (
    "Fénykép készítése"
),
"recipe_images_pending": (
    "Feltöltésre váró képek"
),
"recipe_images_help": (
    "Több kép is feltölthető. "
    "Az első kép lesz a borítókép."
),
"recipe_image_invalid": (
    "A kiválasztott képet nem sikerült feldolgozni."
),
"recipe_search": "Keresés",
"recipe_search_placeholder": (
    "Recept, hozzávaló vagy címke..."
),
"recipe_filter_any": "Bármilyen",
"recipe_filter_max_time": (
    "Maximum elkészítési idő"
),
"recipe_filter_only_available": (
    "Csak azok, amelyekhez minden alapanyag megvan"
),
"recipe_filter_apply": "Szűrés",
"recipe_filter_clear": "Szűrők törlése",
"recipe_ingredients_available": (
    "alapanyag megvan"
),
"recipe_search_no_results": (
    "A megadott feltételekkel nincs találat."
),
"recipe_field_total_time": "Összesen",
"recipe_no_ingredients": (
    "Ehhez a recepthez nincs hozzávaló megadva."
),
"recipe_no_instructions": (
    "Nincs elkészítési leírás megadva."
),
"recipe_ingredient_quantity": "Mennyiség",
"recipe_ingredient_unit": "Mértékegység",
"recipe_ingredients_help": (
    "Add meg a recept hozzávalóit. "
    "Ha találunk egyező saját alapanyagot, "
    "összepárosíthatod vele."
),
"recipe_ingredient_add": "Hozzávaló",
"recipe_ingredient_placeholder": (
    "Kezdd el beírni az alapanyag nevét..."
),
"recipe_edit_title": "Recept szerkesztése",
"recipe_updated": (
    "A recept módosításai elmentve."
),
"recipe_tags_field": "Receptcímkék",
"recipe_tags_help": (
    "Jelöld meg mindazt, ami jellemző a receptre."
),
"recipe_tag_title": "Receptcímkék",
"recipe_tag_description": (
    "A receptekhez használható címkék kezelése."
),
"recipe_tag_new": "Új receptcímke",
"recipe_tag_edit": "Receptcímke szerkesztése",
"recipe_tag_name": "Név",
"recipe_tag_key": "Kulcs",
"recipe_tag_group": "Csoport",
"recipe_tag_sort_order": "Sorrend",
"recipe_tag_group_food_type": "Ételtípus",
"recipe_tag_group_cuisine": "Konyha",
"recipe_tag_group_diet": "Étrend",
"recipe_tag_group_other": "Egyéb",
"recipe_tag_key_exists": (
    "Már létezik ilyen kulcsú receptcímke."
),
"recipe_tag_created": (
    "A receptcímke létrejött."
),
"recipe_tag_updated": (
    "A receptcímke módosítva."
),
"recipe_tag_empty": (
    "Még nincs receptcímke."
),
"recipe_new_title": "Új recept",
"recipe_created": (
    "A recept sikeresen elmentve."
),
"recipe_field_title": "Recept neve",
"recipe_field_description": "Leírás",
"recipe_field_cuisine": "Konyha",
"recipe_field_category": "Kategória",
"recipe_field_difficulty": "Nehézség",
"recipe_field_servings": "Adag",
"recipe_field_prep_time": (
    "Előkészítési idő (perc)"
),
"recipe_field_cook_time": (
    "Főzési / sütési idő (perc)"
),
"recipe_field_instructions": "Elkészítés",
"recipe_difficulty_unspecified": (
    "Nincs megadva"
),
"recipe_difficulty_easy": "Könnyű",
"recipe_difficulty_medium": "Közepes",
"recipe_difficulty_hard": "Nehéz",
"recipe_ingredients_title": "Hozzávalók",
"recipe_ingredients_placeholder": (
    "A hozzávalók kezelése a következő lépésben kerül ide."
),
"recipe_minutes": "perc",
"dashboard_quick_recipes_help": (
    "Saját receptek és receptötletek."
),
"recipe_title": "Receptek",
"recipe_description": (
    "Saját receptek kezelése és receptötletek keresése."
),
"recipe_empty": (
    "Még nincs elmentett recept."
),
"admin_data_management_title": (
    "Adatkezelés"
),
"admin_data_management_description": (
    "Adatok exportálása és karbantartási műveletek."
),
"admin_export_inventory_title": (
    "Aktuális készlet export"
),
"admin_export_inventory_description": (
    "Az aktuális háztartás készlettételeinek letöltése CSV formátumban."
),
"admin_export_products_title": (
    "Terméktörzs export"
),
"admin_export_products_description": (
    "Az aktuális háztartás terméktörzsének letöltése CSV formátumban."
),
"expiring_soon_settings_title": (
    "Szavatossági figyelmeztetés"
),
"expiring_soon_settings_description": (
    "Ennyi nappal a lejárat előtt kezdjen figyelmeztetni a rendszer."
),
"expiring_soon_days_label": (
    "Figyelmeztetés a lejárat előtt"
),
"expiring_soon_days_saved": (
    "A szavatossági figyelmeztetés beállítása elmentve."
),
"days": (
    "nap"
),
"product_refresh_metadata": (
    "OFF-adatok frissítése"
),
"product_details_ingredients": (
    "Összetevők"
),
"product_details_allergens": (
    "Allergének"
),
"product_details_traces": (
    "Nyomokban tartalmazhat"
),
"product_details_categories": (
    "Kategóriák"
),
"product_details_labels": (
    "Címkék"
),
"product_details_nutrition_100g": (
    "Tápérték 100 g-ban"
),
"product_details_energy": (
    "Energia"
),
"product_details_fat": (
    "Zsír"
),
"product_details_saturated_fat": (
    "ebből telített zsírsavak"
),
"product_details_carbohydrates": (
    "Szénhidrát"
),
"product_details_sugars": (
    "ebből cukrok"
),
"product_details_proteins": (
    "Fehérje"
),
"product_details_salt": (
    "Só"
),
"product_details_load_error": (
    "A részletek betöltése nem sikerült."
),
"product_details_loading": (
    "Részletek betöltése..."
),
"product_details": (
    "Részletek"
),
        "product_images_pending": (
            "Feltöltendő képek"
        ),
        "product_images_choose_files": (
            "Fájl(ok) kiválasztása"
        ),
        "product_images_take_photo": (
            "Fotó készítése"
        ),
        "product_field_camera": (
            "Fotó készítése"
        ),
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
"dashboard_next_days": (
    "A következő {days} napban"
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
"movement_col_location": "Storage location",
"inventory_location_filter_all": (
    "All storage locations"
),
"inventory_filter_clear": (
    "Clear filters"
),
"inventory_product_search_placeholder": (
    "Search or enter a new product name..."
),
"recipe_delete_action": "Delete recipe",
"recipe_delete_confirm": (
    "Are you sure you want to delete this recipe?"
),
"recipe_deleted": (
    "Recipe deleted."
),
"recipe_edit_action": "Edit",
"recipe_print": "Print / PDF",
"recipe_image_cover_updated": (
    "Recipe cover image updated."
),
"recipe_image_deleted": (
    "Recipe image deleted."
),
"recipe_image_cover": "Cover image",
"recipe_image_set_cover": (
    "Set as cover"
),
"recipe_image_delete": "Delete image",
"recipe_images_existing": (
    "Saved images"
),
"recipe_images_title": "Images",
"recipe_images_choose_files": (
    "Choose images"
),
"recipe_images_take_photo": (
    "Take photo"
),
"recipe_images_pending": (
    "Images waiting to upload"
),
"recipe_images_help": (
    "Multiple images can be uploaded. "
    "The first image becomes the cover."
),
"recipe_image_invalid": (
    "The selected image could not be processed."
),
"recipe_search": "Search",
"recipe_search_placeholder": (
    "Recipe, ingredient or tag..."
),
"recipe_filter_any": "Any",
"recipe_filter_max_time": (
    "Maximum preparation time"
),
"recipe_filter_only_available": (
    "Only recipes with all ingredients available"
),
"recipe_filter_apply": "Filter",
"recipe_filter_clear": "Clear filters",
"recipe_ingredients_available": (
    "ingredients available"
),
"recipe_search_no_results": (
    "No recipes match the selected filters."
),
"recipe_field_total_time": "Total time",
"recipe_no_ingredients": (
    "No ingredients have been added to this recipe."
),
"recipe_no_instructions": (
    "No preparation instructions have been provided."
),
"recipe_ingredient_quantity": "Quantity",
"recipe_ingredient_unit": "Unit",
"recipe_ingredients_help": (
    "Add the recipe ingredients. "
    "Matching pantry ingredients can be linked."
),
"recipe_ingredient_add": "Ingredient",
"recipe_ingredient_placeholder": (
    "Start typing an ingredient name..."
),
"recipe_edit_title": "Edit recipe",
"recipe_updated": (
    "Recipe changes saved."
),
"recipe_tags_field": "Recipe tags",
"recipe_tags_help": (
    "Select all tags that describe this recipe."
),
"recipe_tag_title": "Recipe tags",
"recipe_tag_description": (
    "Manage tags available for recipes."
),
"recipe_tag_new": "New recipe tag",
"recipe_tag_edit": "Edit recipe tag",
"recipe_tag_name": "Name",
"recipe_tag_key": "Key",
"recipe_tag_group": "Group",
"recipe_tag_sort_order": "Sort order",
"recipe_tag_group_food_type": "Food type",
"recipe_tag_group_cuisine": "Cuisine",
"recipe_tag_group_diet": "Diet",
"recipe_tag_group_other": "Other",
"recipe_tag_key_exists": (
    "A recipe tag with this key already exists."
),
"recipe_tag_created": (
    "Recipe tag created."
),
"recipe_tag_updated": (
    "Recipe tag updated."
),
"recipe_tag_empty": (
    "No recipe tags yet."
),
"recipe_new_title": "New recipe",
"recipe_created": (
    "Recipe saved successfully."
),
"recipe_field_title": "Recipe name",
"recipe_field_description": "Description",
"recipe_field_cuisine": "Cuisine",
"recipe_field_category": "Category",
"recipe_field_difficulty": "Difficulty",
"recipe_field_servings": "Servings",
"recipe_field_prep_time": (
    "Preparation time (minutes)"
),
"recipe_field_cook_time": (
    "Cooking / baking time (minutes)"
),
"recipe_field_instructions": "Instructions",
"recipe_difficulty_unspecified": (
    "Not specified"
),
"recipe_difficulty_easy": "Easy",
"recipe_difficulty_medium": "Medium",
"recipe_difficulty_hard": "Hard",
"recipe_ingredients_title": "Ingredients",
"recipe_ingredients_placeholder": (
    "Ingredient management will be added here in the next step."
),
"recipe_minutes": "min",
"dashboard_quick_recipes_help": (
    "Saved recipes and recipe ideas."
),
"recipe_title": "Recipes",
"recipe_description": (
    "Manage saved recipes and search for recipe ideas."
),
"recipe_empty": (
    "No saved recipes yet."
),
"admin_data_management_title": (
    "Data management"
),
"admin_data_management_description": (
    "Export data and perform maintenance operations."
),
"admin_export_inventory_title": (
    "Current inventory export"
),
"admin_export_inventory_description": (
    "Download the current household inventory batches in CSV format."
),
"admin_export_products_title": (
    "Product master export"
),
"admin_export_products_description": (
    "Download the current household product master in CSV format."
),
"expiring_soon_settings_title": (
    "Expiration warning"
),
"expiring_soon_settings_description": (
    "Number of days before expiration when warnings should begin."
),
"expiring_soon_days_label": (
    "Warn before expiration"
),
"expiring_soon_days_saved": (
    "Expiration warning setting saved."
),
"days": (
    "days"
),
"product_refresh_metadata": (
    "Refresh OFF data"
),
"product_details_ingredients": (
    "Ingredients"
),
"product_details_allergens": (
    "Allergens"
),
"product_details_traces": (
    "May contain traces of"
),
"product_details_categories": (
    "Categories"
),
"product_details_labels": (
    "Labels"
),
"product_details_nutrition_100g": (
    "Nutrition per 100 g"
),
"product_details_energy": (
    "Energy"
),
"product_details_fat": (
    "Fat"
),
"product_details_saturated_fat": (
    "of which saturates"
),
"product_details_carbohydrates": (
    "Carbohydrate"
),
"product_details_sugars": (
    "of which sugars"
),
"product_details_proteins": (
    "Protein"
),
"product_details_salt": (
    "Salt"
),
"product_details_load_error": (
    "Failed to load product details."
),
"product_details_loading": (
    "Loading details..."
),
"product_details": (
    "Details"
),
        "product_images_pending": (
            "Images to upload"
        ),
        "product_images_choose_files": (
            "Choose file(s)"
        ),
        "product_images_take_photo": (
            "Take a photo"
        ),
        "product_field_camera": (
            "Take a photo"
        ),
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
"dashboard_next_days": (
    "Within the next {days} days"
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


def translate(
    key,
    **kwargs,
):
    language = get_language()

    text = (
        TRANSLATIONS
        .get(
            language,
            TRANSLATIONS["hu"],
        )
        .get(
            key,
            TRANSLATIONS["en"].get(
                key,
                key,
            ),
        )
    )

    if not kwargs:
        return text

    try:
        return text.format(
            **kwargs
        )
    except (
        KeyError,
        ValueError,
    ):
        return text
