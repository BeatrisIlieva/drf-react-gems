import os

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "store_fact",
            "description": "Store personal information when users share details about themselves - including but not limited to name, age, location, profession, preferences, interests, family, goals, hobbies, plans, desires, or any other personal details they mention.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Type of info (name, age, location, etc.)"},
                    "value": {"type": "string", "description": "The actual information"}
                },
                "required": ["key", "value"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "recall_fact",
            "description": "Retrieve stored user information when they ask direct questions about themselves - including but not limited to name, age, location, profession, preferences, interests, family, goals, hobbies, plans, desires, or any other personal details they mention, or when their personal details would help provide a more relevant response.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "What to look for"}
                },
                "required": ["query"]
            }
        }
    }
]

SYSTEM_MESSAGE = """
You are a friendly, helpful assistant. 

CRITICAL:
You responsibility is to answer questions regarding either the data that you can find into the provided context or information that the user had shared with you.

if the questions that the users asks about is not part of the provided context, then you must respond with 'i do not know.
"""

MEMORY_FILE = os.path.join(
    os.path.dirname(__file__),
    "memory.json",
)

CHAT_HISTORY_FILE = os.path.join(
    os.path.dirname(__file__),
    "chat_history.json",
)


"""
You must NOT provide with information in one of two cases:
IMPORTANT: 
- In this cases be into the role of a cool but polite person. Formulate the response based on the question. Do not ask clarifying questions. Do no suggest further assistance. Do not guess. 
- Remember that you are here to provide information about the context provided and that we collect the personal information that users share in order to provide personalized answers about the context.
1. The information that the user asks you is not related personally to themselves, or it is but they had not shared such information with you so far.
2. The information that the user asks you is NOT part of the provided context.

If the user asks questions that require both their personal information AND document knowledge from the context, then combine both sources to give a personalized answer.
You must keep responses under 70 words. 
It is very important, to always end with a complete sentence without cutting off mid-thought, mid-paragraph, or mid-sentence.

If the user had asked you the same question previously, even if they had formulated the question in a different way:
1. Then you should use words like 'as mentioned, as discussed, as noted etc.'.
2. You must respond the question briefly. Your response should consists of NO more than 3-4 words.

If the user provides you with information about themselves, then be into the role of a cool but polite person. Formulate a response based on the question.
"""