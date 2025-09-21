from src.chatbot.prompts.base import CONTEXT, PDF_SUMMARY


SYSTEM_MESSAGE_QUERY_FOR_SEARCH_OPTIMIZER = (
CONTEXT +
PDF_SUMMARY +
"""
<note>
- Users interact with the chatbot through conversational questions, and the system's effectiveness depends entirely on successfully retrieving the most relevant chunks from the vectorstore. Query optimization is critical because poor retrieval leads to irrelevant or incomplete responses, directly impacting user satisfaction and system performance.
- Including CUSTOMER PREFERENCES about gender, category, metal type, stone type into the QUESTION is critically important for the effective vector search. 
</note>

<task>
1. Analyze the provided pdf_summary to get to know the data contained in our vectorstore
2. Analyze the CUSTOMER PREFERENCES
3. Formulate a single, well-formed QUESTION in the customer’s voice 
</task>

<next>
Output only the formulated QUESTION.
</next>
"""
)

HUMAN_MESSAGE_QUERY_FOR_SEARCH_OPTIMIZER = (
"""
CUSTOMER PREFERENCES:
- Target Gender: {gender}
- Category: {category}
- Metal: {metal_type}
- Stone: {stone_type}
"""
)