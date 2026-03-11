import streamlit as st
import streamlit.components.v1 as components
import requests
from gtts import gTTS
import io
import time
import base64
import os
import random  # Thêm thư viện random để xáo trộn đáp án

# ============================================================
# CÀI ĐẶT GIAO DIỆN (CSS CUSTOMIZATION)
# ============================================================
background_image_url = "https://i.pinimg.com/originals/9e/43/97/9e4397375b1961fd009b34e3b97101e9.gif"

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
/* Giao diện riêng cho Quiz Card */
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

# --- 1. KHỞI TẠO SESSION STATE ---
if 'current_page' not in st.session_state: st.session_state.current_page = 'home'
if 'is_opening_book' not in st.session_state: st.session_state.is_opening_book = False
if 'current_topic' not in st.session_state: st.session_state.current_topic = 'giao_tiep' 
if 'flashcard_index' not in st.session_state: st.session_state.flashcard_index = 0
if 'is_flipped' not in st.session_state: st.session_state.is_flipped = False
if 'completed_topics' not in st.session_state: st.session_state.completed_topics = []

# State cho Minigame
if 'quiz_index' not in st.session_state: st.session_state.quiz_index = 0
if 'quiz_score' not in st.session_state: st.session_state.quiz_score = 0
if 'quiz_answered' not in st.session_state: st.session_state.quiz_answered = False
if 'quiz_options' not in st.session_state: st.session_state.quiz_options = []

# --- 2. KHO DỮ LIỆU TỪ VỰNG ---
vocab_data = {
    'giao_tiep': {
        "title": "🗣️ Giao tiếp cơ bản",
        "words": [
            {"hanzi": "你好", "pinyin": "nǐ hǎo", "meaning": "Xin chào", "image": "https://i.pinimg.com/originals/bd/a5/34/bda53406f36ebc0ba6da9ff6dfa282f6.gif"},
            {"hanzi": "谢谢", "pinyin": "xièxie", "meaning": "Cảm ơn", "image": "https://i.pinimg.com/originals/af/7e/61/af7e61ff3988f541e24ec17eb735c345.gif"},
            {"hanzi": "对不起", "pinyin": "duìbuqǐ", "meaning": "Xin lỗi", "image": "https://i.pinimg.com/originals/3f/82/b4/3f82b4cc161405e3b5eecce70a312e03.gif"},
            {"hanzi": "再见", "pinyin": "zàijiàn", "meaning": "Tạm biệt", "image": "https://i.pinimg.com/originals/7d/51/db/7d51db21ec3200ab56f8f7cd30e8c050.gif"}
        ]
    },
    'truong_hoc': {
        "title": "🏫 Trường học",
        "words": [
            {"hanzi": "学校", "pinyin": "xuéxiào", "meaning": "Trường học", "image": "https://i.pinimg.com/originals/47/9b/b0/479bb01d4a0af2606553df87ee056ee6.gif"},
            {"hanzi": "老师", "pinyin": "lǎoshī", "meaning": "Giáo viên", "image": "https://i.pinimg.com/originals/f0/73/b5/f073b53fbf5061cdb82c76eec4c207ea.gif"},
            {"hanzi": "学生", "pinyin": "xuésheng", "meaning": "Học sinh", "image": "https://i.pinimg.com/originals/30/b0/78/30b078fb86b51c8a666e8baec635ea78.gif"},
            {"hanzi": "书", "pinyin": "shū", "meaning": "Sách vở", "image": "https://i.pinimg.com/originals/24/f6/45/24f64539eb8ecfa4e320d3678cd6baeb.gif"}
        ]
    },
    'nha_cua': {
        "title": "🏠 Gia đình & Nhà cửa",
        "words": [
            {"hanzi": "家", "pinyin": "jiā", "meaning": "Nhà / Gia đình", "image": "https://i.pinimg.com/originals/f1/ee/39/f1ee391e98d89e490ec72314d101d2ce.gif"},
            {"hanzi": "爸爸", "pinyin": "bàba", "meaning": "Bố", "image": "https://i.pinimg.com/originals/60/79/1a/60791addfc81da367f0f0c0ee992770c.gif"},
            {"hanzi": "妈妈", "pinyin": "māma", "meaning": "Mẹ", "image": "https://i.pinimg.com/originals/71/eb/68/71eb683c3149d5ef7df4c9e472251a2e.gif"},
            {"hanzi": "房间", "pinyin": "fángjiān", "meaning": "Căn phòng", "image": "https://i.pinimg.com/originals/31/3e/dc/313edc0f3c5b8e96f13010b985476a6e.gif"}
        ]
    }
}

# --- 3. GIAO DIỆN CHÍNH ---

# KIỂM TRA HIỆU ỨNG GIF MỞ SÁCH
if st.session_state.is_opening_book:
    st.markdown("<h2 style='text-align: center; color: #5D4037;'>Đang mở sách kiến thức...</h2>", unsafe_allow_html=True)
    play_local_sfx("gió thổi.mp3") # Nếu có file, không có thì bỏ qua
    book_gif_url = "https://i.pinimg.com/originals/5a/8e/72/5a8e72390a066bbede2cd33612760ca3.gif"
    st.image(book_gif_url, use_container_width=True)
    time.sleep(2.5)
    st.session_state.is_opening_book = False
    st.session_state.current_page = 'flashcard'
    st.rerun()

