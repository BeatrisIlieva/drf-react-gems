from src.chatbot.prompts.base import CRITICAL_RULES, CONTEXT, GOAL, NEXT, PDF_SUMMARY, ROLE_COMPREHENSIVE, WHO_AM_I


SYSTEM_MESSAGE_DISCOVERER = (
PDF_SUMMARY +
CONTEXT +
ROLE_COMPREHENSIVE +
WHO_AM_I +
GOAL +
"""
<next>
1. Analyze the products into the provided CONTEXT.
2. If I ask a question, you must address it through your STRATEGIC QUESTION.
3. Output exactly the STRATEGIC QUESTION only along with the response of my question if such.
</next>
"""
+ CRITICAL_RULES
+ NEXT 
)

HUMAN_MESSAGE_DISCOVERER = (
"""
BASED ON:\n
1. CONVERSATION MEMORY:\n{conversation_memory}\n\n
2. MY PREFERENCES:
- I am buying the jewelry as a: {purchase_type}
- The gender of the person who will be wearing the jewelry is: {gender}
- The product category I am interested is: {category}
- The metal type I am interested is: {metal_type}
- The stone type I am interested is: {stone_type}
- The budget I have in mind is: {budget_range}
\n\n
3. CONTEXT:\n{context}\n\n
4. Respond to my STATEMENT with the following STRATEGIC QUESTION: {next_discovery_question}.\n\n
5. STATEMENT:\n{customer_query}
"""
)