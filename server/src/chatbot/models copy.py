from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Dict, List, Optional

from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langgraph.graph import StateGraph, END
import json


from typing import Literal

from enum import Enum

from enum import Enum
from typing import Dict


# class MetalType(str, Enum):
#     ROSE_GOLD = 'Rose Gold'
#     YELLOW_GOLD = 'Yellow Gold'
#     PLATINUM = "Platinum"

class MetalType(BaseModel):
    metal_type: str = Field(description="Rose Gold, Yellow Gold, Platinum")


# class Collection(str, Enum):
#     DAISY = "Daisy (Female collection),"
#     SUNFLOWER = "Sunflower (Female collection),"
#     FORGET_ME_NOT = "Forget Me Not (Female collection),"
#     GERBERA = "Gerbera (Female collection),"
#     BERRY = "Berry (Female collection),"
#     LOTUS = "Lotus (Female collection),"
#     DROP = "Drop (Female collection),"
#     LILY = "Lily (Female collection),"
#     ELEGANCE = "Elegance (Female collection),"
#     CLASSICS = "Classics (Female collection),"
#     MIDNIGHT = "Midnight (Male collection),"
#     OCEAN = "Ocean (Male collection),"

class Collection(BaseModel):
    collection: str = Field(description="Daisy (Female collection), Sunflower (Female collection), Not (Female collection), Gerbera (Female collection), Berry (Female collection), Lotus (Female collection), Drop (Female collection), Lily (Female collection), Elegance (Female collection), Classics (Female collection), Midnight (Male collection), Ocean (Male collection)")

# class Category(str, Enum):
#     """Enum for jewelry product categories"""
#     EARRINGS = "earrings,"
#     NECKLACES = "necklaces,"
#     PENDANTS = "pendants,"
#     RINGS = "rings,"
#     BRACELETS = "bracelets,"
#     WATCHES = "watches,"


class Category(BaseModel):
    category: str = Field(
        description="earrings, necklaces, pendants, rings, bracelets, watches")


# class Stone(str, Enum):
#     WHITE_DIAMOND = "White Diamond,"
#     RED_RUBY = "Red Ruby,"
#     GREEN_EMERALD = "Green Emerald,"
#     BLUE_SAPPHIRE = "Blue Sapphire,"
#     PINK_SAPPHIRE = "Pink Sapphire,"
#     YELLOW_SAPPHIRE = "Yellow Sapphire,"
#     BLUE_AQUAMARINE = "Blue Aquamarine,"


class Stone(BaseModel):
    stone: str = Field(
        description="White Diamond, Red Ruby, Green Emerald, Blue Sapphire, Pink Sapphire, Yellow Sapphire, Blue Aquamarine")

# class Gender(str, Enum):
#     F = 'Female'
#     M = 'Male'


class Gender(BaseModel):
    gender: str = Field(description="F - Female, M - Male")


class CustomerIntent(BaseModel):
    customer_intent: Literal[
        "browsing",
        "return_policy",
        "shipping",
        "sizing_help",
        "care_instructions",
        "brand_story",
        "gift_purchase",
        "self_purchase",
        "off_topic"
    ] = Field(description="The type of intent expressed by the customer")


class ConversationStage(BaseModel):
    conversation_stage: Literal[
        "greeting",
        "discovery",
        "recommendation",
        "details",
        "closing"
    ] = Field(description="The current stage of the conversation")


class Size(str, Enum):
    """Enum for jewelry size labels"""
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"

    @staticmethod
    def get_size_measurements(category: Category) -> Dict[str, str]:
        """Returns a dictionary of size labels to measurements for a given category"""
        size_measurements = {
            Category.EARRINGS: {
                Size.SMALL: "5.2mm (diameter)",
                Size.MEDIUM: "8.1mm (diameter)",
                Size.LARGE: "12.3mm (diameter)"
            },
            Category.NECKLACES: {
                Size.SMALL: "381.0mm (length)",
                Size.MEDIUM: "482.6mm (length)",
                Size.LARGE: "622.3mm (length)"
            },
            Category.PENDANTS: {
                Size.SMALL: "12.4mm (length)",
                Size.MEDIUM: "18.9mm (length)",
                Size.LARGE: "28.1mm (length)"
            },
            Category.RINGS: {
                Size.SMALL: "15.7mm (finger circumference)",
                Size.MEDIUM: "17.3mm (finger circumference)",
                Size.LARGE: "19.8mm (finger circumference)"
            },
            Category.BRACELETS: {
                Size.SMALL: "165.1mm (wrist circumference)",
                Size.MEDIUM: "187.9mm (wrist circumference)",
                Size.LARGE: "218.4mm (wrist circumference)"
            },
            Category.WATCHES: {
                Size.SMALL: "32.5mm (wrist circumference)",
                Size.MEDIUM: "38.4mm (wrist circumference)",
                Size.LARGE: "44.7mm (wrist circumference)"
            }
        }
        return size_measurements.get(category, {})

    @field_validator("size_preference")
    @classmethod
    def validate_size_preference(cls, v, values):
        """Ensure size_preference is a valid Size Enum value and matches category_interest"""
        if v is None:
            return v
        valid_sizes = [size.value for size in Size]
        if v not in valid_sizes:
            raise ValueError(
                f"size_preference must be one of {valid_sizes} or None, got {v}")
        # Check if size is valid for the category (if category is specified)
        if "category_interest" in values and values["category_interest"]:
            category = values["category_interest"]
            measurements = Size.get_size_measurements(category)
            if v not in measurements:
                raise ValueError(
                    f"size_preference '{v}' is not valid for category {category.value}")
        return v


