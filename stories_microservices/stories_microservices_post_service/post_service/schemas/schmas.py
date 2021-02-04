from post_service.config.extentions import ma
from flask_marshmallow.fields import AbsoluteURLFor
from marshmallow import validates, ValidationError, fields

from post_service.models import Recipe, Category

# class TagSchema(ma.Schema):
#     id = ma.INT(required=True)


class RecipeSchema(ma.SQLAlchemyAutoSchema):
    image = AbsoluteURLFor(
        'api.uploaded_file',
        filename='<image>'
    )
    owner_full_name = fields.Method('get_owner_name', dump_only=True)

    class Meta:
        model = Recipe
        include_fk = True
        load_instance = True

    def get_owner_name(self, recipe):
        return recipe.users.get_full_name

    @validates('category_id')
    def validate_category_id(self, category_id):
        """'value' is the datetime parsed from time_created by marshmallow"""
        category = Category.query.filter_by(id=category_id).first()
        print('category', category)
        if not category:
            raise ValidationError(f'Category with "{category_id}" pk not found')

