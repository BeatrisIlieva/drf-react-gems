# from src.chatbot.models import CustomerIntent, ProductPreferences
# from src.chatbot.prompts.customer_intent import ANSWER_TO_PROVIDE_CUSTOMER_SUPPORT_SYSTEM_MESSAGE, ANSWER_TO_RECOMMEND_PRODUCT_SYSTEM_MESSAGE, DISCOVERY_QUESTION_TO_ASK_SYSTEM_MESSAGE, OBJECTION_HANDLING_SYSTEM_MESSAGE, OFF_TOPIC_SYSTEM_MESSAGE, OFFER_HELP_WITH_SELECTING_IDEAL_SIZE_SYSTEM_MESSAGE, PLAIN_HUMAN_MESSAGE, PROVIDE_HELP_WITH_SELECTING_IDEAL_SIZE_SYSTEM_MESSAGE, WITH_MEMORY_AND_DB_CONTENT_HUMAN_MESSAGE, WITH_MEMORY_HUMAN_MESSAGE
# from src.chatbot.prompts.helper_calls import ANALYZE_CONVERSATION_INSIGHTS_HUMAN_MESSAGE, ANALYZE_CONVERSATION_INSIGHTS_SYSTEM_MESSAGE, CUSTOMER_INTENT_HUMAN_MESSAGE, CUSTOMER_INTENT_SYSTEM_MESSAGE, CUSTOMER_PREFERENCE_HUMAN_MESSAGE, CUSTOMER_PREFERENCE_SYSTEM_MESSAGE, OPTIMIZED_VECTOR_SEARCH_QUERY_HUMAN_MESSAGE, OPTIMIZED_VECTOR_SEARCH_QUERY_SYSTEM_MESSAGE
# from src.chatbot.strategies import PreferenceDiscoveryStrategy
# from src.chatbot.utils import generate_formatted_response, retrieve_relevant_content


# class AnalyzeConversationInsightsMixin:
#     def analyze_conversation_insights(self, llm, conversation_history):
#         return generate_formatted_response(
#             llm,
#             ANALYZE_CONVERSATION_INSIGHTS_SYSTEM_MESSAGE,
#             ANALYZE_CONVERSATION_INSIGHTS_HUMAN_MESSAGE,
#             'extract_ai_response_content',
#             conversation_history=conversation_history,
#         )


# class ExtractCustomerIntentMixin:
#     def extract_customer_intent(self, llm, conversation_insights):
#         return generate_formatted_response(
#             llm,
#             CUSTOMER_INTENT_SYSTEM_MESSAGE,
#             CUSTOMER_INTENT_HUMAN_MESSAGE,
#             'extract_and_strip_ai_response_content',
#             CustomerIntent,
#             conversation_insights=conversation_insights,
#         )


# class ProductRecommendationMixin:
#     def handle_product_recommendation(self, llm, vector_store, conversation_memory, conversation_insights):
#         # Determine whether the customer has provided all necessary preferences
#         result = self._determine_next_step(
#             llm,
#             conversation_insights
#         )

#         is_ready_to_proceed = result['is_ready_to_proceed']
#         if not is_ready_to_proceed:
#             discovery_question = result['discovery_question']

#             return self._ask_clarifying_question(llm, discovery_question, conversation_insights)

#         else:
#             customer_preferences = result['customer_preferences']
#             vector_search_query = self._create_optimized_vector_search_query(
#                 llm, conversation_insights, customer_preferences)
#             product = retrieve_relevant_content(
#                 vector_store,
#                 vector_search_query,
#                 1
#             )
#             return self._recommend_product(llm, conversation_memory, conversation_insights, product)

#     def _ask_clarifying_question(self, llm, discovery_question, conversation_insights):

#         return generate_formatted_response(
#             llm,
#             DISCOVERY_QUESTION_TO_ASK_SYSTEM_MESSAGE,
#             PLAIN_HUMAN_MESSAGE,
#             'destructure_messages',
#             discovery_question=discovery_question,
#             conversation_insights=conversation_insights,
#         )

#     def _create_optimized_vector_search_query(self, llm, conversation_insights, customer_preferences):
#         return generate_formatted_response(
#             llm,
#             OPTIMIZED_VECTOR_SEARCH_QUERY_SYSTEM_MESSAGE,
#             OPTIMIZED_VECTOR_SEARCH_QUERY_HUMAN_MESSAGE,
#             'extract_ai_response_content',
#             conversation_insights=conversation_insights,
#             customer_preferences=customer_preferences
#         )

