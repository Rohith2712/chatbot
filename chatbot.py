from langchain_community.tools import DuckDuckGoSearchResults
from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
os.environ['GOOGLE_API_KEY']='AIzaSyAZ2gCeGU1jEj4t0uB2jmjZNtlZUTb_n1c'

llm = ChatGoogleGenerativeAI(model="gemini-pro",convert_system_message_to_human=True)

search = DuckDuckGoSearchResults()
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())


#agents code
from langchain.agents import AgentExecutor,create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system","You are a helpful AI assistant. For answering the user query, look for information in duckduckgo Search and wikipedia and then give the final result"),
    ("placeholder","{history}"),
    ("human","{input}"),
    ("placeholder","{agent_scratchpad}")
]
)
tools = [search,wikipedia]
llm = ChatGoogleGenerativeAI(model="gemini-pro",convert_system_message_to_human=True)
agent = create_tool_calling_agent(llm,tools,prompt) #create agent
agent_executor = AgentExecutor(agent=agent,tools=tools,verbose=True) #to run agent
# agent_executor.invoke({"input":"when did virat kohli born?"})


#session storage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import streamlit as st
from langchain.schema import HumanMessage, AIMessage

if "store" not in st.session_state:
    st.session_state.store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = ChatMessageHistory()
    return st.session_state.store[session_id]



agent_with_history = RunnableWithMessageHistory(agent_executor,get_session_history,input_messages_key="input",history_messages_key="history")



st.set_page_config(page_title="Rohith Chatbot")
st.title("Chat App")


question = st.text_input("Question: ")

btn = st.button("Find Answer")
st.sidebar.markdown("# History")
if btn:
    result = agent_with_history.invoke({"input": question}, config={"configurable": {"session_id": "sess1"}})
    answer = result["output"]
    st.write(answer)
    history = st.session_state.store['sess1']
    messages = history.messages
    questions = []
    answers = []
    for i in range(0, len(messages), 2): 
        question = messages[i].content if isinstance(messages[i], HumanMessage) else None
        answer = messages[i + 1].content if isinstance(messages[i + 1], AIMessage) else None
        # Append question and answer to the respective lists
        if question and answer:
            questions.append(question)
            answers.append(answer)
    for q, a in zip(questions, answers):
        st.sidebar.write(f"**Q:** {q}")
        st.sidebar.write(f"**A:** {a}")
        st.sidebar.write("---") 