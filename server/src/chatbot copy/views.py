import os
from django.conf import settings
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

from django.http import StreamingHttpResponse


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.memory.kg import ConversationKGMemory

from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate

from src.chatbot.serializers import ChatRequestSerializer

from src.chatbot.constants import ERROR_RESPONSE_OBJECT
from src.chatbot.config import SYSTEM_MESSAGE, TOOLS


class ChatBotAPIView(APIView):
    permission_classes = [AllowAny]
    """
    Main chatbot API endpoint that handles user queries and returns AI responses.
    """

    def post(self, request):
        """
        Handle POST requests for chatbot interactions

        Expected payload:
        {
            "message": "User's question"
        }

        Returns:
        {
            "response": "AI response",
            "success": true/false,
        }
        """
        # try:
        # Validate input
        serializer = ChatRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                ERROR_RESPONSE_OBJECT,
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_message = serializer.validated_data['message']
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(base_dir, "docs", "product_catalog.pdf")
        
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,       # ~1-2 paragraphs per chunk
        chunk_overlap=200,     # Preserve context across chunks
        separators=["\n\n", "\n", ". ", " ", ""]
    )

        # Step 2: Split the PDF pages into chunks
        chunks = text_splitter.split_documents(pages)

        embedding_model = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )
        
        # sample_vector = embedding_model.embed_query("What is LangChain?")
        
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory="products_db"
        )
        
        # query = "Explain the purpose of LangChain"
        results = vectorstore.similarity_search(user_message, k=2)
        
        
        llm = ChatOpenAI(
            model="gpt-4o-mini",   # Recommended for fast, cost-effective RAG tasks
            temperature=0.2,       # Low randomness for more precise answers
            max_tokens=100         # Reasonable cap for lecture demos
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Based on the following context, answer the query:"),
            ("system", "Context:\n{results}"),
            ("system", "Known facts extracted so far:\n{history}"),
            ("system", "Subject: {subject}\nSource: {source}"),
            ("human", "{input}")
        ])

        # 3) KG memory: align keys with LLMChain (input='input', output='text'); keep a few turns in view (k)
        kg_memory = ConversationKGMemory(
            llm=llm,
            memory_key="history",   # <- matches prompt
            input_key="input",      # <- LLMChain input dict will have {"input": "..."}
            output_key="text",      # <- LLMChain default output key is "text"
            return_messages=False,  # you can set True if you want message objects instead of string
            k=4                     # consider last 4 utterances (2 pairs) when extracting
        )

        kg_chain = LLMChain(
            llm=llm,
            prompt=prompt,
            memory=kg_memory,
            output_key="text"       # explicit to match memory.output_key
        )
        
        response = kg_chain.invoke({
            "input": user_message,
            "results": results,
            "subject": "",
            "source": ""
        })
        
        streaming_response = StreamingHttpResponse(
                response,
                content_type='text/event-stream'
            )
        
        return streaming_response

        # except Exception:
        #     return Response(
        #         ERROR_RESPONSE_OBJECT,
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     )

    