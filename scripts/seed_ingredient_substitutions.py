from decimal import Decimal
from pathlib import Path
import sys

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )

load_dotenv(
    PROJECT_ROOT / ".env"
)


from app import create_app
from app.extensions import db
from app.models import (
    Ingredient,
    IngredientSubstitution,
)


SUBSTITUTIONS = [
    # -------------------------------------------------
    # POULTRY
    # -------------------------------------------------
    {
        "source": "chicken_breast",
        "target": "chicken_thigh",
        "rating": "good",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "A csirkecomb általában szaftosabb és zsírosabb, "
            "de sok ételben jól helyettesíti a csirkemellet."
        ),
        "note_en": (
            "Chicken thigh is usually juicier and fattier, "
            "but works well instead of chicken breast in many dishes."
        ),
    },
    {
        "source": "chicken_thigh",
        "target": "chicken_breast",
        "rating": "good",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "A csirkemell soványabb és könnyebben kiszárad, "
            "de sok receptben használható csirkecomb helyett."
        ),
        "note_en": (
            "Chicken breast is leaner and can dry out more easily, "
            "but can replace chicken thigh in many recipes."
        ),
    },
    {
        "source": "turkey_breast",
        "target": "chicken_breast",
        "rating": "good",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "A csirkemell ízben és állagban általában jól "
            "helyettesíti a pulykamellet."
        ),
        "note_en": (
            "Chicken breast is generally a good substitute for "
            "turkey breast in flavour and texture."
        ),
    },
    {
        "source": "chicken_breast",
        "target": "turkey_breast",
        "rating": "good",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "A pulykamell sok csirkemelles ételben "
            "közel azonos módon használható."
        ),
        "note_en": (
            "Turkey breast can be used similarly in many "
            "recipes calling for chicken breast."
        ),
    },

    # -------------------------------------------------
    # PORK
    # -------------------------------------------------
    {
        "source": "pork_leg",
        "target": "pork_shoulder",
        "rating": "excellent",
        "ratio": "1",
        "context": "stew",
        "note_hu": (
            "Pörköltekben és hosszabban főtt ételekben a lapocka "
            "kifejezetten jó helyettesítő, gyakran szaftosabb is."
        ),
        "note_en": (
            "For stews and long-cooked dishes, pork shoulder is an "
            "excellent substitute and is often juicier."
        ),
    },
    {
        "source": "pork_shoulder",
        "target": "pork_leg",
        "rating": "good",
        "ratio": "1",
        "context": "stew",
        "note_hu": (
            "A sertéscomb használható lapocka helyett, "
            "de általában soványabb."
        ),
        "note_en": (
            "Pork leg can replace pork shoulder, "
            "but it is generally leaner."
        ),
    },
    {
        "source": "pork_loin",
        "target": "pork_tenderloin",
        "rating": "good",
        "ratio": "1",
        "context": "frying",
        "note_hu": (
            "Szeletben sütve a sertésszűz jól helyettesítheti "
            "a karajt, de általában gyorsabban elkészül."
        ),
        "note_en": (
            "Pork tenderloin can replace pork loin for frying, "
            "but usually cooks faster."
        ),
    },
    {
        "source": "pork_tenderloin",
        "target": "pork_loin",
        "rating": "acceptable",
        "ratio": "1",
        "context": "frying",
        "note_hu": (
            "A karaj helyettesítheti a sertésszüzet, "
            "de kevésbé omlós lehet."
        ),
        "note_en": (
            "Pork loin can replace tenderloin, "
            "but may be less tender."
        ),
    },

    # -------------------------------------------------
    # GROUND MEAT
    # -------------------------------------------------
    {
        "source": "ground_beef",
        "target": "mixed_ground_meat",
        "rating": "excellent",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "A sertés-marha vegyes darált hús sok darált marhás "
            "ételben jól használható, de zsírosabb lehet."
        ),
        "note_en": (
            "Mixed pork-beef mince works well in many dishes calling "
            "for ground beef, but may be fattier."
        ),
    },
    {
        "source": "ground_pork",
        "target": "mixed_ground_meat",
        "rating": "excellent",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "A vegyes darált hús sok darált sertéshúsos ételben "
            "közvetlenül használható."
        ),
        "note_en": (
            "Mixed ground meat can directly replace ground pork "
            "in many dishes."
        ),
    },
    {
        "source": "mixed_ground_meat",
        "target": "ground_beef",
        "rating": "good",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "Darált marhahússal a vegyes darált hús helyettesíthető, "
            "de a végeredmény soványabb és marhásabb ízű lehet."
        ),
        "note_en": (
            "Ground beef can replace mixed mince, but the result "
            "may be leaner and more beef-forward."
        ),
    },
    {
        "source": "mixed_ground_meat",
        "target": "ground_pork",
        "rating": "good",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "Darált sertéshús használható vegyes darált hús helyett, "
            "de az íz és zsírosság eltérhet."
        ),
        "note_en": (
            "Ground pork can replace mixed mince, though flavour "
            "and fat content may differ."
        ),
    },
    {
        "source": "ground_beef",
        "target": "ground_pork",
        "rating": "acceptable",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "Bizonyos darált húsos ételekben használható, "
            "de az íz és a zsírtartalom jelentősen változhat."
        ),
        "note_en": (
            "Usable in some minced-meat dishes, but flavour and "
            "fat content can change significantly."
        ),
    },
    {
        "source": "ground_pork",
        "target": "ground_beef",
        "rating": "acceptable",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "Bizonyos darált húsos ételekben működik, "
            "de markánsabb marhahúsízre kell számítani."
        ),
        "note_en": (
            "Works in some minced-meat dishes, but expect a "
            "stronger beef flavour."
        ),
    },

    # -------------------------------------------------
    # FLOUR
    # -------------------------------------------------
    {
        "source": "all_purpose_flour",
        "target": "pizza_flour",
        "rating": "good",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "A pizzaliszt sok általános búzalisztes receptben "
            "használható, bár a tészta viselkedése kissé eltérhet."
        ),
        "note_en": (
            "Pizza flour can be used in many recipes calling for "
            "all-purpose flour, though dough behaviour may differ."
        ),
    },
    {
        "source": "pizza_flour",
        "target": "all_purpose_flour",
        "rating": "acceptable",
        "ratio": "1",
        "context": "pizza",
        "note_hu": (
            "Finomliszttel is készíthető pizza, de a tészta "
            "rugalmassága és szerkezete eltérhet."
        ),
        "note_en": (
            "Pizza can be made with all-purpose flour, but dough "
            "elasticity and structure may differ."
        ),
    },
    {
        "source": "all_purpose_flour",
        "target": "bread_flour",
        "rating": "good",
        "ratio": "1",
        "context": "baking",
        "note_hu": (
            "Kenyérliszt sok sütési receptben használható finomliszt "
            "helyett, de magasabb sikértartalma miatt az állag változhat."
        ),
        "note_en": (
            "Bread flour can replace all-purpose flour in many baking "
            "recipes, but its higher gluten content may change texture."
        ),
    },
    {
        "source": "bread_flour",
        "target": "all_purpose_flour",
        "rating": "good",
        "ratio": "1",
        "context": "baking",
        "note_hu": (
            "Finomliszt használható kenyérliszt helyett, "
            "de gyengébb tésztaszerkezetet adhat."
        ),
        "note_en": (
            "All-purpose flour can replace bread flour, "
            "but may produce a weaker dough structure."
        ),
    },
    {
        "source": "pizza_flour",
        "target": "bread_flour",
        "rating": "good",
        "ratio": "1",
        "context": "pizza",
        "note_hu": (
            "Kenyérliszt általában jól használható pizzaliszt helyett."
        ),
        "note_en": (
            "Bread flour is generally a good substitute for pizza flour."
        ),
    },
    {
        "source": "bread_flour",
        "target": "pizza_flour",
        "rating": "good",
        "ratio": "1",
        "context": "baking",
        "note_hu": (
            "Pizzaliszt sok kelt tésztában használható kenyérliszt helyett."
        ),
        "note_en": (
            "Pizza flour can be used instead of bread flour "
            "in many yeast doughs."
        ),
    },

    # -------------------------------------------------
    # DAIRY / FATS
    # -------------------------------------------------
    {
        "source": "butter",
        "target": "margarine",
        "rating": "good",
        "ratio": "1",
        "context": "baking",
        "note_hu": (
            "Margarin sok sütési receptben 1:1 arányban használható "
            "vaj helyett, de az íz és víztartalom eltérhet."
        ),
        "note_en": (
            "Margarine can replace butter 1:1 in many baking recipes, "
            "but flavour and water content may differ."
        ),
    },
    {
        "source": "margarine",
        "target": "butter",
        "rating": "excellent",
        "ratio": "1",
        "context": "baking",
        "note_hu": (
            "A vaj általában jól helyettesíti a margarint sütésnél."
        ),
        "note_en": (
            "Butter generally replaces margarine very well in baking."
        ),
    },
    {
        "source": "sour_cream",
        "target": "greek_yogurt",
        "rating": "good",
        "ratio": "1",
        "context": "sauce",
        "note_hu": (
            "Görög joghurt sok hideg szószban és mártásban "
            "jól helyettesíti a tejfölt."
        ),
        "note_en": (
            "Greek yogurt works well instead of sour cream "
            "in many cold sauces and dressings."
        ),
    },
    {
        "source": "greek_yogurt",
        "target": "sour_cream",
        "rating": "good",
        "ratio": "1",
        "context": "sauce",
        "note_hu": (
            "Tejföl használható görög joghurt helyett, "
            "de zsírosabb és savanykásabb lehet."
        ),
        "note_en": (
            "Sour cream can replace Greek yogurt, "
            "but may be richer and tangier."
        ),
    },
    {
        "source": "cream",
        "target": "sour_cream",
        "rating": "limited",
        "ratio": "1",
        "context": "sauce",
        "note_hu": (
            "Tejföl egyes szószokban helyettesítheti a tejszínt, "
            "de savanykásabb és sűrűbb eredményt ad."
        ),
        "note_en": (
            "Sour cream can replace cream in some sauces, "
            "but gives a tangier and thicker result."
        ),
    },

    # -------------------------------------------------
    # RICE / GRAINS
    # -------------------------------------------------
    {
        "source": "white_rice",
        "target": "basmati_rice",
        "rating": "excellent",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "A basmati rizs sok általános rizses ételben "
            "közvetlenül használható fehér rizs helyett."
        ),
        "note_en": (
            "Basmati rice can directly replace white rice "
            "in many general rice dishes."
        ),
    },
    {
        "source": "white_rice",
        "target": "jasmine_rice",
        "rating": "excellent",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "A jázmin rizs sok általános rizses ételben "
            "jól helyettesíti a fehér rizst."
        ),
        "note_en": (
            "Jasmine rice works well instead of white rice "
            "in many general rice dishes."
        ),
    },
    {
        "source": "basmati_rice",
        "target": "jasmine_rice",
        "rating": "good",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "Jázmin rizs használható basmati helyett, "
            "de aromája és állaga eltér."
        ),
        "note_en": (
            "Jasmine rice can replace basmati, "
            "but aroma and texture differ."
        ),
    },
    {
        "source": "jasmine_rice",
        "target": "basmati_rice",
        "rating": "good",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "Basmati használható jázmin rizs helyett, "
            "de aromája és állaga eltér."
        ),
        "note_en": (
            "Basmati can replace jasmine rice, "
            "but aroma and texture differ."
        ),
    },

    # -------------------------------------------------
    # OILS
    # -------------------------------------------------
    {
        "source": "sunflower_oil",
        "target": "olive_oil",
        "rating": "good",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "Olívaolaj sok ételben használható napraforgóolaj helyett, "
            "de karakteresebb ízt ad."
        ),
        "note_en": (
            "Olive oil can replace sunflower oil in many dishes, "
            "but adds a stronger flavour."
        ),
    },
    {
        "source": "olive_oil",
        "target": "sunflower_oil",
        "rating": "good",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "Napraforgóolaj sok esetben használható olívaolaj helyett, "
            "de semlegesebb ízű."
        ),
        "note_en": (
            "Sunflower oil can replace olive oil in many cases, "
            "but has a more neutral flavour."
        ),
    },

    # -------------------------------------------------
    # VEGETABLES / FLAVOUR BASE
    # -------------------------------------------------
    {
        "source": "onion",
        "target": "red_onion",
        "rating": "good",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "Lilahagyma sok ételben használható vöröshagyma helyett, "
            "de enyhébb és édeskésebb lehet."
        ),
        "note_en": (
            "Red onion can replace yellow onion in many dishes, "
            "but may taste milder and sweeter."
        ),
    },
    {
        "source": "red_onion",
        "target": "onion",
        "rating": "excellent",
        "ratio": "1",
        "context": "general",
        "note_hu": (
            "Vöröshagyma szinte minden főtt ételben jól "
            "helyettesíti a lilahagymát."
        ),
        "note_en": (
            "Yellow onion replaces red onion very well "
            "in most cooked dishes."
        ),
    },
]


