from langchain_core.prompts import ChatPromptTemplate

prompt_template = """
    あなたは優秀なAI要約アシスタントです。
    1回の質問と回答をみて文脈を30文字以内に要約してタイトルを作成してください。
    
    質問: {user_question}
    回答: {ai_answer}

    たいとる: 
"""

prompt = ChatPromptTemplate.from_template(prompt_template)
