from flask_login import current_user


TRANSLATIONS = {
    "hu": {
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
