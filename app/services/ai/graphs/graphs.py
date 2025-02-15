from typing import Annotated, TypedDict, List
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from ..chains.chain import chain

# from langgraph.checkpoint.postgres import PostgresSaver


class ChatState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    current_step: str
    memory: dict
    session_id: str


# checkpointer = PostgresSaver(
#     table_name="chat_state",
#     checkpoint_id_column="session_id",
#     checkpoint_data_column="memory",
# )

graph_builder = StateGraph(ChatState)


async def process_message(state: ChatState) -> ChatState:
    messages = state["messages"]
    response = await chain.ainvoke(messages)

    print(response)

    # response가 BaseMessage 타입인지 확인하고 변환
    if not isinstance(response, BaseMessage):
        response = AIMessage(content=str(response))

    return {"messages": messages + [response], "current_step": "complete"}


# 그래프 빌더 생성
graph_builder = StateGraph(ChatState)

# 노드 추가
graph_builder.add_node("process", process_message)

# 엣지 설정
graph_builder.set_entry_point("process")
graph_builder.add_edge("process", END)

# 그래프 컴파일
graph = graph_builder.compile()


async def run_chat(message: str):
    result = await graph.ainvoke(
        {"messages": [HumanMessage(content=message)], "current_step": "process"}
    )
    return {"answer": result["messages"][-1].content}
