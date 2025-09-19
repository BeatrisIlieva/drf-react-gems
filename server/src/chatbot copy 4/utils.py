# import re
# import json

# from langchain.prompts import ChatPromptTemplate
# from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
# from langchain.output_parsers import PydanticOutputParser


# def build_conversation_history(customer_query, conversation_state, max_messages=30):
#     """
#     Build conversation history with the last max_messages customer-AI message pairs.
#     """
#     if not conversation_state:
#         return [f'{1}. customer: {customer_query};']

#     conversation_history = []
#     messages = conversation_state['channel_values']['messages']

#     # Extract customer and assistant messages
#     customer_messages = [
#         msg.content.split('STATEMENT:')[-1].strip()
#         for msg in messages if msg.__class__.__name__ == 'HumanMessage'
#     ]
#     assistant_messages = [
#         msg.content.strip()
#         for msg in messages if msg.__class__.__name__ == 'AIMessage'
#     ]

#     # Take the last max_messages pairs (or fewer if not enough pairs)
#     num_pairs = len(customer_messages)
#     start_index = max(0, num_pairs - max_messages)

#     # Build history with the most recent message pairs
#     for i in range(start_index, num_pairs):
#         conversation_history.append(
#             f'{i + 1}. customer: {customer_messages[i]}, assistant: {assistant_messages[i]};')

#     # Append the current customer query
#     conversation_history.append(
#         f'{num_pairs + 1}. customer: {customer_query};')

#     return '\n'.join(conversation_history)


# def generate_formatted_response(
#     llm,
#     system_message,
#     human_message,
#     response_format,
#     response_model=None,
#     **kwargs
# ):
#     if response_model:
#         instructions = PydanticOutputParser(
#             pydantic_object=response_model
#         ).get_format_instructions()

#         kwargs['instructions'] = instructions

#     prompt = ChatPromptTemplate.from_messages([
#         SystemMessagePromptTemplate.from_template(
#             system_message
#         ),
#         HumanMessagePromptTemplate.from_template(
#             human_message
#         ),
#     ])

#     messages = prompt.format_messages(**kwargs)

#     def get_and_format_customer_preferences():
#         customer_preferences = json.loads(re.sub(
#             r'```json\s*|\s*```', '',
#             llm.invoke(messages).content
#         ).strip())

#         if isinstance(customer_preferences, dict) and 'properties' in customer_preferences:
#             customer_preferences = customer_preferences['properties']

#         return customer_preferences

#     response_format_mapper = {
#         'extract_and_strip_ai_response_content':
#         get_and_format_customer_preferences,

#         'extract_ai_response_content':
#         lambda: llm.invoke(messages).content,

#         'destructure_messages':
#         lambda: (messages[0], messages[1])
#     }

#     return response_format_mapper[response_format]()





# utils.py - Async Utils
import re
import json
import asyncio
from typing import Dict, Any, Callable
from asgiref.sync import sync_to_async

from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser


async def async_build_conversation_history(customer_query, conversation_state, max_messages=30):
    """
    Build conversation history with the last max_messages customer-AI message pairs.
    """
    return await sync_to_async(build_conversation_history)(
        customer_query, conversation_state, max_messages
    )


def build_conversation_history(customer_query, conversation_state, max_messages=30):
    """
    Build conversation history with the last max_messages customer-AI message pairs.
    """
    if not conversation_state:
        return [f'{1}. customer: {customer_query};']

    conversation_history = []
    messages = conversation_state['channel_values']['messages']

    # Extract customer and assistant messages
    customer_messages = [
        msg.content.split('STATEMENT:')[-1].strip()
        for msg in messages if msg.__class__.__name__ == 'HumanMessage'
    ]
    assistant_messages = [
        msg.content.strip()
        for msg in messages if msg.__class__.__name__ == 'AIMessage'
    ]

    # Take the last max_messages pairs (or fewer if not enough pairs)
    num_pairs = len(customer_messages)
    start_index = max(0, num_pairs - max_messages)

    # Build history with the most recent message pairs
    for i in range(start_index, num_pairs):
        conversation_history.append(
            f'{i + 1}. customer: {customer_messages[i]}, assistant: {assistant_messages[i]};')

    # Append the current customer query
    conversation_history.append(
        f'{num_pairs + 1}. customer: {customer_query};')

    return '\n'.join(conversation_history)


async def async_generate_formatted_response(
    llm,
    system_message,
    human_message,
    response_format,
    response_model=None,
    **kwargs
):
    """Async version of generate_formatted_response"""
    
    if response_model:
        instructions = await sync_to_async(
            lambda: PydanticOutputParser(pydantic_object=response_model).get_format_instructions()
        )()
        kwargs['instructions'] = instructions

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_message),
        HumanMessagePromptTemplate.from_template(human_message),
    ])

    messages = prompt.format_messages(**kwargs)

    async def get_and_format_customer_preferences():
        response = await sync_to_async(llm.invoke)(messages)
        customer_preferences = json.loads(re.sub(
            r'```json\s*|\s*```', '',
            response.content
        ).strip())

        if isinstance(customer_preferences, dict) and 'properties' in customer_preferences:
            customer_preferences = customer_preferences['properties']

        return customer_preferences

    async def extract_ai_response_content():
        response = await sync_to_async(llm.invoke)(messages)
        return response.content

    async def destructure_messages():
        return (messages[0], messages[1])

    response_format_mapper = {
        'extract_and_strip_ai_response_content': get_and_format_customer_preferences,
        'extract_ai_response_content': extract_ai_response_content,
        'destructure_messages': destructure_messages
    }

    return await response_format_mapper[response_format]()