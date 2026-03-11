import streamlit as st
import time

# ==========================================
# 1. CẤU HÌNH TRANG ĐỘC LẬP
# ==========================================
st.set_page_config(page_title="Hệ thống Tài khoản", page_icon="🔐", layout="centered")

def inject_fullpage_css():
    st.markdown("""
        <style>
        /* Hình nền mờ ảo cho toàn trang */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
        }
        @keyframes gradientBG {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        
        /* Căn giữa thẻ Form */
        .main .block-container {
            max-width: 600px;
            padding-top: 5vh;
        }
        
        /* Hiệu ứng Kính (Glassmorphism) cho Card */
        .glass-card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.5);
            padding: 40px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        }
        
        /* Tùy chỉnh Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            justify-content: center;
            margin-bottom: 20px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: transparent !important;
            font-size: 18px;
            font-weight: bold;
            color: #555;
            padding: 10px 20px;
        }
        .stTabs [aria-selected="true"] {
            color: #e73c7e !important;
            border-bottom: 3px solid #e73c7e !important;
        }
        
        /* Nút bấm Gradient */
        .stButton>button[kind="primary"] {
            background: linear-gradient(135deg, #e73c7e 0%, #ee7752 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
            width: 100%;
            transition: all 0.3s;
        }
        .stButton>button[kind="primary"]:hover {
            transform: scale(1.02);
            box-shadow: 0 5px 15px rgba(231, 60, 126, 0.4);
        }
        
        /* Thẻ User Profile */
        .profile-header {
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 2px dashed #ccc;
            margin-bottom: 20px;
        }
        .profile-avatar {
            font-size: 70px;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. KHỞI TẠO TRẠNG THÁI
# ==========================================
with st.sidebar:
    st.image("https://i.pinimg.com/originals/7b/d8/00/7bd800f192401fc0c2e2b03d67bccb72.gif")
if "user_logged_in" not in st.session_state: 
    st.session_state.user_logged_in = False
if "user_info" not in st.session_state: 
    st.session_state.user_info = {"name": "", "email": "", "phone": "", "bio": ""}
if "is_verifying" not in st.session_state: 
    st.session_state.is_verifying = False
if "temp_data" not in st.session_state: 
    st.session_state.temp_data = {}

# ==========================================
# 3. GIAO DIỆN CHÍNH
# ==========================================
inject_fullpage_css()

# Bọc toàn bộ trong một div Glassmorphism
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

if not st.session_state.user_logged_in:
    
    # ---------------------------------------------------------
    # BƯỚC XÁC THỰC EMAIL (OTP)
    # ---------------------------------------------------------
    if st.session_state.is_verifying:
        st.markdown("<h2 style='text-align: center; color: #333;'>Vui lòng kiểm tra Email 📧</h2>", unsafe_allow_html=True)
        st.write(f"<p style='text-align: center; color: #666;'>Mã xác thực đã được gửi tới <b>{st.session_state.temp_data.get('email', '')}</b></p>", unsafe_allow_html=True)
        st.write("---")
        
        otp = st.text_input("Nhập mã OTP 4 số (Nhập: 1234)", max_chars=4)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("✅ Hoàn tất đăng ký", type="primary", use_container_width=True):
                if otp == "1234":
                    with st.spinner("Đang thiết lập tài khoản..."): time.sleep(1.5)
                    # Cập nhật state
                    st.session_state.user_logged_in = True
                    st.session_state.user_info = {
                        "name": st.session_state.temp_data['name'],
                        "email": st.session_state.temp_data['email'],
                        "phone": "",
                        "bio": "Xin chào! Tôi là thành viên mới."
                    }
                    st.session_state.is_verifying = False
                    st.toast("🎉 Đăng ký thành công!")
                    st.rerun()
                else:
                    st.error("⚠️ Mã OTP không hợp lệ!")
        with col_btn2:
            if st.button("⬅️ Quay lại", use_container_width=True):
                st.session_state.is_verifying = False
                st.rerun()

    # ---------------------------------------------------------
    # LUỒNG ĐĂNG NHẬP / ĐĂNG KÝ
    # ---------------------------------------------------------
    else:
        st.markdown("<h1 style='text-align: center; color: #333; margin-bottom: 5px;'>Hệ thống Tài khoản</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #777; margin-bottom: 30px;'>Quản lý thông tin và bảo mật của bạn</p>", unsafe_allow_html=True)
        
        tab_log, tab_sign, tab_forgot = st.tabs(["Đăng nhập", "Đăng ký", "Quên mật khẩu"])
        
        # --- LOGIN ---
        with tab_log:
            log_email = st.text_input("Địa chỉ Email", placeholder="user@example.com", key="l_email")
            log_pass = st.text_input("Mật khẩu", type="password", placeholder="••••••••", key="l_pass")
            
            if st.button("Đăng nhập vào hệ thống 🚀", type="primary", use_container_width=True):
                if log_email and log_pass:
                    with st.spinner("Đang xác thực..."): time.sleep(1)
                    st.session_state.user_logged_in = True
                    st.session_state.user_info = {
                        "name": log_email.split('@')[0].capitalize(),
                        "email": log_email,
                        "phone": "0123456789",
                        "bio": "Người dùng đam mê công nghệ."
                    }
                    st.rerun()
                else:
                    st.error("Vui lòng điền đầy đủ thông tin.")
                    
        # --- SIGN UP ---
        with tab_sign:
            reg_name = st.text_input("Họ và Tên", placeholder="Nguyễn Văn A", key="r_name")
            reg_email = st.text_input("Địa chỉ Email", placeholder="user@example.com", key="r_email")
            reg_pass = st.text_input("Mật khẩu", type="password", placeholder="Tối thiểu 8 ký tự", key="r_pass")
            reg_pass_confirm = st.text_input("Xác nhận Mật khẩu", type="password", key="r_pass2")
            
            if st.button("Tạo tài khoản mới ✨", type="primary", use_container_width=True):
                if reg_name and reg_email and reg_pass:
                    if reg_pass == reg_pass_confirm:
                        st.session_state.temp_data = {"name": reg_name, "email": reg_email, "pass": reg_pass}
                        st.session_state.is_verifying = True
                        st.rerun()
                    else:
                        st.error("Mật khẩu xác nhận không khớp!")
                else:
                    st.warning("Vui lòng điền đầy đủ thông tin đăng ký.")

        # --- FORGOT PASSWORD ---
        with tab_forgot:
            st.info("Nhập email đã đăng ký, chúng tôi sẽ gửi hướng dẫn khôi phục mật khẩu.")
            fg_email = st.text_input("Email của bạn", key="f_email")
            if st.button("Gửi yêu cầu khôi phục 📩", type="primary", use_container_width=True):
                if fg_email:
                    st.success(f"Yêu cầu đã được gửi tới **{fg_email}**! Vui lòng kiểm tra hộp thư.")
                else:
                    st.error("Vui lòng nhập Email.")

else:
    # ---------------------------------------------------------
    # TRANG USER PROFILE (KHI ĐÃ ĐĂNG NHẬP)
    # ---------------------------------------------------------
    user = st.session_state.user_info
    
    # Header Profile
    st.markdown(f"""
        <div class="profile-header">
            <div class="profile-avatar">✨👤✨</div>
            <h2 style="color: #333; margin:0;">Xin chào, {user['name']}!</h2>
            <p style="color: #666; margin-top:5px;">{user['email']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Cập nhật thông tin cá nhân")
    
    # Form cập nhật Update Profile
    with st.form("update_profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Họ và Tên", value=user['name'])
            new_phone = st.text_input("Số điện thoại", value=user.get('phone', ''))
        with col2:
            st.text_input("Email (Không thể thay đổi)", value=user['email'], disabled=True)
            new_bio = st.text_input("Nghề nghiệp / Mô tả", value=user.get('bio', ''))
            
        submitted = st.form_submit_button("💾 Lưu thay đổi", use_container_width=True)
        if submitted:
            st.session_state.user_info['name'] = new_name
            st.session_state.user_info['phone'] = new_phone
            st.session_state.user_info['bio'] = new_bio
            st.success("✅ Cập nhật thông tin thành công!")
            time.sleep(1)
            st.rerun()
            
    st.write("---")
    if st.button("🚪 Đăng xuất an toàn", use_container_width=True):
        st.session_state.user_logged_in = False
        st.session_state.user_info = {}
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)