def get_ingredient(key):
    ingredient = (
        db.session.query(Ingredient)
        .filter_by(
            canonical_key=key
        )
        .one_or_none()
    )

    if ingredient is None:
        raise RuntimeError(
            f"Missing ingredient: {key}"
        )

    return ingredient


def seed_substitutions():
    ingredient_cache = {}

    def cached_ingredient(key):
        if key not in ingredient_cache:
            ingredient_cache[key] = (
                get_ingredient(key)
            )

        return ingredient_cache[key]

    for item in SUBSTITUTIONS:
        source = cached_ingredient(
            item["source"]
        )

        target = cached_ingredient(
            item["target"]
        )

        substitution = (
            db.session.query(
                IngredientSubstitution
            )
            .filter_by(
                source_ingredient_id=source.id,
                target_ingredient_id=target.id,
                context=item["context"],
            )
            .one_or_none()
        )

        if substitution is None:
            substitution = (
                IngredientSubstitution(
                    source_ingredient=source,
                    target_ingredient=target,
                    context=item["context"],
                )
            )

            db.session.add(
                substitution
            )

        substitution.rating = (
            item["rating"]
        )

        substitution.quantity_ratio = (
            Decimal(
                item["ratio"]
            )
        )

        substitution.note_hu = (
            item["note_hu"]
        )

        substitution.note_en = (
            item["note_en"]
        )

        substitution.is_active = True

    db.session.commit()


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        seed_substitutions()

        print(
            f"Seeded {len(SUBSTITUTIONS)} "
            "ingredient substitutions."
        )
