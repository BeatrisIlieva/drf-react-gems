from src.chatbot.prompts.base import CRITICAL_RULES, CONTEXT, DO_NOT_RECOMMEND_PRODUCT, NEXT, ROLE_CONCISE, WHO_AM_I


SYSTEM_MESSAGE_COMPANY_SIZE_HELP_HANDLER = (
CONTEXT +
ROLE_CONCISE +
WHO_AM_I +
""" 
Analyze MY PREFERENCES to find out if I have mentioned any category type.
- If I have not mentioned a category type, then respond to my STATEMENT by asking a question to understand if I am interested in earrings, necklaces, pendants, bracelets, watches or rings.
- If I have mentioned category type, then respond to my STATEMENT by providing sizing guide only regarding the preferred category.
"""
+ DO_NOT_RECOMMEND_PRODUCT
+ CRITICAL_RULES
+ NEXT
)

HUMAN_MESSAGE_COMPANY_SIZE_HELP_HANDLER = (
""" 
BASED ON:\n
CONVERSATION MEMORY:\n{conversation_memory}\n\n
CONTEXT:\n{context}\n\n
Respond to my STATEMENT:\n\n{customer_query}
"""
)