import json

from src.chatbot.adapters import LLMAdapter, MemoryAdapter, VectorStoreAdapter
from src.chatbot.handlers import HANDLERS_MAPPER, build_conversation_history
from src.chatbot.utils import retrieve_relevant_content
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda


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
                customer_preferences=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['customer_preferences'](
                        llm,
                        conversation_history=inputs["conversation_history"]
                    )
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
            | RunnableLambda(
                lambda inputs: HANDLERS_MAPPER[inputs['customer_intent']['primary_intent']](
                    llm,
                    context=inputs["context"],
                    customer_query=inputs["customer_query"],
                    customer_preferences=inputs["customer_preferences"],
                    conversation_memory=inputs["conversation_memory"]
                )
            )
        )

        system_message, human_message = chain.invoke(
            {
                "conversation_history": conversation_history,
                "conversation_memory": conversation_memory,
                "customer_query": customer_query,
            }
        )

        for event in app.stream({"messages": [system_message, human_message]}, config, stream_mode="updates"):
            ai_response = event['model']['messages'].content

            for chunk in ai_response:
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
