from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from langchain.agents import Tool
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

class AgentInput(BaseModel):
    """Agent 입력을 위한 기본 모델"""
    query: str
    context: Optional[Dict[str, Any]] = None

class AgentOutput(BaseModel):
    """Agent 출력을 위한 기본 모델"""
    response: str
    thought_process: Optional[str] = None
    used_tools: Optional[List[str]] = None
    error: Optional[str] = None

class BaseAIAgent(ABC):
    """AI Agent를 위한 기본 클래스"""
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        verbose: bool = False
    ):
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.verbose = verbose
        self.tools = self._get_tools()
        self.chain = self._create_chain()

    @abstractmethod
    def _get_tools(self) -> List[Tool]:
        """Agent가 사용할 도구들을 정의"""
        pass

    @abstractmethod
    def _create_chain(self) -> LLMChain:
        """Agent의 추론 체인을 생성"""
        pass

    @abstractmethod
    def input_prompt(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """입력 프롬프트 생성"""
        pass

    @abstractmethod
    async def process(self, input_data: AgentInput) -> AgentOutput:
        """입력을 처리하고 결과를 반환"""
        pass

    def _format_thought_process(self, thoughts: List[str]) -> str:
        """사고 과정을 포맷팅"""
        return "\n".join([f"- {thought}" for thought in thoughts])

    def _handle_error(self, error: Exception) -> AgentOutput:
        """에러 처리"""
        return AgentOutput(
            response="처리 중 오류가 발생했습니다.",
            error=str(error)
        )

class ResearchAgent(BaseAIAgent):
    """리서치 작업을 수행하는 Agent"""
    
    def _get_tools(self) -> List[Tool]:
        return [
            Tool(
                name="Search",
                func=self._search,
                description="인터넷에서 정보를 검색합니다."
            ),
            Tool(
                name="Summarize",
                func=self._summarize,
                description="긴 텍스트를 요약합니다."
            )
        ]

    def _create_chain(self) -> LLMChain:
        prompt = PromptTemplate(
            input_variables=["query", "context"],
            template="""
            다음 질문에 대해 리서치를 수행하세요:
            질문: {query}
            
            컨텍스트:
            {context}
            
            단계별로 접근하여 답변을 작성하세요.
            """
        )
        return LLMChain(llm=self.llm, prompt=prompt)

    def input_prompt(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        context_str = "\n".join([f"{k}: {v}" for k, v in (context or {}).items()])
        return f"Query: {query}\nContext: {context_str}"

    async def process(self, input_data: AgentInput) -> AgentOutput:
        try:
            # 사고 과정 기록
            thoughts = []
            
            # 검색 수행
            thoughts.append("관련 정보 검색 중...")
            search_results = await self._search(input_data.query)
            
            # 결과 요약
            thoughts.append("검색 결과 요약 중...")
            summary = await self._summarize(search_results)
            
            # 최종 응답 생성
            thoughts.append("최종 응답 생성 중...")
            response = await self.chain.arun(
                query=input_data.query,
                context=summary
            )
            
            return AgentOutput(
                response=response,
                thought_process=self._format_thought_process(thoughts),
                used_tools=["Search", "Summarize"]
            )
            
        except Exception as e:
            return self._handle_error(e)

    async def _search(self, query: str) -> str:
        """검색 기능 구현"""
        # 실제 검색 로직 구현 필요
        pass

    async def _summarize(self, text: str) -> str:
        """요약 기능 구현"""
        # 실제 요약 로직 구현 필요
        pass