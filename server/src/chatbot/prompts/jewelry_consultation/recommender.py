from src.chatbot.prompts.base import CRITICAL_RULES, CONTEXT, GOAL, NEXT, ROLE_CONCISE, WHO_AM_I


SYSTEM_MESSAGE_RECOMMENDER = (
CONTEXT +
ROLE_CONCISE +
WHO_AM_I +
GOAL + 
"""
<task>
Recommend the PRODUCT TO RECOMMEND by using the described format.
</task>

<product_recommendation>
1. Include its image url and link to the product page using Markdown format for display in the chat. 
2. Extract the necessary details (collection, category, stone, metal, description, target gender, size, price, average rating, product ID, image URL) directly from the context that correspond to THAT SPECIFIC product.
3. Use the Image URL as the display image. 
4. Do not include anything else into your response except the content into the recommendation_format tag

<recommendation_format>
**Collection Name Category**: brief emotional benefit
[![[Collection Name] [Category]](image_url_from_context)](http://localhost:5173/products/[category_lowercase_plural]/[product_id]/)
</recommendation_format>
</product_recommendation>
"""
+ CRITICAL_RULES
+ NEXT
)

HUMAN_MESSAGE_RECOMMENDER  = (
"""
BASED ON:\n
1. CONVERSATION MEMORY:\n{conversation_memory}\n\n
2. MY PREFERENCES:
- I am buying the jewelry as a: {purchase_type}
- The gender of the person who will be wearing the jewelry is: {gender}
- The product category I am interested is: {category}
- The metal type I am interested is: {metal_type}
- The stone type I am interested is: {stone_type}
\n\n
3. PRODUCT TO RECOMMEND:\n{product_to_recommend}\n\n
Respond to my STATEMENT by recommending me the PRODUCT TO RECOMMEND.\n\n
4. STATEMENT:\n{customer_query}
"""
)