from typing import Literal, Optional, Dict
from enum import Enum

from pydantic import BaseModel, Field


from enum import Enum


class CustomerIntentEnum(str, Enum):
    WANTS_PRODUCT_INFORMATION = 'wants_product_information'
    WANTS_DETAILS_ABOUT_RECOMMENDED_PRODUCT = 'wants_details_about_recommended_product'
    IS_INTERESTED_IN_RECOMMENDED_PRODUCT_AFTER_RECEIVING_DETAILS = 'is_interested_in_recommended_product_after_receiving_details'
    IS_INTERESTED_IN_RECEIVING_HELP_IN_SELECTING_IDEAL_SIZE_FOR_SELF_PURCHASE = 'interested_in_receiving_help_in_selecting_ideal_size_for_self_purchase'
    SIZING_HELP = 'sizing_help'
    CARE_INSTRUCTIONS = 'care_instructions'
    RETURN_POLICY = 'return_policy'
    SHIPPING_INFORMATION = 'shipping_information'
    BRAND_INFORMATION = 'brand_information'
    ISSUE_OR_CONCERN_OR_HESITATION = 'issue_or_concern_or_hesitation'
    OFF_TOPIC = 'off_topic'


class CustomerIntent(BaseModel):
    primary_intent: CustomerIntentEnum = Field(
        description='The primary intent the customer is expressing'
    )


class GenderClassification(BaseModel):
    gender: Literal['male', 'female'] = Field(
        description='Gender of the person who will wear the jewelry, determined from conversational context such as pronouns, relationships, names, or direct statements'
    )


class PurchaseClassification(BaseModel):
    purchase_type: Literal['self_purchase', 'gift_purchase'] = Field(
        description='Whether the jewelry is for the customer themselves or as a gift for someone else'
    )
    recipient_relationship: Optional[str] = Field(
        default=None,
        description='Required when purchase_type is `gift_purchase` - relationship between customer and gift recipient'
    )


class CategoryClassification(BaseModel):
    category: str = Field(
        description='Jewelry type (e.g. brooches) the customer has shown interest in through any means - direct requests, positive responses to assistant suggestions, questions about jewelry type, or any indication of preference for a specific jewelry type'
    )


class MetalClassification(BaseModel):
    metal_type: str = Field(
        description='Metal type (e.g. silver) the customer has shown interest in through any means - direct requests, positive responses to assistant suggestions, questions about metal types, or any indication of preference for a specific metal type'
    )


class StoneClassification(BaseModel):
    stone_type: str = Field(
        description='Stone type (e.g. diamond) type the customer has shown interest in through any means - direct requests, positive responses to assistant suggestions, questions about gemstone types, or any indication of preference for a specific gemstone type'
    )


class ColorClassification(BaseModel):
    color: str = Field(
        description='Color (e.g. purple) the customer has shown interest in through any means - direct requests, positive responses to assistant suggestions, questions about color, or any indication of preference for a specific color'
    )


class OccasionClassification(BaseModel):
    occasion: str = Field(
        description='The occasion for which the customer needs the jewelry.'
    )


class FilteredProduct(BaseModel):
    collection: str
    stone: str
    metal: str
    category: str
    product_id: str
    image_url: str
    sizes: Dict[str, str]
    description: str
    target_gender: str
    average_rating: str
