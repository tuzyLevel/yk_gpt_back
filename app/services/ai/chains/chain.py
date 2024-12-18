from ..llms.llms import gemini_llm
from ..prompts.base import prompt
from ..output_parsers.output_parser import parser


chain = prompt | gemini_llm | parser
