from langchain_community.tools import DuckDuckGoSearchResults
from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables.history import RunnableWithMessageHistory
import config
from history_manager import HistoryManager

class AgentHandler:
    search = DuckDuckGoSearchResults()
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. For answering the user query, look for information in DuckDuckGo Search and Wikipedia and then give the final result"),
        ("placeholder", "{history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)
    tools = [search, wikipedia]
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    @staticmethod
    def ask_question(question: str):
        agent_with_history = RunnableWithMessageHistory(AgentHandler.agent_executor, HistoryManager.get_history, input_messages_key="input", history_messages_key="history")
        return agent_with_history.invoke({"input": question}, config={"configurable": {"session_id": "sess1"}})