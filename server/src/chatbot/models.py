from enum import Enum

from pydantic import BaseModel, Field

from django.db import models
from django.db.models import JSONField


class CustomerIntentEnum(str, Enum):
    SIZING_HELP = 'general_sizing_help_about_measurement_not_related_to_products_availability'
    PRICING = 'pricing'
    CARE_INSTRUCTIONS = 'care_instructions'
    RETURN_POLICY = 'return_policy'
    SHIPPING_INFORMATION = 'shipping_information'
    ORDER_PLACING = 'placing_an_order_or_making_a_purchase_or_processing_transaction'
    BRAND_INFORMATION = 'brand_information'
    CONCERN_OR_HESITATION = 'concern_or_hesitation'
    PRODUCTS_INFO = 'wants_product_information_or_products_availability_information_or_shares_preferences'
    OFF_TOPIC = 'off_topic'


class CustomerIntent(BaseModel):
    primary_intent: CustomerIntentEnum = Field(
        default=CustomerIntentEnum.OFF_TOPIC,
        description='The primary intent the customer is expressing'
    )


class PurchaseTypeEnum(str, Enum):
    SELF_PURCHASE = 'self_purchase'
    GIFT_PURCHASE = 'gift_purchase'


class PurchaseType(BaseModel):
    purchase_type: PurchaseTypeEnum = Field(
        default='',
        description='Whether the jewelry is for the customer themselves or as a gift for someone else'
    )


class WearerGenderEnum(str, Enum):
    FEMALE = 'female'
    MALE = 'male'


class WearerGender(BaseModel):
    gender: WearerGenderEnum = Field(
        default='',
        description='Gender of the person who will wear the jewelry, determined by pronouns, relationships, names, or direct statements'
    )


class CategoryTypeEnum(str, Enum):
    EARRINGS = 'earrings'
    NECKLACES = 'necklaces'
    PENDANTS = 'pendants'
    BRACELETS = 'bracelets'
    WATCHES = 'watches'
    RINGS = 'rings'


class CategoryType(BaseModel):
    category: CategoryTypeEnum = Field(
        default='',
        description='Jewelry type the customer has shown interest in'
    )


class MetalTypeEnum(str, Enum):
    ROSE_GOLD = 'Rose Gold'
    YELLOW_GOLD = 'Yellow Gold'
    PLATINUM = 'Platinum'


class MetalType(BaseModel):
    metal_type: MetalTypeEnum = Field(
        default='',
        description='Metal type the customer has shown interest in'
    )


class StoneTypeEnum(str, Enum):
    PINK_SAPPHIRE = 'Pink Sapphire'
    BLUE_SAPPHIRE = 'Blue Sapphire'
    YELLOW_SAPPHIRE = 'Yellow Sapphire'
    AQUAMARINE = 'Aquamarine'
    EMERALD = 'Emerald'
    RUBY = 'Ruby'
    WHITE_DIAMOND = 'Diamond'


class StoneType(BaseModel):
    stone_type: StoneTypeEnum = Field(
        default='',
        description='Stone type the customer has shown interest in'
    )
