import json

from src.chatbot.config import TOP_N_RESULTS
from src.chatbot.prompts.jewelry_consultation import (
    HUMAN_MESSAGE_JEWELRY_CONSULTANT,
    SYSTEM_MESSAGE_JEWELRY_CONSULTANT
)
from src.chatbot.prompts.query_for_search_optimizer import (
    HUMAN_MESSAGE_QUERY_FOR_SEARCH_OPTIMIZER,
    SYSTEM_MESSAGE_QUERY_FOR_SEARCH_OPTIMIZER
)
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class ChatbotService:
    """Core service for generating chatbot responses."""

    def __init__(self, session_id, vector_store, memory, llm, streaming_llm, customer_query):
        self.session_id = session_id
        self.vector_store = vector_store
        self.conversation_memory = memory
        self.llm = llm
        self.streaming_llm = streaming_llm
        self.customer_query = customer_query

    def generate_response_stream(self):
        """Generate streaming response for the customer query."""
        # Yield session_id
        yield f'data: {json.dumps({'session_id': self.session_id})}\n\n'

        try:
            memory_vars = self.conversation_memory.load_memory_variables({})
            conversation_history = memory_vars.get('conversation_memory', '')

            # Step 1: Optimize query for search (NON-STREAMING)
            optimized_query = self._generate_non_streaming_response(
                SYSTEM_MESSAGE_QUERY_FOR_SEARCH_OPTIMIZER,
                HUMAN_MESSAGE_QUERY_FOR_SEARCH_OPTIMIZER,
                customer_query=self.customer_query,
                conversation_history=conversation_history,
            )

            # Step 2: Retrieve relevant content
            context = self._retrieve_relevant_content(optimized_query)

            # Step 3: Generate and stream final response (STREAMING)
            accumulated_response = ''

            for chunk in self._generate_streaming_response(
                SYSTEM_MESSAGE_JEWELRY_CONSULTANT,
                HUMAN_MESSAGE_JEWELRY_CONSULTANT,
                context=context,
                customer_query=self.customer_query,
                conversation_history=conversation_history,
            ):
                accumulated_response += chunk
                yield f'data: {json.dumps({'chunk': chunk})}\n\n'

            # Step 4: Save complete response to memory
            self.conversation_memory.save_context(
                {'input': self.customer_query},
                {'response': accumulated_response}
            )

        except Exception as e:
            print(f'Error in generate_response_stream: {e}')
            yield f'data: {json.dumps({'error': 'Something went wrong. Please try again.'})}\n\n'

    def _generate_non_streaming_response(self, system_message, human_message, **kwargs):
        """Generate non-streaming AI response - returns string directly."""
        messages = self._format_messages(
            system_message,
            human_message,
            **kwargs,
        )

        return self.llm.invoke(messages).content

    def _generate_streaming_response(self, system_message, human_message, **kwargs):
        """Generate streaming AI response - returns generator."""
        messages = self._format_messages(
            system_message,
            human_message,
            **kwargs,
        )

        for chunk in self.streaming_llm.stream(messages):
            if chunk.content:
                yield chunk.content

    def _format_messages(
        self,
        system_message,
        human_message,
        **kwargs
    ):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                system_message
            ),
            HumanMessagePromptTemplate.from_template(
                human_message
            ),
        ])

        return prompt.format_messages(**kwargs)

    def _retrieve_relevant_content(self, query, k=TOP_N_RESULTS):
        results = self.vector_store.similarity_search(
            query,
            k=k
        )

        context = '\n'.join(
            result.page_content for result in results
        )

        return context.strip()
