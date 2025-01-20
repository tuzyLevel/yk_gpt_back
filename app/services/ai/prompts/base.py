from langchain_core.prompts import ChatPromptTemplate
from .example import output_example

prompt_template = """
    あなたは優秀なAI事務職アシスタントです。ユーザーの質問に対してできるだけ詳しく説明してください。
    回答の例を参照して形式を守って回答してください。
    回答の例:{output_example}

    質問: {message}
    回答: 
"""

prompt = ChatPromptTemplate.from_template(prompt_template)
prompt = prompt.partial(output_example=output_example)
