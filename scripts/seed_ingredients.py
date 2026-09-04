import os
from pathlib import Path
import re
import sys
import unicodedata

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )

if not os.getenv("DATABASE_URL"):
    env_file = PROJECT_ROOT / ".env"
    if env_file.is_file():
        load_dotenv(env_file)


from app import create_app
from app.extensions import db
from app.models import (
    Ingredient,
    IngredientAlias,
    IngredientCategory,
    IngredientTranslation,
    Unit,
)


INGREDIENTS = [
    # -------------------------------------------------
    # POULTRY
    # -------------------------------------------------
    {
        "key": "chicken_breast",
        "category": "poultry",
        "unit": "g",
        "hu": "csirkemell",
        "en": "chicken breast",
        "aliases_hu": [
            "csirke mell",
            "csirkemellfilé",
            "csirke mellfilé",
            "filézett csirkemell",
        ],
        "aliases_en": [
            "chicken breasts",
            "boneless chicken breast",
            "chicken breast fillet",
            "chicken fillet",
        ],
    },
    {
        "key": "chicken_thigh",
        "category": "poultry",
        "unit": "g",
        "hu": "csirkecomb",
        "en": "chicken thigh",
        "aliases_hu": [
            "csirke comb",
            "csirke felsőcomb",
            "csirkecombfilé",
            "csirke combfilé",
        ],
        "aliases_en": [
            "chicken thighs",
            "boneless chicken thigh",
            "chicken thigh fillet",
        ],
    },
    {
        "key": "chicken_drumstick",
        "category": "poultry",
        "unit": "g",
        "hu": "csirke alsócomb",
        "en": "chicken drumstick",
        "aliases_hu": [
            "alsó csirkecomb",
            "csirke alsó comb",
        ],
        "aliases_en": [
            "chicken drumsticks",
            "drumstick",
        ],
    },
    {
        "key": "chicken_wing",
        "category": "poultry",
        "unit": "g",
        "hu": "csirkeszárny",
        "en": "chicken wing",
        "aliases_hu": [
            "csirke szárny",
        ],
        "aliases_en": [
            "chicken wings",
        ],
    },
    {
        "key": "whole_chicken",
        "category": "poultry",
        "unit": "g",
        "hu": "egész csirke",
        "en": "whole chicken",
        "aliases_hu": [
            "csirke egészben",
            "konyhakész csirke",
        ],
        "aliases_en": [
            "whole roasting chicken",
            "roasting chicken",
        ],
    },
    {
        "key": "turkey_breast",
        "category": "poultry",
        "unit": "g",
        "hu": "pulykamell",
        "en": "turkey breast",
        "aliases_hu": [
            "pulyka mell",
            "pulykamellfilé",
        ],
        "aliases_en": [
            "turkey breast fillet",
        ],
    },
    {
        "key": "turkey_thigh",
        "category": "poultry",
        "unit": "g",
        "hu": "pulykacomb",
        "en": "turkey thigh",
        "aliases_hu": [
            "pulyka comb",
        ],
        "aliases_en": [
            "turkey thighs",
        ],
    },
    {
        "key": "duck_breast",
        "category": "poultry",
        "unit": "g",
        "hu": "kacsamell",
        "en": "duck breast",
        "aliases_hu": [
            "kacsa mell",
        ],
        "aliases_en": [
            "duck breasts",
        ],
    },
    {
        "key": "duck_leg",
        "category": "poultry",
        "unit": "g",
        "hu": "kacsacomb",
        "en": "duck leg",
        "aliases_hu": [
            "kacsa comb",
        ],
        "aliases_en": [
            "duck legs",
        ],
    },

    # -------------------------------------------------
    # PORK
    # -------------------------------------------------
    {
        "key": "pork_leg",
        "category": "pork",
        "unit": "g",
        "hu": "sertéscomb",
        "en": "pork leg",
        "aliases_hu": [
            "disznócomb",
            "sertés comb",
        ],
        "aliases_en": [
            "leg of pork",
            "pork hind leg",
        ],
    },
    {
        "key": "pork_shoulder",
        "category": "pork",
        "unit": "g",
        "hu": "sertéslapocka",
        "en": "pork shoulder",
        "aliases_hu": [
            "lapocka",
            "disznólapocka",
            "sertés lapocka",
        ],
        "aliases_en": [
            "pork shoulder roast",
        ],
    },
    {
        "key": "pork_loin",
        "category": "pork",
        "unit": "g",
        "hu": "sertéskaraj",
        "en": "pork loin",
        "aliases_hu": [
            "karaj",
            "sertés karaj",
        ],
        "aliases_en": [
            "pork loin roast",
        ],
    },
    {
        "key": "pork_tenderloin",
        "category": "pork",
        "unit": "g",
        "hu": "sertésszűz",
        "en": "pork tenderloin",
        "aliases_hu": [
            "szűzpecsenye",
            "sertés szűzpecsenye",
        ],
        "aliases_en": [
            "pork fillet",
        ],
    },
    {
        "key": "pork_belly",
        "category": "pork",
        "unit": "g",
        "hu": "sertésoldalas",
        "en": "pork belly",
        "aliases_hu": [
            "oldalas",
            "sertés oldalas",
        ],
        "aliases_en": [
            "belly pork",
        ],
    },
    {
        "key": "pork_ribs",
        "category": "pork",
        "unit": "g",
        "hu": "sertésborda",
        "en": "pork ribs",
        "aliases_hu": [
            "sertés borda",
            "bordacsont",
        ],
        "aliases_en": [
            "pork rib",
            "spare ribs",
        ],
    },
    {
        "key": "ground_pork",
        "category": "pork",
        "unit": "g",
        "hu": "darált sertéshús",
        "en": "ground pork",
        "aliases_hu": [
            "sertés darált hús",
            "darált disznóhús",
        ],
        "aliases_en": [
            "minced pork",
            "pork mince",
        ],
    },

    # -------------------------------------------------
    # BEEF
    # -------------------------------------------------
    {
        "key": "beef_chuck",
        "category": "beef",
        "unit": "g",
        "hu": "marhalapocka",
        "en": "beef chuck",
        "aliases_hu": [
            "marha lapocka",
        ],
        "aliases_en": [
            "chuck steak",
            "chuck roast",
        ],
    },
    {
        "key": "beef_round",
        "category": "beef",
        "unit": "g",
        "hu": "marhacomb",
        "en": "beef round",
        "aliases_hu": [
            "marha comb",
        ],
        "aliases_en": [
            "round steak",
        ],
    },
    {
        "key": "beef_sirloin",
        "category": "beef",
        "unit": "g",
        "hu": "hátszín",
        "en": "beef sirloin",
        "aliases_hu": [
            "marhahátszín",
        ],
        "aliases_en": [
            "sirloin steak",
            "sirloin",
        ],
    },
    {
        "key": "beef_tenderloin",
        "category": "beef",
        "unit": "g",
        "hu": "marhabélszín",
        "en": "beef tenderloin",
        "aliases_hu": [
            "bélszín",
        ],
        "aliases_en": [
            "beef fillet",
            "fillet steak",
        ],
    },
    {
        "key": "beef_brisket",
        "category": "beef",
        "unit": "g",
        "hu": "marhaszegy",
        "en": "beef brisket",
        "aliases_hu": [
            "marha szegy",
        ],
        "aliases_en": [
            "brisket",
        ],
    },
    {
        "key": "ground_beef",
        "category": "beef",
        "unit": "g",
        "hu": "darált marhahús",
        "en": "ground beef",
        "aliases_hu": [
            "marha darált hús",
        ],
        "aliases_en": [
            "minced beef",
            "beef mince",
        ],
    },
    {
        "key": "mixed_ground_meat",
        "category": "other_meat",
        "unit": "g",
        "hu": "vegyes darált hús",
        "en": "mixed ground meat",
        "aliases_hu": [
            "sertés-marha darált hús",
            "darált hús vegyesen",
        ],
        "aliases_en": [
            "mixed mince",
            "mixed minced meat",
            "pork beef mince",
        ],
    },

    # -------------------------------------------------
    # OTHER MEAT
    # -------------------------------------------------
    {
        "key": "lamb_leg",
        "category": "other_meat",
        "unit": "g",
        "hu": "báránycomb",
        "en": "leg of lamb",
        "aliases_hu": [
            "bárány comb",
        ],
        "aliases_en": [
            "lamb leg",
        ],
    },
    {
        "key": "lamb_shoulder",
        "category": "other_meat",
        "unit": "g",
        "hu": "báránylapocka",
        "en": "lamb shoulder",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "bacon",
        "category": "other_meat",
        "unit": "g",
        "hu": "bacon",
        "en": "bacon",
        "aliases_hu": [
            "szeletelt bacon",
            "angolszalonna",
        ],
        "aliases_en": [
            "streaky bacon",
        ],
    },
    {
        "key": "ham",
        "category": "other_meat",
        "unit": "g",
        "hu": "sonka",
        "en": "ham",
        "aliases_hu": [
            "főtt sonka",
        ],
        "aliases_en": [
            "cooked ham",
        ],
    },
    {
        "key": "sausage",
        "category": "other_meat",
        "unit": "g",
        "hu": "kolbász",
        "en": "sausage",
        "aliases_hu": [
            "sült kolbász",
        ],
        "aliases_en": [
            "sausages",
        ],
    },

    # -------------------------------------------------
    # FISH AND SEAFOOD
    # -------------------------------------------------
    {
        "key": "salmon",
        "category": "fish_and_seafood",
        "unit": "g",
        "hu": "lazac",
        "en": "salmon",
        "aliases_hu": [
            "lazacfilé",
        ],
        "aliases_en": [
            "salmon fillet",
        ],
    },
    {
        "key": "tuna",
        "category": "fish_and_seafood",
        "unit": "g",
        "hu": "tonhal",
        "en": "tuna",
        "aliases_hu": [
            "tonhalfilé",
        ],
        "aliases_en": [
            "tuna steak",
        ],
    },
    {
        "key": "cod",
        "category": "fish_and_seafood",
        "unit": "g",
        "hu": "tőkehal",
        "en": "cod",
        "aliases_hu": [
            "tőkehalfilé",
        ],
        "aliases_en": [
            "cod fillet",
        ],
    },
    {
        "key": "hake",
        "category": "fish_and_seafood",
        "unit": "g",
        "hu": "hekk",
        "en": "hake",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "carp",
        "category": "fish_and_seafood",
        "unit": "g",
        "hu": "ponty",
        "en": "carp",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "trout",
        "category": "fish_and_seafood",
        "unit": "g",
        "hu": "pisztráng",
        "en": "trout",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "shrimp",
        "category": "fish_and_seafood",
        "unit": "g",
        "hu": "garnélarák",
        "en": "shrimp",
        "aliases_hu": [
            "garnéla",
            "garnélarák",
        ],
        "aliases_en": [
            "prawn",
            "prawns",
            "shrimps",
        ],
    },

    # -------------------------------------------------
    # DAIRY
    # -------------------------------------------------
    {
        "key": "milk",
        "category": "milk",
        "unit": "ml",
        "hu": "tej",
        "en": "milk",
        "aliases_hu": [
            "tehéntej",
        ],
        "aliases_en": [
            "cow milk",
            "whole milk",
        ],
    },
    {
        "key": "lactose_free_milk",
        "category": "milk",
        "unit": "ml",
        "hu": "laktózmentes tej",
        "en": "lactose-free milk",
        "aliases_hu": [
            "laktóz mentes tej",
        ],
        "aliases_en": [
            "lactose free milk",
        ],
    },
    {
        "key": "cream",
        "category": "cream_and_sour_cream",
        "unit": "ml",
        "hu": "tejszín",
        "en": "cream",
        "aliases_hu": [
            "főzőtejszín",
            "habtejszín",
        ],
        "aliases_en": [
            "cooking cream",
            "heavy cream",
            "double cream",
        ],
    },
    {
        "key": "sour_cream",
        "category": "cream_and_sour_cream",
        "unit": "g",
        "hu": "tejföl",
        "en": "sour cream",
        "aliases_hu": [],
        "aliases_en": [
            "soured cream",
        ],
    },
    {
        "key": "yogurt",
        "category": "yogurt",
        "unit": "g",
        "hu": "joghurt",
        "en": "yogurt",
        "aliases_hu": [
            "natúr joghurt",
        ],
        "aliases_en": [
            "yoghurt",
            "plain yogurt",
        ],
    },
    {
        "key": "greek_yogurt",
        "category": "yogurt",
        "unit": "g",
        "hu": "görög joghurt",
        "en": "Greek yogurt",
        "aliases_hu": [],
        "aliases_en": [
            "Greek yoghurt",
        ],
    },
    {
        "key": "butter",
        "category": "butter_and_spreads",
        "unit": "g",
        "hu": "vaj",
        "en": "butter",
        "aliases_hu": [],
        "aliases_en": [
            "unsalted butter",
            "salted butter",
        ],
    },
    {
        "key": "margarine",
        "category": "butter_and_spreads",
        "unit": "g",
        "hu": "margarin",
        "en": "margarine",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "cottage_cheese",
        "category": "cheese",
        "unit": "g",
        "hu": "túró",
        "en": "cottage cheese",
        "aliases_hu": [
            "tehéntúró",
        ],
        "aliases_en": [
            "curd cheese",
        ],
    },
    {
        "key": "mozzarella",
        "category": "cheese",
        "unit": "g",
        "hu": "mozzarella",
        "en": "mozzarella",
        "aliases_hu": [],
        "aliases_en": [
            "mozzarella cheese",
        ],
    },
    {
        "key": "cheddar",
        "category": "cheese",
        "unit": "g",
        "hu": "cheddar sajt",
        "en": "cheddar",
        "aliases_hu": [
            "cheddar",
        ],
        "aliases_en": [
            "cheddar cheese",
        ],
    },
    {
        "key": "parmesan",
        "category": "cheese",
        "unit": "g",
        "hu": "parmezán",
        "en": "parmesan",
        "aliases_hu": [
            "parmezán sajt",
        ],
        "aliases_en": [
            "parmesan cheese",
            "parmigiano reggiano",
        ],
    },
    {
        "key": "gouda",
        "category": "cheese",
        "unit": "g",
        "hu": "gouda sajt",
        "en": "gouda",
        "aliases_hu": [
            "gouda",
        ],
        "aliases_en": [
            "gouda cheese",
        ],
    },
    {
        "key": "emmental",
        "category": "cheese",
        "unit": "g",
        "hu": "ementáli sajt",
        "en": "emmental",
        "aliases_hu": [
            "ementáli",
        ],
        "aliases_en": [
            "emmentaler",
            "emmental cheese",
        ],
    },
    {
        "key": "feta",
        "category": "cheese",
        "unit": "g",
        "hu": "feta sajt",
        "en": "feta",
        "aliases_hu": [
            "feta",
        ],
        "aliases_en": [
            "feta cheese",
        ],
    },

    # -------------------------------------------------
    # EGGS
    # -------------------------------------------------
    {
        "key": "egg",
        "category": "eggs",
        "unit": "pc",
        "hu": "tojás",
        "en": "egg",
        "aliases_hu": [
            "tyúktojás",
        ],
        "aliases_en": [
            "eggs",
            "chicken egg",
        ],
    },

    # -------------------------------------------------
    # FLOUR AND MILLING
    # -------------------------------------------------
    {
        "key": "all_purpose_flour",
        "category": "wheat_flour",
        "unit": "g",
        "hu": "finomliszt",
        "en": "all-purpose flour",
        "aliases_hu": [
            "búzafinomliszt",
            "búza finomliszt",
            "BL55 liszt",
            "BL 55",
        ],
        "aliases_en": [
            "all purpose flour",
            "plain flour",
            "white flour",
        ],
    },
    {
        "key": "bread_flour",
        "category": "wheat_flour",
        "unit": "g",
        "hu": "kenyérliszt",
        "en": "bread flour",
        "aliases_hu": [
            "BL80 liszt",
            "BL 80",
        ],
        "aliases_en": [
            "strong flour",
            "strong bread flour",
        ],
    },
    {
        "key": "pizza_flour",
        "category": "wheat_flour",
        "unit": "g",
        "hu": "pizzaliszt",
        "en": "pizza flour",
        "aliases_hu": [
            "pizza liszt",
            "00 liszt",
            "tipo 00 liszt",
        ],
        "aliases_en": [
            "00 flour",
            "tipo 00 flour",
        ],
    },
    {
        "key": "whole_wheat_flour",
        "category": "wheat_flour",
        "unit": "g",
        "hu": "teljes kiőrlésű búzaliszt",
        "en": "whole wheat flour",
        "aliases_hu": [
            "teljes kiőrlésű liszt",
            "tk liszt",
        ],
        "aliases_en": [
            "wholemeal flour",
            "whole grain flour",
        ],
    },
    {
        "key": "rye_flour",
        "category": "specialty_flour",
        "unit": "g",
        "hu": "rozsliszt",
        "en": "rye flour",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "rice_flour",
        "category": "specialty_flour",
        "unit": "g",
        "hu": "rizsliszt",
        "en": "rice flour",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "corn_flour",
        "category": "specialty_flour",
        "unit": "g",
        "hu": "kukoricaliszt",
        "en": "corn flour",
        "aliases_hu": [],
        "aliases_en": [
            "cornflour",
        ],
    },
    {
        "key": "oat_flour",
        "category": "specialty_flour",
        "unit": "g",
        "hu": "zabliszt",
        "en": "oat flour",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "semolina",
        "category": "meal_and_semolina",
        "unit": "g",
        "hu": "búzadara",
        "en": "semolina",
        "aliases_hu": [
            "gríz",
        ],
        "aliases_en": [
            "semolina flour",
        ],
    },
    {
        "key": "cornmeal",
        "category": "meal_and_semolina",
        "unit": "g",
        "hu": "kukoricadara",
        "en": "cornmeal",
        "aliases_hu": [
            "puliszkaliszt",
        ],
        "aliases_en": [
            "polenta",
        ],
    },

    # -------------------------------------------------
    # PASTA
    # -------------------------------------------------
    {
        "key": "spaghetti",
        "category": "pasta",
        "unit": "g",
        "hu": "spagetti",
        "en": "spaghetti",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "penne",
        "category": "pasta",
        "unit": "g",
        "hu": "penne",
        "en": "penne",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "fusilli",
        "category": "pasta",
        "unit": "g",
        "hu": "orsótészta",
        "en": "fusilli",
        "aliases_hu": [
            "fusilli",
        ],
        "aliases_en": [
            "spiral pasta",
        ],
    },
    {
        "key": "tagliatelle",
        "category": "pasta",
        "unit": "g",
        "hu": "szélesmetélt",
        "en": "tagliatelle",
        "aliases_hu": [
            "tagliatelle",
        ],
        "aliases_en": [],
    },
    {
        "key": "macaroni",
        "category": "pasta",
        "unit": "g",
        "hu": "makaróni",
        "en": "macaroni",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "lasagne_sheets",
        "category": "pasta",
        "unit": "g",
        "hu": "lasagne tészta",
        "en": "lasagne sheets",
        "aliases_hu": [
            "lasagne lap",
            "lasagna tészta",
        ],
        "aliases_en": [
            "lasagna sheets",
            "lasagne pasta",
        ],
    },

    # -------------------------------------------------
    # RICE AND GRAINS
    # -------------------------------------------------
    {
        "key": "white_rice",
        "category": "rice",
        "unit": "g",
        "hu": "fehér rizs",
        "en": "white rice",
        "aliases_hu": [
            "rizs",
        ],
        "aliases_en": [
            "rice",
        ],
    },
    {
        "key": "brown_rice",
        "category": "rice",
        "unit": "g",
        "hu": "barna rizs",
        "en": "brown rice",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "basmati_rice",
        "category": "rice",
        "unit": "g",
        "hu": "basmati rizs",
        "en": "basmati rice",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "jasmine_rice",
        "category": "rice",
        "unit": "g",
        "hu": "jázmin rizs",
        "en": "jasmine rice",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "arborio_rice",
        "category": "rice",
        "unit": "g",
        "hu": "arborio rizs",
        "en": "arborio rice",
        "aliases_hu": [
            "rizottórizs",
        ],
        "aliases_en": [
            "risotto rice",
        ],
    },
    {
        "key": "oats",
        "category": "grains",
        "unit": "g",
        "hu": "zabpehely",
        "en": "oats",
        "aliases_hu": [
            "zab",
        ],
        "aliases_en": [
            "rolled oats",
            "oat flakes",
        ],
    },
    {
        "key": "barley",
        "category": "grains",
        "unit": "g",
        "hu": "árpagyöngy",
        "en": "barley",
        "aliases_hu": [
            "gersli",
        ],
        "aliases_en": [
            "pearl barley",
        ],
    },
    {
        "key": "bulgur",
        "category": "grains",
        "unit": "g",
        "hu": "bulgur",
        "en": "bulgur",
        "aliases_hu": [],
        "aliases_en": [
            "bulgur wheat",
        ],
    },
    {
        "key": "couscous",
        "category": "grains",
        "unit": "g",
        "hu": "kuszkusz",
        "en": "couscous",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "quinoa",
        "category": "grains",
        "unit": "g",
        "hu": "quinoa",
        "en": "quinoa",
        "aliases_hu": [
            "kinoa",
        ],
        "aliases_en": [],
    },

    # -------------------------------------------------
    # LEGUMES
    # -------------------------------------------------
    {
        "key": "red_lentils",
        "category": "legumes",
        "unit": "g",
        "hu": "vöröslencse",
        "en": "red lentils",
        "aliases_hu": [
            "vörös lencse",
        ],
        "aliases_en": [
            "red lentil",
        ],
    },
    {
        "key": "green_lentils",
        "category": "legumes",
        "unit": "g",
        "hu": "zöld lencse",
        "en": "green lentils",
        "aliases_hu": [
            "lencse",
        ],
        "aliases_en": [
            "green lentil",
            "lentils",
        ],
    },
    {
        "key": "chickpeas",
        "category": "legumes",
        "unit": "g",
        "hu": "csicseriborsó",
        "en": "chickpeas",
        "aliases_hu": [],
        "aliases_en": [
            "chickpea",
            "garbanzo beans",
        ],
    },
    {
        "key": "kidney_beans",
        "category": "legumes",
        "unit": "g",
        "hu": "vörösbab",
        "en": "kidney beans",
        "aliases_hu": [
            "vörös bab",
        ],
        "aliases_en": [
            "kidney bean",
        ],
    },
    {
        "key": "white_beans",
        "category": "legumes",
        "unit": "g",
        "hu": "fehérbab",
        "en": "white beans",
        "aliases_hu": [
            "fehér bab",
        ],
        "aliases_en": [
            "white bean",
        ],
    },
    {
        "key": "green_peas",
        "category": "legumes",
        "unit": "g",
        "hu": "zöldborsó",
        "en": "green peas",
        "aliases_hu": [
            "borsó",
        ],
        "aliases_en": [
            "peas",
            "green pea",
        ],
    },

    # -------------------------------------------------
    # VEGETABLES
    # -------------------------------------------------
    {
        "key": "potato",
        "category": "vegetables",
        "unit": "g",
        "hu": "burgonya",
        "en": "potato",
        "aliases_hu": [
            "krumpli",
        ],
        "aliases_en": [
            "potatoes",
        ],
    },
    {
        "key": "sweet_potato",
        "category": "vegetables",
        "unit": "g",
        "hu": "édesburgonya",
        "en": "sweet potato",
        "aliases_hu": [
            "batáta",
        ],
        "aliases_en": [
            "sweet potatoes",
            "yam",
        ],
    },
    {
        "key": "onion",
        "category": "vegetables",
        "unit": "g",
        "hu": "vöröshagyma",
        "en": "onion",
        "aliases_hu": [
            "hagyma",
        ],
        "aliases_en": [
            "onions",
            "yellow onion",
        ],
    },
    {
        "key": "red_onion",
        "category": "vegetables",
        "unit": "g",
        "hu": "lilahagyma",
        "en": "red onion",
        "aliases_hu": [
            "lila hagyma",
        ],
        "aliases_en": [
            "red onions",
        ],
    },
    {
        "key": "garlic",
        "category": "vegetables",
        "unit": "g",
        "hu": "fokhagyma",
        "en": "garlic",
        "aliases_hu": [],
        "aliases_en": [
            "garlic cloves",
            "garlic clove",
        ],
    },
    {
        "key": "carrot",
        "category": "vegetables",
        "unit": "g",
        "hu": "sárgarépa",
        "en": "carrot",
        "aliases_hu": [
            "répa",
        ],
        "aliases_en": [
            "carrots",
        ],
    },
    {
        "key": "parsley_root",
        "category": "vegetables",
        "unit": "g",
        "hu": "petrezselyemgyökér",
        "en": "parsley root",
        "aliases_hu": [
            "fehérrépa",
            "gyökér",
        ],
        "aliases_en": [
            "root parsley",
        ],
    },
    {
        "key": "celeriac",
        "category": "vegetables",
        "unit": "g",
        "hu": "zeller",
        "en": "celeriac",
        "aliases_hu": [
            "zellergumó",
        ],
        "aliases_en": [
            "celery root",
        ],
    },
    {
        "key": "celery",
        "category": "vegetables",
        "unit": "g",
        "hu": "szárzeller",
        "en": "celery",
        "aliases_hu": [],
        "aliases_en": [
            "celery stalk",
        ],
    },
    {
        "key": "tomato",
        "category": "vegetables",
        "unit": "g",
        "hu": "paradicsom",
        "en": "tomato",
        "aliases_hu": [],
        "aliases_en": [
            "tomatoes",
        ],
    },
    {
        "key": "bell_pepper",
        "category": "vegetables",
        "unit": "g",
        "hu": "paprika",
        "en": "bell pepper",
        "aliases_hu": [
            "édes paprika",
            "tv paprika",
        ],
        "aliases_en": [
            "sweet pepper",
            "capsicum",
        ],
    },
    {
        "key": "chili_pepper",
        "category": "vegetables",
        "unit": "g",
        "hu": "csilipaprika",
        "en": "chili pepper",
        "aliases_hu": [
            "chili",
            "csili",
            "erős paprika",
        ],
        "aliases_en": [
            "chilli pepper",
            "chili",
            "chilli",
        ],
    },
    {
        "key": "cucumber",
        "category": "vegetables",
        "unit": "g",
        "hu": "uborka",
        "en": "cucumber",
        "aliases_hu": [],
        "aliases_en": [
            "cucumbers",
        ],
    },
    {
        "key": "zucchini",
        "category": "vegetables",
        "unit": "g",
        "hu": "cukkini",
        "en": "zucchini",
        "aliases_hu": [],
        "aliases_en": [
            "courgette",
        ],
    },
    {
        "key": "eggplant",
        "category": "vegetables",
        "unit": "g",
        "hu": "padlizsán",
        "en": "eggplant",
        "aliases_hu": [],
        "aliases_en": [
            "aubergine",
        ],
    },
    {
        "key": "broccoli",
        "category": "vegetables",
        "unit": "g",
        "hu": "brokkoli",
        "en": "broccoli",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "cauliflower",
        "category": "vegetables",
        "unit": "g",
        "hu": "karfiol",
        "en": "cauliflower",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "white_cabbage",
        "category": "vegetables",
        "unit": "g",
        "hu": "fejes káposzta",
        "en": "white cabbage",
        "aliases_hu": [
            "káposzta",
        ],
        "aliases_en": [
            "cabbage",
            "green cabbage",
        ],
    },
    {
        "key": "red_cabbage",
        "category": "vegetables",
        "unit": "g",
        "hu": "lilakáposzta",
        "en": "red cabbage",
        "aliases_hu": [
            "lila káposzta",
        ],
        "aliases_en": [],
    },
    {
        "key": "spinach",
        "category": "vegetables",
        "unit": "g",
        "hu": "spenót",
        "en": "spinach",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "mushroom",
        "category": "vegetables",
        "unit": "g",
        "hu": "csiperkegomba",
        "en": "mushroom",
        "aliases_hu": [
            "gomba",
            "csiperke",
        ],
        "aliases_en": [
            "mushrooms",
            "button mushroom",
        ],
    },

    # -------------------------------------------------
    # FRUIT
    # -------------------------------------------------
    {
        "key": "apple",
        "category": "fruit",
        "unit": "g",
        "hu": "alma",
        "en": "apple",
        "aliases_hu": [],
        "aliases_en": [
            "apples",
        ],
    },
    {
        "key": "pear",
        "category": "fruit",
        "unit": "g",
        "hu": "körte",
        "en": "pear",
        "aliases_hu": [],
        "aliases_en": [
            "pears",
        ],
    },
    {
        "key": "banana",
        "category": "fruit",
        "unit": "g",
        "hu": "banán",
        "en": "banana",
        "aliases_hu": [],
        "aliases_en": [
            "bananas",
        ],
    },
    {
        "key": "orange",
        "category": "fruit",
        "unit": "g",
        "hu": "narancs",
        "en": "orange",
        "aliases_hu": [],
        "aliases_en": [
            "oranges",
        ],
    },
    {
        "key": "lemon",
        "category": "fruit",
        "unit": "g",
        "hu": "citrom",
        "en": "lemon",
        "aliases_hu": [],
        "aliases_en": [
            "lemons",
        ],
    },
    {
        "key": "lime",
        "category": "fruit",
        "unit": "g",
        "hu": "lime",
        "en": "lime",
        "aliases_hu": [
            "zöldcitrom",
        ],
        "aliases_en": [
            "limes",
        ],
    },
    {
        "key": "strawberry",
        "category": "fruit",
        "unit": "g",
        "hu": "eper",
        "en": "strawberry",
        "aliases_hu": [
            "szamóca",
        ],
        "aliases_en": [
            "strawberries",
        ],
    },
    {
        "key": "blueberry",
        "category": "fruit",
        "unit": "g",
        "hu": "áfonya",
        "en": "blueberry",
        "aliases_hu": [],
        "aliases_en": [
            "blueberries",
        ],
    },
    {
        "key": "raspberry",
        "category": "fruit",
        "unit": "g",
        "hu": "málna",
        "en": "raspberry",
        "aliases_hu": [],
        "aliases_en": [
            "raspberries",
        ],
    },
    {
        "key": "peach",
        "category": "fruit",
        "unit": "g",
        "hu": "őszibarack",
        "en": "peach",
        "aliases_hu": [
            "barack",
        ],
        "aliases_en": [
            "peaches",
        ],
    },
    {
        "key": "apricot",
        "category": "fruit",
        "unit": "g",
        "hu": "sárgabarack",
        "en": "apricot",
        "aliases_hu": [],
        "aliases_en": [
            "apricots",
        ],
    },

    # -------------------------------------------------
    # HERBS AND SPICES
    # -------------------------------------------------
    {
        "key": "salt",
        "category": "spices",
        "unit": "g",
        "hu": "só",
        "en": "salt",
        "aliases_hu": [
            "konyhasó",
        ],
        "aliases_en": [
            "table salt",
        ],
    },
    {
        "key": "black_pepper",
        "category": "spices",
        "unit": "g",
        "hu": "fekete bors",
        "en": "black pepper",
        "aliases_hu": [
            "bors",
        ],
        "aliases_en": [
            "pepper",
            "ground black pepper",
        ],
    },
    {
        "key": "paprika_powder",
        "category": "spices",
        "unit": "g",
        "hu": "pirospaprika",
        "en": "paprika",
        "aliases_hu": [
            "őrölt paprika",
            "fűszerpaprika",
        ],
        "aliases_en": [
            "paprika powder",
            "ground paprika",
        ],
    },
    {
        "key": "cumin",
        "category": "spices",
        "unit": "g",
        "hu": "római kömény",
        "en": "cumin",
        "aliases_hu": [],
        "aliases_en": [
            "ground cumin",
            "cumin seed",
        ],
    },
    {
        "key": "caraway",
        "category": "spices",
        "unit": "g",
        "hu": "köménymag",
        "en": "caraway",
        "aliases_hu": [
            "kömény",
        ],
        "aliases_en": [
            "caraway seeds",
        ],
    },
    {
        "key": "cinnamon",
        "category": "spices",
        "unit": "g",
        "hu": "fahéj",
        "en": "cinnamon",
        "aliases_hu": [
            "őrölt fahéj",
        ],
        "aliases_en": [
            "ground cinnamon",
        ],
    },
    {
        "key": "nutmeg",
        "category": "spices",
        "unit": "g",
        "hu": "szerecsendió",
        "en": "nutmeg",
        "aliases_hu": [],
        "aliases_en": [
            "ground nutmeg",
        ],
    },
    {
        "key": "turmeric",
        "category": "spices",
        "unit": "g",
        "hu": "kurkuma",
        "en": "turmeric",
        "aliases_hu": [],
        "aliases_en": [
            "ground turmeric",
        ],
    },
    {
        "key": "curry_powder",
        "category": "spices",
        "unit": "g",
        "hu": "currypor",
        "en": "curry powder",
        "aliases_hu": [
            "curry por",
        ],
        "aliases_en": [
            "curry spice",
        ],
    },
    {
        "key": "oregano",
        "category": "herbs",
        "unit": "g",
        "hu": "oregánó",
        "en": "oregano",
        "aliases_hu": [
            "szurokfű",
        ],
        "aliases_en": [
            "dried oregano",
        ],
    },
    {
        "key": "basil",
        "category": "herbs",
        "unit": "g",
        "hu": "bazsalikom",
        "en": "basil",
        "aliases_hu": [],
        "aliases_en": [
            "fresh basil",
            "dried basil",
        ],
    },
    {
        "key": "thyme",
        "category": "herbs",
        "unit": "g",
        "hu": "kakukkfű",
        "en": "thyme",
        "aliases_hu": [],
        "aliases_en": [
            "dried thyme",
        ],
    },
    {
        "key": "rosemary",
        "category": "herbs",
        "unit": "g",
        "hu": "rozmaring",
        "en": "rosemary",
        "aliases_hu": [],
        "aliases_en": [
            "fresh rosemary",
            "dried rosemary",
        ],
    },
    {
        "key": "parsley",
        "category": "herbs",
        "unit": "g",
        "hu": "petrezselyemzöld",
        "en": "parsley",
        "aliases_hu": [
            "petrezselyem",
        ],
        "aliases_en": [
            "fresh parsley",
        ],
    },
    {
        "key": "dill",
        "category": "herbs",
        "unit": "g",
        "hu": "kapor",
        "en": "dill",
        "aliases_hu": [],
        "aliases_en": [
            "fresh dill",
        ],
    },

    # -------------------------------------------------
    # OILS AND FATS
    # -------------------------------------------------
    {
        "key": "sunflower_oil",
        "category": "oils_and_fats",
        "unit": "ml",
        "hu": "napraforgóolaj",
        "en": "sunflower oil",
        "aliases_hu": [
            "étolaj",
        ],
        "aliases_en": [],
    },
    {
        "key": "olive_oil",
        "category": "oils_and_fats",
        "unit": "ml",
        "hu": "olívaolaj",
        "en": "olive oil",
        "aliases_hu": [],
        "aliases_en": [
            "extra virgin olive oil",
            "evoo",
        ],
    },
    {
        "key": "lard",
        "category": "oils_and_fats",
        "unit": "g",
        "hu": "sertészsír",
        "en": "lard",
        "aliases_hu": [
            "zsír",
        ],
        "aliases_en": [
            "pork lard",
        ],
    },

    # -------------------------------------------------
    # SUGAR AND SWEETENERS
    # -------------------------------------------------
    {
        "key": "granulated_sugar",
        "category": "sugar_and_sweeteners",
        "unit": "g",
        "hu": "kristálycukor",
        "en": "granulated sugar",
        "aliases_hu": [
            "cukor",
        ],
        "aliases_en": [
            "white sugar",
            "sugar",
        ],
    },
    {
        "key": "powdered_sugar",
        "category": "sugar_and_sweeteners",
        "unit": "g",
        "hu": "porcukor",
        "en": "powdered sugar",
        "aliases_hu": [],
        "aliases_en": [
            "icing sugar",
            "confectioners sugar",
        ],
    },
    {
        "key": "brown_sugar",
        "category": "sugar_and_sweeteners",
        "unit": "g",
        "hu": "barna cukor",
        "en": "brown sugar",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "honey",
        "category": "sugar_and_sweeteners",
        "unit": "g",
        "hu": "méz",
        "en": "honey",
        "aliases_hu": [],
        "aliases_en": [],
    },

    # -------------------------------------------------
    # BAKING
    # -------------------------------------------------
    {
        "key": "baking_powder",
        "category": "baking",
        "unit": "g",
        "hu": "sütőpor",
        "en": "baking powder",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "baking_soda",
        "category": "baking",
        "unit": "g",
        "hu": "szódabikarbóna",
        "en": "baking soda",
        "aliases_hu": [],
        "aliases_en": [
            "bicarbonate of soda",
            "sodium bicarbonate",
        ],
    },
    {
        "key": "dry_yeast",
        "category": "baking",
        "unit": "g",
        "hu": "szárított élesztő",
        "en": "dry yeast",
        "aliases_hu": [
            "instant élesztő",
        ],
        "aliases_en": [
            "instant yeast",
            "active dry yeast",
        ],
    },
    {
        "key": "fresh_yeast",
        "category": "baking",
        "unit": "g",
        "hu": "friss élesztő",
        "en": "fresh yeast",
        "aliases_hu": [
            "élesztő",
        ],
        "aliases_en": [
            "compressed yeast",
        ],
    },
    {
        "key": "cornstarch",
        "category": "baking",
        "unit": "g",
        "hu": "kukoricakeményítő",
        "en": "cornstarch",
        "aliases_hu": [
            "étkezési keményítő",
        ],
        "aliases_en": [
            "corn starch",
            "cornflour starch",
        ],
    },
    {
        "key": "cocoa_powder",
        "category": "baking",
        "unit": "g",
        "hu": "kakaópor",
        "en": "cocoa powder",
        "aliases_hu": [
            "cukrozatlan kakaópor",
        ],
        "aliases_en": [
            "unsweetened cocoa powder",
        ],
    },
    {
        "key": "dark_chocolate",
        "category": "baking",
        "unit": "g",
        "hu": "étcsokoládé",
        "en": "dark chocolate",
        "aliases_hu": [
            "étcsoki",
        ],
        "aliases_en": [
            "dark choc",
        ],
    },
    {
        "key": "vanilla_extract",
        "category": "baking",
        "unit": "ml",
        "hu": "vaníliakivonat",
        "en": "vanilla extract",
        "aliases_hu": [
            "vanília kivonat",
        ],
        "aliases_en": [],
    },

    # -------------------------------------------------
    # SAUCES AND CONDIMENTS
    # -------------------------------------------------
    {
        "key": "tomato_paste",
        "category": "sauces_and_condiments",
        "unit": "g",
        "hu": "paradicsompüré",
        "en": "tomato paste",
        "aliases_hu": [
            "sűrített paradicsom",
        ],
        "aliases_en": [
            "tomato puree concentrate",
        ],
    },
    {
        "key": "passata",
        "category": "sauces_and_condiments",
        "unit": "ml",
        "hu": "passata",
        "en": "passata",
        "aliases_hu": [
            "passzírozott paradicsom",
        ],
        "aliases_en": [
            "tomato passata",
            "strained tomatoes",
        ],
    },
    {
        "key": "ketchup",
        "category": "sauces_and_condiments",
        "unit": "g",
        "hu": "ketchup",
        "en": "ketchup",
        "aliases_hu": [],
        "aliases_en": [
            "tomato ketchup",
        ],
    },
    {
        "key": "mustard",
        "category": "sauces_and_condiments",
        "unit": "g",
        "hu": "mustár",
        "en": "mustard",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "mayonnaise",
        "category": "sauces_and_condiments",
        "unit": "g",
        "hu": "majonéz",
        "en": "mayonnaise",
        "aliases_hu": [],
        "aliases_en": [
            "mayo",
        ],
    },
    {
        "key": "soy_sauce",
        "category": "sauces_and_condiments",
        "unit": "ml",
        "hu": "szójaszósz",
        "en": "soy sauce",
        "aliases_hu": [],
        "aliases_en": [
            "soya sauce",
        ],
    },
    {
        "key": "worcestershire_sauce",
        "category": "sauces_and_condiments",
        "unit": "ml",
        "hu": "Worcestershire-szósz",
        "en": "Worcestershire sauce",
        "aliases_hu": [
            "Worcester szósz",
        ],
        "aliases_en": [
            "Worcester sauce",
        ],
    },
    {
        "key": "vinegar",
        "category": "sauces_and_condiments",
        "unit": "ml",
        "hu": "ecet",
        "en": "vinegar",
        "aliases_hu": [],
        "aliases_en": [],
    },
    {
        "key": "balsamic_vinegar",
        "category": "sauces_and_condiments",
        "unit": "ml",
        "hu": "balzsamecet",
        "en": "balsamic vinegar",
        "aliases_hu": [],
        "aliases_en": [],
    },

    # -------------------------------------------------
    # NUTS AND SEEDS
    # -------------------------------------------------
    {
        "key": "walnut",
        "category": "nuts_and_seeds",
        "unit": "g",
        "hu": "dió",
        "en": "walnut",
        "aliases_hu": [
            "dióbél",
        ],
        "aliases_en": [
            "walnuts",
        ],
    },
    {
        "key": "almond",
        "category": "nuts_and_seeds",
        "unit": "g",
        "hu": "mandula",
        "en": "almond",
        "aliases_hu": [],
        "aliases_en": [
            "almonds",
        ],
    },
    {
        "key": "hazelnut",
        "category": "nuts_and_seeds",
        "unit": "g",
        "hu": "mogyoró",
        "en": "hazelnut",
        "aliases_hu": [
            "törökmogyoró",
        ],
        "aliases_en": [
            "hazelnuts",
        ],
    },
    {
        "key": "peanut",
        "category": "nuts_and_seeds",
        "unit": "g",
        "hu": "földimogyoró",
        "en": "peanut",
        "aliases_hu": [],
        "aliases_en": [
            "peanuts",
        ],
    },
    {
        "key": "sunflower_seeds",
        "category": "nuts_and_seeds",
        "unit": "g",
        "hu": "napraforgómag",
        "en": "sunflower seeds",
        "aliases_hu": [],
        "aliases_en": [
            "sunflower seed",
        ],
    },
    {
        "key": "pumpkin_seeds",
        "category": "nuts_and_seeds",
        "unit": "g",
        "hu": "tökmag",
        "en": "pumpkin seeds",
        "aliases_hu": [],
        "aliases_en": [
            "pumpkin seed",
            "pepitas",
        ],
    },

    # -------------------------------------------------
    # CANNED / PRESERVED
    # -------------------------------------------------
    {
        "key": "canned_tomatoes",
        "category": "canned_and_preserved",
        "unit": "g",
        "hu": "konzerv paradicsom",
        "en": "canned tomatoes",
        "aliases_hu": [
            "darabolt paradicsom konzerv",
        ],
        "aliases_en": [
            "tinned tomatoes",
            "chopped tomatoes",
        ],
    },
    {
        "key": "canned_tuna",
        "category": "canned_and_preserved",
        "unit": "g",
        "hu": "tonhalkonzerv",
        "en": "canned tuna",
        "aliases_hu": [
            "konzerv tonhal",
        ],
        "aliases_en": [
            "tinned tuna",
        ],
    },
    {
        "key": "pickles",
        "category": "canned_and_preserved",
        "unit": "g",
        "hu": "savanyú uborka",
        "en": "pickles",
        "aliases_hu": [
            "csemegeuborka",
            "kovászos uborka",
        ],
        "aliases_en": [
            "pickled cucumber",
            "gherkins",
        ],
    },
]


