from typing import Any, Dict, List, Optional, Sequence

from langchain.agents.agent import AgentExecutor, BaseSingleActionAgent
from langchain.agents.agent_toolkits.sql.prompt import (
    SQL_FUNCTIONS_SUFFIX,
    SQL_PREFIX,
    SQL_SUFFIX,
)
from langchain.agents.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.agents.mrkl.base import ZeroShotAgent
from langchain.agents.mrkl.prompt import FORMAT_INSTRUCTIONS
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.callbacks.base import BaseCallbackManager
from langchain.chains.llm import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema.language_model import BaseLanguageModel
from langchain.schema.messages import AIMessage, SystemMessage
from langchain.tools import BaseTool
from langchain.schema.messages import BaseMessage


def create_sql_agent_custom(
    llm: BaseLanguageModel,
    toolkit: SQLDatabaseToolkit,
    agent_type: AgentType = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    callback_manager: Optional[BaseCallbackManager] = None,
    prefix: str = SQL_PREFIX,
    suffix: Optional[str] = None,
    format_instructions: str = FORMAT_INSTRUCTIONS,
    input_variables: Optional[List[str]] = None,
    top_k: int = 10,
    max_iterations: Optional[int] = 15,
    max_execution_time: Optional[float] = None,
    early_stopping_method: str = "force",
    verbose: bool = False,
    agent_executor_kwargs: Optional[Dict[str, Any]] = None,
    extra_tools: Sequence[BaseTool] = (),
    messages: Sequence[BaseMessage]= None,
    chatHistory: str=None,
    **kwargs: Dict[str, Any],
) -> AgentExecutor:
    """Construct an SQL agent from an LLM and tools."""
    tools = toolkit.get_tools() + list(extra_tools)
    prefix = prefix.format(dialect=toolkit.dialect, top_k=top_k)
    agent: BaseSingleActionAgent
    input_variables = ["input", "agent_scratchpad"]
    _prompt = ChatPromptTemplate(input_variables=input_variables, messages=messages)
    
    agent = OpenAIFunctionsAgent(
            llm=llm,
            prompt=_prompt,
            tools=tools,
            callback_manager=callback_manager,
            **kwargs,
        )
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        callback_manager=callback_manager,
        verbose=verbose,
        max_iterations=max_iterations,
        max_execution_time=max_execution_time,
        early_stopping_method=early_stopping_method,
        **(agent_executor_kwargs or {}),
    )