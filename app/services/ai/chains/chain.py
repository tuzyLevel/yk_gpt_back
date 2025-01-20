from ..llms.llms import gemini_llm
from ..prompts.base import prompt
from ..output_parsers.output_parser import parser
from langchain_core.runnables import RunnableSerializable


chain = prompt | gemini_llm | parser


class AIService:
    def __init__(self, llm=gemini_llm, prompt=prompt, output_parser=parser):
        self.llm = llm
        self.prompt = prompt
        self.output_parser = output_parser
        self.chain: RunnableSerializable = prompt | llm | output_parser

    async def chat(self, message: str):
        async for item in self.chain.astream({"message": message}):
            temp = item.model_dump()
            print(temp)
            yield temp
