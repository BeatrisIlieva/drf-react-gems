# import json

# from src.chatbot.adapters import LLMAdapter, MemoryAdapter, VectorStoreAdapter
# from src.chatbot.handlers import HANDLERS_MAPPER, build_conversation_history
# from src.chatbot.models import BudgetRange, CategoryType, CustomerIntentEnum, MetalType, PurchaseType, StoneType, WearerGender
# from src.chatbot.strategies import PreferenceDiscoveryStrategy
# from src.chatbot.utils import all_preferences_collected, retrieve_relevant_content
# from langchain.schema.runnable import RunnablePassthrough, RunnableLambda, RunnableBranch


# class ChatbotService:
#     """Core service for generating chatbot responses."""

#     @staticmethod
#     def generate_response_stream(customer_query, session_id):
#         vector_store = VectorStoreAdapter.get_vectorstore()
#         conversation_memory = MemoryAdapter.get_memory()
#         llm = LLMAdapter.get_llm()
#         app = MemoryAdapter.get_app()

#         # Yield session_id first
#         yield f"data: {json.dumps({'session_id': session_id})}\n\n"

#         config = {"configurable": {"thread_id": session_id}}

#         conversation_state = conversation_memory.get(config)
#         conversation_history = build_conversation_history(
#             customer_query, conversation_state)

#         # Define the discovery continuation chain (when preferences are missing)
#         continue_discovery_chain = (
#             RunnablePassthrough.assign(
#                 next_discovery_question=RunnableLambda(
#                     lambda inputs: PreferenceDiscoveryStrategy.get_next_question(
#                         inputs['purchase_type'] | inputs['gender'] | inputs['category'] |
#                         inputs['metal_type'] | inputs['stone_type'] | inputs['budget_range']
#                     )
#                 )
#             )
#             | RunnableLambda(
#                 lambda inputs: HANDLERS_MAPPER['investigate'](
#                     llm,
#                     context=inputs["context"],
#                     customer_query=inputs["customer_query"],
#                     next_discovery_question=inputs['next_discovery_question'],
#                     purchase_type=inputs["purchase_type"]["purchase_type"] if inputs["purchase_type"]["purchase_type"] else '',
#                     gender=inputs["gender"]["gender"] if inputs["gender"]["gender"] else '',
#                     category=inputs["category"]["category"] if inputs["category"]["category"] else '',
#                     metal_type=inputs["metal_type"]["metal_type"] if inputs["metal_type"]["metal_type"] else '',
#                     stone_type=inputs["stone_type"]["stone_type"] if inputs["stone_type"]["stone_type"] else '',
#                     budget_range=inputs["budget_range"]["budget_range"] if inputs["budget_range"]["budget_range"] else '',
#                     conversation_memory=inputs["conversation_memory"]
#                 )
#             )
#         )

#         # Define the recommendation chain (when all preferences are collected)
#         recommend_product_chain = RunnableLambda(
#             lambda inputs: HANDLERS_MAPPER['recommend_product'](
#                 llm,
#                 context=inputs["context"],
#                 customer_query=inputs["customer_query"],
#                 purchase_type=inputs["purchase_type"]["purchase_type"],
#                 gender=inputs["gender"]["gender"],
#                 category=inputs["category"]["category"],
#                 metal_type=inputs["metal_type"]["metal_type"],
#                 stone_type=inputs["stone_type"]["stone_type"],
#                 budget_range=inputs["budget_range"]["budget_range"],
#                 conversation_memory=inputs["conversation_memory"]
#             )
#         )

#         # Now the correct conditional structure
#         continue_discovery_or_recommend_product_chain = RunnableBranch(
#             (
#                 # If all preferences are collected, recommend products
#                 lambda x: all_preferences_collected(x),
#                 recommend_product_chain
#             ),
#             # Otherwise (default), continue discovery
#             continue_discovery_chain
#         )

#         available_options_navigator_chain = RunnableLambda(
#             lambda inputs: HANDLERS_MAPPER['available_options_navigator'](
#                 llm,
#                 context=inputs["context"],
#                 customer_query=inputs["customer_query"],
#                 purchase_type=inputs["purchase_type"]["purchase_type"],
#                 gender=inputs["gender"]["gender"],
#                 category=inputs["category"]["category"],
#                 metal_type=inputs["metal_type"]["metal_type"],
#                 stone_type=inputs["stone_type"]["stone_type"],
#                 budget_range=inputs["budget_range"]["budget_range"],
#                 conversation_memory=inputs["conversation_memory"]
#             )
#         )

