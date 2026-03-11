import streamlit as st
import google.generativeai as genai
import time
from gtts import gTTS
import io
import streamlit.components.v1 as components
import base64
import os

# ============================================================
# 1. CẤU HÌNH TRANG & GIAO DIỆN
# ============================================================
st.set_page_config(
    page_title="AI Chinese Tutor",
    page_icon="🐼",
    layout="wide"
)

# --- HÀM TẠO ÂM THANH TIẾNG TRUNG ---
def get_audio_bytes(text, lang='zh-CN'):
    try:
        tts = gTTS(text=text, lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception:
        return None

# --- CSS TỐI ƯU HÓA UI CHAT ---
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://i.pinimg.com/736x/0a/be/1e/0abe1e429f2a91473cc1edf5ab6036d5.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .main .block-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* 2. Làm mờ Sidebar để đồng bộ */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(10px);
    }
    
    h1 {
        color: #FFD700 !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
        text-align: center;
        font-family: 'Arial Black', sans-serif;
    }
    [data-testid="user-message"] {
        background: linear-gradient(135deg, #D32F2F 0%, #E53935 100%) !important;
        color: white !important;
        border-radius: 20px 20px 0px 20px !important;
        padding: 15px;
        box-shadow: 0 4px 10px rgba(211, 47, 47, 0.3);
    }
    [data-testid="assistant-message"] {
        background: rgba(255, 255, 255, 0.9) !important;
        color: #333 !important;
        border-radius: 20px 20px 20px 0px !important;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border-left: 5px solid #FFD700;
    }
    .loading-text {
        font-size: 18px;
        font-weight: bold;
        color: black; 
        text-align: center;
        padding: 10px;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { opacity: 0.6; transform: scale(0.98); }
        50% { opacity: 1; transform: scale(1.02); }
        100% { opacity: 0.6; transform: scale(0.98); }
    }
</style>
""", unsafe_allow_html=True)

def play_local_sfx(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            data = f.read()
            b64_audio = base64.b64encode(data).decode()
            
        components.html(
            f"""
            <audio autoplay loop>
                <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
            </audio>
            """,
            height=0, width=0,
        )

# ============================================================
# 2. QUẢN LÝ API KEY, SESSION & FLASHCARD
# ============================================================
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    with st.sidebar:
        st.info("💡 Cung cấp API Key để bắt đầu")
        api_key = st.text_input("GEMINI_API_KEY", type="password")

if "history" not in st.session_state: st.session_state.history = []
if "word_count" not in st.session_state: st.session_state.word_count = 0
if "flashcards" not in st.session_state: st.session_state.flashcards = []

# Hàm lưu Flashcard (Lưu Toàn bộ giải thích để lật xem)
def save_to_flashcard(word, explanation):
    if not any(fc['word'] == word for fc in st.session_state.flashcards):
        st.session_state.flashcards.append({"word": word, "explanation": explanation})
        st.toast(f"🎉 Đã tạo Flashcard cho '{word}' thành công!")
    else:
        st.toast(f"⚠️ Thẻ '{word}' đã có trong bộ sưu tập rồi!")

# --- SIDEBAR: THỐNG KÊ & GIAO DIỆN FLASHCARD CÁ NHÂN ---
with st.sidebar:
    st.image("https://i.pinimg.com/originals/43/09/d8/4309d867ef83a975346a0607244024aa.gif", width=200)
    st.markdown(f"### 📈 Tiến độ hôm nay\nĐã học: **{st.session_state.word_count}** từ/câu")
    
    if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
        st.session_state.history = []
        st.session_state.word_count = 0
        st.rerun()

    st.divider()
    
    # Khu vực bộ bài Flashcard
    st.markdown("### 🗂️ Flashcard Cá Nhân")
    if len(st.session_state.flashcards) == 0:
        st.info("Chưa có thẻ nào. Trò chuyện và nhấn 'Lưu' để tạo thẻ nhé! 🐼")
    else:
        for fc in st.session_state.flashcards:
            word_key = fc['word']
            
            # Khởi tạo trạng thái LẬT THẺ cho từng từ
            if f"flip_{word_key}" not in st.session_state:
                st.session_state[f"flip_{word_key}"] = False

            with st.container():
                if not st.session_state[f"flip_{word_key}"]:
                    # --- MẶT TRƯỚC (Từ Vựng) ---
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #FFD700 0%, #FFB300 100%); 
                                min-height: 180px; display: flex; align-items: center; justify-content: center;
                                border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.3); 
                                border: 3px solid white; margin-bottom: 10px; padding: 15px;">
                        <h2 style="font-size: 38px; margin: 0; color: #B71C1C; 
                                   text-shadow: 1px 1px 2px rgba(255,255,255,0.6); text-align: center; word-wrap: break-word;">
                            {word_key}
                        </h2>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # --- MẶT SAU (Nghĩa & Giải thích chi tiết) ---
                    st.markdown(f"""
                    <div style="background: #B71C1C; color: #FFD700; padding: 8px; 
                                border-radius: 15px 15px 0 0; font-weight: bold; text-align: center; 
                                border: 2px solid white; border-bottom: none;">
                        Nghĩa của "{word_key}"
                    </div>
                    """, unsafe_allow_html=True)
                    # Container giới hạn chiều cao tạo thanh Scroll cho mặt sau
                    with st.container(height=200):
                        st.markdown(fc['explanation'])

                # Nút thao tác thẻ
                col1, col2 = st.columns(2)
                with col1:
                    btn_text = "📖 Xem nghĩa" if not st.session_state[f"flip_{word_key}"] else "🔄 Úp thẻ"
                    if st.button(btn_text, key=f"btn_flip_{word_key}", use_container_width=True):
                        st.session_state[f"flip_{word_key}"] = not st.session_state[f"flip_{word_key}"]
                        st.rerun()
                with col2:
                    if st.button("❌ Xóa thẻ", key=f"btn_del_{word_key}", use_container_width=True):
                        # Xóa từ khỏi list và xóa luôn trạng thái lật thẻ
                        st.session_state.flashcards = [item for item in st.session_state.flashcards if item['word'] != word_key]
                        if f"flip_{word_key}" in st.session_state:
                            del st.session_state[f"flip_{word_key}"]
                        st.rerun()
            st.write("---")

# ============================================================
# 3. NỘI DUNG CHÍNH: HSK AI TUTOR
# ============================================================
st.title("🐼 HSK AI Tutor")
st.markdown("<p style='text-align: center; color: white;'>Nhập chữ Hán, Pinyin hoặc tiếng Việt để AI giải thích và phân tích bộ thủ nhé!</p>", unsafe_allow_html=True)
st.write("---")

# Hiển thị lịch sử chat
for i, message in enumerate(st.session_state.history):
    with st.chat_message(message["role"], avatar=message.get("avatar")):
        st.markdown(f"<div data-testid='{message['role']}-message'>{message['content']}</div>", unsafe_allow_html=True)
        if "audio" in message and message["audio"] is not None:
            st.audio(message["audio"], format="audio/mp3")
        
        # Sửa lỗi: Gắn nút Lưu Flashcard trực tiếp vào lịch sử để không bị mất khi rerun
        if message["role"] == "assistant" and "word" in message:
            st.button(f"💾 Lưu '{message['word']}' vào Flashcard", 
                      key=f"save_btn_hist_{i}", 
                      on_click=save_to_flashcard, 
                      args=(message['word'], message['content']))

user_input = st.chat_input("Tra từ vựng (VD: 喜欢, xǐhuan, vui vẻ...)")

if user_input:
    if not api_key:
        st.warning("⚠️ Vui lòng nhập API Key để tiếp tục.")
    else:
        # In ngay câu hỏi của user
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(f"<div data-testid='user-message'>{user_input}</div>", unsafe_allow_html=True)
        st.session_state.history.append({"role": "user", "content": user_input, "avatar": "🧑‍🎓"})

        try:
            with st.chat_message("assistant", avatar="🐼"):
                loading_placeholder = st.empty()
                with loading_placeholder.container():
                    col_gif, col_text = st.columns([1, 3])
                    with col_gif:
                        st.image("https://i.pinimg.com/originals/26/1e/29/261e290ab1957c7e2c6e7e8254382876.gif", width=150)
                        play_local_sfx("loading.mp3")
                    
                    with col_text:
                        text_box = st.empty()
                        fun_phrases = [
                            "Lão sư đang lăn tăn...",
                            "Chờ chút, đang nhai nốt cây trúc...",
                            "Chờ xíii",
                            "Để lão sư trèo xuống đã ...",
                            "Á bị té...",
                            "Lọc cọc lọc cọc..."
                        ]
                        phrase_idx = 0
                        text_box.markdown(f"<div class='loading-text'>{fun_phrases[phrase_idx]}</div>", unsafe_allow_html=True)
                
                # Cấu hình API và sinh phản hồi
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash') # Đã sửa thành model ổn định
                
                prompt = f"""Bạn là một giáo viên dạy tiếng Trung (chuyên luyện HSK) tên là lão sư (con gấu trúc thích ăn cây trúc). Học sinh đang hỏi về từ/cụm từ "{user_input}".
                Hãy giải thích thật chi tiết và sinh động theo format sau:
                
                1. 📌 **Chữ Hán, Pinyin & Âm Hán Việt**.
                2. 📝 **Ý nghĩa & Loại từ** (Giải thích cách dùng rõ ràng).
                3. 🗣️ **3 Ví dụ thực tế** (Bắt buộc có chữ Hán, Pinyin và tiếng Việt, ngữ cảnh tự nhiên).
                4. 🧩 **Chiết tự & Mẹo nhớ chữ**: Phân tích các bộ thủ tạo nên chữ Hán này, bịa một câu chuyện vui hoặc logic để học sinh nhớ cách viết mãi mãi.
                5. 🔄 **Mở rộng**: Từ đồng nghĩa, trái nghĩa hoặc từ ghép phổ biến.
                
                Chỉ trả về nội dung đã yêu cầu, trình bày bằng Markdown đẹp mắt, dùng nhiều emoji."""
                
                response_stream = model.generate_content(prompt, stream=True)
                
                full_response = ""
                last_update_time = time.time()
                
                for chunk in response_stream:
                    full_response += chunk.text
                    current_time = time.time()
                    if current_time - last_update_time > 1.8:
                        phrase_idx += 1
                        text_box.markdown(f"<div class='loading-text'>{fun_phrases[phrase_idx % len(fun_phrases)]}</div>", unsafe_allow_html=True)
                        last_update_time = current_time
                        
                audio_bytes = get_audio_bytes(user_input, lang='zh-CN')
                loading_placeholder.empty()

                # Cập nhật state và lưu vào history (bao gồm cả trường "word")
                st.session_state.word_count += 1
                st.session_state.history.append({
                    "role": "assistant", 
                    "content": full_response, 
                    "avatar": "🐼",
                    "audio": audio_bytes,
                    "word": user_input
                })

                if st.session_state.word_count % 3 == 0:
                    st.balloons()

            # Rerun để hiển thị sạch sẽ từ history
            st.rerun()

        except Exception as e:
            st.error(f"Lỗi kết nối: {str(e)}")