def normalize_alias(value):
    value = unicodedata.normalize(
        "NFKD",
        value,
    )

    value = "".join(
        char
        for char in value
        if not unicodedata.combining(char)
    )

    value = value.lower().strip()

    value = re.sub(
        r"[^a-z0-9]+",
        " ",
        value,
    )

    return re.sub(
        r"\s+",
        " ",
        value,
    ).strip()


def get_category(key):
    category = (
        db.session.query(
            IngredientCategory
        )
        .filter_by(
            canonical_key=key
        )
        .one_or_none()
    )

    if category is None:
        raise RuntimeError(
            f"Missing ingredient category: {key}"
        )

    return category


def get_unit(code):
    unit = (
        db.session.query(Unit)
        .filter_by(
            code=code
        )
        .one_or_none()
    )

    if unit is None:
        raise RuntimeError(
            f"Missing unit: {code}"
        )

    return unit


def upsert_translation(
    ingredient,
    language_code,
    name,
):
    translation = next(
        (
            item
            for item in ingredient.translations
            if item.language_code
            == language_code
        ),
        None,
    )

    if translation is None:
        translation = IngredientTranslation(
            language_code=language_code,
            name=name,
        )

        ingredient.translations.append(
            translation
        )

    else:
        translation.name = name


def sync_aliases(
    ingredient,
    language_code,
    primary_name,
    aliases,
):
    desired = []

    for alias in [
        primary_name,
        *aliases,
    ]:
        normalized = normalize_alias(
            alias
        )

        if not normalized:
            continue

        desired.append(
            (
                alias,
                normalized,
            )
        )

    unique_desired = {}

    for alias, normalized in desired:
        unique_desired[
            normalized
        ] = alias

    existing = {
        item.normalized_alias: item
        for item in ingredient.aliases
        if item.language_code
        == language_code
    }

    for normalized, alias in (
        unique_desired.items()
    ):
        item = existing.get(
            normalized
        )

        if item is None:
            item = IngredientAlias(
                language_code=language_code,
                alias=alias,
                normalized_alias=normalized,
            )

            ingredient.aliases.append(
                item
            )

        else:
            item.alias = alias

    for normalized, item in list(
        existing.items()
    ):
        if normalized not in unique_desired:
            db.session.delete(
                item
            )


