import streamlit as st
import google.generativeai as genai
import os
from htbuilder import div, styles
from htbuilder.units import rem
import time
from PIL import Image
st.set_page_config(
   page_title="AI",
   page_icon=":volleyball:",
   layout="wide"
)

#thiết lập UI
st.html(div(style=styles(font_size=rem(5), line_height=1)))


st.title("AI English Checker")
#nếu có api rồi


if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.text_input("Nhập GEMINI_API_KEY", type = "password")

#-------------------------------
def check_grammar(user_input): 
    if user_input:
        if not api_key:
            st.warning("Please fill in API key")
        elif not user_input:
            st.warning("Please write your sentence")
        else:
            # hiển thị lịch sử
            for message in st.session_state.history_check:
                with st.chat_message(message["role"], avatar = message.get("avatar")):
                    st.markdown(message["content"])

            with st.chat_message("user", avatar = "👀"):
                st.write(user_input)

                st.session_state.history_check.append(
                    {
                        "role" : "user",
                        "content" : user_input,
                        "avatar" : "👀",
                    }
                )

            # gọi AI
            genai.configure(api_key = api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')

            prompt = f"""
            Bạn là một chuyên gia ngữ pháp tiếng anh, hãy giúp tôi: 
            1. Sửa lại đoạn văn sau cho đúng ngữ pháp
            2. Chỉ ra lỗi sia cụ thể và giải thích ngắn gọn
            3. Đề xuất cách viết khác tốt hơn

            Đoạn văn gốc: "{user_input}"
            """
            with st.chat_message("assistant"):
                with st.spinner("Loading..."):
                    response = model.generate_content(prompt)

            st.session_state.history_check.append(
                    {
                        "role" : "assistant",
                        "content" : response.text,
                    }
                )
            st.balloons()
            st.success("Finished")
            st.markdown(response.text)
            st.markdown(
    ":orange-badge[⚠️ Needs review]")
            user_input = None
    
# #----------------------------------------------------------------------------

def Learn_Grammar(user_input):   

    if user_input:
        if not api_key:
            st.warning("Please fill in API key")
        if not user_input:
            st.warning("Please fill in your answer")
        else:
            # hiển thị lịch sử
            for message in st.session_state.learn_grammar_history:
                with st.chat_message(message["role"] , avatar = message.get("avatar")):
                    st.markdown(message["content"])

            with st.chat_message("user", avatar = "🦖"):
                st.write(user_input)
                st.session_state.learn_grammar_history.append({
                        "role" : "user",
                        "content" : user_input,
                        "avatar" : "🦖",
                    })
            #chọn api key
            genai.configure(api_key = api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            prompt = f"""
            Bạn là một chuyên gia ngữ pháp tiếng anh, hãy chỉ tôi học bài học ngữ
            pháp về chủ đề "{user_input}"
            """
            with st.chat_message("assistant"):
                with st.spinner("Loading..."):
                    response = model.generate_content(prompt)
                
                st.session_state.learn_grammar_history.append(
                    {
                        "role" : "assistant",
                        "content" : response.text,
                    }
                )
                st.success("Success!")
                st.balloons()
                st.info(response.text)
                st.markdown(
                ":orange-badge[⚠️ Needs review]")


st.sidebar.header("Welcome to AI English Checker!")

with st.sidebar:
    if st.button("About us"):
        st.session_state.current = "about_us_sidebar"
    if st.button("Grammar"):
        st.session_state.current = "grammar_sidebar"
    if st.button("Vocabulary"):
        st.session_state.current = "voc_sidebar"

if ("current" not in st.session_state) or st.session_state.current == "about_us_sidebar":
    st.session_state.current = ""
    st.image("data:image/png;base64,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")
    st.image("data:image/jpeg;base64,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")



# note = st.sidebar.button("Note")
# tip = st.sidebar.button("Tips")


    



if st.session_state.current == "grammar_sidebar":
    mode = st.radio("Menu" , ["Learn grammar", "Check grammar"], horizontal=True)
    
    if "grammar_current" not in st.session_state:
        st.session_state.grammar_current = ""

    if mode == "Learn grammar":
        st.session_state.grammar_current = "learn"

    if mode == "Check grammar":
        st.session_state.grammar_current = "check"
    
    ##check grammar:

    if st.session_state.grammar_current == "check":
        
        if "history_check" not in st.session_state:
            st.session_state.history_check = []

        user_input = st.chat_input("What do you want to check? ")
        col1, col2 = st.columns([0.8, 0.2])
        with col2:
            if st.button("Clear history"):
                st.session_state.history_check = []
                st.rerun()
        with col1:
            check_grammar(user_input)


    ##learn grammar
    # #----------------------------------
    if st.session_state.grammar_current == "learn":
        if "learn_grammar_history" not in st.session_state:
            st.session_state.learn_grammar_history = []

        user_input = st.chat_input("You want to learn: ", key = "learn_grammar_1")
        col1, col2 = st.columns([0.9, 0.1])
        with col2:
            if st.button("Clear"):
                learn_grammar_history = []
                st.rerun()
        with col1:
            Learn_Grammar(user_input)

#-------------vocabulary-----------------

#lưu lịch sử chat

if "history" not in st.session_state:
    st.session_state.history = []

if "voc_sb" not in st.session_state:
    st.session_state.voc_sb = False

if st.session_state.current == "voc_sidebar":
    user_input = st.chat_input("Text here")
    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        if st.button("Clear history"):
            st.session_state.history = []
            st.rerun()

    with col1:
        while user_input:
            if not api_key:
                st.warning("Please fill in api key")
            if not user_input:
                st.warning("Please fill in your answer")
            else:
                for h in st.session_state.history:
                    with st.chat_message(h["role"], avatar = h.get("avatar")):
                        st.markdown(h["content"])

                with st.chat_message("user", avatar = "🫰"):
                    st.session_state.history.append({
                        "role" : "user", 
                        "content" : user_input, 
                        "avatar" : "🫰"}
                    )
                    st.write(user_input)
                
                genai.configure(api_key = api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                prompt = f"""Hãy cho tôi các nghĩa khác nhau của từ {user_input},
                cho những từ đồng nghĩa, trái nghĩa, cách sử dụng và ngữ cảnh sử dụng nó"""

                with st.chat_message("assistant"):
                    with st.spinner("Loading..."):
                        st.toast("No pain, no gain")
                        time.sleep(10)
                        st.toast("Practice makes perfect")
                        time.sleep(10)
                        st.toast("Blood, sweet and tears", icon="🎉")
                        response = model.generate_content(prompt)

                    
                    st.success("Success!")
                    st.snow()
                    st.info(response.text)
                    st.markdown(
                    ":orange-badge[⚠️ Needs review]")
                    st.session_state.history.append({
                        "role" : "assistant", 
                        "content" : response.text,
                    })
                    user_input = None

        
    




