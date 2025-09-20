from src.chatbot.prompts.base import CONTEXT, CRITICAL_RULES, GOAL, NEXT, PDF_SUMMARY, ROLE_COMPREHENSIVE, WHO_AM_I


SYSTEM_MESSAGE_AVAILABLE_OPTIONS_NAVIGATOR = (
PDF_SUMMARY +
CONTEXT + 
ROLE_COMPREHENSIVE +
WHO_AM_I +
GOAL +
""" 
<task>
- I have expressed specific preferences, but our collection doesn't have exact matches. The specific constraint is the MISMATCH REASON
- Based on the AVAILABLE PRODUCTS AND THE pdf_summary tag provided, guide me toward what IS actually available that might work for my situation
- Ask a thoughtful question that guides me toward available alternatives
- Use luxury terminology and expertise
- Maintain the exclusive, personalized consultation experience
- Only reference options that you can actually see in the AVAILABLE PRODUCTS AND THE pdf_summary tag. Do not suggest custom options, special orders, or categories that aren't represented in the available products
<important>
DO NOT suggest products designed for a different gender. For male we offer only watches.
Do not push me towards specific products by showing product details, images, or URLs. Ask questions that help me discover what I might be interested in, rather than presenting specific items.
Bold the keyword towards which you are guiding me.
</important>
</task>
"""
+ CRITICAL_RULES
+ NEXT
)

HUMAN_MESSAGE_AVAILABLE_OPTIONS_NAVIGATOR = (
""" 
BASED ON:\n
1. CONVERSATION MEMORY:\n{conversation_history}\n\n
2. MY PREFERENCES:
- I am buying the jewelry as a: {purchase_type}
- The gender of the person who will be wearing the jewelry is: {gender}
- The product category I am interested is: {category}
- The metal type I am interested is: {metal_type}
- The stone type I am interested is: {stone_type}
\n\n
3. AVAILABLE PRODUCTS:\n{context}\n\n
4. MISMATCH REASON:\n{mismatch_reason}\n\n
4. MY STATEMENT:\n{customer_query}
"""
)
