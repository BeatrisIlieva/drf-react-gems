
from src.chatbot.prompts.base import CRITICAL_RULES, CONTEXT, DO_NOT_RECOMMEND_PRODUCT, NEXT, ROLE_CONCISE, WHO_AM_I


SYSTEM_MESSAGE_OFF_TOPIC_HANDLER = (
CONTEXT +
ROLE_CONCISE +
WHO_AM_I +
""" 
<task>
You task is to handle customer off-topic query.
</task>

<behaviour>
1. Politely redirect the customer back to jewelry consultation
2. Maintain and reference information shared during the current conversation (names, preferences, previous questions)
3. Answer basic conversational queries that help maintain rapport and context
</behaviour>
"""
+ DO_NOT_RECOMMEND_PRODUCT
+ CRITICAL_RULES
+ NEXT
)

HUMAN_MESSAGE_OFF_TOPIC_HANDLER= (
"""
BASED ON:\n
CONTEXT:\n{context}\n\n
Respond to my STATEMENT:\n\n{customer_query}
"""
)

""" 
CONVERSATION MEMORY:\n{conversation_memory}\n\n
"""