# from src.chatbot.models import CustomerIntent, CustomerIntentEnum
# from src.chatbot.utils import generate_formatted_response

# from src.chatbot.prompts.query_for_intent_optimizer import HUMAN_MESSAGE_QUERY_FOR_INTENT_OPTIMIZER, SYSTEM_MESSAGE_QUERY_FOR_INTENT_OPTIMIZER
# from src.chatbot.prompts.query_for_search_optimizer import HUMAN_MESSAGE_QUERY_FOR_SEARCH_OPTIMIZER, SYSTEM_MESSAGE_QUERY_FOR_SEARCH_OPTIMIZER
# from src.chatbot.prompts.customer_intent_determiner import HUMAN_MESSAGE_INTENT_DETERMINER, SYSTEM_MESSAGE_INTENT_DETERMINER
# from src.chatbot.prompts.general.company_information_handler import HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER, SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER
# from src.chatbot.prompts.general.objection_handler import HUMAN_MESSAGE_OBJECTION_HANDLER, SYSTEM_MESSAGE_OBJECTION_HANDLER
# from src.chatbot.prompts.general.off_topic_handler import HUMAN_MESSAGE_OFF_TOPIC_HANDLER, SYSTEM_MESSAGE_OFF_TOPIC_HANDLER
# from src.chatbot.prompts.general.sizing_help_handler import HUMAN_MESSAGE_COMPANY_SIZE_HELP_HANDLER, SYSTEM_MESSAGE_COMPANY_SIZE_HELP_HANDLER
# from src.chatbot.prompts.jewelry_consultation.available_options_navigator import HUMAN_MESSAGE_AVAILABLE_OPTIONS_NAVIGATOR, SYSTEM_MESSAGE_AVAILABLE_OPTIONS_NAVIGATOR
# from src.chatbot.prompts.jewelry_consultation.inventory_validator import HUMAN_MESSAGE_INVENTORY_VALIDATOR, SYSTEM_MESSAGE_INVENTORY_VALIDATOR
# from src.chatbot.prompts.jewelry_consultation.preferences_builder import HUMAN_MESSAGE_CUSTOMER_PREFERENCES_BUILDER, SYSTEM_MESSAGE_CUSTOMER_PREFERENCES_BUILDER
# from src.chatbot.prompts.jewelry_consultation.recommender import HUMAN_MESSAGE_RECOMMENDER, SYSTEM_MESSAGE_RECOMMENDER
# from src.chatbot.prompts.jewelry_consultation.discoverer import HUMAN_MESSAGE_DISCOVERER, SYSTEM_MESSAGE_DISCOVERER


# HANDLERS_MAPPER = {
#     'create_optimized_query_for_intent': lambda llm, **kwargs: generate_formatted_response(
#         llm,
#         SYSTEM_MESSAGE_QUERY_FOR_INTENT_OPTIMIZER,
#         HUMAN_MESSAGE_QUERY_FOR_INTENT_OPTIMIZER,
#         'extract_ai_response_content',
#         **kwargs
#     ),

#     'create_optimized_query_for_search': lambda llm, **kwargs: generate_formatted_response(
#         llm,
#         SYSTEM_MESSAGE_QUERY_FOR_SEARCH_OPTIMIZER,
#         HUMAN_MESSAGE_QUERY_FOR_SEARCH_OPTIMIZER,
#         'extract_ai_response_content',
#         **kwargs
#     ),

#     'extract_customer_intent': lambda llm, **kwargs: generate_formatted_response(
#         llm,
#         SYSTEM_MESSAGE_INTENT_DETERMINER,
#         HUMAN_MESSAGE_INTENT_DETERMINER,
#         'extract_and_strip_ai_response_content',
#         CustomerIntent,
#         **kwargs
#     )['primary_intent'],

#     CustomerIntentEnum.SIZING_HELP: lambda llm, **kwargs: generate_formatted_response(
#         llm,
#         SYSTEM_MESSAGE_COMPANY_SIZE_HELP_HANDLER,
#         HUMAN_MESSAGE_COMPANY_SIZE_HELP_HANDLER,
#         'destructure_messages',
#         **kwargs
#     ),

#     CustomerIntentEnum.CARE_INSTRUCTIONS: lambda llm, **kwargs: generate_formatted_response(
#         llm,
#         SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER,
#         HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER,
#         'destructure_messages',
#         **kwargs
#     ),

#     CustomerIntentEnum.PRICING: lambda llm, **kwargs: generate_formatted_response(
#         llm,
#         SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER,
#         HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER,
#         'destructure_messages',
#         **kwargs
#     ),

