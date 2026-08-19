import uuid

from sqlalchemy import func

from app.extensions import db

recipe_tags = db.Table(
    "recipe_tags",

    db.Column(
        "recipe_id",
        db.Integer,
        db.ForeignKey(
            "recipes.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),

    db.Column(
        "tag_id",
        db.Integer,
        db.ForeignKey(
            "recipe_tag_definitions.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
)


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    public_id = db.Column(
        db.Uuid,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
        index=True,
    )

    household_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "households.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    title = db.Column(
        db.String(255),
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=True,
    )

    cuisine = db.Column(
        db.String(100),
        nullable=True,
        index=True,
    )

    category = db.Column(
        db.String(100),
        nullable=True,
        index=True,
    )

    difficulty = db.Column(
        db.String(30),
        nullable=True,
        index=True,
    )

    servings = db.Column(
        db.Integer,
        nullable=True,
    )

    prep_time_minutes = db.Column(
        db.Integer,
        nullable=True,
    )

    cook_time_minutes = db.Column(
        db.Integer,
        nullable=True,
    )

    total_time_minutes = db.Column(
        db.Integer,
        nullable=True,
        index=True,
    )

    instructions_text = db.Column(
        db.Text,
        nullable=True,
    )

    source_type = db.Column(
        db.String(60),
        nullable=False,
        default="manual",
        index=True,
    )

    source_id = db.Column(
        db.String(160),
        nullable=True,
        index=True,
    )

    source_url = db.Column(
        db.Text,
        nullable=True,
    )

    external_data = db.Column(
        db.JSON,
        nullable=True,
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        index=True,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    household = db.relationship(
        "Household",
    )

    ingredients = db.relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete-orphan",
        order_by=(
            "RecipeIngredient.sort_order, "
            "RecipeIngredient.id"
        ),
    )

    tags = db.relationship(
        "RecipeTag",
        secondary=recipe_tags,
        back_populates="recipes",
        order_by="RecipeTag.sort_order, RecipeTag.name",
    )

    images = db.relationship(
        "RecipeImage",
        back_populates="recipe",
        cascade="all, delete-orphan",
        order_by=(
            "RecipeImage.sort_order, "
            "RecipeImage.id"
        ),
    )


class RecipeImage(db.Model):
    __tablename__ = "recipe_images"

    __table_args__ = (
        db.UniqueConstraint(
            "recipe_id",
            "stored_filename",
            name="uq_recipe_image_file",
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    public_id = db.Column(
        db.Uuid,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
        index=True,
    )

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "recipes.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    original_filename = db.Column(
        db.String(255),
        nullable=True,
    )

    stored_filename = db.Column(
        db.String(255),
        nullable=False,
    )

    is_cover = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        index=True,
    )

    sort_order = db.Column(
        db.Integer,
        nullable=False,
        default=100,
    )

    width = db.Column(
        db.Integer,
        nullable=True,
    )

    height = db.Column(
        db.Integer,
        nullable=True,
    )

    file_size = db.Column(
        db.Integer,
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    recipe = db.relationship(
        "Recipe",
        back_populates="images",
    )


class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredients"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "recipes.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    ingredient_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "ingredients.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    original_name = db.Column(
        db.String(255),
        nullable=False,
    )

    quantity = db.Column(
        db.Numeric(
            precision=18,
            scale=6,
        ),
        nullable=True,
    )

    unit_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "units.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    unit_text = db.Column(
        db.String(80),
        nullable=True,
    )

    note = db.Column(
        db.Text,
        nullable=True,
    )

    is_optional = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    sort_order = db.Column(
        db.Integer,
        nullable=False,
        default=100,
    )

    recipe = db.relationship(
        "Recipe",
        back_populates="ingredients",
    )

    ingredient = db.relationship(
        "Ingredient",
    )

    unit = db.relationship(
        "Unit",
    )

class RecipeTag(db.Model):
    __tablename__ = "recipe_tag_definitions"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    key = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
        index=True,
    )

    name = db.Column(
        db.String(120),
        nullable=False,
    )

    group_name = db.Column(
        db.String(50),
        nullable=False,
        index=True,
    )

    sort_order = db.Column(
        db.Integer,
        nullable=False,
        default=100,
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        index=True,
    )

    recipes = db.relationship(
        "Recipe",
        secondary=recipe_tags,
        back_populates="tags",
    )
