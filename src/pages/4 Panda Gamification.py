import streamlit as st
import time
import streamlit.components.v1 as components
import base64
import os

# ============================================================
# CÀI ĐẶT TRANG CHÍNH (PHẢI ĐẶT ĐẦU TIÊN)
# ============================================================
st.set_page_config(
    page_title="Khu Bảo Tồn Gấu Trúc",
    page_icon="🐼",
    layout="wide" 
)

# ============================================================
# CÀI ĐẶT GIAO DIỆN (CSS CUSTOMIZATION)
# ============================================================
background_image_url = "https://i.pinimg.com/originals/97/50/8f/97508f63790e74b828245e811e556495.gif"

page_bg_css = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("{background_image_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
/* Làm mờ Sidebar để đồng bộ */
[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.3) !important;
    backdrop-filter: blur(10px);
}}
/* Hiệu ứng kính mờ (Glassmorphism) */
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
</style>
"""
st.markdown(page_bg_css, unsafe_allow_html=True)

# sidebar
with st.sidebar:
    st.image("https://i.pinimg.com/originals/02/44/06/02440610e6ef16c198de712e1655085b.gif")

# --- 1. KHỞI TẠO SESSION STATE ---
if 'user_xp' not in st.session_state:
    st.session_state.user_xp = 20
if 'diem_pandan' not in st.session_state:
    st.session_state.diem_pandan = 0

# Thay thế just_fed bằng current_action để quản lý nhiều hành động
if 'current_action' not in st.session_state:
    st.session_state.current_action = None 

if 'is_leveling_up' not in st.session_state:
    st.session_state.is_leveling_up = False
if 'is_max_level_celebration' not in st.session_state:
    st.session_state.is_max_level_celebration = False

st.subheader("🎋 Khu bảo tồn Gấu trúc của bạn")

# hàm phát âm thanh
def play_local_sfx(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            data = f.read()
            b64_audio = base64.b64encode(data).decode()
            
        components.html(
            f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
            </audio>
            """,
            height=0, width=0,
        )
    else:
        st.warning(f"⚠️ Thiếu file âm thanh: {file_name}")

# ============================================================
# CHIA BỐ CỤC: TRÁI (Dashboard 40%) - PHẢI (Khu vực chơi 60%)
# ============================================================
col_dash, col_game = st.columns([0.4, 0.6])

# ----------------------------------------
# CỘT TRÁI: DASHBOARD
# ----------------------------------------
with col_dash:
    with st.container(border=True):
        st.metric(label="🌟 XP Hiện tại (Năng lượng)", value=f"{st.session_state.user_xp}")
        st.metric(label="🐼 Điểm trưởng thành", value=f"{st.session_state.diem_pandan} / 8")
        
        st.write("**Tiến trình tiến hóa:**")
        st.progress(min(st.session_state.diem_pandan / 8.0, 1.0))
        
        if st.session_state.user_xp <= 0:
            st.error("❌ Hết năng lượng chăm sóc!")
            if st.button("Xin 10 XP"):
                st.session_state.user_xp += 10
                st.rerun()

