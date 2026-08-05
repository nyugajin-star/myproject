#stramlit webapp의 pages 경로 밑에 서브 페이지로 다음을 생성해주세요.
#머신러닝의 개념에 대해 학습할 콘텐츠 생성
#간단하게 머신러닝의 개념을 실습할 수 있는 시뮬레이터 포함(mock data를 생성해서(분류데이터) 직접 실습하도록 함)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

# 페이지 기본 설정
st.set_page_config(page_title="머신러닝의 개념", page_icon="🤖", layout="wide")

# ==========================================
# 1. 머신러닝 학습 콘텐츠 섹션
# ==========================================
st.title("🤖 머신러닝(Machine Learning)이란?")

st.markdown("""
머신러닝은 컴퓨터가 명시적으로 프로그램되지 않아도, **데이터를 통해 학습하고 경험을 기반으로 성능을 향상**시키는 인공지능의 한 분야입니다. 
마치 사람이 경험을 통해 무언가를 배우는 것처럼, 컴퓨터는 수많은 데이터를 분석하여 패턴을 찾아내고 예측을 수행합니다.

### 📌 머신러닝의 3가지 주요 방식
1. **지도 학습 (Supervised Learning):** 정답(Label)이 있는 데이터를 학습하여 새로운 데이터의 결과를 예측합니다. (예: 스팸 메일 분류, 주택 가격 예측)
2. **비지도 학습 (Unsupervised Learning):** 정답이 없는 데이터에서 숨겨진 구조나 패턴을 찾아냅니다. (예: 고객 군집화, 추천 시스템)
3. **강화 학습 (Reinforcement Learning):** 행동에 대한 보상과 처벌을 통해 최적의 행동 방식을 학습합니다. (예: 알파고, 자율주행)

---
""")

# ==========================================
# 2. 머신러닝 분류(Classification) 시뮬레이터 섹션
# ==========================================
st.header("🎯 머신러닝 시뮬레이터: 데이터 분류해보기")
st.write("""
아래 시뮬레이터는 **지도 학습 중 '분류(Classification)'** 문제를 실습해볼 수 있는 공간입니다.
좌측 사이드바에서 데이터와 머신러닝 모델의 설정을 변경하며, 인공지능이 어떻게 두 가지 색상의 데이터를 구분(결정 경계 생성)하는지 확인해 보세요!
""")

# --- 사이드바 설정 ---
st.sidebar.header("⚙️ 시뮬레이터 설정")

st.sidebar.subheader("1. 가상 데이터 생성")
n_samples = st.sidebar.slider("데이터 개수", 50, 500, 200, step=50, help="점(데이터)의 총 개수를 설정합니다.")
noise = st.sidebar.slider("데이터 섞임 정도 (Noise)", 0.1, 1.0, 0.3, step=0.1, help="값이 클수록 두 데이터 그룹이 겹쳐서 분류하기 어려워집니다.")

st.sidebar.subheader("2. 머신러닝 알고리즘 선택")
classifier_name = st.sidebar.selectbox(
    "알고리즘 종류",
    ("KNN (K-최근접 이웃)", "SVM (서포트 벡터 머신)", "Logistic Regression (로지스틱 회귀)")
)

# 알고리즘별 하이퍼파라미터 설정
if classifier_name == "KNN (K-최근접 이웃)":
    k = st.sidebar.slider("K 값 (참조할 이웃의 수)", 1, 15, 5)
    clf = KNeighborsClassifier(n_neighbors=k)
    st.sidebar.info("새로운 데이터 주변에 있는 K개의 데이터 색상을 보고 다수결로 분류하는 직관적인 알고리즘입니다.")
    
elif classifier_name == "SVM (서포트 벡터 머신)":
    c = st.sidebar.slider("C 값 (규제 강도)", 0.01, 10.0, 1.0)
    clf = SVC(C=c, kernel='linear')
    st.sidebar.info("두 데이터 그룹 사이의 여백(Margin)을 가장 넓게 가지는 직선을 그어 분류하는 알고리즘입니다.")
    
else:
    clf = LogisticRegression()
    st.sidebar.info("데이터가 특정 클래스에 속할 확률을 계산하여 분류하는 기본적인 선형 알고리즘입니다.")

# --- 데이터 생성 및 모델 학습 ---
# 가상의 2차원 데이터 생성 (make_classification 사용)
X, y = make_classification(
    n_samples=n_samples, 
    n_features=2, 
    n_informative=2,
    n_redundant=0, 
    n_clusters_per_class=1,
    class_sep=1/noise, 
    random_state=42
)

# 모델 학습 (Fit)
clf.fit(X, y)

# --- 시각화 (결정 경계 및 데이터 포인트) ---
fig, ax = plt.subplots(figsize=(8, 6))

# 결정 경계를 그리기 위한 메시그리드 생성
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.05),
                     np.arange(y_min, y_max, 0.05))

# 배경 영역 예측
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# 결정 경계 및 데이터 포인트 플롯
ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.coolwarm)
ax.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', cmap=plt.cm.coolwarm)
ax.set_title(f"Decision Boundary of {classifier_name}", fontsize=14)
ax.set_xlabel("Feature 1")
ax.set_ylabel("Feature 2")

# Streamlit에 차트 렌더링
col1, col2 = st.columns([2, 1])

with col1:
    st.pyplot(fig)

with col2:
    st.success("✅ **학습 완료!**")
    st.write(f"현재 인공지능은 **{classifier_name}** 알고리즘을 사용하여 푸른색 영역과 붉은색 영역을 나누는 기준(결정 경계)을 학습했습니다.")
    st.write("---")
    st.write("💡 **실습 팁:**")
    st.write("- 좌측의 데이터 섞임 정도(Noise)를 높여보세요. 데이터가 복잡해질수록 경계를 나누기 어려워집니다.")
    st.write("- 알고리즘을 변경해가며 경계선의 모양(직선, 곡선 등)이 어떻게 변하는지 관찰해 보세요.")