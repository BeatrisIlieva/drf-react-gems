from src.chatbot.prompts.base import CONTEXT, CONVERSATION_ANALYST, CRITICAL_RULES, ROLE, WHO_AM_I

BUILD_CONVERSATION_SUMMARY_SYSTEM_MESSAGE = (
f"""
{CONVERSATION_ANALYST}
<next>
1. Analyze the provided CONVERSATION HISTORY. It consists of chronologically arranged customer-assistant conversation transcripts.
2. Create a summary of the CONVERSATION HISTORY extracting the information that our sales consultant (assistant) will need to handle the customer further.
3. Do not assume or invent anything beyond what is explicitly stated into the CONVERSATION HISTORY.
3. Return only the conversation summary as plain text.
</next>
"""
)

BUILD_CONVERSATION_SUMMARY_HUMAN_MESSAGE = (
""" 
CONVERSATION HISTORY: {conversation_history}
"""
)

EXTRACT_CUSTOMER_PREFERENCE_SYSTEM_MESSAGE = (
f"""
{CONVERSATION_ANALYST}
<next>
1. Analyze the provided CUSTOMER QUERY. 
2. If a required value cannot be definitively determined from the CUSTOMER QUERY, include the key in the schema and set its value to an empty string (""). 
3. Do not make assumptions or infer values beyond what is explicitly stated in the conversation summary.
</next>
"""
)

EXTRACT_CUSTOMER_PREFERENCE_HUMAN_MESSAGE = (
""" 
CUSTOMER QUERY: {optimized_query}\n
INSTRUCTIONS: {instructions}
"""
)

BUILD_DISCOVERY_QUESTION_SYSTEM_MESSAGE = (
f""" 
{CONTEXT}\n
{WHO_AM_I}\n 
{ROLE}\n
<next>
1. Analyze the CONVERSATION SUMMARY to get to know the customer.
2. Analyze the CUSTOMER PREFERENCES and identify empty fields (those with no value after the colon).
3. Formulate a targeted strategic question to gather only the missing information needed to complete their jewelry preferences.
4. Return only the targeted strategic question.
</next>
{CRITICAL_RULES}
"""
)

BUILD_DISCOVERY_QUESTION_HUMAN_MESSAGE = (
""" 
CONVERSATION SUMMARY: \n{conversation_summary}\n
CUSTOMER PREFERENCES: {customer_preferences}
"""
)

BUILD_OPTIMIZED_SEARCH_QUERY_SYSTEM_MESSAGE = f"""
{CONVERSATION_ANALYST}
<goal>
Your goal is to formulate targeted search queries that will retrieve the most relevant product from our jewelry catalog by performing a vector search (RAG).
</goal>

<context>
<product_structure>
Our vector database contains individual product entries with this exact structure:
Collection: [name]; Stone: [type]; Metal: [type]; Category: [type]; Product ID: [number]; Image URL: [url]; Sizes: Size: Small - Price: $X.XX, Size: Medium - Price: $X.XX, Size: Large - Price: $X.XX; Description: [detailed description]; Target Gender: [F/M]; Average Rating: [X.X]/5 stars;
</product_structure>

<product_catalog_structure>
- Collections: Daisy, Sunflower, Forget Me Not, Gerbera, Berry, Lotus, Drop, Lily (all Female), Elegance, Classics (Female), Midnight, Ocean (Male)
- Categories: earrings, necklaces, pendants, rings, bracelets, watches
- Metals: Platinum, Rose Gold, Yellow Gold  
- Stones: White Diamond, Red Ruby, Green Emerald, Blue Sapphire, Pink Sapphire, Yellow Sapphire, Blue Aquamarine
- Target Gender: F (Female), M (Male)
- Sizes: Small, Medium, Large
- Price Range: $1,500 - $21,700
- Ratings: 3.2 - 4.7 stars out of 5
</product_catalog_structure>
</context>

<next>
1. Examine the conversation summary to determine the precise product characteristics the customer is interested in.
2. Generate ONE optimized search query that will retrieve a product matching the customer's preferences.
3. Return only the optimized search query without explanation or additional text.
</next>
"""

BUILD_OPTIMIZED_SEARCH_QUERY_HUMAN_MESSAGE = (
""" 
CONVERSATION SUMMARY: {conversation_summary}
"""
)

INTENT_CLASSIFICATION_SYSTEM_MESSAGE = (
f"""
{CONVERSATION_ANALYST}
<next>
Analyze the CONVERSATION SUMMARY (customer-assistant conversation) to determine the current intent of the customer.
</next>
"""
)

INTENT_CLASSIFICATION_HUMAN_MESSAGE = (
""" 
CONVERSATION SUMMARY: {conversation_summary}\n
INSTRUCTIONS: {format_instructions}\n
"""
)

EXTRACT_FILTERED_PRODUCTS_SYSTEM_MESSAGE = (
f""" 
{CONVERSATION_ANALYST}
<next>
1. Analyze the CONVERSATION SUMMARY (customer-assistant conversation) to determine the customer needs and preferences.
2. Analyze CUSTOMER_PREFERENCES to identify the exact characteristics the customer is seeking in a product.
3. Analyze the provided PRODUCTS descriptions.
4. Choose the most suitable product for the customer needs and preferences.
- Connect product features to customer specific situation
- For gifts: Consider relationship stage and appropriateness (new relationships: consider pendants/earrings over rings, established relationships: consider meaningful, personal pieces)
3. Populate the schema with the characteristics of the exact product you have chosen.
</next>
"""
)

EXTRACT_FILTERED_PRODUCTS_HUMAN_MESSAGE = (
""" 
CONVERSATION SUMMARY:\n {conversation_summary}\n
CUSTOMER_PREFERENCES:\n {customer_preferences}\n
PRODUCTS:\n {products}\n
INSTRUCTIONS: {format_instructions}
"""
)