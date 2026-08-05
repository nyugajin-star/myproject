import streamlit as st

# Streamlit 페이지 설정 (반드시 최상단에 위치해야 합니다)
st.set_page_config(page_title="국어과 AIDT", page_icon="📖", layout="wide")

st.title('This is my first webapp!!')
st.subheader('국어과 AIDT')

# ----------------------------------------------------
# 1차시 동영상 & Tips
# ----------------------------------------------------
col1, col2 = st.columns((4, 1))

with col1:
    with st.expander('1차시_ 동영상', expanded=True):
        st.title('동영상 시청......')
        url = 'https://www.youtube.com/watch?v=U57LVkQVf4o'
        st.video(url)

with col2:
    with st.expander('Tips...'):
        st.subheader('Tips...')
        imgpath = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5HN3nhykNlU4ABubCJmdq2tmIr88v65bMo9igA9k2eA&s=10'
        st.image(imgpath)
        st.write('This is a term....')


# ----------------------------------------------------
# 2차시 동영상 & Tips (내용 채움 완료)
# ----------------------------------------------------
col2_1, col2_2 = st.columns((4, 1))

with col2_1:
    with st.expander('2차시_ 국어의 개념 이해'):
        st.title('국어의 개념')
        st.markdown("""
        ### 📌 머신러닝 핵심 정리 (개조식)
        - **개념**: 데이터로부터 스스로 패턴을 학습하여 예측이나 판단을 수행하는 인공지능 분야
        - **학습 프로세스**: 데이터 수집 → 전처리 → 모델 선택 및 학습 → 평가 및 예측
        - **주요 학습 유형**:
          - **지도학습(Supervised)**: 정답(Label)이 있는 데이터 학습 (분류, 회귀)
          - **비지도학습(Unsupervised)**: 정답이 없는 데이터의 구조 분석 (군집화)
          - **강화학습(Reinforcement)**: 보상을 통한 최적의 행동 학습
        """)

with col2_2:
    with st.expander('Tips...'):
        st.subheader('Tips...')
        imgpath2 = 'https://i.ytimg.com/vi/MP8R6kBykzE/hqdefault.jpg'
        st.image(imgpath2)
        st.markdown("""
        **💡 핵심 하위 개념**
        - **분류(Classification)**: 범주형 정답 예측
        - **회귀(Regression)**: 연속형 수치 예측
        - **군집화(Clustering)**: 유사 그룹 묶기
        """)


# ----------------------------------------------------
# 3차시 동영상 & Tips
# ----------------------------------------------------
col3_1, col3_2 = st.columns((4, 1))

with col3_1:
    with st.expander('3차시_ 머신러닝의 심화'):
        st.title('머신러닝의 개념')
        st.markdown("""
        - **정의**: 컴퓨터가 명시적인 프로그래밍 없이 데이터로부터 스스로 학습하여 능력을 개선하는 인공지능의 하위 분야입니다.
        - **핵심 원리**: 대량의 데이터를 기반으로 통계적 패턴과 규칙을 스스로 찾아냅니다.
        - **목적**: 학습한 모델을 바탕으로 새로운 데이터에 대한 미래를 예측하거나 최적의 결정을 내립니다.
        - **특징**: 사람이 직접 규칙을 코딩하는 전통적 방식과 달리, 데이터와 경험이 쌓일수록 성능이 향상됩니다.
        """)

with col3_2:
    with st.expander('Tips...'):
        st.subheader('Tips...')
        st.markdown("""
        **📌 머신러닝 하위 개념**
        - **지도학습**: 정답(Label)이 있는 데이터로 학습 (분류, 회귀)
        - **비지도학습**: 정답이 없는 데이터에서 패턴과 구조 발견 (군집화, 차원 축소)
        - **강화학습**: 시행착오를 통한 보상(Reward) 기반 학습
        """)
