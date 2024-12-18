from typing import TypedDict, Annotated, Sequence
from langgraph.graph import Graph, MessageGraph
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# 상태를 관리하기 위한 TypedDict 정의
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    next: str | None

# 채팅 모델 초기화
model = ChatOllama(model='llama3.2-vision:11b')

# 기본 프롬프트 템플릿 설정
prompt = ChatPromptTemplate.from_messages([
    ("system", "あなたは親切なAIアシスタントです。ユーザーの質問に丁寧に日本語で回答してください。"),
    ("human", "{input}")
])

# AI 응답을 처리하는 함수
async def ai_response(state: AgentState) -> AgentState:
    messages = state["messages"]
    response = await model.ainvoke(messages)
    return {
        "messages": [*messages, response],
        "next": None
    }

# 그래프 생성
workflow = Graph()

# 노드 추가
workflow.add_node("ai", ai_response)

# 엣지 설정
workflow.set_entry_point("ai")

# 실행 가능한 그래프로 컴파일
chain = workflow.compile()

# 사용 예시
if __name__ == "__main__":
    messages = [HumanMessage(content="こんにちは！")]
    result = chain.invoke({
        "messages": messages,
        "next": "ai"
    })
    print(result["messages"][-1].content)
