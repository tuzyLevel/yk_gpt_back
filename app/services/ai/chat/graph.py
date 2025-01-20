import os
import asyncio
from typing import List, Dict, Any, Generator, TypedDict
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from socketio.async_server import AsyncServer

# from app.schemas.chat import ChatLine
from pydantic import BaseModel, Field


class ChatLine(BaseModel):
    key: str = Field(..., description="chat key")
    chat_id: str | None = Field(None, description="chat_id")
    writer: str = Field(..., description="sender")
    message: str = Field(..., description="message from sender")


# Google Gemini 모델 설정
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.7)


class GraphState(TypedDict):
    __async_server: AsyncServer | None
    chat_id: str = ""
    previous_chatlines: List[BaseMessage]
    chatline: ChatLine


config = {"configurable": {"thread_id": 1}}


async def generate_answer(state: GraphState):
    try:
        if not state["chatline"].message:
            return {}  # 메시지가 없으면 빈 배열 반환

        messages = state["previous_chatlines"] + [
            HumanMessage(content=state["chatline"].message)
        ]
        full_response = ""
        async for chunk in model.astream(messages):
            full_response += chunk.content
            print(chunk)
        # 응답 메시지를 state에 추가하는 로직이 필요합니다.  아래는 예시입니다. 실제 응답 형식에 맞춰 수정해야 합니다.
        # state["previous_chatlines"].append(
        #     HumanMessage(content=state["chatline"].message)
        # )
        # state["previous_chatlines"].append(AIMessage(content=full_response))
        return {"previous_chatlines": []}

    except Exception as e:
        print(f"Error in generate_answer: {e}")
        return {"previous_chatlines": []}


graph = StateGraph(GraphState)

# graph.add_node(load_previous_chat, "load_previous_chat")
graph.add_node(generate_answer, "generate_answer")

# graph.add_edge("load_previous_chat", "generate_answer")
graph.add_edge("generate_answer", END)

# graph.set_entry_point("load_previous_chat")
graph.set_entry_point("generate_answer")

compiled_graph = graph.compile()


if __name__ == "__main__":
    asyncio.run(
        compiled_graph.ainvoke(
            GraphState(
                previous_chatlines=[
                    HumanMessage(content="내 이름은 Park, 31살"),
                    AIMessage(content="반갑습니다! Park!"),
                ],
                chatline=ChatLine(
                    key="asdfasdfadf",
                    chat_id="sdlkjgklsdfg",
                    writer="park",
                    message="내 나이와 이름은?",
                ),
            ),
        )
    )