class ProductRecommendation(BaseModel):
    """Structured product recommendation"""
    product_id: str
    collection: Collection
    category: Category
    stone: Stone
    metal: MetalType
    description: str
    price_range: str
    image_url: str
    recommendation_reason: str
    target_gender: str
    sizes_available: List[Size]

    @field_validator("sizes_available")
    @classmethod
    def validate_sizes_available(cls, v: Optional[Size], info) -> Optional[Size]:
        """Ensure sizes_available is valid for the category"""
        if v is None or "category" not in info.data or not info.data["category"]:
            return v
        category = info.data["category"]
        measurements = Size.get_size_measurements(category)
        if v.value not in measurements:
            raise ValueError(
                f"sizes_available '{v.value}' is not valid for category {category.value}")
        return v


class CustomerProfile(BaseModel):
    """Structured customer information extracted from conversation"""
    name: Optional[str] = None
    gender: Optional[Gender] = None
    occasion: Optional[str] = None
    recipient_relationship: Optional[str] = None
    budget_range: Optional[str] = None
    size_preference: Optional[Size] = None
    collection_preference: Optional[Collection] = None
    metal_preference: Optional[MetalType] = None
    stone_preference: Optional[Stone] = None
    category_interest: Optional[Category] = None

    @field_validator("size_preference")
    @classmethod
    def validate_size_preference(cls, v: Optional[Size], info) -> Optional[Size]:
        """Ensure size_preference is valid for the category_interest"""
        if v is None or "category_interest" not in info.data or not info.data["category_interest"]:
            return v
        category = info.data["category_interest"]
        measurements = Size.get_size_measurements(category)
        if v.value not in measurements:
            raise ValueError(
                f"size_preference '{v.value}' is not valid for category {category.value}")
        return v

    model_config = ConfigDict(
        # Serialize Enums as their values (e.g., Category.RINGS to "rings")
        use_enum_values=True
    )


class ConversationState(BaseModel):
    """Complete conversation state"""
    conversation_stage: ConversationStage
    current_intent: CustomerIntent
    customer_profile: CustomerProfile
    messages: List[Dict[str, str]]
    products_information: Optional[List[ProductRecommendation]] = None
    other_information: Optional[str] = None


class ProductPreferences(BaseModel):
    metal_type: Literal[
        'Rose Gold',
        'Yellow Gold',
        'Platinum'
    ] = Field(
        description="The type of metal the customer has expressed a preference for."
    )
    collection: Literal[
        'Daisy (Female collection)',
        'Sunflower (Female collection)',
        'Not (Female collection)',
        'Gerbera (Female collection)',
        'Berry (Female collection)',
        'Lotus (Female collection)',
        'Drop (Female collection)',
        'Lily (Female collection)',
        'Elegance (Female collection)',
        'Classics (Female collection)',
        'Midnight (Male collection)',
        'Ocean (Male collection)'
    ] = Field(
        description="The name of the collection the customer has expressed a preference for."
    )
    category: Literal[
        'earrings',
        'necklaces',
        'pendants',
        'rings',
        'bracelets',
        'watches'
    ] = Field(
        description="The type of category the customer has expressed a preference for."
    )
    stone: Literal[
        'White Diamond',
        'Red Ruby',
        'Green Emerald',
        'Blue Sapphire',
        'Pink Sapphire',
        'Yellow Sapphire',
        'Blue Aquamarine'
    ] = Field(
        description="The type of gemstone the customer has expressed a preference for."
    )
    gender: Literal[
        'F - Female',
        'M - Male'
    ] = Field(
        description="The customer gender, or the recipient gender if the product is for a gift, that the customer has expressed a preference for."
    )
    price: Literal['$1,500 - $21,700'] = Field(
        description="The price range the customer has expressed they are looking for. Our product prices varies between $1,500 - $21,700")
    size: Literal[
        'EARRINGS Size SMALL: 5.2mm (diameter)',
        'EARRINGS Size MEDIUM: 8.1mm (diameter)',
        'EARRINGS Size LARGE: 12.3mm (diameter)',
        'NECKLACES Size SMALL: 381.0mm (length)',
        'NECKLACES Size MEDIUM: 482.6mm (length)',
        'NECKLACES Size LARGE: 622.3mm (length)',
        'PENDANTS Size SMALL: 12.4mm (length)',
        'PENDANTS Size MEDIUM: 18.9mm (length)',
        'PENDANTS Size LARGE: 28.1mm (length)',
        'RINGS Size SMALL: 15.7mm (finger circumference)',
        'RINGS Size MEDIUM: 17.3mm (finger circumference)',
        'RINGS Size LARGE: 19.8mm (finger circumference)',
        'BRACELETS Size SMALL: 165.1mm (wrist circumference)',
        'BRACELETS Size MEDIUM: 187.9mm (wrist circumference)',
        'BRACELETS Size LARGE: 218.4mm (wrist circumference)',
        'WATCHES Size SMALL: 32.5mm (wrist circumference)',
        'WATCHES Size MEDIUM: 38.4mm (wrist circumference)',
        'WATCHES Size LARGE: 44.7mm (wrist circumference)',
    ] = Field(
        description="The size the customer has expressed a preference for."
    )


class CustomerProfile(BaseModel):
    """Structured customer information extracted from conversation"""
    name: Optional[str] = None
    age: Optional[str] = None
    profession: Optional[str] = None
    occasion: Optional[str] = None
    recipient_relationship: Optional[str] = None
