import re

from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser


def generate_formatted_response(llm, system_message_template, human_message_template, response_format, response_model=None, **kwargs):
    if response_model:
        instructions = PydanticOutputParser(
            pydantic_object=response_model
        ).get_format_instructions()

        kwargs['instructions'] = instructions

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            system_message_template
        ),
        HumanMessagePromptTemplate.from_template(
            human_message_template
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


def retrieve_relevant_content(vectorstore, query, k=4):
    results = vectorstore.similarity_search(query, k=k)
    context = '\n'.join(result.page_content for result in results)

    return context.strip()
