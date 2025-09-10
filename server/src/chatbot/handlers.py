import json
from typing import Optional, Tuple

from src.chatbot.models import (
    CategoryClassification,
    ColorClassification,
    CustomerIntent,
    FilteredProduct,
    GenderClassification,
    MetalClassification,
    OccasionClassification,
    PurchaseClassification,
    StoneClassification
)

from src.chatbot.prompts.customer_intent import (
    ANSWER_TO_PROVIDE_CUSTOMER_SUPPORT_SYSTEM_MESSAGE,
    ANSWER_TO_PROVIDE_DETAILS_ABOUT_RECOMMENDED_PRODUCT_SYSTEM_MESSAGE,
    OBJECTION_HANDLING_SYSTEM_MESSAGE,
    OFF_TOPIC_SYSTEM_MESSAGE,
    PLAIN_HUMAN_MESSAGE,
    ANSWER_TO_RECOMMEND_PRODUCT_SYSTEM_MESSAGE,
    DISCOVERY_QUESTION_TO_ASK_SYSTEM_MESSAGE,
    WITH_MEMORY_AND_DB_CONTENT_HUMAN_MESSAGE,
    WITH_MEMORY_HUMAN_MESSAGE
)
from src.chatbot.prompts.helper_calls import (
    ANALYZE_CONVERSATION_INSIGHTS_HUMAN_MESSAGE,
    ANALYZE_CONVERSATION_INSIGHTS_SYSTEM_MESSAGE,
    DISCOVERY_QUESTION_HUMAN_MESSAGE,
    DISCOVERY_QUESTION_SYSTEM_MESSAGE,
    CUSTOMER_INTENT_HUMAN_MESSAGE,
    CUSTOMER_INTENT_SYSTEM_MESSAGE,
    CUSTOMER_PREFERENCE_HUMAN_MESSAGE,
    CUSTOMER_PREFERENCE_SYSTEM_MESSAGE,
    FILTERED_PRODUCTS_HUMAN_MESSAGE,
    FILTERED_PRODUCTS_SYSTEM_MESSAGE
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
    customer_messages = [msg.content.split('QUERY:')[-1].strip()
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


def analyze_conversation_insights(llm, conversation_history):
    return generate_formatted_response(
        llm,
        ANALYZE_CONVERSATION_INSIGHTS_SYSTEM_MESSAGE,
        ANALYZE_CONVERSATION_INSIGHTS_HUMAN_MESSAGE,
        'extract_ai_response_content',
        conversation_history=conversation_history,
    )


def extract_customer_preferences(
    llm,
    conversation_insights: str,
) -> Tuple[Optional[str], bool]:
    """Extract customer preferences and check if ready for recommendations."""

    # Define classifications to extract
    classifications = [
        (GenderClassification, 'gender'),
        (ColorClassification, 'color'),
        (CategoryClassification, 'category'),
        (StoneClassification, 'stone_type'),
        (MetalClassification, 'metal_type'),
        (PurchaseClassification, 'purchase_type'),
        (OccasionClassification, 'occasion')
    ]

    # Extract all values
    extracted = {}
    for classification_class, key in classifications:
        result = json.loads(
            generate_formatted_response(
                llm,
                CUSTOMER_PREFERENCE_SYSTEM_MESSAGE,
                CUSTOMER_PREFERENCE_HUMAN_MESSAGE,
                'extract_and_strip_ai_response_content',
                classification_class,
                conversation_insights=conversation_insights,
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


def build_discovery_question(llm, conversation_insights, customer_preferences):
    return generate_formatted_response(
        llm,
        DISCOVERY_QUESTION_SYSTEM_MESSAGE,
        DISCOVERY_QUESTION_HUMAN_MESSAGE,
        'extract_ai_response_content',
        conversation_insights=conversation_insights,
        customer_preferences=customer_preferences,
    )


def build_discovery_question_to_ask(llm, discovery_question, customer_query):
    return generate_formatted_response(
        llm,
        DISCOVERY_QUESTION_TO_ASK_SYSTEM_MESSAGE,
        PLAIN_HUMAN_MESSAGE,
        'destructure_messages',
        discovery_question=discovery_question,
        customer_query=customer_query,
    )


def extract_filtered_products(llm, customer_preferences, products):
    return generate_formatted_response(
        llm,
        FILTERED_PRODUCTS_SYSTEM_MESSAGE,
        FILTERED_PRODUCTS_HUMAN_MESSAGE,
        'extract_and_strip_ai_response_content',
        response_model=FilteredProduct,
        customer_preferences=customer_preferences,
        products=products,
    )


def build_answer_to_recommend_product(llm, filtered_product, conversation_memory, customer_query):
    return generate_formatted_response(
        llm,
        ANSWER_TO_RECOMMEND_PRODUCT_SYSTEM_MESSAGE,
        WITH_MEMORY_HUMAN_MESSAGE,
        'destructure_messages',
        product_to_recommend=filtered_product,
        customer_query=customer_query,
        conversation_memory=conversation_memory
    )


def extract_customer_intent(llm, conversation_insights):
    return generate_formatted_response(
        llm,
        CUSTOMER_INTENT_SYSTEM_MESSAGE,
        CUSTOMER_INTENT_HUMAN_MESSAGE,
        'extract_and_strip_ai_response_content',
        response_model=CustomerIntent,
        conversation_insights=conversation_insights,
    )


def build_answer_to_provide_details_about_recommended_product(llm, conversation_memory, customer_query):
    return generate_formatted_response(
        llm,
        ANSWER_TO_PROVIDE_DETAILS_ABOUT_RECOMMENDED_PRODUCT_SYSTEM_MESSAGE,
        WITH_MEMORY_HUMAN_MESSAGE,
        'destructure_messages',
        conversation_memory=conversation_memory,
        customer_query=customer_query,
    )


def build_answer_to_provide_customer_support(llm, conversation_memory, customer_query, content):
    return generate_formatted_response(
        llm,
        ANSWER_TO_PROVIDE_CUSTOMER_SUPPORT_SYSTEM_MESSAGE,
        WITH_MEMORY_AND_DB_CONTENT_HUMAN_MESSAGE,
        'destructure_messages',
        conversation_memory=conversation_memory,
        customer_query=customer_query,
        content=content,
    )


def build_objection_handling_answer(llm, conversation_memory, customer_query, content):
    return generate_formatted_response(
        llm,
        OBJECTION_HANDLING_SYSTEM_MESSAGE,
        WITH_MEMORY_AND_DB_CONTENT_HUMAN_MESSAGE,
        'destructure_messages',
        conversation_memory=conversation_memory,
        customer_query=customer_query,
        content=content,
    )


def build_off_topic_answer(llm, conversation_memory, customer_query):
    return generate_formatted_response(
        llm,
        OFF_TOPIC_SYSTEM_MESSAGE,
        WITH_MEMORY_HUMAN_MESSAGE,
        'destructure_messages',
        conversation_memory=conversation_memory,
        customer_query=customer_query,
    )
