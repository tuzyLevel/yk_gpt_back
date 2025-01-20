from .model import gemini_llm
from .prompt import prompt
from .output_parser import output_parser


chain = prompt | gemini_llm | output_parser
