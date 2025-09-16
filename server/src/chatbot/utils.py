import re
import json

from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser


def generate_formatted_response(
    llm,
    system_message,
    human_message,
    response_format,
    response_model=None,
    **kwargs
):
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
    
    def get_and_format_customer_preferences():
        customer_preferences = json.loads(re.sub(
                r'```json\s*|\s*```', '',
                llm.invoke(messages).content
            ).strip())
        
        if isinstance(customer_preferences, dict) and 'properties' in customer_preferences:
            customer_preferences = customer_preferences['properties']
            
        return customer_preferences

    response_format_mapper = {
        # 'extract_and_strip_ai_response_content':
        # lambda: json.loads(re.sub(
        #     r'```json\s*|\s*```', '',
        #     llm.invoke(messages).content
        # ).strip()),
        'extract_and_strip_ai_response_content':
        get_and_format_customer_preferences,

        'extract_ai_response_content':
        lambda: llm.invoke(messages).content,

        'destructure_messages':
        lambda: (messages[0], messages[1])
    }

    return response_format_mapper[response_format]()


def retrieve_relevant_content(vectorstore, query, k=4):
    results = vectorstore.similarity_search(query, k=k)
    context = '\n'.join(result.page_content for result in results)

    return context.strip()
