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

        
    