def seed_ingredients():
    category_cache = {}
    unit_cache = {}

    for item in INGREDIENTS:
        category_key = item["category"]
        unit_code = item["unit"]

        if category_key not in category_cache:
            category_cache[
                category_key
            ] = get_category(
                category_key
            )

        if unit_code not in unit_cache:
            unit_cache[
                unit_code
            ] = get_unit(
                unit_code
            )

        ingredient = (
            db.session.query(
                Ingredient
            )
            .filter_by(
                canonical_key=item["key"]
            )
            .one_or_none()
        )

        if ingredient is None:
            ingredient = Ingredient(
                canonical_key=item["key"]
            )

            db.session.add(
                ingredient
            )

        ingredient.category = (
            category_cache[
                category_key
            ]
        )

        ingredient.default_unit = (
            unit_cache[
                unit_code
            ]
        )

        ingredient.is_active = True

        upsert_translation(
            ingredient,
            "hu",
            item["hu"],
        )

        upsert_translation(
            ingredient,
            "en",
            item["en"],
        )

        sync_aliases(
            ingredient,
            "hu",
            item["hu"],
            item["aliases_hu"],
        )

        sync_aliases(
            ingredient,
            "en",
            item["en"],
            item["aliases_en"],
        )

    db.session.commit()


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        seed_ingredients()

        print(
            f"Seeded {len(INGREDIENTS)} ingredients."
        )