#     CustomerIntentEnum.RETURN_POLICY: lambda llm, **kwargs: generate_formatted_response(
#         llm,
#         SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER,
#         HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER,
#         'destructure_messages',
#         **kwargs
#     ),

#     CustomerIntentEnum.SHIPPING_INFORMATION: lambda llm, **kwargs: generate_formatted_response(
#         llm,
#         SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER,
#         HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER,
#         'destructure_messages',
#         **kwargs
#     ),

#     CustomerIntentEnum.ORDER_PLACING: lambda llm, **kwargs: generate_formatted_response(
#         llm,
#         SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER,
#         HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER,
#         'destructure_messages',
#         **kwargs
#     ),

#     CustomerIntentEnum.BRAND_INFORMATION: lambda llm, **kwargs: generate_formatted_response(
#         llm,
#         SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER,
#         HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER,
#         'destructure_messages',
#         **kwargs
#     ),

#     CustomerIntentEnum.CONCERN_OR_HESITATION: lambda llm, **kwargs: generate_formatted_response(
#         llm,
#         SYSTEM_MESSAGE_OBJECTION_HANDLER,
#         HUMAN_MESSAGE_OBJECTION_HANDLER,
#         'destructure_messages',
#         **kwargs
#     ),

#     CustomerIntentEnum.OFF_TOPIC: lambda llm, **kwargs: generate_formatted_response(
#         llm,
#         SYSTEM_MESSAGE_OFF_TOPIC_HANDLER,
#         HUMAN_MESSAGE_OFF_TOPIC_HANDLER,
#         'destructure_messages',
#         **kwargs
#     ),

#     'extract_customer_preferences': lambda llm, response_model, **kwargs: generate_formatted_response(
#         llm,
#         SYSTEM_MESSAGE_CUSTOMER_PREFERENCES_BUILDER,
#         HUMAN_MESSAGE_CUSTOMER_PREFERENCES_BUILDER,
#         'extract_and_strip_ai_response_content',
#         response_model,
#         **kwargs
#     ),

#     'check_for_products_matching_customer_preferences': lambda llm, **kwargs: generate_formatted_response(
#         llm,
#         SYSTEM_MESSAGE_INVENTORY_VALIDATOR,
#         HUMAN_MESSAGE_INVENTORY_VALIDATOR,
#         'extract_ai_response_content',
#         **kwargs
#     ),

#     'navigate_towards_available_options': lambda llm, **kwargs: generate_formatted_response(
#         llm,
#         SYSTEM_MESSAGE_AVAILABLE_OPTIONS_NAVIGATOR,
#         HUMAN_MESSAGE_AVAILABLE_OPTIONS_NAVIGATOR,
#         'destructure_messages',
#         **kwargs
#     ),

#     'discover_customer_preferences': lambda llm, **kwargs: generate_formatted_response(
#         llm,
#         SYSTEM_MESSAGE_DISCOVERER,
#         HUMAN_MESSAGE_DISCOVERER,
#         'destructure_messages',
#         **kwargs
#     ),

#     'recommend_product': lambda llm, **kwargs: generate_formatted_response(
#         llm,
#         SYSTEM_MESSAGE_RECOMMENDER,
#         HUMAN_MESSAGE_RECOMMENDER,
#         'destructure_messages',
#         **kwargs
#     )
# }





from src.chatbot.models import CustomerIntent, CustomerIntentEnum
from src.chatbot.utils import async_generate_formatted_response

from src.chatbot.prompts.query_for_intent_optimizer import HUMAN_MESSAGE_QUERY_FOR_INTENT_OPTIMIZER, SYSTEM_MESSAGE_QUERY_FOR_INTENT_OPTIMIZER
from src.chatbot.prompts.query_for_search_optimizer import HUMAN_MESSAGE_QUERY_FOR_SEARCH_OPTIMIZER, SYSTEM_MESSAGE_QUERY_FOR_SEARCH_OPTIMIZER
from src.chatbot.prompts.customer_intent_determiner import HUMAN_MESSAGE_INTENT_DETERMINER, SYSTEM_MESSAGE_INTENT_DETERMINER
from src.chatbot.prompts.general.company_information_handler import HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER, SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER
from src.chatbot.prompts.general.objection_handler import HUMAN_MESSAGE_OBJECTION_HANDLER, SYSTEM_MESSAGE_OBJECTION_HANDLER
from src.chatbot.prompts.general.off_topic_handler import HUMAN_MESSAGE_OFF_TOPIC_HANDLER, SYSTEM_MESSAGE_OFF_TOPIC_HANDLER
from src.chatbot.prompts.general.sizing_help_handler import HUMAN_MESSAGE_COMPANY_SIZE_HELP_HANDLER, SYSTEM_MESSAGE_COMPANY_SIZE_HELP_HANDLER
from src.chatbot.prompts.jewelry_consultation.available_options_navigator import HUMAN_MESSAGE_AVAILABLE_OPTIONS_NAVIGATOR, SYSTEM_MESSAGE_AVAILABLE_OPTIONS_NAVIGATOR
from src.chatbot.prompts.jewelry_consultation.inventory_validator import HUMAN_MESSAGE_INVENTORY_VALIDATOR, SYSTEM_MESSAGE_INVENTORY_VALIDATOR
from src.chatbot.prompts.jewelry_consultation.preferences_builder import HUMAN_MESSAGE_CUSTOMER_PREFERENCES_BUILDER, SYSTEM_MESSAGE_CUSTOMER_PREFERENCES_BUILDER
from src.chatbot.prompts.jewelry_consultation.recommender import HUMAN_MESSAGE_RECOMMENDER, SYSTEM_MESSAGE_RECOMMENDER
from src.chatbot.prompts.jewelry_consultation.discoverer import HUMAN_MESSAGE_DISCOVERER, SYSTEM_MESSAGE_DISCOVERER


