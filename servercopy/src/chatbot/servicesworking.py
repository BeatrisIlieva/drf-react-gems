import json


from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

from src.chatbot.adapters import LLMAdapter, MemoryAdapter, VectorStoreAdapter

from src.chatbot.prompts import ENHANCED_HUMAN_MESSAGE, ENHANCED_SYSTEM_MESSAGE, HUMAN_MESSAGE, SYSTEM_MESSAGE

from langchain_core.messages import HumanMessage, SystemMessage


from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph


class ContextService:
    """Handles document retrieval and context building."""

    @staticmethod
    def get_context(vectorstore, query, k=4):
        results = vectorstore.similarity_search(query, k=k)
        # for i, doc in enumerate(results, 1):
        # print(f"--- Chunk {i} ---")
        # print(doc.page_content, "...\n")
        context = '\n'.join(result.page_content for result in results)

        return context.strip()


class ChatbotService:
    """Core service for generating chatbot responses."""
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._initialize()

        return cls._instance

    @classmethod
    def _initialize(cls):
        cls._instance.memory = MemorySaver()
        cls._instance.workflow = StateGraph(state_schema=MessagesState)
        cls._instance.workflow.add_edge(START, "model")
        cls._instance.workflow.add_node("model", cls._instance._call_model)
        cls._instance.app = cls._instance.workflow.compile(
            checkpointer=cls._instance.memory)

    @classmethod
    def get_memory(cls):
        return cls().memory

    @classmethod
    def get_app(cls):
        return cls().app

    @classmethod
    def _call_model(cls, state: MessagesState):
        llm = LLMAdapter.get_llm()
        user_query = state['messages'][-1].content
        vector_store = VectorStoreAdapter.get_vectorstore()
        conversation_memory = ChatbotService.get_memory()
        context = ContextService.get_context(
                vector_store, user_query
            )
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(SYSTEM_MESSAGE),
            HumanMessagePromptTemplate.from_template(HUMAN_MESSAGE),
        ])

        messages = prompt.format_messages(
            conversation_memory=conversation_memory,
            input=user_query,
            context=context
        )
        
        print(messages)
        
        response = llm.invoke(messages)

        return {"messages": response}

    @staticmethod
    def generate_response_stream(user_query, session_id):
        # vector_store = VectorStoreAdapter.get_vectorstore()
        # conversation_memory = MemoryAdapter.get_memory()
        # app = MemoryAdapter.get_app()
        app = ChatbotService.get_app()

        # Yield session_id first
        yield f"data: {json.dumps({'session_id': session_id})}\n\n"

        config = {"configurable": {"thread_id": session_id}}

        # conversation_state = conversation_memory.get(config)
        # if conversation_state:
        #     conversation_history = ChatbotService._build_conversation_history(
        #         conversation_state, user_query)

        #     enhanced_query = ChatbotService._create_enhanced_query(
        #         conversation_history)
        #     context = ContextService.get_context(
        #         vector_store, enhanced_query)

        # else:
        #     context = ContextService.get_context(
        #         vector_store, user_query
        #     )

        # prompt = ChatPromptTemplate.from_messages([
        #     SystemMessagePromptTemplate.from_template(SYSTEM_MESSAGE),
        #     HumanMessagePromptTemplate.from_template(HUMAN_MESSAGE),
        # ])

        # messages = prompt.format_messages(
        #     conversation_memory=conversation_memory,
        #     input=user_query,
        #     context=context
        # )

        # system_message, human_message = messages[0], messages[1]

        for event in app.stream({"messages": [user_query]}, config, stream_mode="updates"):
            ai_response = event['model']['messages'].content

            for chunk in ai_response:
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"

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
                ENHANCED_SYSTEM_MESSAGE),
            HumanMessagePromptTemplate.from_template(ENHANCED_HUMAN_MESSAGE),
        ])

        messages = prompt.format_messages(
            conversation_history='\n'.join(conversation_history),
        )

        llm = LLMAdapter.get_llm()

        enhanced_query = llm.invoke(messages).content
        print('enhanced_query', enhanced_query)
        return enhanced_query
