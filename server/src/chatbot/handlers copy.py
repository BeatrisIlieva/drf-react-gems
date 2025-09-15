import json
from typing import Optional, Tuple

from src.chatbot.models import (
    CategoryClassification,
    ColorClassification,
    GenderClassification,
    MetalClassification,
    OccasionClassification,
    PurchaseClassification,
    StoneClassification
)


from src.chatbot.prompts.helper_calls import (
    CUSTOMER_PREFERENCE_HUMAN_MESSAGE,
    CUSTOMER_PREFERENCE_SYSTEM_MESSAGE,
)
from src.chatbot.utils import generate_formatted_response


def build_conversation_history(customer_query, conversation_state, max_messages=20):
    """
    Build conversation history with the last max_messages customer-AI message pairs.
    """
    if not conversation_state:
        return [f'{1}. customer: {customer_query};']

    conversation_history = []
    messages = conversation_state['channel_values']['messages']

    # Extract customer and assistant messages
    customer_messages = [
        msg.content.split('STATEMENT:')[-1].strip()
        for msg in messages if msg.__class__.__name__ == 'HumanMessage'
    ]
    assistant_messages = [
        msg.content.strip()
        for msg in messages if msg.__class__.__name__ == 'AIMessage'
    ]

    # Take the last max_messages pairs (or fewer if not enough pairs)
    num_pairs = len(customer_messages)
    start_index = max(0, num_pairs - max_messages)

    # Build history with the most recent message pairs
    for i in range(start_index, num_pairs):
        conversation_history.append(
            f'{i + 1}. customer: {customer_messages[i]}, assistant: {assistant_messages[i]};')

    # Append the current customer query
    conversation_history.append(
        f'{num_pairs + 1}. customer: {customer_query};')

    return '\n'.join(conversation_history)


def extract_customer_preferences(
    llm,
    conversation_insights: str,
) -> Tuple[Optional[str], bool]:
    """Extract customer preferences and check if ready for recommendations."""

    # Define classifications to extract
    classifications = [
        (
            GenderClassification,
            'gender'
        ),
        (
            ColorClassification,
            'color'
        ),
        (
            CategoryClassification,
            'category'
        ),
        (
            StoneClassification,
            'stone_type'
        ),
        (
            MetalClassification,
            'metal_type'
        ),
        (
            PurchaseClassification,
            'purchase_type'
        ),
        (
            OccasionClassification,
            'occasion'
        )
    ]

    # Extract all values
    extracted = {}
    for classification_class, key in classifications:
        result = generate_formatted_response(
            llm,
            CUSTOMER_PREFERENCE_SYSTEM_MESSAGE,
            CUSTOMER_PREFERENCE_HUMAN_MESSAGE,
            'extract_and_strip_ai_response_content',
            classification_class,
            conversation_insights=conversation_insights,
        )

        extracted[key] = result[key]

        # Also get recipient_relationship from purchase classification
        if classification_class == PurchaseClassification:
            extracted['recipient_relationship'] = result.get(
                'recipient_relationship'
            )

    # Check if all required fields are present
    required_fields = [key for _, key in classifications]
    if extracted['purchase_type'] == 'gift_purchase':
        required_fields.append(
            'recipient_relationship'
        )

    ready_to_transition = all(
        extracted[field] for field in required_fields
    )

    # Build preferences string
    preferences_items = [
        f'{field}: {extracted[field]}' for field in required_fields]
    customer_preferences = '\n'.join(
        preferences_items
    )

    return customer_preferences, ready_to_transition