#sidebar
with st.sidebar:
    st.image("https://i.pinimg.com/originals/41/43/a3/4143a3fdbeb54c8801f38598b42fe6a7.gif")


# ==========================================
# TRANG 1: MÀN HÌNH CHỌN BÀI HỌC
# ==========================================
if st.session_state.current_page == 'home':
    st.subheader("📚 CHỌN CHỦ ĐỀ HỌC")
    
    # Thanh tiến trình tổng
    total_topics = len(vocab_data)
    completed = len(st.session_state.completed_topics)
    st.progress(completed / total_topics, text=f"🌟 Đã chinh phục: {completed}/{total_topics} chủ đề")


    col1, col2, col3 = st.columns(3)

    def trigger_book_open(topic_key):
        st.session_state.current_topic = topic_key
        st.session_state.is_opening_book = True
        st.session_state.flashcard_index = 0 
        st.session_state.is_flipped = False
        st.rerun()

    with col1:
        st.image("https://i.pinimg.com/736x/58/0b/30/580b30ec43a4652c3486b6aa74b5669f.jpg")
        btn_text = "✅ Đã học: Giao tiếp" if 'giao_tiep' in st.session_state.completed_topics else "🗣️ Giao tiếp cơ bản"
        if st.button(btn_text, key="btn_gt", use_container_width=True): trigger_book_open('giao_tiep')

    with col2:
        st.image("https://i.pinimg.com/736x/d1/ba/0f/d1ba0f628926d932fd696ef855675682.jpg")
        btn_text = "✅ Đã học: Trường học" if 'truong_hoc' in st.session_state.completed_topics else "🏫 Trường học"
        if st.button(btn_text, key="btn_th", use_container_width=True): trigger_book_open('truong_hoc')

    with col3:
        st.image("https://i.pinimg.com/736x/80/12/59/801259176fab97ce11f12587a1579a2a.jpg")
        btn_text = "✅ Đã học: Gia đình" if 'nha_cua' in st.session_state.completed_topics else "🏠 Gia đình & Nhà cửa"
        if st.button(btn_text, key="btn_nc", use_container_width=True): trigger_book_open('nha_cua')


# ==========================================
# TRANG 2: MÀN HÌNH FLASHCARD
# ==========================================
elif st.session_state.current_page == 'flashcard':

    # SỬA LỖI 1: Thêm key="quiz_btn_top"
    if st.button("🎮 Chơi Quiz Ôn Tập!", key="quiz_btn_top", use_container_width=True, type="primary"):
        st.session_state.current_page = 'quiz'
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_answered = False
        st.session_state.quiz_options = []
        st.rerun()

    if st.button("⬅️ Quay lại Kệ sách"):
        st.session_state.current_page = 'home'
        st.rerun()

    current_topic_data = vocab_data[st.session_state.current_topic]
    word_list = current_topic_data["words"]
    
    st.write(f"### {current_topic_data['title']}")
    
    total = len(word_list)
    idx = st.session_state.flashcard_index
    st.progress((idx + 1) / total, text=f"Từ thứ {idx + 1} trên tổng số {total}")
    word = word_list[idx]

    # Mặt trước thẻ: Hiện chữ Hán
    st.markdown(f"""
        <div style="background-color: #FFFDE7; padding: 60px; border-radius: 15px; border-left: 10px solid #FBC02D; box-shadow: 4px 4px 10px rgba(0,0,0,0.1); text-align: center;">
            <h1 style="font-size: 100px; color: #212121; margin: 0;">{word['hanzi']}</h1>
        </div>
    """, unsafe_allow_html=True)

    # Mặt sau thẻ (Khi lật): Hiện Ảnh + Pinyin + Nghĩa + Phát âm
    if st.session_state.is_flipped:
        st.write("---")
        
        # Tạo 3 cột để căn giữa hình ảnh (Cột giữa to nhất)
        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        with col_img2:
            # Lấy link ảnh từ data, nếu có thì hiển thị
            if "image" in word and word["image"]:
                st.image(word["image"], use_container_width=True)
                
        st.markdown(f"<h2 style='text-align: center; color: #D32F2F;'>{word['pinyin']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>{word['meaning']}</h3>", unsafe_allow_html=True)
        st.audio(get_audio_bytes(word['hanzi']), format="audio/mp3", autoplay=True)
    else:
        st.write("")
        st.info("💡 Mẹo: Hãy thử nhớ nghĩa trước khi lật thẻ!")

    st.write("---")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if idx > 0 and st.button("⬅️ Trước", use_container_width=True):
            st.session_state.flashcard_index -= 1
            st.session_state.is_flipped = False
            st.rerun()
    with c2:
        if st.button("Lật thẻ 🔄", type="primary", use_container_width=True):
            play_sfx("https://www.soundjay.com/buttons/sounds/button-10.mp3")
            time.sleep(0.15) 
            st.session_state.is_flipped = not st.session_state.is_flipped
            st.rerun()
    with c3:
        if idx < total - 1:
            if st.button("Tiếp ➡️", use_container_width=True):
                st.session_state.flashcard_index += 1
                st.session_state.is_flipped = False
                st.rerun()
        else:
            # SỬA LỖI 2: Thêm key="quiz_btn_bottom"
            if st.button("🎮 Chơi Quiz Ôn Tập!", key="quiz_btn_bottom", use_container_width=True, type="primary"):
                st.session_state.current_page = 'quiz'
                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_answered = False
                st.session_state.quiz_options = []
                st.rerun()

