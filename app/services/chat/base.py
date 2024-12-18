from ..ai.chains.chain import chain


async def chat(question: str):
    return chain.invoke({"question": question})
