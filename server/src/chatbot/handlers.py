import json
from typing import Optional, Tuple

from src.chatbot.models import (
    CategoryClassification,
    ColorClassification,
    FilteredProduct,
    GenderClassification,
    MetalClassification,
    PurchaseClassification,
    StoneClassification
)

from src.chatbot.prompts.customer_intent import (
    HUMAN_MESSAGE,
    BUILD_ANSWER_TO_RECOMMEND_PRODUCT_SYSTEM_MESSAGE,
    BUILD_DISCOVERY_QUESTION_TO_ASK_SYSTEM_MESSAGE
)
from src.chatbot.prompts.helper_calls import (
    BUILD_CONVERSATION_SUMMARY_HUMAN_MESSAGE,
    BUILD_CONVERSATION_SUMMARY_SYSTEM_MESSAGE,
    BUILD_DISCOVERY_QUESTION_HUMAN_MESSAGE,
    BUILD_DISCOVERY_QUESTION_SYSTEM_MESSAGE,
    BUILD_OPTIMIZED_SEARCH_QUERY_HUMAN_MESSAGE,
    BUILD_OPTIMIZED_SEARCH_QUERY_SYSTEM_MESSAGE,
    EXTRACT_CUSTOMER_PREFERENCE_HUMAN_MESSAGE,
    EXTRACT_CUSTOMER_PREFERENCE_SYSTEM_MESSAGE,
    EXTRACT_FILTERED_PRODUCTS_HUMAN_MESSAGE,
    EXTRACT_FILTERED_PRODUCTS_SYSTEM_MESSAGE
)
from src.chatbot.utils import generate_formatted_response


def build_conversation_history(customer_query, conversation_state, max_messages=20):
    """
    Build conversation history with the last max_messages customer-AI message pairs.

    Args:
        conversation_state: Dictionary containing the conversation state with messages.
        customer_query: The current customer query to append.
        max_messages: Maximum number of previous message pairs to include (default: 3).

    Returns:
        List of strings representing the conversation history.

    Raises:
        ValueError: If the number of customer and AI messages is not equal.
    """
    if not conversation_state:
        return [f'{1}. customer: {customer_query};']

    conversation_history = []
    messages = conversation_state['channel_values']['messages']

    # Extract customer and assistant messages
    customer_messages = [msg.content.split('INPUT:')[-1].strip()
                         for msg in messages if msg.__class__.__name__ == 'HumanMessage']
    assistant_messages = [msg.content.strip()
                          for msg in messages if msg.__class__.__name__ == 'AIMessage']

    # Validate that customer and assistant messages are paired (equal counts)
    if len(customer_messages) != len(assistant_messages):
        raise ValueError(
            f"Mismatched message counts: {len(customer_messages)} customer messages, "
            f"{len(assistant_messages)} assistant messages. Expected equal counts."
        )

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


def build_conversation_summary(llm, conversation_history):
    return generate_formatted_response(
        llm,
        BUILD_CONVERSATION_SUMMARY_SYSTEM_MESSAGE,
        BUILD_CONVERSATION_SUMMARY_HUMAN_MESSAGE,
        'extract_ai_response_content',
        conversation_history=conversation_history,
    )


def build_optimized_query(llm, conversation_summary):
    return generate_formatted_response(
        llm,
        BUILD_OPTIMIZED_SEARCH_QUERY_SYSTEM_MESSAGE,
        BUILD_OPTIMIZED_SEARCH_QUERY_HUMAN_MESSAGE,
        'extract_ai_response_content',
        conversation_summary=conversation_summary,
    )


def extract_customer_preferences(
    llm,
    optimized_query: str,
) -> Tuple[Optional[str], bool]:
    """Extract customer preferences and check if ready for recommendations."""

    # Define classifications to extract
    classifications = [
        (GenderClassification, 'gender'),
        (ColorClassification, 'color'),
        (CategoryClassification, 'category'),
        (StoneClassification, 'stone_type'),
        (MetalClassification, 'metal_type'),
        (PurchaseClassification, 'purchase_type')
    ]

    # Extract all values
    extracted = {}
    for classification_class, key in classifications:
        result = json.loads(
            generate_formatted_response(
                llm,
                EXTRACT_CUSTOMER_PREFERENCE_SYSTEM_MESSAGE,
                EXTRACT_CUSTOMER_PREFERENCE_HUMAN_MESSAGE,
                'extract_and_strip_ai_response_content',
                classification_class,
                optimized_query=optimized_query,
            )
        )
        extracted[key] = result[key]

        # Also get recipient_relationship from purchase classification
        if classification_class == PurchaseClassification:
            extracted['recipient_relationship'] = result.get(
                'recipient_relationship')

    # Check if all required fields are present
    required_fields = [key for _, key in classifications]
    if extracted['purchase_type'] == 'gift_purchase':
        required_fields.append('recipient_relationship')

    ready_to_transition = all(
        extracted[field] for field in required_fields
    )

    # Build preferences string
    preferences_items = [
        f"{field}: {extracted[field]}" for field in required_fields]
    customer_preferences = '\n'.join(preferences_items)

    return customer_preferences, ready_to_transition


def build_discovery_question(llm, conversation_summary, customer_preferences):
    return generate_formatted_response(
        llm,
        BUILD_DISCOVERY_QUESTION_SYSTEM_MESSAGE,
        BUILD_DISCOVERY_QUESTION_HUMAN_MESSAGE,
        'extract_ai_response_content',
        conversation_summary=conversation_summary,
        customer_preferences=customer_preferences,
    )


def build_discovery_question_to_ask(llm, discovery_question, customer_query):
    return generate_formatted_response(
        llm,
        BUILD_DISCOVERY_QUESTION_TO_ASK_SYSTEM_MESSAGE,
        HUMAN_MESSAGE,
        'destructure_messages',
        discovery_question=discovery_question,
        input=customer_query,
    )


def extract_filtered_products(llm, conversation_summary, customer_preferences, products):
    return generate_formatted_response(
        llm,
        EXTRACT_FILTERED_PRODUCTS_SYSTEM_MESSAGE,
        EXTRACT_FILTERED_PRODUCTS_HUMAN_MESSAGE,
        'extract_and_strip_ai_response_content',
        response_model=FilteredProduct,
        conversation_summary=conversation_summary,
        customer_preferences=customer_preferences,
        products=products,
    )


def build_answer_to_recommend_product(llm, filtered_product, customer_query):
    return generate_formatted_response(
        llm,
        BUILD_ANSWER_TO_RECOMMEND_PRODUCT_SYSTEM_MESSAGE,
        HUMAN_MESSAGE,
        'destructure_messages',
        product_to_recommend=filtered_product,
        input=customer_query,
    )
