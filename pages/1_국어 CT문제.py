import streamlit as st
import streamlit.components.v1 as components
import os

# 페이지 기본 설정
st.set_page_config(
    page_title="국어문법 문제 해결 사례",
    page_icon="💡",
    layout="wide"
)

st.title("💡 국어문법 문제 해결 사례")
st.write("개발된 머신러닝 문제 해결 사례(aa.html)를 시각적으로 확인합니다.")
st.write("---")

# html 파일 경로 지정 (프로젝트 최상위 경로 기준)
HTML_FILE_PATH = "./html/ccc_gajin.html"

# HTML 파일 존재 여부 확인 후 렌더링
if os.path.exists(HTML_FILE_PATH):
    try:
        # UTF-8 인코딩으로 HTML 파일 읽기
        with open(HTML_FILE_PATH, "r", encoding="utf-8") as f:
            html_content = f.read()

        # iframe 형태로 HTML 렌더링
        # width: 1024px, height: 768px, scrolling=True (상하/좌우 스크롤 가능)
        components.html(
            html_content,
            width=1024,
            height=800,
            scrolling=True
        )

    except Exception as e:
        st.error(f"HTML 파일을 읽는 중 오류가 발생했습니다: {e}")

else:
    st.warning(f"⚠️ `{HTML_FILE_PATH}` 파일을 찾을 수 없습니다.")
    st.info("""
    **💡 안내 사항:**
    - `aaa.html` 파일을 `app.py`가 있는 **최상위 프로젝트 폴더**에 저장해 주세요.
    - 파일명이 대소문자까지 일치하는지 확인해 주세요 (`aa.html`).
    """)
