from enum import Enum
from typing import Literal, Union

from pydantic import BaseModel, Field


class CustomerIntentEnum(str, Enum):
    SIZING_HELP = 'general_sizing_help_about_measurement_not_related_to_products_availability'
    PRICING = 'pricing'
    CARE_INSTRUCTIONS = 'care_instructions'
    RETURN_POLICY = 'return_policy'
    SHIPPING_INFORMATION = 'shipping_information'
    ORDER_PLACING = 'placing_and_order_or_making_purchase'
    BRAND_INFORMATION = 'brand_information'
    CONCERN_OR_HESITATION = 'concern_or_hesitation'
    PRODUCTS_INFO = 'wants_product_information_or_products_availability_information_or_shares_preferences'
    OFF_TOPIC = 'off_topic'


class CustomerIntent(BaseModel):
    primary_intent: CustomerIntentEnum = Field(
        default=CustomerIntentEnum.OFF_TOPIC,
        description='The primary intent the customer is expressing'
    )


class PurchaseType(BaseModel):
    purchase_type: Union[Literal['self_purchase', 'gift_purchase'], str] = Field(
        default='',
        description='Whether the jewelry is for the customer themselves or as a gift for someone else. Do not make assumptions beyond what is explicitly mentioned into the STATEMENT.'
    )


class WearerGender(BaseModel):
    gender: Union[Literal['male', 'female'], str] = Field(
        default='',
        description='Gender of the person who will wear the jewelry, determined by pronouns, relationships, names, or direct statements. Do not make assumptions beyond what is explicitly mentioned into the STATEMENT.'
    )


class CategoryType(BaseModel):
    category: Union[Literal['earrings', 'necklaces', 'pendants', 'bracelets', 'watches', 'rings'], str] = Field(
        default='',
        description='Jewelry type the customer has shown interest. Do not make assumptions beyond what is explicitly mentioned into the STATEMENT.'
    )


class MetalType(BaseModel):
    metal_type: Union[Literal['Rose Gold', 'Yellow Gold', 'Platinum'], str] = Field(
        default='',
        description='Metal type the customer has shown interest. Do not make assumptions beyond what is explicitly mentioned into the STATEMENT.'
    )


class StoneType(BaseModel):
    stone_type: Union[Literal['Pink Sapphire', 'Blue Sapphire', 'Yellow Sapphire', 'Aquamarine', 'Emerald', 'Ruby', 'White Diamond'], str] = Field(
        default='',
        description='Stone type the customer has shown interest. Do not make assumptions beyond what is explicitly mentioned into the STATEMENT.'
    )


class BudgetRange(BaseModel):
    budget_range: str = Field(
        default='',
        description='Approximate price the customer has expressed they feel comfortable with. Do not be too restrictive.'
    )
