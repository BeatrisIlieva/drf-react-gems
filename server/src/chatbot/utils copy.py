import re

from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser


def generate_formatted_response(llm, system_message, human_message, response_format, response_model=None, **kwargs):
    if response_model:
        instructions = PydanticOutputParser(
            pydantic_object=response_model
        ).get_format_instructions()

        kwargs['instructions'] = instructions

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            system_message
        ),
        HumanMessagePromptTemplate.from_template(
            human_message
        ),
    ])

    messages = prompt.format_messages(**kwargs)

    response_format_mapper = {
        'extract_and_strip_ai_response_content':
        lambda: re.sub(
            r'```json\s*|\s*```', '',
            llm.invoke(messages).content
        ).strip(),

        'extract_ai_response_content':
        lambda: llm.invoke(messages).content,

        'destructure_messages':
        lambda: (messages[0], messages[1])
    }

    return response_format_mapper[response_format]()


def get_classification_json(llm, optimized_query, system_message, human_message, classification):
    parser = PydanticOutputParser(pydantic_object=classification)
    instructions = parser.get_format_instructions()

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            system_message),
        HumanMessagePromptTemplate.from_template(
            human_message),
    ])

    messages = prompt.format_messages(
        optimized_query=optimized_query,
        instructions=instructions,
    )

    ai_response = llm.invoke(messages).content

    return re.sub(r'```json\s*|\s*```', '', ai_response).strip()


def get_filtered_product(llm, conversation_summary, customer_preferences, products, system_message, human_message, classification):
    parser = PydanticOutputParser(pydantic_object=classification)
    instructions = parser.get_format_instructions()

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            system_message),
        HumanMessagePromptTemplate.from_template(
            human_message),
    ])

    messages = prompt.format_messages(
        conversation_summary=conversation_summary,
        customer_preferences=customer_preferences,
        products=products,
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
        conversation_summary=conversation_summary,
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
        conversation_summary=conversation_summary,
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
        conversation_summary=conversation_summary,
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

def create_prompt(system_message, human_message):
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            system_message
        ),
        HumanMessagePromptTemplate.from_template(
            human_message
        ),
    ])


def create_messages(llm, prompt, **kwargs):
    messages = prompt.format_messages(**kwargs)

    return llm.invoke(messages)


def create_formatted_instructions(model_name):
    parser = PydanticOutputParser(pydantic_object=model_name)

    return parser.get_format_instructions()


def strip_ai_response(ai_response):
    return re.sub(r'```json\s*|\s*```', '', ai_response.content).strip()
