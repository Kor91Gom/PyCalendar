import streamlit as st
import calendar
from datetime import datetime

# 현재 날짜 기준 초기화
now = datetime.now()
if "year" not in st.session_state:
    st.session_state.year = now.year
if "month" not in st.session_state:
    st.session_state.month = now.month
if "day" not in st.session_state:
    st.session_state.day = now.day

# 🎨 사용자 설정
st.sidebar.header("🎨 색상 및 스타일 설정")
calendar_bg = st.sidebar.color_picker("캘린더 배경색", "#ffffff")
calendar_text = st.sidebar.color_picker("캘린더 글자색", "#000000")
highlight_bg = st.sidebar.color_picker("오늘 날짜 배경색", "#e6e6ff")
highlight_text = st.sidebar.color_picker("오늘 날짜 글자색", "#5a00b0")
font_size = st.sidebar.slider("글자 크기(px)", 12, 32, 16)
font_weight = st.sidebar.selectbox("글자 두께", ["normal", "bold"])  # cSpell:ignore selectbox

# 💅 스타일 적용
st.markdown(
    f"""
    <style>
    .calendar-header {{
        position: relative;
        background-color: {calendar_bg};
        color: {calendar_text};
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        font-size: {font_size + 4}px;
        font-weight: {font_weight};
    }}
    .day-box {{
        background-color: {calendar_bg};
        color: {calendar_text};
        border: 1px solid #ddd;
        padding: 10px;
        height: 100px;
        border-radius: 5px;
        font-size: {font_size}px;
        font-weight: {font_weight};
        text-align: center;
    }}
    .today-box {{
        background-color: {highlight_bg};
        color: {highlight_text};
        border: 2px solid {highlight_text};
        padding: 10px;
        height: 100px;
        border-radius: 5px;
        font-size: {font_size}px;
        font-weight: {font_weight};
        text-align: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ⬅️▶️ 버튼 인터페이스
col_left, col_center, col_right = st.columns([1, 4, 1])
with col_left:
    if st.button("◀"):
        if st.session_state.month == 1:
            st.session_state.month = 12
            st.session_state.year -= 1
        else:
            st.session_state.month -= 1
with col_center:
    st.markdown(
        f"<div class='calendar-header'>{st.session_state.year}년 {st.session_state.month}월</div>",
        unsafe_allow_html=True
    )
with col_right:
    if st.button("▶"):
        if st.session_state.month == 12:
            st.session_state.month = 1
            st.session_state.year += 1
        else:
            st.session_state.month += 1

# 📌 공휴일 및 대체공휴일 목록
holidays = {
    "2025-01-01": "신정",
    "2025-03-01": "삼일절",
    "2025-05-05": "어린이날",
    "2025-06-06": "현충일",
    "2025-08-15": "광복절",
    "2025-09-15": "추석",
    "2025-09-16": "추석 연휴",
    "2025-09-17": "추석 연휴",
    "2025-10-03": "개천절",
    "2025-10-09": "한글날",
    "2025-10-10": "대체공휴일",
    "2025-12-25": "성탄절"
}

# 📆 날짜 정보
year = st.session_state.year
month = st.session_state.month
month_days = calendar.monthrange(year, month)[1]
first_weekday = calendar.monthrange(year, month)[0]

# 🗓 요일 표시
weekdays = ["월", "화", "수", "목", "금", "토", "일"]
cols = st.columns(7)
for i, weekday in enumerate(weekdays):
    cols[i].markdown(
        f"<div style='text-align:center;font-size:{font_size}px;font-weight:{font_weight};color:{calendar_text};'>{weekday}</div>",
        unsafe_allow_html=True
    )

# 📅 날짜 표시
d = 1
row = 0
while d <= month_days:
    cols = st.columns(7)
    for i in range(7):
        if row == 0 and i < first_weekday:
            cols[i].markdown("")
        elif d <= month_days:
            date_str = f"{year}-{month:02d}-{d:02d}"
            is_today = (year == now.year and month == now.month and d == now.day)
            box_class = "today-box" if is_today else "day-box"

            content = f"<div class='{box_class}'><strong>{d}일</strong>"
            if date_str in holidays:
                content += f"<br><span style='color:red;font-weight:bold'>{holidays[date_str]}</span>"
            content += "</div>"

            cols[i].markdown(content, unsafe_allow_html=True)
            d += 1
    row += 1