ASYNC_HANDLERS_MAPPER = {
    'create_optimized_query_for_intent': lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_QUERY_FOR_INTENT_OPTIMIZER,
        HUMAN_MESSAGE_QUERY_FOR_INTENT_OPTIMIZER,
        'extract_ai_response_content',
        **kwargs
    ),

    'create_optimized_query_for_search': lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_QUERY_FOR_SEARCH_OPTIMIZER,
        HUMAN_MESSAGE_QUERY_FOR_SEARCH_OPTIMIZER,
        'extract_ai_response_content',
        **kwargs
    ),

    'extract_customer_intent': lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_INTENT_DETERMINER,
        HUMAN_MESSAGE_INTENT_DETERMINER,
        'extract_and_strip_ai_response_content',
        CustomerIntent,
        **kwargs
    )['primary_intent'],

    CustomerIntentEnum.SIZING_HELP: lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_COMPANY_SIZE_HELP_HANDLER,
        HUMAN_MESSAGE_COMPANY_SIZE_HELP_HANDLER,
        'destructure_messages',
        **kwargs
    ),

    CustomerIntentEnum.CARE_INSTRUCTIONS: lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER,
        HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER,
        'destructure_messages',
        **kwargs
    ),

    CustomerIntentEnum.PRICING: lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER,
        HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER,
        'destructure_messages',
        **kwargs
    ),

    CustomerIntentEnum.RETURN_POLICY: lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER,
        HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER,
        'destructure_messages',
        **kwargs
    ),

    CustomerIntentEnum.SHIPPING_INFORMATION: lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER,
        HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER,
        'destructure_messages',
        **kwargs
    ),

    CustomerIntentEnum.ORDER_PLACING: lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER,
        HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER,
        'destructure_messages',
        **kwargs
    ),

    CustomerIntentEnum.BRAND_INFORMATION: lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_COMPANY_INFORMATION_HANDLER,
        HUMAN_MESSAGE_COMPANY_INFORMATION_HANDLER,
        'destructure_messages',
        **kwargs
    ),

    CustomerIntentEnum.CONCERN_OR_HESITATION: lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_OBJECTION_HANDLER,
        HUMAN_MESSAGE_OBJECTION_HANDLER,
        'destructure_messages',
        **kwargs
    ),

    CustomerIntentEnum.OFF_TOPIC: lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_OFF_TOPIC_HANDLER,
        HUMAN_MESSAGE_OFF_TOPIC_HANDLER,
        'destructure_messages',
        **kwargs
    ),

    'extract_customer_preferences': lambda llm, response_model, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_CUSTOMER_PREFERENCES_BUILDER,
        HUMAN_MESSAGE_CUSTOMER_PREFERENCES_BUILDER,
        'extract_and_strip_ai_response_content',
        response_model,
        **kwargs
    ),

    'check_for_products_matching_customer_preferences': lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_INVENTORY_VALIDATOR,
        HUMAN_MESSAGE_INVENTORY_VALIDATOR,
        'extract_ai_response_content',
        **kwargs
    ),

    'navigate_towards_available_options': lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_AVAILABLE_OPTIONS_NAVIGATOR,
        HUMAN_MESSAGE_AVAILABLE_OPTIONS_NAVIGATOR,
        'destructure_messages',
        **kwargs
    ),

    'discover_customer_preferences': lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_DISCOVERER,
        HUMAN_MESSAGE_DISCOVERER,
        'destructure_messages',
        **kwargs
    ),

    'recommend_product': lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_RECOMMENDER,
        HUMAN_MESSAGE_RECOMMENDER,
        'destructure_messages',
        **kwargs
    )
}