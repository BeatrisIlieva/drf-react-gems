from typing import Literal, Optional

from pydantic import BaseModel, Field


class CustomerIntent(BaseModel):
    primary_intent: Literal[
        "discovery",
        "recommendation",
        "details",
        "closing",
        "sizing_help",
        "care_instructions",
        "return_policy",
        "shipping_information",
        "brand_information",
        "issue_or_concern_or_hesitation",
        "off_topic"
    ] = Field(
        description="The primary intent the customer is expressing"
    )


class GenderClassification(BaseModel):
    gender: Literal["male", "female"] = Field(
        description="Gender of the person who will wear the jewelry, determined from conversational context such as pronouns, relationships, names, or direct statements"
    )


class PurchaseClassification(BaseModel):
    purchase_type: Literal["self_purchase", "gift_purchase"] = Field(
        description="Whether the jewelry is for the customer themselves or as a gift for someone else"
    )
    recipient_relationship: Optional[str] = Field(
        default=None,
        description="Required when purchase_type is 'gift_purchase' - relationship between customer and gift recipient"
    )


class CategoryClassification(BaseModel):
    category: str = Field(
        description="Jewelry type (e.g. brooches) the customer has shown interest in through any means - direct requests, positive responses to assistant suggestions, questions about jewelry type, or any indication of preference for a specific jewelry type"
    )


class MetalClassification(BaseModel):
    metal_type: str = Field(
        description="Metal type (e.g. silver) the customer has shown interest in through any means - direct requests, positive responses to assistant suggestions, questions about metal types, or any indication of preference for a specific metal type"
    )


class StoneClassification(BaseModel):
    stone_type: str = Field(
        description="Stone type (e.g. diamond) type the customer has shown interest in through any means - direct requests, positive responses to assistant suggestions, questions about gemstone types, or any indication of preference for a specific gemstone type"
    )


class ColorClassification(BaseModel):
    color: str = Field(
        description="Color (e.g. purple) the customer has shown interest in through any means - direct requests, positive responses to assistant suggestions, questions about color, or any indication of preference for a specific color"
    )


class ConversationStage(BaseModel):
    conversation_stage: Literal[
        "discovery",
        "recommendation",
        "details",
        "closing",
    ] = Field(
        description="The current stage of the conversation"
    )

    extracted_info: dict = Field(
        description="gender, purchase_type, product_characteristics")
