from typing import Literal

from pydantic import BaseModel, Field


class CustomerIntent(BaseModel):
    primary_intent: Literal[
        "product_exploration",
        "product_information",
        "sizing_help",
        "care_instructions",
        "return_policy",
        "shipping_information",
        "brand_information",
        "off_topic"
    ] = Field(
        description="The primary intent the customer is expressing"
    )


class ConversationStage(BaseModel):
    conversation_stage: Literal[
        "greeting",
        "discovery",
        "recommendation",
        "details",
        "closing"
    ] = Field(
        description="The current stage of the conversation"
    )
