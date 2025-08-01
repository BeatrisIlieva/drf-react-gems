from django.apps import apps


from src.products.models.base import BaseProduct


def get_valid_categories():
    """
    Dynamically get all models that inherit from BaseProduct
    """
    valid_categories = []

    for model in apps.get_app_config('products').get_models():
        if (
            hasattr(model, '_meta')
            and model._meta.abstract is False
            and issubclass(model, BaseProduct)
            and model != BaseProduct
        ):
            valid_categories.append(model._meta.model_name)

    return valid_categories
