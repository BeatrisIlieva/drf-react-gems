from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

# ====================================== 
# Chain 1: Customer Intent Classification
# ======================================
class CustomerIntent(BaseModel):
    intent_type: str = Field(description="browsing, gift_purchase, self_purchase, information_request, off_topic")
    confidence: float = Field(description="Confidence score 0-1")
    extracted_info: dict = Field(description="Key details mentioned by customer")
    
intent_parser = PydanticOutputParser(pydantic_object=CustomerIntent)

print(intent_parser.get_format_instructions())