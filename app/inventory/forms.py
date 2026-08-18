from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    DateField,
    DecimalField,
    IntegerField,
    FileField,
    HiddenField,
    MultipleFileField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
    Optional,
)


class StorageLocationForm(FlaskForm):
    name = StringField(
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=160,
            ),
        ],
    )

    location_type = SelectField(
        choices=[],
        validators=[
            DataRequired(),
        ],
    )

    parent_id = SelectField(
        choices=[],
        coerce=int,
        validators=[
            Optional(),
        ],
    )

    sort_order = IntegerField(
        default=100,
        validators=[
            DataRequired(),
            NumberRange(
                min=0,
                max=99999,
            ),
        ],
    )

    submit = SubmitField()


class InventoryBatchForm(FlaskForm):
    ingredient_id = SelectField(
        choices=[],
        coerce=int,
        validators=[
            DataRequired(),
        ],
    )

    product_id = SelectField(
        choices=[],
        coerce=int,
        validators=[
            Optional(),
        ],
    )

    barcode = StringField(
        validators=[
            Optional(),
            Length(max=64),
        ],
    )

    new_product_name = StringField(
        validators=[
            Optional(),
            Length(max=255),
        ],
    )

    new_product_brand = StringField(
        validators=[
            Optional(),
            Length(max=160),
        ],
    )

    external_metadata = HiddenField(
        validators=[
            Optional(),
        ],
    )

    storage_location_id = SelectField(
        choices=[],
        coerce=int,
        validators=[
            DataRequired(),
        ],
    )

    quantity = DecimalField(
        places=6,
        validators=[
            DataRequired(),
            NumberRange(
                min=0.000001
            ),
        ],
    )

    unit_id = SelectField(
        choices=[],
        coerce=int,
        validators=[
            DataRequired(),
        ],
    )

    purchase_date = DateField(
        validators=[
            Optional(),
        ],
    )

    expiration_date = DateField(
        validators=[
            Optional(),
        ],
    )

    note = TextAreaField(
        validators=[
            Optional(),
            Length(max=2000),
        ],
    )

    submit = SubmitField()

class ProductForm(FlaskForm):
    ingredient_id = SelectField(
        choices=[],
        coerce=int,
        validators=[
            DataRequired(),
        ],
    )

    name = StringField(
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=255,
            ),
        ],
    )

    brand = StringField(
        validators=[
            Optional(),
            Length(max=160),
        ],
    )

    package_quantity = DecimalField(
        places=6,
        validators=[
            Optional(),
            NumberRange(
                min=0.000001,
            ),
        ],
    )

    package_unit_id = SelectField(
        choices=[],
        coerce=int,
        validators=[
            Optional(),
        ],
    )

    barcode = StringField(
        validators=[
            Optional(),
            Length(max=64),
        ],
    )

    barcode_type = SelectField(
        choices=[
            ("", "—"),
            ("ean13", "EAN-13"),
            ("ean8", "EAN-8"),
            ("upca", "UPC-A"),
            ("upce", "UPC-E"),
            ("code128", "CODE-128"),
            ("other", "Other"),
        ],
        validators=[
            Optional(),
        ],
    )

    images = MultipleFileField(
        validators=[
            Optional(),
            FileAllowed(
                [
                    "jpg",
                    "jpeg",
                    "png",
                    "webp",
                ],
                (
                    "JPG, PNG vagy WEBP "
                    "kép tölthető fel."
                ),
            ),
        ],
    )

    camera_image = FileField(
        validators=[
            Optional(),
            FileAllowed(
                [
                    "jpg",
                    "jpeg",
                    "png",
                    "webp",
                ],
                (
                    "JPG, PNG vagy WEBP "
                    "kép tölthető fel."
                ),
            ),
        ],
    )

    submit = SubmitField()

class BatchQuantityActionForm(FlaskForm):
    quantity = DecimalField(
        places=6,
        validators=[
            DataRequired(),
            NumberRange(
                min=0.000001,
            ),
        ],
    )

    note = TextAreaField(
        validators=[
            Optional(),
            Length(max=2000),
        ],
    )

    submit = SubmitField()


class BatchAdjustmentForm(FlaskForm):
    quantity = DecimalField(
        places=6,
        validators=[
            DataRequired(),
            NumberRange(
                min=0,
            ),
        ],
    )

    note = TextAreaField(
        validators=[
            Optional(),
            Length(max=2000),
        ],
    )

    submit = SubmitField()


class BatchTransferForm(FlaskForm):
    storage_location_id = SelectField(
        choices=[],
        coerce=int,
        validators=[
            DataRequired(),
        ],
    )

    note = TextAreaField(
        validators=[
            Optional(),
            Length(max=2000),
        ],
    )

    submit = SubmitField()

class StockRuleForm(FlaskForm):
    ingredient_id = SelectField(
        choices=[],
        coerce=int,
        validators=[
            DataRequired(),
        ],
    )

    minimum_quantity = DecimalField(
        places=6,
        validators=[
            DataRequired(),
            NumberRange(
                min=0,
            ),
        ],
    )

    unit_id = SelectField(
        choices=[],
        coerce=int,
        validators=[
            DataRequired(),
        ],
    )

    note = TextAreaField(
        validators=[
            Optional(),
            Length(max=2000),
        ],
    )

    submit = SubmitField()