#     def _recommend_product(self, llm, conversation_memory, conversation_insights, product):
#         return generate_formatted_response(
#             llm,
#             ANSWER_TO_RECOMMEND_PRODUCT_SYSTEM_MESSAGE,
#             WITH_MEMORY_HUMAN_MESSAGE,
#             'destructure_messages',
#             product_to_recommend=product,
#             conversation_insights=conversation_insights,
#             conversation_memory=conversation_memory,
#         )

#     def _determine_next_step(
#         self,
#         llm,
#         conversation_insights: str,
#     ):
#         """
#         Extract preferences and generate next question using strategic ordering.
#         Returns (preferences, next_question, is_complete)
#         """

#         # Extract current preferences
#         preferences = generate_formatted_response(
#             llm,
#             CUSTOMER_PREFERENCE_SYSTEM_MESSAGE,
#             CUSTOMER_PREFERENCE_HUMAN_MESSAGE,
#             'extract_and_strip_ai_response_content',
#             ProductPreferences,
#             conversation_insights=conversation_insights,
#         )
        
#         print('customer_preferences')
#         print(preferences)
#         print('-----')

#         # Check if discovery is complete (minimum required fields)
#         required_fields = PreferenceDiscoveryStrategy.DISCOVERY_SEQUENCE
#         is_ready_to_proceed = all(preferences.get(field) not in ('', None) for field in required_fields)

#         if is_ready_to_proceed:
#             preferences_as_string = ''

#             for key, value in preferences.items():
#                 preferences_as_string += f'{key}: {value}\n'

#             return {'is_ready_to_proceed': is_ready_to_proceed, 'customer_preferences': preferences_as_string}

#         # Get next question using strategy
#         next_question = PreferenceDiscoveryStrategy.get_next_question(
#             preferences)

#         return {'is_ready_to_proceed': is_ready_to_proceed, 'discovery_question': next_question}


# class OfferSizeHelp:
#     def handle_offer_size_help(self, llm, conversation_memory, conversation_insights):
#         return generate_formatted_response(
#             llm,
#             OFFER_HELP_WITH_SELECTING_IDEAL_SIZE_SYSTEM_MESSAGE,
#             WITH_MEMORY_HUMAN_MESSAGE,
#             'destructure_messages',
#             conversation_memory=conversation_memory,
#             conversation_insights=conversation_insights,
#         )


# class ProvideSizeHelp:
#     def handle_provide_size_help(self, llm, conversation_memory, conversation_insights):
#         return generate_formatted_response(
#             llm,
#             PROVIDE_HELP_WITH_SELECTING_IDEAL_SIZE_SYSTEM_MESSAGE,
#             WITH_MEMORY_HUMAN_MESSAGE,
#             'destructure_messages',
#             conversation_memory=conversation_memory,
#             conversation_insights=conversation_insights,
#         )


# class CustomerSupportMixin:
#     def handle_customer_support(self, llm, vector_store, conversation_memory, conversation_insights):
#         content = retrieve_relevant_content(
#             vector_store,
#             conversation_insights
#         )

#         return generate_formatted_response(
#             llm,
#             ANSWER_TO_PROVIDE_CUSTOMER_SUPPORT_SYSTEM_MESSAGE,
#             WITH_MEMORY_AND_DB_CONTENT_HUMAN_MESSAGE,
#             'destructure_messages',
#             conversation_memory=conversation_memory,
#             content=content,
#             conversation_insights=conversation_insights
#         )


# class ObjectionHandlingMixin:
#     def handle_objections(self, llm, vector_store, conversation_memory, conversation_insights):
#         content = retrieve_relevant_content(
#             vector_store,
#             conversation_insights
#         )

#         return generate_formatted_response(
#             llm,
#             OBJECTION_HANDLING_SYSTEM_MESSAGE,
#             WITH_MEMORY_AND_DB_CONTENT_HUMAN_MESSAGE,
#             'destructure_messages',
#             conversation_memory=conversation_memory,
#             content=content,
#             conversation_insights=conversation_insights,
#         )


# class OffTopicMixin:
#     def handle_off_topic(self, llm, conversation_memory, conversation_insights):
#         return generate_formatted_response(
#             llm,
#             OFF_TOPIC_SYSTEM_MESSAGE,
#             WITH_MEMORY_HUMAN_MESSAGE,
#             'destructure_messages',
#             conversation_memory=conversation_memory,
#             conversation_insights=conversation_insights,
#         )