# ----------------------------------------
# CỘT PHẢI: KHU VỰC CHƠI GAME & CHĂM SÓC
# ----------------------------------------
with col_game:
    with st.container(border=True):
        
        # TRẠNG THÁI 1: CUTSCENE TIẾN HÓA TỐI ĐA (MAX LEVEL)
        if st.session_state.is_max_level_celebration:
            st.markdown("<h2 style='text-align: center; color: #FF4500 !important; text-shadow: 0px 0px 15px #FFD700;'>👑 TIẾN HÓA TỐI THƯỢNG 👑</h2>", unsafe_allow_html=True)
            st.audio("https://actions.google.com/sounds/v1/crowds/crowd_cheer.ogg", format="audio/ogg", autoplay=True)
            
            st.markdown("""
                <div style="display: flex; justify-content: center;">
                    <img src="https://i.pinimg.com/originals/21/a7/15/21a715a4012db474455fce3d8356cab4.gif" 
                         style="width: 100%; max-width: 500px; height: 400px; object-fit: cover; border-radius: 20px; box-shadow: 0px 0px 50px 20px rgba(255, 69, 0, 0.7);">
                </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
            st.snow()
            st.toast("🔥 HUYỀN THOẠI! Gấu trúc đã trở thành Thần Thú!", icon="👑")
            
            time.sleep(6) 
            st.session_state.is_max_level_celebration = False
            st.rerun()

        # TRẠNG THÁI 2: CUTSCENE TIẾN HÓA THƯỜNG
        elif st.session_state.is_leveling_up:
            st.markdown("<h2 style='text-align: center; color: #FFD700 !important; text-shadow: 2px 2px 4px #000;'>✨ ĐANG LỘT XÁC... ✨</h2>", unsafe_allow_html=True)
            st.audio("https://actions.google.com/sounds/v1/cartoon/magic_chime.ogg", format="audio/ogg", autoplay=True)
            
            st.markdown("""
                <div style="display: flex; justify-content: center;">
                    <img src="https://i.pinimg.com/originals/3a/63/41/3a6341fbc09db1e4dd41995e8bc1fe6f.gif" 
                         style="width: 100%; max-width: 500px; height: 400px; object-fit: cover; border-radius: 20px; box-shadow: 0px 0px 30px 10px rgba(255, 215, 0, 0.6);">
                </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
            st.toast("🎉 Tén tèn! Gấu trúc đang lột xác!", icon="✨")
            
            time.sleep(4) 
            st.session_state.is_leveling_up = False
            st.rerun()
            
        # TRẠNG THÁI 3: ĐANG CHĂM SÓC (Ăn / Uống / Xoa Đầu)
        elif st.session_state.current_action:
            action = st.session_state.current_action
            
            if action == "eat":
                play_local_sfx("nhai.mp3")
                st.image("https://i.pinimg.com/originals/ae/6c/f7/ae6cf73906190b8cd35d420f47755526.gif", use_container_width=True)
                st.toast("🐼 Măm măm! (+1 Điểm trưởng thành)", icon="🎋")
                
            elif action == "drink":
                play_local_sfx("uong.mp3")
                st.image("https://i.pinimg.com/originals/19/b6/67/19b66767ce68886ee8039d3ada659b46.gif", use_container_width=True)
                st.toast("🐼 Ực ực... Khát quá! (+1 Điểm trưởng thành)", icon="🥛")
                
            elif action == "pet":
                play_local_sfx("xoa_dau.mp3")
                st.image("https://i.pinimg.com/originals/80/da/0d/80da0da2fdbf7e8326244ebf3dcf1ecc.gif", use_container_width=True)
                st.toast("🐼 Thích quá! Cọ cọ~ (+1 Điểm trưởng thành)", icon="❤️")
            
            time.sleep(2.5)
            st.session_state.current_action = None
            st.rerun()
            
        # TRẠNG THÁI 4: BÌNH THƯỜNG
        else:
            if st.session_state.diem_pandan < 2:
                st.image("https://i.pinimg.com/originals/0f/bb/07/0fbb072f50573a4f334d933074b7d9ab.gif", use_container_width=True)
            elif 2 <= st.session_state.diem_pandan < 4:
                st.image("https://i.pinimg.com/originals/ca/a1/66/caa166bc1a6275c1bafd537717a0f3a6.gif", use_container_width=True)
            elif 4 <= st.session_state.diem_pandan < 6:
                st.image("https://i.pinimg.com/originals/6e/a6/8b/6ea68bd2c7252befe464dc6be2edc55c.gif", use_container_width=True)
            elif 6 <= st.session_state.diem_pandan < 8:
                st.image("https://i.pinimg.com/originals/21/a7/15/21a715a4012db474455fce3d8356cab4.gif", use_container_width=True)
            elif st.session_state.diem_pandan >= 8:
                st.image("https://i.pinimg.com/originals/21/a7/15/21a715a4012db474455fce3d8356cab4.gif", use_container_width=True)
            
            # --- MENU CHĂM SÓC ---
            if st.session_state.diem_pandan >= 20:
                st.success("👑 Kỷ nguyên Tối cao: Gấu trúc đã trở thành Thần Thú! Bạn đã phá đảo trò chơi này.")
            elif st.session_state.user_xp > 0:
                st.write("---")
                st.write("**Chọn hành động chăm sóc (Mỗi lần tốn 1 XP):**")
                
                # Chia làm 3 cột cho 3 nút
                col1, col2, col3 = st.columns(3)
                
                # Hàm xử lý logic chung cho cả 3 nút
                def handle_action(action_type):
                    st.session_state.user_xp -= 1
                    st.session_state.diem_pandan += 1
                    
                    if st.session_state.diem_pandan == 8:
                        st.session_state.is_max_level_celebration = True
                    elif st.session_state.diem_pandan in [2, 6, 8]:
                        st.session_state.is_leveling_up = True
                    else:
                        st.session_state.current_action = action_type

                with col1:
                    if st.button("🎋 Cho ăn", use_container_width=True):
                        handle_action("eat")
                        st.rerun()
                with col2:
                    if st.button("🥛 Cho uống", use_container_width=True):
                        handle_action("drink")
                        st.rerun()
                with col3:
                    if st.button("👋 Nựng má", use_container_width=True):
                        handle_action("pet")
                        st.rerun()