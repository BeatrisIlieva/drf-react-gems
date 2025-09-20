from src.chatbot.prompts.base import CRITICAL_RULES, CONTEXT, GOAL, NEXT, PDF_SUMMARY, ROLE_COMPREHENSIVE, WHO_AM_I


SYSTEM_MESSAGE_DISCOVERER = (
PDF_SUMMARY +
CONTEXT +
ROLE_COMPREHENSIVE +
WHO_AM_I +
GOAL +
"""
<next>
1. Analyze the AVAILABLE PRODUCTS.
2. Analyze the INSTRUCTION.
3. Analyze MY STATEMENT.
4. Follow the instruction to formulate one STRATEGIC QUESTION.
5. Address MY STATEMENT through your STRATEGIC QUESTION.
6. Formulate your FINAL ANSWER to first respond to my question if such, followed by the STRATEGIC QUESTION.
6. Output your FINAL ANSWER.
</next>
"""
+ CRITICAL_RULES
+ NEXT 
)

HUMAN_MESSAGE_DISCOVERER = (
"""
BASED ON:\n
1. CONVERSATION MEMORY:\n{conversation_history}\n\n
2. MY PREFERENCES:
- The gender of the person who will be wearing the jewelry is: {gender}
- The product category I am interested is: {category}
- The metal type I am interested is: {metal_type}
- The stone type I am interested is: {stone_type}
\n\n
3. AVAILABLE PRODUCTS:\n{context}\n\n
4. INSTRUCTION: {next_discovery_question}.\n\n
5. MY STATEMENT:\n{customer_query}
"""
)