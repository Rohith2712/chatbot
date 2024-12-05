import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain.schema import HumanMessage, AIMessage

class HistoryManager:
    @staticmethod
    def get_history(session_id: str) -> BaseChatMessageHistory:
        if "store" not in st.session_state:
            st.session_state.store = {}
        if session_id not in st.session_state.store:
            st.session_state.store[session_id] = ChatMessageHistory()
        return st.session_state.store[session_id]
    
    @staticmethod
    def display_history(history: BaseChatMessageHistory):
        messages = history.messages
        questions = []
        answers = []
        for i in range(0, len(messages), 2): 
            question = messages[i].content if isinstance(messages[i], HumanMessage) else None
            answer = messages[i + 1].content if isinstance(messages[i + 1], AIMessage) else None
            if question and answer:
                questions.append(question)
                answers.append(answer)
        for q, a in zip(questions, answers):
            st.sidebar.write(f"**Q:** {q}")
            st.sidebar.write(f"**A:** {a}")
            st.sidebar.write("---")
