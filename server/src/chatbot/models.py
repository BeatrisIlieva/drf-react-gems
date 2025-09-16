from typing import Literal, Optional
from enum import Enum
from pydantic import BaseModel, Field


class CustomerIntentEnum(str, Enum):
    WANTS_PRODUCT_INFORMATION_OR_PRODUCTS_AVAILABILITY_INFORMATION_OR_SHARES_PREFERENCES = 'wants_product_information_or_products_availability_information_or_shares_preferences'
    GENERAL_SIZING_HELP_ABOUT_MEASUREMENT_NOT_RELATED_TO_PRODUCTS_AVAILABILITY = 'general_sizing_help_about_measurement_not_related_to_products_availability'
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


# class ProductPreferences(BaseModel):
#     """Enhanced preference model for luxury jewelry consultation."""

#     purchase_type: Optional[Literal['self_purchase', 'gift_purchase']] = Field(
#         default='',
#         description='Whether the jewelry is for the customer themselves or as a gift for someone else'
#     )

#     # Secondary Discovery Phase
#     gender: Optional[Literal['male', 'female']] = Field(
#         default='',
#         description='Gender of the person who will wear the jewelry, determined from the CUSTOMER STATEMENT such as pronouns, relationships, names, or direct statements'
#     )

#     # Style Discovery Phase
#     category: Optional[Literal['earrings', 'necklaces', 'pendants', 'bracelets', 'watches', 'rings']] = Field(
#         default='',
#         description='Jewelry type the customer has shown interest in through any means - direct requests, positive responses to assistant suggestions, questions about jewelry type, or any indication of preference for a specific jewelry type'
#     )

#     # Material Discovery Phase
#     metal_type: Optional[Literal['Rose Gold', 'Yellow Gold', "Platinum"]] = Field(
#         default='',
#         description='Metal type the customer has shown interest in through any means - direct requests, positive responses to assistant suggestions, questions about metal types, or any indication of preference for a specific metal type'
#     )

#     stone_type: Optional[Literal['Pink Sapphire', 'Blue Sapphire', 'Yellow Sapphire', 'Aquamarine', 'Emerald', 'Ruby', 'White Diamond']] = Field(
#         default='',
#         description='Stone type type the customer has shown interest in through any means - direct requests, positive responses to assistant suggestions, questions about gemstone types, or any indication of preference for a specific gemstone type'
#     )

#     # Budget Discovery Phase (for online, this is more delicate)
#     budget_range: Optional[str] = Field(
#         default='',
#         description='Price sensitivity level'
#     )


from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Literal, Union, Any, Dict
import json

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
class ProductPreferences(BaseModel):
    """Enhanced preference model for luxury jewelry consultation."""

    # # Model validator to handle properties wrapper (equivalent to root_validator)
    # @model_validator(mode='before')
    # @classmethod
    # def handle_wrapper_formats(cls, data: Any) -> Any:
    #     """Handle different wrapper formats"""
    #     if isinstance(data, dict):
    #         # Handle properties wrapper
    #         if 'properties' in data:
    #             return data['properties']
    #         # Handle description wrapper
    #         if 'description' in data and 'properties' in data:
    #             return data['properties']
    #     return data

    # # Field validators (equivalent to validator)
    # @field_validator('purchase_type', mode='before')
    # @classmethod
    # def validate_purchase_type(cls, v: Any) -> str:
    #     return cls._clean_field_value(v)

    # @field_validator('gender', mode='before')
    # @classmethod
    # def validate_gender(cls, v: Any) -> str:
    #     return cls._clean_field_value(v)

    # @field_validator('category', mode='before')
    # @classmethod
    # def validate_category(cls, v: Any) -> str:
    #     return cls._clean_field_value(v)

    # @field_validator('metal_type', mode='before')
    # @classmethod
    # def validate_metal_type(cls, v: Any) -> str:
    #     return cls._clean_field_value(v)

    # @field_validator('stone_type', mode='before')
    # @classmethod
    # def validate_stone_type(cls, v: Any) -> str:
    #     return cls._clean_field_value(v)

    # @field_validator('budget_range', mode='before')
    # @classmethod
    # def validate_budget_range(cls, v: Any) -> str:
    #     return cls._clean_field_value(v)

    # @staticmethod
    # def _clean_field_value(v: Any) -> str:
    #     """Helper method to clean field values"""
    #     if v is None:
    #         return ''
    #     if isinstance(v, dict):
    #         # Handle enum schema format
    #         if 'enum' in v and isinstance(v['enum'], list) and v['enum']:
    #             return str(v['enum'][0])
    #         # Handle reference format
    #         if '$ref' in v:
    #             return ''
    #         # Handle type-only format
    #         return ''
    #     return str(v)

    # def model_dump(self, **kwargs) -> Dict[str, str]:
    #     """Override model_dump to ensure clean output"""
    #     result = super().model_dump(**kwargs)
    #     # Ensure all values are strings, convert None to empty string
    #     for key, value in result.items():
    #         if value is None:
    #             result[key] = ''
    #         else:
    #             result[key] = str(value)
    #     return result