from djangoTSGems.products.models.abstract import FixedSizeProduct, FlexibleSizeProduct


class DropEarring(FixedSizeProduct):
    pass


class StudEarring(FixedSizeProduct):
    pass


class Charm(FixedSizeProduct):
    pass


class Necklace(FlexibleSizeProduct):
    SIZE_CHOICES = (
        ("S", "40.64"),
        ("M", "43.18"),
        ("L", "45.72"),
    )


class Pendant(FlexibleSizeProduct):
    SIZE_CHOICES = (
        ("S", "43.64"),
        ("M", "45.18"),
        ("L", "47.72"),
    )


class Bracelet(FlexibleSizeProduct):
    SIZE_CHOICES = (
        ("S", "15.2"),
        ("M", "17.8"),
        ("L", "19.3"),
    )


class Ring(FlexibleSizeProduct):
    SIZE_CHOICES = (
        ("S", "4.05"),
        ("M", "4.98"),
        ("L", "5.86"),
    )
