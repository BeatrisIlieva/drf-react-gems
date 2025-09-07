import re
import json

from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

from langchain.output_parsers import PydanticOutputParser


def build_conversation_history(conversation_state, customer_query, max_messages=20):
    """
    Build conversation history with the last max_messages customer-AI message pairs.

    Args:
        conversation_state: Dictionary containing the conversation state with messages.
        customer_query: The current customer query to append.
        max_messages: Maximum number of previous message pairs to include (default: 3).

    Returns:
        List of strings representing the conversation history.

    Raises:
        ValueError: If the number of customer and AI messages is not equal.
    """
    conversation_history = []
    messages = conversation_state['channel_values']['messages']

    # Extract customer and assistant messages
    customer_messages = [msg.content.split('INPUT:')[-1].strip()
                         for msg in messages if msg.__class__.__name__ == 'HumanMessage']
    assistant_messages = [msg.content.strip()
                          for msg in messages if msg.__class__.__name__ == 'AIMessage']

    # Validate that customer and assistant messages are paired (equal counts)
    if len(customer_messages) != len(assistant_messages):
        raise ValueError(
            f"Mismatched message counts: {len(customer_messages)} customer messages, "
            f"{len(assistant_messages)} assistant messages. Expected equal counts."
        )

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

    return conversation_history


def get_classification_json(llm, conversation_summary, human_message, system_message, classification):
    parser = PydanticOutputParser(pydantic_object=classification)
    instructions = parser.get_format_instructions()

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            system_message),
        HumanMessagePromptTemplate.from_template(
            human_message),
    ])

    messages = prompt.format_messages(
        conversation_summary='\n'.join(conversation_summary),
        instructions=instructions,
    )

    ai_response = llm.invoke(messages).content

    return re.sub(r'```json\s*|\s*```', '', ai_response).strip()


def create_conversation_summary(llm, conversation_history: str, system_message: str, human_message: str):
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            system_message),
        HumanMessagePromptTemplate.from_template(
            human_message),
    ])

    messages = prompt.format_messages(
        conversation_history='\n'.join(conversation_history),
    )

    ai_response = llm.invoke(messages).content

    return ai_response


def create_enhanced_query(llm, conversation_summary, system_message, human_message):
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            system_message),
        HumanMessagePromptTemplate.from_template(
            human_message),
    ])

    messages = prompt.format_messages(
        conversation_summary='\n'.join(conversation_summary),
    )

    enhanced_query = llm.invoke(messages).content
    # print('enhanced_query', enhanced_query)
    return enhanced_query


def classify_customer_intent(llm, conversation_summary, customer_intent, system_message, human_message):
    intent_parser = PydanticOutputParser(pydantic_object=customer_intent)
    format_instructions = intent_parser.get_format_instructions()
    # print('instructions', format_instructions + '\n\n')

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            system_message),
        HumanMessagePromptTemplate.from_template(
            human_message),
    ])

    messages = prompt.format_messages(
        conversation_summary='\n'.join(conversation_summary),
        format_instructions=format_instructions
    )

    customer_intent = llm.invoke(messages).content

    return customer_intent

def formulate_question_to_discover_customer_preferences(llm, conversation_summary, customer_preferences, system_message, human_message):
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            system_message),
        HumanMessagePromptTemplate.from_template(
            human_message),
    ])

    messages = prompt.format_messages(
        conversation_summary='\n'.join(conversation_summary),
        customer_preferences=customer_preferences,
    )

    ai_response = llm.invoke(messages).content
    
    return ai_response


# def make_product_recommendation(llm, customer_preferences, system_message, human_message):
#     prompt = ChatPromptTemplate.from_messages([
#     SystemMessagePromptTemplate.from_template(
#         system_message),
#     HumanMessagePromptTemplate.from_template(
#         human_message),
# ])

#     messages = prompt.format_messages(
#         conversation_summary='\n'.join(customer_preferences),
#     )

#     ai_response = llm.invoke(messages).content

#     return ai_response