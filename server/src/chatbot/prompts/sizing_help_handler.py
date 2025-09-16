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
1. CONVERSATION MEMORY:\n{conversation_memory}\n\n
2. I am buying the jewelry as a: {purchase_type}
3. The gender of the person who will be wearing the jewelry is: {gender}
4. The product category I am interested is: {category}
5. The metal type I am interested is: {metal_type}
6. The stone type I am interested is: {stone_type}
7. The budget I have in mind is: {budget_range}\n\n
8. CONTEXT:\n{context}\n\n
Respond to my STATEMENT:\n\n{customer_query}
"""
)