Python
import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg') # Thêm dòng này để tránh xung đột giao diện đồ họa trên server
import matplotlib.pyplot as plt

# --- DỮ LIỆU & XỬ LÝ (Giữ nguyên phần đầu của bạn) ---
data = {
    'Họ và tên': ['An', 'Bình', 'Chi', 'Dũng', 'Hà', 'Lan', 'Minh', 'Nam', 'Phúc', 'Trang'],
    'Chuyên cần': [8, 9, 7, 6, 10, 8, 9, 7, 8, 9],
    'Giữa kỳ': [7, 8, 6, 7, 9, 8, 7, 6, 8, 9],
    'Cuối kỳ': [8, 8.5, 7, 6.5, 9, 8, 8, 7, 8.5, 9]
}
df = pd.DataFrame(data)
df['Tong_ket'] = 0.2 * df['Chuyên cần'] + 0.3 * df['Giữa kỳ'] + 0.5 * df['Cuối kỳ']

def xep_loai(dtk):
    if dtk >= 8.5: return 'Giỏi'
    elif dtk >= 7.0: return 'Khá'
    elif dtk >= 5.0: return 'Trung bình'
    else: return 'Yếu'

df['Xep_loai'] = df['Tong_ket'].apply(xep_loai)

# --- GIAO DIỆN STREAMLIT ---
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

st.subheader("📋 Bảng điểm chi tiết của 10 sinh viên")
st.dataframe(df)

st.subheader("📊 Thống kê chung của lớp")
dtk_tb = df['Tong_ket'].mean()
max_sv = df.loc[df['Tong_ket'].idxmax()]
min_sv = df.loc[df['Tong_ket'].idxmin()]
so_sv_dat = len(df[df['Tong_ket'] >= 5.0])

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Điểm trung bình của lớp", value=f"{dtk_tb:.2f}")
    st.metric(label="Số sinh viên đạt (>= 5.0)", value=f"{so_sv_dat}/10")

with col2:
    st.write(f"🌟 **Điểm cao nhất:** {max_sv['Họ và tên']} ({max_sv['Tong_ket']:.2f})")
    st.write(f"⚠️ **Điểm thấp nhất:** {min_sv['Họ và tên']} ({min_sv['Tong_ket']:.2f})")

st.subheader("🔍 Tra cứu thông tin sinh viên")
selected_student = st.selectbox("Chọn tên sinh viên:", df['Họ và tên'].tolist())
student_info = df[df['Họ và tên'] == selected_student].iloc[0]
st.info(f"""
* **Họ và tên:** {student_info['Họ và tên']}
* **Điểm Chuyên cần:** {student_info['Chuyên cần']}
* **Điểm Giữa kỳ:** {student_info['Giữa kỳ']}
* **Điểm Cuối kỳ:** {student_info['Cuối kỳ']}
* **Điểm Tổng kết:** {student_info['Tong_ket']:.2f}
* **Xếp loại:** {student_info['Xep_loai']}
""")

st.subheader("📈 Biểu đồ điểm tổng kết của 10 sinh viên")
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df['Họ và tên'], df['Tong_ket'], color='skyblue')
ax.set_xlabel("Họ và tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_title("Biểu đồ điểm tổng kết của sinh viên")
ax.set_ylim(0, 10)
st.pyplot(fig)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: small;'>Người tạo ứng dụng: [Họ tên của bạn] - [MSSV]</p>", unsafe_allow_html=True)
