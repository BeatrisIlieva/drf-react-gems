from typing import Literal, Optional
from enum import Enum
from pydantic import BaseModel, Field


class CustomerIntentEnum(str, Enum):
    WANTS_PRODUCT_INFORMATION_OR_SHARES_PREFERENCES = 'wants_product_information_or_shares_preferences'
    IS_INTERESTED_IN_RECOMMENDED_PRODUCT = 'is_interested_in_recommended_product'
    IS_INTERESTED_IN_RECEIVING_HELP_IN_SELECTING_IDEAL_SIZE_FOR_SELF_PURCHASE = 'is_interested_in_receiving_help_in_selecting_ideal_size_for_self_purchase'
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


class ProductPreferences(BaseModel):
    """Enhanced preference model for luxury jewelry consultation."""

    # Primary Discovery Phase
    occasion: Optional[str] = Field(
        default=None,
        description='The occasion or life moment for which the customer needs the jewelry (e.g., anniversary, achievement, birthday, engagement)'
    )

    purchase_type: Optional[Literal['self_purchase', 'gift_purchase']] = Field(
        default=None,
        description='Whether the jewelry is for the customer themselves or as a gift for someone else'
    )

    # Secondary Discovery Phase
    gender: Optional[Literal['male', 'female']] = Field(
        default=None,
        description='Gender of the person who will wear the jewelry, determined from the CUSTOMER STATEMENT such as pronouns, relationships, names, or direct statements'
    )

    # Style Discovery Phase
    category: Optional[str] = Field(
        default=None,
        description='Jewelry type (e.g. brooches) the customer has shown interest in through any means - direct requests, positive responses to assistant suggestions, questions about jewelry type, or any indication of preference for a specific jewelry type'
    )

    # Material Discovery Phase
    metal_type: Optional[str] = Field(
        default=None,
        description='Metal type (e.g. silver) the customer has shown interest in through any means - direct requests, positive responses to assistant suggestions, questions about metal types, or any indication of preference for a specific metal type'
    )

    stone_type: Optional[str] = Field(
        default=None,
        description='Stone type (e.g. diamond) type the customer has shown interest in through any means - direct requests, positive responses to assistant suggestions, questions about gemstone types, or any indication of preference for a specific gemstone type'
    )

    # Budget Discovery Phase (for online, this is more delicate)
    budget_range: Optional[float] = Field(
        default=None,
        description='Price sensitivity level'
    )