# ==========================================
# TRANG 3: MINIGAME (TRẮC NGHIỆM)
# ==========================================
elif st.session_state.current_page == 'quiz':
    current_topic_data = vocab_data[st.session_state.current_topic]
    word_list = current_topic_data["words"]
    total_q = len(word_list)
    q_idx = st.session_state.quiz_index
    
    st.subheader(f"🎮 Minigame: Trắc nghiệm siêu tốc ({current_topic_data['title']})")
    
    # Hiển thị điểm số hiện tại
    st.progress(q_idx / total_q, text=f"Câu hỏi: {q_idx + 1}/{total_q}  |  🏆 Điểm: {st.session_state.quiz_score}")

    # Lấy câu hỏi hiện tại
    current_word = word_list[q_idx]
    correct_meaning = current_word['meaning']

    # Khởi tạo 4 đáp án (Chỉ chạy 1 lần mỗi câu hỏi)
    if not st.session_state.quiz_options:
        options = [w['meaning'] for w in word_list] # Lấy toàn bộ 4 nghĩa trong bài
        random.shuffle(options) # Xáo trộn vị trí
        st.session_state.quiz_options = options

    # Giao diện Câu hỏi khổng lồ
    st.markdown(f"""
        <div class="quiz-card">
            <h3 style="color: gray;">Từ này có nghĩa là gì?</h3>
            <h1 style="font-size: 80px; color: #1565C0; margin: 10px 0;">{current_word['hanzi']}</h1>
            <p style="font-size: 20px; color: #555;">({current_word['pinyin']})</p>
        </div>
    """, unsafe_allow_html=True)

    # Nếu người dùng đã chọn đáp án
    if st.session_state.quiz_answered:
        # Hiển thị kết quả
        if st.session_state.selected_answer == correct_meaning:
            
            st.success(f"🎉 Chính xác! **{current_word['hanzi']}** nghĩa là **{correct_meaning}**.")
            play_local_sfx("đúng.mp3")
        else: 
            st.error(f"❌ Sai rồi! **{current_word['hanzi']}** phải là **{correct_meaning}**.")
            play_local_sfx("sai.mp3")
        # Nút Chuyển câu
        st.write("---")
        if q_idx < total_q - 1:
            if st.button("Tiếp tục ➡️", use_container_width=True, type="primary"):
                st.session_state.quiz_index += 1
                st.session_state.quiz_answered = False
                st.session_state.quiz_options = [] # Reset options cho câu sau
                st.rerun()
        else:
            st.balloons()
            st.image("https://i.pinimg.com/1200x/76/c0/02/76c00211851fbb0bb3e543922e31e5ae.jpg")
            st.success(f"🏆 Chúc mừng! Bạn đạt **{st.session_state.quiz_score}/{total_q}** điểm.")
            if st.button("Hoàn thành & Nhận chứng chỉ 🎓", use_container_width=True, type="primary"):
                play_local_sfx("tada.mp3")
                if st.session_state.current_topic not in st.session_state.completed_topics:
                    st.session_state.completed_topics.append(st.session_state.current_topic)
                time.sleep(1.5)
                st.session_state.current_page = 'home'
                st.rerun()

    # Nếu đang trong trạng thái đợi người dùng trả lời
    else:
        # Tạo lưới 2x2 cho 4 nút bấm
        col1, col2 = st.columns(2)
        
        # Hàm xử lý khi bấm nút chọn đáp án
        def check_answer(ans):
            st.session_state.selected_answer = ans
            st.session_state.quiz_answered = True
            if ans == correct_meaning:
                st.session_state.quiz_score += 1

        # Nút 1 & 2
        with col1:
            if st.button(st.session_state.quiz_options[0], key="opt0", use_container_width=True): 
                check_answer(st.session_state.quiz_options[0])
                st.rerun()
            if st.button(st.session_state.quiz_options[1], key="opt1", use_container_width=True): 
                check_answer(st.session_state.quiz_options[1])
                st.rerun()
        # Nút 3 & 4
        with col2:
            if st.button(st.session_state.quiz_options[2], key="opt2", use_container_width=True): 
                check_answer(st.session_state.quiz_options[2])
                st.rerun()
            if st.button(st.session_state.quiz_options[3], key="opt3", use_container_width=True): 
                check_answer(st.session_state.quiz_options[3])
                st.rerun()