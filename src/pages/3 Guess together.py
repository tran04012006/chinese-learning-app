import streamlit as st
import streamlit.components.v1 as components
from gtts import gTTS
import io
import time
import base64
import os
import random

# ============================================================
# CÀI ĐẶT TRANG
# ============================================================
st.set_page_config(page_title="Thử Thách Hàng Ngày", page_icon="🎁", layout="wide")

# ============================================================
# CÀI ĐẶT GIAO DIỆN (CSS TỪ CODE GỐC CỦA BẠN)
# ============================================================
background_image_url = "https://i.pinimg.com/originals/4c/61/f8/4c61f8dbda3404dce696a74c25236d75.gif"

page_bg_css = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("{background_image_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.3) !important;
    backdrop-filter: blur(10px);
}}
div[data-testid="stVerticalBlock"] > div {{
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 15px;
    padding: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}}
h2, h3, h4 {{
    color: #2E7D32 !important;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
}}
/* Giao diện riêng cho Quiz Card (Dùng làm thẻ Bí ẩn luôn) */
.quiz-card {{
    background: linear-gradient(135deg, #ffffff 0%, #f1f8e9 100%);
    padding: 40px;
    border-radius: 20px;
    border: 3px solid #81C784;
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    text-align: center;
    margin-bottom: 20px;
}}
</style>
"""
st.markdown(page_bg_css, unsafe_allow_html=True)

# --- HÀM PHÁT ÂM THANH ---
def play_sfx(sound_url):
    components.html(f'<audio autoplay><source src="{sound_url}" type="audio/mp3"></audio>', height=0, width=0)

def play_local_sfx(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            b64_audio = base64.b64encode(f.read()).decode()
        components.html(f'<audio autoplay><source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3"></audio>', height=0, width=0)

def get_audio_bytes(text, lang='zh-CN'):
    tts = gTTS(text=text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# --- KHO DỮ LIỆU TỪ VỰNG ---
vocab_data = {
    'giao_tiep': {
        "title": "🗣️ Giao tiếp cơ bản",
        "words": [
            {"hanzi": "你好", "pinyin": "nǐ hǎo", "meaning": "Xin chào"},
            {"hanzi": "谢谢", "pinyin": "xièxie", "meaning": "Cảm ơn"},
            {"hanzi": "对不起", "pinyin": "duìbuqǐ", "meaning": "Xin lỗi"},
            {"hanzi": "再见", "pinyin": "zàijiàn", "meaning": "Tạm biệt"}
        ]
    },
    'truong_hoc': {
        "title": "🏫 Trường học",
        "words": [
            {"hanzi": "学校", "pinyin": "xuéxiào", "meaning": "Trường học"},
            {"hanzi": "老师", "pinyin": "lǎoshī", "meaning": "Giáo viên"},
            {"hanzi": "学生", "pinyin": "xuésheng", "meaning": "Học sinh"},
            {"hanzi": "书", "pinyin": "shū", "meaning": "Sách vở"}
        ]
    },
    'nha_cua': {
        "title": "🏠 Gia đình & Nhà cửa",
        "words": [
            {"hanzi": "家", "pinyin": "jiā", "meaning": "Nhà / Gia đình"},
            {"hanzi": "爸爸", "pinyin": "bàba", "meaning": "Bố"},
            {"hanzi": "妈妈", "pinyin": "māma", "meaning": "Mẹ"},
            {"hanzi": "房间", "pinyin": "fángjiān", "meaning": "Căn phòng"}
        ]
    }
}

def get_random_word():
    all_words = []
    for topic_key, data in vocab_data.items():
        for w in data['words']:
            w['topic'] = data['title']
            all_words.append(w)
    return random.choice(all_words)

# --- KHỞI TẠO SESSION STATE ---
if 'dc_word' not in st.session_state: st.session_state.dc_word = get_random_word()
if 'dc_hints' not in st.session_state: st.session_state.dc_hints = 0
if 'dc_points' not in st.session_state: st.session_state.dc_points = 0
if 'dc_solved' not in st.session_state: st.session_state.dc_solved = False

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.image("https://i.pinimg.com/originals/9e/2c/6e/9e2c6e22c6cf706dec782c96eeb2e62c.gif")
    st.markdown("## 🏆 Bảng Điểm")
    st.markdown(f"### Điểm hiện tại: **{st.session_state.dc_points}**")
    st.info("💡 Đoán đúng từ bí ẩn để nhận ngay 10 điểm!")

# ============================================================
# GIAO DIỆN CHÍNH
# ============================================================
st.subheader("🕵️‍♂️ THỬ THÁCH HÀNG NGÀY (DAILY CHALLENGE)")

word = st.session_state.dc_word

# ---------------------------------------------------------
# TRẠNG THÁI: CHƯA ĐOÁN RA
# ---------------------------------------------------------
if not st.session_state.dc_solved:
    
    # Sử dụng nguyên class quiz-card của bạn
    st.markdown(f"""
        <div class="quiz-card">
            <h3 style="color: gray;">Từ bí ẩn hôm nay là gì?</h3>
            <h1 style="font-size: 80px; color: #1565C0; margin: 10px 0;">{"❓" * len(word['hanzi'])}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("#### 💡 Mở khóa gợi ý:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state.dc_hints < 1:
            if st.button("Mở Gợi ý 1", use_container_width=True): 
                st.session_state.dc_hints = 1
                st.rerun()
        else:
            st.success(f"**Gợi ý 1:** Từ này có **{len(word['hanzi'])}** chữ Hán.")
            
    with col2:
        if st.session_state.dc_hints < 2:
            if st.button("Mở Gợi ý 2", use_container_width=True, disabled=(st.session_state.dc_hints < 1)): 
                st.session_state.dc_hints = 2
                st.rerun()
        else:
            st.success(f"**Gợi ý 2:** Thuộc chủ đề **{word['topic']}**.")
            
    with col3:
        if st.session_state.dc_hints < 3:
            if st.button("Mở Gợi ý 3", use_container_width=True, disabled=(st.session_state.dc_hints < 2)): 
                st.session_state.dc_hints = 3
                st.rerun()
        else:
            st.warning(f"**Gợi ý 3:** Pinyin là **{word['pinyin']}**.")

    st.write("---")
    
    # Form nhập đáp án
    with st.form("guess_form", clear_on_submit=True):
        st.write("📝 **Nhập đáp án của bạn (Hán tự, Pinyin hoặc Tiếng Việt đều được):**")
        user_guess = st.text_input("Câu trả lời:", label_visibility="collapsed")
        submitted = st.form_submit_button("Chốt đáp án! 🎯", use_container_width=True, type="primary")
        
        if submitted:
            if user_guess:
                ans = user_guess.lower().strip()
                # Chấp nhận đúng 1 trong 3 dạng
                if ans == word['hanzi'].lower() or ans == word['pinyin'].lower() or ans == word['meaning'].lower():
                    st.session_state.dc_solved = True
                    st.session_state.dc_points += 10
                    play_local_sfx("đúng.mp3") # Giả định bạn có file đúng.mp3 giống code cũ
                    st.rerun()
                else:
                    st.error("❌ Oái, chưa đúng rồi! Hãy thử lại hoặc mở thêm gợi ý xem sao.")
                    play_local_sfx("sai.mp3")
            else:
                st.warning("⚠️ Bạn chưa nhập gì cả!")

# ---------------------------------------------------------
# TRẠNG THÁI: ĐÃ ĐOÁN ĐÚNG (THÀNH CÔNG)
# ---------------------------------------------------------
else:
    st.balloons()
    st.success(f"🎉 CHÍNH XÁC! Bạn đã nhận được **+10 Điểm**.")
    
    # Hiển thị kết quả bằng chính class quiz-card của bạn
    st.markdown(f"""
        <div class="quiz-card">
            <h3 style="color: gray;">Đáp án chính xác là:</h3>
            <h1 style="font-size: 80px; color: #1565C0; margin: 10px 0;">{word['hanzi']}</h1>
            <p style="font-size: 20px; color: #555;">({word['pinyin']})</p>
            <h2 style="color: #2E7D32;">{word['meaning']}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Tự động đọc từ vựng
    st.audio(get_audio_bytes(word['hanzi']), format="audio/mp3", autoplay=True)
    
    st.write("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1,2,1])
    with col_btn2:
        if st.button("🔄 Tạo thử thách mới", use_container_width=True, type="primary"):
            st.session_state.dc_word = get_random_word()
            st.session_state.dc_hints = 0
            st.session_state.dc_solved = False
            st.rerun()