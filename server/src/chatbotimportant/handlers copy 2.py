from src.chatbot.models import CustomerIntent, ProductPreferences
from src.chatbot.prompts.company_information_handler import HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER, SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER
from src.chatbot.prompts.customer_intent_determiner import HUMAN_MESSAGE_INTENT_DETERMINER, SYSTEM_MESSAGE_INTENT_DETERMINER
from src.chatbot.prompts.inventory_validator import HUMAN_MESSAGE_INVENTORY_VALIDATOR, SYSTEM_MESSAGE_INVENTORY_VALIDATOR
from src.chatbot.prompts.investigator import HUMAN_MESSAGE_INVESTIGATOR, SYSTEM_MESSAGE_INVESTIGATOR
from src.chatbot.prompts.objection_handler import HUMAN_MESSAGE_OBJECTION_HANDLER, SYSTEM_MESSAGE_OBJECTION_HANDLER
from src.chatbot.prompts.preferences_builder import HUMAN_MESSAGE_CUSTOMER_PREFERENCES_BUILDER, SYSTEM_MESSAGE_CUSTOMER_PREFERENCES_BUILDER
from src.chatbot.prompts.query_for_search_optimizer import HUMAN_MESSAGE_QUERY_OPTIMIZER, SYSTEM_MESSAGE_QUERY_OPTIMIZER
from src.chatbot.prompts.recommender import HUMAN_MESSAGE_RECOMMENDER, SYSTEM_MESSAGE_RECOMMENDER
from src.chatbot.prompts.sizing_help_handler import HUMAN_MESSAGE_COMPANY_SIZE_HELP_HANDLER, SYSTEM_MESSAGE_COMPANY_SIZE_HELP_HANDLER
from src.chatbot.utils import generate_formatted_response


def should_recommend_product_or_continue_investigate(llm, **kwargs):
    """Decision logic that returns the appropriate handler function"""
    
    purchase_type = kwargs['purchase_type']
    gender = kwargs['gender']
    category = kwargs['category']
    metal_type = kwargs['metal_type']
    stone_type = kwargs['stone_type']
    budget_range = kwargs['budget_range']

    print(purchase_type)
    print(gender)
    print(category)
    print(metal_type)
    print(stone_type)
    print(budget_range)

    if not all(x != "" for x in [purchase_type, gender, category, metal_type, stone_type, budget_range]):
        is_there_a_product_that_meets_the_customer_preferences = generate_formatted_response(
            llm,
            SYSTEM_MESSAGE_INVENTORY_VALIDATOR,
            HUMAN_MESSAGE_INVENTORY_VALIDATOR,
            'destructure_messages',
            **kwargs
        )
        
        product_that_meets_current_preferences = is_there_a_product_that_meets_the_customer_preferences == 'MATCH'
        
        if product_that_meets_current_preferences:
            return generate_formatted_response(
                llm,
                SYSTEM_MESSAGE_INVESTIGATOR,
                HUMAN_MESSAGE_INVESTIGATOR,
                'destructure_messages',
                **kwargs
            )

    return generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_RECOMMENDER,
        HUMAN_MESSAGE_RECOMMENDER,
        'destructure_messages',
        **kwargs
    )


HANDLERS_MAPPER = {
    'optimized_query': lambda llm, **kwargs: generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_QUERY_OPTIMIZER,
        HUMAN_MESSAGE_QUERY_OPTIMIZER,
        'extract_ai_response_content',
        **kwargs
    ),
    
    'customer_intent': lambda llm, **kwargs: generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_INTENT_DETERMINER,
        HUMAN_MESSAGE_INTENT_DETERMINER,
        'extract_and_strip_ai_response_content',
        CustomerIntent,
        **kwargs
    ),

    'customer_preferences': lambda llm, response_model, **kwargs: generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_CUSTOMER_PREFERENCES_BUILDER,
        HUMAN_MESSAGE_CUSTOMER_PREFERENCES_BUILDER,
        'extract_and_strip_ai_response_content',
        response_model,
        **kwargs
    ),
    
    'general_sizing_help_about_measurement_not_related_to_products_availability': lambda llm, **kwargs: generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_COMPANY_SIZE_HELP_HANDLER,
        HUMAN_MESSAGE_COMPANY_SIZE_HELP_HANDLER,
        'destructure_messages',
        **kwargs
    ),

    'care_instructions': lambda llm, **kwargs: generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER,
        HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER,
        'destructure_messages',
        **kwargs
    ),
    
    'pricing': lambda llm, **kwargs: generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER,
        HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER,
        'destructure_messages',
        **kwargs
    ),

    'return_policy': lambda llm, **kwargs: generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER,
        HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER,
        'destructure_messages',
        **kwargs
    ),

    'shipping_information': lambda llm, **kwargs: generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER,
        HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER,
        'destructure_messages',
        **kwargs
    ),

    'brand_information': lambda llm, **kwargs: generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER,
        HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER,
        'destructure_messages',
        **kwargs
    ),

    'concern_or_hesitation': lambda llm, **kwargs: generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_OBJECTION_HANDLER,
        HUMAN_MESSAGE_OBJECTION_HANDLER,
        'destructure_messages',
        **kwargs
    ),

    'off_topic': lambda llm, **kwargs: generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_OBJECTION_HANDLER,
        HUMAN_MESSAGE_OBJECTION_HANDLER,
        'destructure_messages',
        **kwargs
    ),

    'wants_product_information_or_products_availability_information_or_shares_preferences': \
        lambda llm, **kwargs: should_recommend_product_or_continue_investigate(
        llm, 
        **kwargs
    ),
}


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
