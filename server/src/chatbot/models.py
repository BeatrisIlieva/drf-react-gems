from enum import Enum

from pydantic import BaseModel, Field


class CustomerIntentEnum(str, Enum):
    SIZING_HELP = 'general_sizing_help_about_measurement_not_related_to_products_availability'
    PRICING = 'pricing'
    CARE_INSTRUCTIONS = 'care_instructions'
    RETURN_POLICY = 'return_policy'
    SHIPPING_INFORMATION = 'shipping_information'
    BRAND_INFORMATION = 'brand_information'
    CONCERN_OR_HESITATION = 'concern_or_hesitation'
    PROCESSING_TRANSACTION = 'processing_transaction_or_completing_an_order'
    PRODUCTS_INFO = 'wants_product_information_or_products_availability_information_or_shares_preferences'
    OFF_TOPIC = 'off_topic'


class CustomerIntent(BaseModel):
    primary_intent: CustomerIntentEnum = Field(
        default=CustomerIntentEnum.OFF_TOPIC,
        description='The primary intent the customer is expressing'
    )


class WearerGenderEnum(str, Enum):
    FEMALE = 'female'
    MALE = 'male'
    UNKNOWN = 'unknown'


class WearerGender(BaseModel):
    gender: WearerGenderEnum = Field(
        default=WearerGenderEnum.UNKNOWN,
        description='Gender of the intended wearer of the jewelry, not necessarily the purchaser. Determined from pronouns, relationships, names, or direct statements in the conversation.'
    )


class CategoryTypeEnum(str, Enum):
    EARRINGS = 'earrings'
    NECKLACES = 'necklaces'
    PENDANTS = 'pendants'
    BRACELETS = 'bracelets'
    WATCHES = 'watches'
    RINGS = 'rings'
    UNKNOWN = 'unknown'


class CategoryType(BaseModel):
    category: CategoryTypeEnum = Field(
        default=CategoryTypeEnum.UNKNOWN,
        description='The jewelry type the customer is currently focused on. If the customer shifts from one type to another, update to reflect their current interest. IMPORTANT: Reset to unknown if customer starts a new search for a different person or separate product request.'
    )


class MetalTypeEnum(str, Enum):
    ROSE_GOLD = 'Rose Gold'
    YELLOW_GOLD = 'Yellow Gold'
    PLATINUM = 'Platinum'
    UNKNOWN = 'unknown'


class MetalType(BaseModel):
    metal_type: MetalTypeEnum = Field(
        default=MetalTypeEnum.UNKNOWN,
        description='The metal type the customer is currently focused on. If the customer shifts from one type to another, update to reflect their current interest. IMPORTANT: Reset to unknown if customer starts a new search for a different person or separate product request.'
    )


class StoneTypeEnum(str, Enum):
    PINK_SAPPHIRE = 'Pink Sapphire'
    BLUE_SAPPHIRE = 'Blue Sapphire'
    AQUAMARINE = 'Aquamarine'
    EMERALD = 'Emerald'
    RUBY = 'Ruby'
    WHITE_DIAMOND = 'Diamond'
    UNKNOWN = 'unknown'


class StoneType(BaseModel):
    stone_type: StoneTypeEnum = Field(
        default=StoneTypeEnum.UNKNOWN,
        description='The stone type the customer is currently focused on. If the customer shifts from one type to another, update to reflect their current interest. IMPORTANT: Reset to unknown if customer starts a new search for a different person or separate product request.'
    )
