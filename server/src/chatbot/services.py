import json
from langchain.prompts import ChatPromptTemplate
from src.chatbot.config import SYSTEM_MESSAGE

class RetrievalService:
    """Handles document retrieval and context building."""
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore

    def get_context(self, query, k=4):
        results = self.vectorstore.similarity_search(query, k=k)
        context = '\n'.join(result.page_content for result in results)
        return context.strip()


class ChatbotService:
    """Core service for generating chatbot responses."""
    def __init__(self, llm, vectorstore):
        self.llm = llm
        self.retrieval_service = RetrievalService(vectorstore)

    def generate_response_stream(self, user_query, session_id, memory):
        # Get context
        context = self.retrieval_service.get_context(user_query)

        # Yield session_id first
        yield f"data: {json.dumps({'session_id': session_id})}\n\n"

        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_MESSAGE),
            ("system", f"""You are a helpful assistant. You have access to:

            1. Document context (product information):
            {context}

            2. Previous conversation history: {{chat_history}}

            Use both sources to answer the user's question. If you learned something about the user in previous conversations (like their name or preferences), make sure to reference that information when relevant."""),
            ("human", "{input}")
        ])

        # Get chat history
        chat_history = memory.load_memory_variables({})['chat_history']

        # Format messages
        messages = prompt.format_messages(
            input=user_query,
            chat_history=chat_history
        )

        # Stream response
        full_response = ""
        for chunk in self.llm.stream(messages):
            content = chunk.content
            if content:
                full_response += content
                yield f"data: {json.dumps({'chunk': content})}\n\n"

        # Save to memory
        memory.save_context({"input": user_query}, {"text": full_response})

        # Completion signal
        yield f"data: {json.dumps({'chunk': '[DONE]'})}\n\n"