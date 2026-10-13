matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Tiêu đề ứng dụng
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.markdown("---")

# #1. Tạo frame (Dữ liệu 10 sinh viên)
data = {
    "Ho_va_ten": [
        "Nguyễn Văn An",
        "Trần Thị Bình",
        "Lê Hoàng Chi",
        "Phạm Đình Dũng",
        "Hoàng Thị Hà",
        "Vũ Văn Lân",
        "Đỗ Thị Minh",
        "Bùi Văn Nam",
        "Ngô Hồng Phúc",
        "Lý Thu Trang",
    ],
    "Chuyen_can": [9.0, 8.0, 7.5, 6.0, 9.5, 4.0, 8.5, 7.0, 10.0, 5.5],
    "Giua_ky": [8.0, 7.5, 7.0, 5.5, 8.5, 4.5, 9.0, 6.5, 9.5, 5.0],
    "Cuoi_ky": [8.5, 7.0, 8.0, 5.0, 9.0, 3.5, 8.5, 6.0, 9.5, 4.5],
}

df = pd.DataFrame(data)

# #2. Tính điểm tổng kết
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"] + 0.3 * df["Giua_ky"] + 0.5 * df["Cuoi_ky"]
)
df["Tong_ket"] = df["Tong_ket"].round(2)


# Xếp loại sinh viên
def xep_loai(diem):
  if diem >= 8.5:
    return "Giỏi"
  elif diem >= 7.0:
    return "Khá"
  elif diem >= 5.0:
    return "Trung bình"
  else:
    return "Yếu"


df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# Hiển thị bảng điểm
st.subheader("Bảng điểm chi tiết của 10 sinh viên")
st.dataframe(df)

# #3. Thống kê cơ bản
dtb_lop = df["Tong_ket"].mean()
sv_max = df.loc[df["Tong_ket"].idxmax()]
sv_min = df.loc[df["Tong_ket"].idxmin()]
so_sv_dat = (df["Tong_ket"] >= 5.0).sum()

st.subheader("Thống kê chung của lớp")
col1, col2 = st.columns(2)
with col1:
  st.metric(label="Điểm trung bình lớp", value=f"{dtb_lop:.2f}")
  st.metric(label="Số sinh viên đạt (>= 5.0)", value=f"{so_sv_dat} / 10")
with col2:
  st.metric(
      label="Sinh viên cao điểm nhất",
      value=f"{sv_max['Ho_va_ten']} ({sv_max['Tong_ket']} đ)",
  )
  st.metric(
      label="Sinh viên thấp điểm nhất",
      value=f"{sv_min['Ho_va_ten']} ({sv_min['Tong_ket']} đ)",
  )

st.markdown("---")

# #4. Danh sách chọn sinh viên (Selectbox)
st.subheader("Tra cứu thông tin cá nhân sinh viên")
ten_sinh_vien = st.selectbox(
    "Chọn tên sinh viên để xem chi tiết:", df["Ho_va_ten"]
)

# Lọc thông tin sinh viên được chọn
thong_tin_sv = df[df["Ho_va_ten"] == ten_sinh_vien].iloc[0]

st.write(f"**Họ và tên:** {thong_tin_sv['Ho_va_ten']}")
st.write(f"- Điểm Chuyên cần: {thong_tin_sv['Chuyen_can']}")
st.write(f"- Điểm Giữa kỳ: {thong_tin_sv['Giua_ky']}")
st.write(f"- Điểm Cuối kỳ: {thong_tin_sv['Cuoi_ky']}")
st.write(f"- **Điểm tổng kết:** {thong_tin_sv['Tong_ket']}")
st.write(f"- **Xếp loại:** {thong_tin_sv['Xep_loai']}")

st.markdown("---")

# #5. Trực quan hóa dữ liệu (Biểu đồ cột)
st.subheader("Biểu đồ điểm tổng kết của lớp")
fig, ax = plt.subplots(figsize=(10, 5))

# Dùng họ tên rút gọn hoặc họ tên đầy đủ để hiển thị trục X
ax.bar(df["Ho_va_ten"], df["Tong_ket"], color="skyblue", edgecolor="black")
ax.set_title("Biểu đồ điểm tổng kết của 10 sinh viên", fontsize=12, fontweight="bold")
ax.set_xlabel("Sinh viên", fontsize=10)
ax.set_ylabel("Điểm tổng kết", fontsize=10)
ax.set_ylim(0, 10)
plt.xticks(rotation=45, ha="right")

# Gắn giá trị số lên đầu mỗi cột
for i, v in enumerate(df["Tong_ket"]):
  ax.text(i, v + 0.15, str(v), ha="center", fontsize=9, fontweight="bold")

ax.grid(axis="y", linestyle="--", alpha=0.7)
st.pyplot(fig)

st.markdown("---")

# Hiển thị thông tin người tạo ở cuối trang (chữ nhỏ)
st.markdown(
    "<p style='text-align: center; font-size: small; color: gray;'>Họ và"
    " tên: Nguyễn Xuân Bắc - MSSV: [Điền MSSV của bạn vào đây]</p>",
    unsafe_allow_html=True,
)