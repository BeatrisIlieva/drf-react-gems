from src.products.models.relationships import FirstImage, SecondImage

models_mapper = {
    'first_image': FirstImage,
    'second_image': SecondImage
}


def create_media(image_url, model_to_be_used):
    model = models_mapper[model_to_be_used]

    media = model.objects.create(
        image_url=image_url
    )

    return media
