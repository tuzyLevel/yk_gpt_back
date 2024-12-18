from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain.schema import HumanMessage
import getpass
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini", )

# Define a new graph
workflow = StateGraph(state_schema=MessagesState)


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str




config = {"configurable": {"thread_id": "abc123"}}


prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability in {{language}}.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)



# Define the function that calls the model
def call_model(state: State):
    prompt = prompt_template.invoke(state)
    response = model.invoke(prompt)
    return {"messages": [response]}


# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

if __name__ == "__main__":
    query = "Hi! I'm Bob."
    language = 'Korean'

    input_messages = [HumanMessage(content=query)]
    output = app.invoke({"messages": input_messages, "language": language}, config)
    output["messages"][-1].pretty_print()  # output contains all messages in state