#         handle_jewelry_consultation_process_chain = (
#             RunnablePassthrough.assign(
#                 purchase_type=RunnableLambda(
#                     lambda inputs: HANDLERS_MAPPER['customer_preferences'](
#                         llm,
#                         PurchaseType,
#                         conversation_history=inputs["conversation_history"]
#                     )
#                 )
#             )
#             | RunnablePassthrough.assign(
#                 gender=RunnableLambda(
#                     lambda inputs: HANDLERS_MAPPER['customer_preferences'](
#                         llm,
#                         WearerGender,
#                         conversation_history=inputs["conversation_history"]
#                     )
#                 )
#             )
#             | RunnablePassthrough.assign(
#                 category=RunnableLambda(
#                     lambda inputs: HANDLERS_MAPPER['customer_preferences'](
#                         llm,
#                         CategoryType,
#                         conversation_history=inputs["conversation_history"]
#                     )
#                 )
#             )
#             | RunnablePassthrough.assign(
#                 metal_type=RunnableLambda(
#                     lambda inputs: HANDLERS_MAPPER['customer_preferences'](
#                         llm,
#                         MetalType,
#                         conversation_history=inputs["conversation_history"]
#                     )
#                 )
#             )
#             | RunnablePassthrough.assign(
#                 stone_type=RunnableLambda(
#                     lambda inputs: HANDLERS_MAPPER['customer_preferences'](
#                         llm,
#                         StoneType,
#                         conversation_history=inputs["conversation_history"]
#                     )
#                 )
#             )
#             | RunnablePassthrough.assign(
#                 budget_range=RunnableLambda(
#                     lambda inputs: HANDLERS_MAPPER['customer_preferences'](
#                         llm,
#                         BudgetRange,
#                         conversation_history=inputs["conversation_history"]
#                     )
#                 )
#             )
#             | RunnablePassthrough.assign(
#                 product_that_meets_current_preferences=RunnableLambda(
#                     lambda inputs: HANDLERS_MAPPER['product_that_meets_current_preferences'](
#                         llm,
#                         context=inputs["context"],
#                         customer_query=inputs["customer_query"],
#                         purchase_type=inputs["purchase_type"]["purchase_type"] if inputs["purchase_type"]["purchase_type"] else '',
#                         gender=inputs["gender"]["gender"] if inputs["gender"]["gender"] else '',
#                         category=inputs["category"]["category"] if inputs["category"]["category"] else '',
#                         metal_type=inputs["metal_type"]["metal_type"] if inputs["metal_type"]["metal_type"] else '',
#                         stone_type=inputs["stone_type"]["stone_type"] if inputs["stone_type"]["stone_type"] else '',
#                         budget_range=inputs["budget_range"]["budget_range"] if inputs["budget_range"]["budget_range"] else '',
#                         conversation_memory=inputs["conversation_memory"]
#                     )
#                 )
#             )
#             | RunnableBranch(
#                 (
#                     lambda x: x['product_that_meets_current_preferences'] == 'MATCH',
#                     continue_discovery_or_recommend_product_chain
#                 ),
#                 available_options_navigator_chain
#             )
#         )

#         general_info_chain = RunnableLambda(
#             lambda inputs: HANDLERS_MAPPER['general-info'](
#                 llm,
#                 context=inputs["context"],
#                 customer_query=inputs["customer_query"],
#                 conversation_memory=inputs["conversation_memory"]
#             )
#         )

#         chain = (
#             RunnablePassthrough.assign(
#                 optimized_query=RunnableLambda(
#                     lambda inputs: HANDLERS_MAPPER['optimized_query'](
#                         llm,
#                         conversation_history=inputs["conversation_history"],
#                     )
#                 )
#             )
#             | RunnablePassthrough.assign(
#                 context=lambda x: retrieve_relevant_content(
#                     vector_store,
#                     x["optimized_query"],
#                 )
#             )
#             | RunnablePassthrough.assign(
#                 customer_intent=RunnableLambda(
#                     lambda inputs: HANDLERS_MAPPER['customer_intent'](
#                         llm,
#                         conversation_history=inputs["conversation_history"]
#                     )
#                 )
#             )
#             | RunnableBranch(
#                 (
#                     lambda x: x['customer_intent'] == CustomerIntentEnum.PRODUCTS_INFO,
#                     handle_jewelry_consultation_process_chain
#                 ),
#                 general_info_chain
#             )
#         )

