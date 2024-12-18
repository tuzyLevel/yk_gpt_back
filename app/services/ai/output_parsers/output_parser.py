from langchain.output_parsers import PydanticOutputParser
from app.api.chat.schema import ResponseChat

parser = PydanticOutputParser(pydantic_object=ResponseChat)
