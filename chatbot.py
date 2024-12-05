import streamlit as st
from agent_handler import AgentHandler
from history_manager import HistoryManager

st.set_page_config(page_title="Rohith Chatbot")
st.title("Chat App")

question = st.text_input("Question: ")
btn = st.button("Find Answer")

st.sidebar.markdown("# History")

if btn:
    result = AgentHandler.ask_question(question)
    answer = result["output"]
    st.write(answer)
    
    history = HistoryManager.get_history("sess1")
    HistoryManager.display_history(history)
