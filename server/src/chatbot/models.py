from enum import Enum
from typing import Literal, Union

from pydantic import BaseModel, Field


class CustomerIntentEnum(str, Enum):
    PRODUCTS_INFO = 'wants_product_information_or_products_availability_information_or_shares_preferences'
    SIZING_HELP = 'general_sizing_help_about_measurement_not_related_to_products_availability'
    PRICING = 'pricing'
    CARE_INSTRUCTIONS = 'care_instructions'
    RETURN_POLICY = 'return_policy'
    SHIPPING_INFORMATION = 'shipping_information'
    BRAND_INFORMATION = 'brand_information'
    CONCERN_OR_HESITATION = 'concern_or_hesitation'
    OFF_TOPIC = 'off_topic'


class CustomerIntent(BaseModel):
    primary_intent: CustomerIntentEnum = Field(
        default=CustomerIntentEnum.OFF_TOPIC,
        description='The primary intent the customer is expressing'
    )


class PurchaseType(BaseModel):
    purchase_type: Union[Literal['self_purchase', 'gift_purchase'], str] = Field(
        default='',
        description='Whether the jewelry is for the customer themselves or as a gift for someone else'
    )


class WearerGender(BaseModel):
    gender: Union[Literal['male', 'female'], str] = Field(
        default='',
        description='Gender of the person who will wear the jewelry, determined from the CONVERSATION HISTORY such as pronouns, relationships, names, or direct statements'
    )


class CategoryType(BaseModel):
    category: Union[Literal['earrings', 'necklaces', 'pendants', 'bracelets', 'watches', 'rings'], str] = Field(
        default='',
        description='Jewelry type the customer has shown interest in through any means - direct requests, positive responses to assistant suggestions, questions about jewelry type, or any indication of preference for a specific jewelry type'
    )


class MetalType(BaseModel):
    metal_type: Union[Literal['Rose Gold', 'Yellow Gold', 'Platinum'], str] = Field(
        default='',
        description='Metal type the customer has shown interest in through any means - direct requests, positive responses to assistant suggestions, questions about metal types, or any indication of preference for a specific metal type'
    )


class StoneType(BaseModel):
    stone_type: Union[Literal['Pink Sapphire', 'Blue Sapphire', 'Yellow Sapphire', 'Aquamarine', 'Green Emerald', 'Red Ruby', 'White Diamond'], str] = Field(
        default='',
        description='Stone type type the customer has shown interest in through any means - direct requests, positive responses to assistant suggestions, questions about gemstone types, or any indication of preference for a specific gemstone type. Keep in mind that if the customer expressed preference for green color, this should be matched with Emerald; for red color this should be matched to Ruby.'
    )


class BudgetRange(BaseModel):
    budget_range: str = Field(
        default='',
        description='Price sensitivity level'
    )
