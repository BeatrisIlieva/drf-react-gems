import json
from typing import Optional, Tuple

from src.chatbot.models import (
    ProductPreferences
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


# def extract_customer_preferences(
#     llm,
#     conversation_insights: str,
# ) -> Tuple[Optional[str], bool]:
#     """Extract customer preferences and check if ready for recommendations."""

#     # Extract all values

#     result = generate_formatted_response(
#         llm,
#         CUSTOMER_PREFERENCE_SYSTEM_MESSAGE,
#         CUSTOMER_PREFERENCE_HUMAN_MESSAGE,
#         'extract_and_strip_ai_response_content',
#         ProductPreferences,
#         conversation_insights=conversation_insights,
#     )

#     extracted = []
#     ready_to_transition = True

#     for key, value in result.items():
#         if value == '':
#             ready_to_transition = False

#         extracted.append(f'{key}: {value}')

#     customer_preferences = '\n'.join(
#         extracted
#     )

#     return customer_preferences, ready_to_transition
