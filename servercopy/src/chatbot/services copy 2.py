import json

from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.schema.runnable import RunnablePassthrough

from src.chatbot.adapters import LLMAdapter, MemoryAdapter, VectorStoreAdapter

from src.chatbot.prompts import ENHANCED_SYSTEM_TEMPLATE, ENHANCED_HUMAN_TEMPLATE, SYSTEM_TEMPLATE_GENERATE_THREE_BEST_ANSWERS, SYSTEM_TEMPLATE_CHOOSE_THE_BEST_ANSWER, HUMAN_TEMPLATE_CHOOSE_BEST_ANSWER, HUMAN_TEMPLATE_GENERATE_THREE_BEST_ANSWERS


class ContextService:
    """Handles document retrieval and context building."""

    @staticmethod
    def get_context(vectorstore, query, k=10):
        results = vectorstore.similarity_search(query, k=k)
        # for i, doc in enumerate(results, 1):
        # print(f"--- Chunk {i} ---")
        # print(doc.page_content, "...\n")
        context = '\n'.join(result.page_content for result in results)

        return context.strip()


class ChatbotService:
    """Core service for generating chatbot responses."""

    @staticmethod
    def generate_response_stream(user_query, session_id):
        vector_store = VectorStoreAdapter.get_vectorstore()
        conversation_memory = MemoryAdapter.get_memory()
        app = MemoryAdapter.get_app()

        # Yield session_id first
        yield f"data: {json.dumps({'session_id': session_id})}\n\n"

        config = {"configurable": {"thread_id": session_id}}

        conversation_state = conversation_memory.get(config)
        if conversation_state:
            conversation_history = ChatbotService._build_conversation_history(
                conversation_state, user_query)
            print('history', conversation_history)
            enhanced_query = ChatbotService._create_enhanced_query(
                conversation_history)
            context = ContextService.get_context(
                vector_store, enhanced_query)

        else:
            context = ContextService.get_context(
                vector_store, user_query
            )

        generate_three_best_answers_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                SYSTEM_TEMPLATE_GENERATE_THREE_BEST_ANSWERS),
            HumanMessagePromptTemplate.from_template(HUMAN_TEMPLATE_GENERATE_THREE_BEST_ANSWERS),
        ])


        best_answer_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                SYSTEM_TEMPLATE_CHOOSE_THE_BEST_ANSWER),
            HumanMessagePromptTemplate.from_template(HUMAN_TEMPLATE_CHOOSE_BEST_ANSWER),
        ])

        llm = LLMAdapter.get_llm()

        chain = (
            {
                "three_best_answers": generate_three_best_answers_prompt | llm,
                "conversation_memory": RunnablePassthrough(),
                "input": RunnablePassthrough(),
                "context": RunnablePassthrough(),
            }
            | best_answer_prompt
            | llm
        )

        best_answer = chain.invoke({
            "conversation_memory": conversation_memory, "input": user_query, "context": context
        }).content
        
        three_best_answers_response = generate_three_best_answers_prompt | llm
        three_best_answers = three_best_answers_response.invoke({
            "conversation_memory": conversation_memory,
            "input": user_query,
            # "context": context
        }).content

        # Print the generated three answers
        print("🔹 Three best answers:\n", three_best_answers)
        
        system_message = SystemMessage(content=best_answer)
        human_message = HumanMessage(content=user_query)
        
        for _ in app.stream({"messages": [system_message, human_message]}, config, stream_mode="updates"):
            for chunk in best_answer:
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"

        yield f"data: {json.dumps({'chunk': '[DONE]'})}\n\n"

    @staticmethod
    def _build_conversation_history(conversation_state, user_query):
        conversation_history = []
        messages = conversation_state['channel_values']['messages']
        user_messages = [msg.content.split('INPUT:')[-1].strip()
                         for msg in messages if msg.__class__.__name__ == 'HumanMessage']
        assistant_messages = [msg.content.strip()
                              for msg in messages if msg.__class__.__name__ == 'AIMessage']

        for i in range(len(user_messages)):
            conversation_history.append(
                f'{i + 1}. user: {user_messages[i]}, assistant: {assistant_messages[i]};')

        conversation_history.append(
            f'{len(user_messages) + 1}. user: {user_query};')

        return conversation_history

    @staticmethod
    def _create_enhanced_query(conversation_history):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                ENHANCED_SYSTEM_TEMPLATE),
            HumanMessagePromptTemplate.from_template(ENHANCED_HUMAN_TEMPLATE),
        ])

        messages = prompt.format_messages(
            conversation_history='\n'.join(conversation_history),
        )

        llm = LLMAdapter.get_llm()

        enhanced_query = llm.invoke(messages).content
        print('enhanced_query', enhanced_query)
        return enhanced_query

