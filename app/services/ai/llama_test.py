from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

if __name__ == "__main__":

    model = ChatOllama(model='llama3.2-vision:11b')

    propmt = ChatPromptTemplate.from_template("""
        あなたは親切なAIアシスタントです。
        ユーザーの質問にできるだけ詳しく日本語で回答してください。
        質問: {question}
    """)


    chain = propmt | model | StrOutputParser()

    output = chain.invoke({"question" : "あなたはだれですか"} )
    print(output)