#         system_message, human_message = chain.invoke(
#             {
#                 "conversation_history": conversation_history,
#                 "conversation_memory": conversation_memory,
#                 "customer_query": customer_query,
#             }
#         )

#         for event in app.stream({"messages": [system_message, human_message]}, config, stream_mode="updates"):
#             ai_response = event['model']['messages'].content

#             for chunk in ai_response:
#                 yield f"data: {json.dumps({'chunk': chunk})}\n\n"


import json

from src.chatbot.adapters import LLMAdapter, MemoryAdapter, VectorStoreAdapter
from src.chatbot.handlers import HANDLERS_MAPPER, build_conversation_history
from src.chatbot.models import BudgetRange, CategoryType, CustomerIntentEnum, MetalType, PurchaseType, StoneType, WearerGender
from src.chatbot.strategies import PreferenceDiscoveryStrategy
from src.chatbot.utils import all_preferences_collected, retrieve_relevant_content
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda, RunnableBranch


class ChatbotService:
    """Core service for generating chatbot responses."""

    @staticmethod
    def generate_response_stream(customer_query, session_id):
        vector_store = VectorStoreAdapter.get_vectorstore()
        conversation_memory = MemoryAdapter.get_memory()
        llm = LLMAdapter.get_llm()
        app = MemoryAdapter.get_app()

        # Yield session_id first
        yield f"data: {json.dumps({'session_id': session_id})}\n\n"

        config = {"configurable": {"thread_id": session_id}}

        conversation_state = conversation_memory.get(config)
        conversation_history = build_conversation_history(
            customer_query, conversation_state)

        # Define the discovery continuation chain (when preferences are missing)
        continue_discovery_chain = (
            RunnablePassthrough.assign(
                next_discovery_question=RunnableLambda(
                    lambda inputs: PreferenceDiscoveryStrategy.get_next_question(
                        inputs['purchase_type'] | inputs['gender'] | inputs['category'] |
                        inputs['metal_type'] | inputs['stone_type'] | inputs['budget_range']
                    )
                )
            )
            | RunnableLambda(
                lambda inputs: HANDLERS_MAPPER['investigate'](
                    llm,
                    context=inputs["context"],
                    customer_query=inputs["customer_query"],
                    next_discovery_question=inputs['next_discovery_question'],
                    purchase_type=inputs["purchase_type"]["purchase_type"] if inputs["purchase_type"]["purchase_type"] else '',
                    gender=inputs["gender"]["gender"] if inputs["gender"]["gender"] else '',
                    category=inputs["category"]["category"] if inputs["category"]["category"] else '',
                    metal_type=inputs["metal_type"]["metal_type"] if inputs["metal_type"]["metal_type"] else '',
                    stone_type=inputs["stone_type"]["stone_type"] if inputs["stone_type"]["stone_type"] else '',
                    budget_range=inputs["budget_range"]["budget_range"] if inputs["budget_range"]["budget_range"] else '',
                    conversation_memory=inputs["conversation_memory"]
                )
            )
        )

        # Define the recommendation chain (when all preferences are collected)
        recommend_product_chain = RunnableLambda(
            lambda inputs: HANDLERS_MAPPER['recommend_product'](
                llm,
                context=inputs["context"],
                customer_query=inputs["customer_query"],
                purchase_type=inputs["purchase_type"]["purchase_type"],
                gender=inputs["gender"]["gender"],
                category=inputs["category"]["category"],
                metal_type=inputs["metal_type"]["metal_type"],
                stone_type=inputs["stone_type"]["stone_type"],
                budget_range=inputs["budget_range"]["budget_range"],
                conversation_memory=inputs["conversation_memory"]
            )
        )

        # Now the correct conditional structure
        continue_discovery_or_recommend_product_chain = RunnableBranch(
            (
                # If all preferences are collected, recommend products
                lambda x: all_preferences_collected(x),
                recommend_product_chain
            ),
            # Otherwise (default), continue discovery
            continue_discovery_chain
        )

        # Define the available options navigator chain
        available_options_navigator_chain = RunnableLambda(
            lambda inputs: HANDLERS_MAPPER['available_options_navigator'](
                llm,
                context=inputs["context"],
                customer_query=inputs["customer_query"],
                purchase_type=inputs["purchase_type"]["purchase_type"] if inputs["purchase_type"]["purchase_type"] else '',
                gender=inputs["gender"]["gender"] if inputs["gender"]["gender"] else '',
                category=inputs["category"]["category"] if inputs["category"]["category"] else '',
                metal_type=inputs["metal_type"]["metal_type"] if inputs["metal_type"]["metal_type"] else '',
                stone_type=inputs["stone_type"]["stone_type"] if inputs["stone_type"]["stone_type"] else '',
                budget_range=inputs["budget_range"]["budget_range"] if inputs["budget_range"]["budget_range"] else '',
                conversation_memory=inputs["conversation_memory"]
            )
        )

        # Define the jewelry consultation process chain
        handle_jewelry_consultation_process_chain = (
            RunnablePassthrough.assign(
                purchase_type=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['customer_preferences'](
                        llm,
                        PurchaseType,
                        conversation_history=inputs["conversation_history"]
                    )
                )
            )
            | RunnablePassthrough.assign(
                gender=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['customer_preferences'](
                        llm,
                        WearerGender,
                        conversation_history=inputs["conversation_history"]
                    )
                )
            )
            | RunnablePassthrough.assign(
                category=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['customer_preferences'](
                        llm,
                        CategoryType,
                        conversation_history=inputs["conversation_history"]
                    )
                )
            )
            | RunnablePassthrough.assign(
                metal_type=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['customer_preferences'](
                        llm,
                        MetalType,
                        conversation_history=inputs["conversation_history"]
                    )
                )
            )
            | RunnablePassthrough.assign(
                stone_type=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['customer_preferences'](
                        llm,
                        StoneType,
                        conversation_history=inputs["conversation_history"]
                    )
                )
            )
            | RunnablePassthrough.assign(
                budget_range=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['customer_preferences'](
                        llm,
                        BudgetRange,
                        conversation_history=inputs["conversation_history"]
                    )
                )
            )
            | RunnablePassthrough.assign(
                product_that_meets_current_preferences=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['product_that_meets_current_preferences'](
                        llm,
                        context=inputs["context"],
                        customer_query=inputs["customer_query"],
                        purchase_type=inputs["purchase_type"]["purchase_type"] if inputs["purchase_type"]["purchase_type"] else '',
                        gender=inputs["gender"]["gender"] if inputs["gender"]["gender"] else '',
                        category=inputs["category"]["category"] if inputs["category"]["category"] else '',
                        metal_type=inputs["metal_type"]["metal_type"] if inputs["metal_type"]["metal_type"] else '',
                        stone_type=inputs["stone_type"]["stone_type"] if inputs["stone_type"]["stone_type"] else '',
                        budget_range=inputs["budget_range"]["budget_range"] if inputs["budget_range"]["budget_range"] else '',
                        conversation_memory=inputs["conversation_memory"]
                    )
                )
            )
            | RunnableBranch(
                (
                    lambda x: x['product_that_meets_current_preferences'] == 'MATCH',
                    continue_discovery_or_recommend_product_chain
                ),
                available_options_navigator_chain
            )
        )

        # Define the general info chain
        general_info_chain = RunnableLambda(
            lambda inputs: HANDLERS_MAPPER['general-info'](
                llm,
                context=inputs["context"],
                customer_query=inputs["customer_query"],
                conversation_memory=inputs["conversation_memory"]
            )
        )

        # Main chain with conditional branching based on customer intent
        chain = (
            RunnablePassthrough.assign(
                optimized_query=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['optimized_query'](
                        llm,
                        conversation_history=inputs["conversation_history"],
                    )
                )
            )
            | RunnablePassthrough.assign(
                context=lambda x: retrieve_relevant_content(
                    vector_store,
                    x["optimized_query"],
                )
            )
            | RunnablePassthrough.assign(
                customer_intent=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['customer_intent'](
                        llm,
                        conversation_history=inputs["conversation_history"]
                    )
                )
            )
            | RunnableBranch(
                (
                    # Check if customer intent is product-related
                    lambda x: x['customer_intent'] == CustomerIntentEnum.PRODUCTS_INFO,
                    handle_jewelry_consultation_process_chain
                ),
                # Default: general information
                general_info_chain
            )
        )

        # Execute the chain
        system_message, human_message = chain.invoke(
            {
                "conversation_history": conversation_history,
                "conversation_memory": conversation_memory,
                "customer_query": customer_query,
            }
        )

        # Stream the response
        for event in app.stream({"messages": [system_message, human_message]}, config, stream_mode="updates"):
            ai_response = event['model']['messages'].content

            for chunk in ai_response:
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"