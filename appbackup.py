import streamlit as st # alias : 예명
st.title('This is my first webapp!!')
st.subheader('국어과 AIDT')
col1, col2 = st.columns((4,1))
with col1:
    with st.expander('1차시_ 동영상'):
        st.title('동영상 시청......')
        url = 'https://www.youtube.com/watch?v=U57LVkQVf4o'
        st.video(url)
with col2:
    with st.expander('Tips...'):
        st.subheader('Tips...')
        imgpath='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5HN3nhykNlU4ABubCJmdq2tmIr88v65bMo9igA9k2eA&s=10'
        st.image(imgpath)
        st.write('This is a term....')
coll1, coll2 = st.columns((4,1))
with coll1:
    with st.expander('2차시_ 동영상'):
        st.title('동영상 시청......')
        imgpath1 = './img/images.jpg'
        st.video(imgpath1)
with coll2:
    with st.expander('Tips...'):
        st.subheader('Tips...')
        imgpath = 'https://i.ytimg.com/vi/MP8R6kBykzE/hqdefault.jpg'
        st.image(imgpath)
        st.write('This is a term....')
        coll1, coll2 = st.columns((4,1))
colll1, colll2 = st.columns((4,1))
with colll1:
    with st.expander('2차시_ 동영상'):
        st.title('머신러닝의 개념')
        # 이 자리에 머신러닝의 개념을 설명하는 개조식 텍스를 만들어 채워 주세요. 
        # streamlit webapp의 코드임을 감안해 주세요. 
with colll2:
    with st.expander('Tips...'):
        st.subheader('Tips...')
        # 이 자리에 머신러닝 하위 개념 위주로 팀텍스트 정리를 해 주세요. 짧게 작성합니다.
        # streamlit webapp의 코드임을 감안해 주세요.
collll1, collll2 = st.columns((4, 1))
with collll1:
  with st.expander('3차시_ 동영상'):
    st.title('머신러닝의 개념')
    st.markdown("""
        - **정의**: 컴퓨터가 명시적인 프로그래밍 없이 데이터로부터 스스로 학습하여 능력을 개선하는 인공지능의 하위 분야입니다.
        - **핵심 원리**: 대량의 데이터를 기반으로 통계적 패턴과 규칙을 스스로 찾아냅니다.
        - **목적**: 학습한 모델을 바탕으로 새로운 데이터에 대한 미래를 예측하거나 최적의 결정을 내립니다.
        - **특징**: 사람이 직접 규칙을 코딩하는 전통적 방식과 달리, 데이터와 경험이 쌓일수록 성능이 향상됩니다.
        """)
with collll2:
  with st.expander('Tips...'):
    st.subheader('Tips...')
    st.markdown("""
        **📌 머신러닝 하위 개념**
        - **지도학습**: 정답(Label)이 있는 데이터로 학습 (분류, 회귀)
        - **비지도학습**: 정답이 없는 데이터에서 패턴과 구조 발견 (군집화, 차원 축소)
        - **강화학습**: 시행착오를 통한 보상(Reward) 기반 학습
        """)        
st.set_page_config(layout="wide")        