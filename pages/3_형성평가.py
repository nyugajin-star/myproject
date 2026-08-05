import streamlit as st
import sqlite3
import hashlib
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="3_형성평가", page_icon="📝", layout="wide")

DB_FILE = "myproject.db"

# ==========================================
# 1. 데이터베이스(DB) 관련 함수
# ==========================================
def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # users 테이블 생성
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # learning_history 테이블 생성
    c.execute('''
        CREATE TABLE IF NOT EXISTS learning_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid TEXT NOT NULL,
            m1 INTEGER, m2 INTEGER, m3 INTEGER, m4 INTEGER, m5 INTEGER,
            m6 INTEGER, m7 INTEGER, m8 INTEGER, m9 INTEGER, m10 INTEGER,
            score INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# 비밀번호 암호화 (SHA-256)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 회원가입
def register_user(userid, password):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (userid, password) VALUES (?, ?)", 
                  (userid, hash_password(password)))
        conn.commit()
        return True, "회원가입이 성공적으로 완료되었습니다!"
    except sqlite3.IntegrityError:
        return False, "이미 존재하는 계정 ID입니다. 다른 ID를 입력해 주세요."
    finally:
        conn.close()

# 로그인 검증
def login_user(userid, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE userid = ? AND password = ?", 
              (userid, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user is not None

# 시험 결과 저장
def save_score(userid, user_answers, score):
    conn = get_connection()
    c = conn.cursor()
    query = '''
        INSERT INTO learning_history (userid, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    c.execute(query, (userid, *user_answers, score))
    conn.commit()
    conn.close()

# 응시 이력 가져오기
def get_user_history(userid):
    conn = get_connection()
    query = "SELECT m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, score, created_at FROM learning_history WHERE userid = ? ORDER BY created_at DESC"
    df = pd.read_sql_query(query, conn, params=(userid,))
    conn.close()
    return df

# DB 초기화 수행
init_db()

# ==========================================
# 2. 세션 상태 관리 (로그인 처리)
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'userid' not in st.session_state:
    st.session_state['userid'] = ""

st.title("📝 머신러닝 개념 형성평가")

# ==========================================
# 3. 로그인 및 회원가입 화면
# ==========================================
if not st.session_state['logged_in']:
    st.info("💡 형성평가 응시 및 제출 이력 관리를 위해 로그인이 필요합니다.")
    tab1, tab2 = st.tabs(["🔑 로그인", "📝 회원가입"])

    with tab1:
        st.subheader("로그인")
        login_id = st.text_input("아이디", key="login_id")
        login_pw = st.text_input("비밀번호", type="password", key="login_pw")
        if st.button("로그인", use_container_width=True):
            if login_user(login_id, login_pw):
                st.session_state['logged_in'] = True
                st.session_state['userid'] = login_id
                st.success(f"{login_id}님 환영합니다!")
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

    with tab2:
        st.subheader("회원가입")
        reg_id = st.text_input("새 아이디", key="reg_id")
        reg_pw = st.text_input("새 비밀번호", type="password", key="reg_pw")
        if st.button("회원가입 실행", use_container_width=True):
            if reg_id and reg_pw:
                success, msg = register_user(reg_id, reg_pw)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.warning("아이디와 비밀번호를 모두 입력해 주세요.")

# ==========================================
# 4. 형성평가 문항 및 이력 섹션 (로그인 후)
# ==========================================
else:
    # 사용자 정보 및 로그아웃 버튼
    col_user1, col_user2 = st.columns([4, 1])
    with col_user1:
        st.write(f"👤 **현재 접속 사용자:** `{st.session_state['userid']}`")
    with col_user2:
        if st.button("🚪 로그아웃", key="logout"):
            st.session_state['logged_in'] = False
            st.session_state['userid'] = ""
            st.rerun()

    st.write("---")

    # 형성평가 10문항 데이터 정의
    questions = [
        {
            "id": 1,
            "question": "1. 머신러닝(Machine Learning)의 가장 적절한 정의는 무엇인가요?",
            "options": [
                "① 사람이 모든 규칙을 직접 하드코딩하여 동작하도록 만드는 시스템",
                "② 데이터로부터 알고리즘이 스스로 학습하여 예측이나 결정을 내리는 기술",
                "③ 단순히 데이터를 엑셀 시트에 저장하고 정렬하는 데이터베이스 기술",
                "④ 로봇의 물리적 하드웨어를 제작하는 기계 공학 기술",
                "⑤ 컴퓨터 화면의 디자인 요소를 자동으로 배치해 주는 그래픽 도구"
            ],
            "answer": 2,
            "hint": "명시적인 프로그래밍 없이 데이터 기반으로 패턴을 찾아내는 인공지능의 분야입니다.",
            "explanation": "머신러닝은 데이터를 기반으로 컴퓨터가 통계적 패턴을 학습하는 인공지능 하위 기술입니다."
        },
        {
            "id": 2,
            "question": "2. 지도학습(Supervised Learning)에 대한 설명으로 옳은 것은 무엇인가요?",
            "options": [
                "① 정답(Label)이 없는 데이터만 사용하여 데이터 간의 구조를 분석한다.",
                "② 데이터와 함께 '정답(Label)'이 제공되어 모델을 학습시킨다.",
                "③ 보상(Reward)과 처벌 시스템을 통해 최적의 행동 방식을 학습한다.",
                "④ 데이터의 차원을 줄이는 기술로만 구성된다.",
                "⑤ 인공지능이 인간의 개입 없이 스스로 목적을 재설정하는 학습 방식이다."
            ],
            "answer": 2,
            "hint": "입력 데이터(X)와 함께 문제의 정답(y)을 미리 알려주고 학습시킵니다.",
            "explanation": "지도학습은 입력 특징과 그에 해당하는 정답(라벨) 쌍을 학습 데이터로 사용합니다."
        },
        {
            "id": 3,
            "question": "3. 다음 중 비지도학습(Unsupervised Learning)의 대표적인 활용 예시는 무엇인가요?",
            "options": [
                "① 스팸 메일 분류 (스팸 / 일반)",
                "② 주택의 위치와 크기를 바탕으로 한 집값 가격 예측",
                "③ 유사한 구매 패턴을 가진 고객그룹을 만드는 군집화(Clustering)",
                "④ 사진 속 동물이 고양이인지 강아지인지 판별하기",
                "⑤ 게임 캐릭터가 장애물을 피해 도착지까지 가도록 학습하기"
            ],
            "answer": 3,
            "hint": "라벨(정답)이 없는 상태에서 유사한 특징을 가진 데이터끼리 무리를 짓습니다.",
            "explanation": "군집화(Clustering)는 정답이 없는 데이터의 숨겨진 패턴이나 그룹 구조를 찾아내는 비지도학습 기법입니다."
        },
        {
            "id": 4,
            "question": "4. 강화학습(Reinforcement Learning)의 핵심 요소에 포함되지 않는 것은 무엇인가요?",
            "options": [
                "① 에이전트 (Agent)",
                "② 환경 (Environment)",
                "③ 보상 (Reward)",
                "④ 라벨링된 정답 데이터 (Labeled Ground Truth)",
                "⑤ 상태 (State)"
            ],
            "answer": 4,
            "hint": "강화학습은 정답을 주는 대신 행동에 대한 '보상'을 통해 학습합니다.",
            "explanation": "강화학습은 시행착오를 통해 보상을 극대화하는 방식이며, 정답 라벨 데이터는 지도학습에 필요합니다."
        },
        {
            "id": 5,
            "question": "5. 모델이 학습 데이터에 지나치게 적응하여 새로운 입력 데이터에 대한 예측 능력이 떨어지는 현상을 무엇이라 하나요?",
            "options": [
                "① 과소적합 (Underfitting)",
                "② 과대적합 (Overfitting)",
                "③ 정규화 (Normalization)",
                "④ 차원의 축소 (Dimensionality Reduction)",
                "⑤ 교차 검증 (Cross Validation)"
            ],
            "answer": 2,
            "hint": "학습 데이터에서는 높은 성능을 보이지만 검증/테스트 데이터에서는 낮은 성능을 보입니다.",
            "explanation": "Overfitting(과대적합)은 모델이 학습 데이터의 노이즈까지 지나치게 기억하여 일반화 성능이 떨어지는 상태입니다."
        },
        {
            "id": 6,
            "question": "6. 머신러닝에서 데이터를 훈련 데이터(Train Data)와 테스트 데이터(Test Data)로 나누는 주요 이유는 무엇인가요?",
            "options": [
                "① 데이터 저장 용량을 줄이기 위해",
                "② 모델 학습 속도를 2배로 높이기 위해",
                "③ 모델의 Generalization(일반화) 평가 능력을 객관적으로 검증하기 위해",
                "④ 결측치(Missing Value)를 자동으로 채우기 위해",
                "⑤ 데이터의 정답 라벨을 삭제하기 위해"
            ],
            "answer": 3,
            "hint": "학습에 사용되지 않은 미지의 데이터에 대해 인공지능이 잘 작동하는지 파악해야 합니다.",
            "explanation": "테스트 데이터 세트는 학습에 전혀 참여하지 않은 데이터를 통해 객관적인 성능을 측정하기 위해 따로 분리합니다."
        },
        {
            "id": 7,
            "question": "7. 연속적인 숫자 데이터(예: 온도, 집값, 매출액)를 예측하는 머신러닝 문제를 무엇이라 하나요?",
            "options": [
                "① 회귀 (Regression)",
                "② 분류 (Classification)",
                "③ 군집화 (Clustering)",
                "④ 차원 축소 (Dimension Reduction)",
                "⑤ 연관 규칙 분석 (Association Rule)"
            ],
            "answer": 1,
            "hint": "범주(이메일 스팸 여부 등)를 구분하는 것은 '분류', 연속된 양적 수치를 예측하는 것은 '이것'입니다.",
            "explanation": "회귀(Regression)는 연속적인 수치를 예측하는 지도학습의 대표적인 과제입니다."
        },
        {
            "id": 8,
            "question": "8. 머신러닝 모델 학습에 입력되는 데이터의 속성 또는 변수를 의미하는 용어는 무엇인가요?",
            "options": [
                "① 레이블 (Label)",
                "② 특성 (Feature)",
                "③ 에포크 (Epoch)",
                "④ 가중치 (Weight)",
                "⑤ 편향 (Bias)"
            ],
            "answer": 2,
            "hint": "예를 들어 주택 가격 예측 문제에서 '방의 개수', '면적', '위치' 등이 이에 해당합니다.",
            "explanation": "특성(Feature)은 머신러닝 모델이 예측을 수행하기 위해 학습 데이터로 사용하는 개별 측정 가능 속성입니다."
        },
        {
            "id": 9,
            "question": "9. 머신러닝 모델이 스스로 학습하는 파라미터가 아니라, 사용자가 직접 설정해 주어야 하는 매개변수는 무엇인가요?",
            "options": [
                "① 하이퍼파라미터 (Hyperparameter)",
                "② 손실 함수값 (Loss Value)",
                "③ 예측값 (Predicted Value)",
                "④ 잔차 (Residual)",
                "⑤ 기울기 (Gradient)"
            ],
            "answer": 1,
            "hint": "KNN의 K값, 학습률(Learning Rate)처럼 모델 구조나 학습 동작 방식을 개발자가 사전에 지정하는 설정값입니다.",
            "explanation": "하이퍼파라미터는 모델 학습 전에 사람이 직접 지정해야 하는 매개변수입니다."
        },
        {
            "id": 10,
            "question": "10. 분류 모델의 성능을 평가할 때, 전체 예측 중에서 올바르게 맞춘 비율을 의미하는 지표는 무엇인가요?",
            "options": [
                "① 재현율 (Recall)",
                "② 정밀도 (Precision)",
                "③ 정확도 (Accuracy)",
                "④ F1-Score",
                "⑤ Mean Squared Error (MSE)"
            ],
            "answer": 3,
            "hint": "(맞춘 전체 개수) / (전체 샘플 개수) 로 계산됩니다.",
            "explanation": "정확도(Accuracy)는 전체 데이터 중 모델이 올바르게 예측한 샘플의 비율을 뜻합니다."
        }
    ]

    # 평가지 Form
    with st.form("quiz_form"):
        st.subheader("📋 10문항 형성평가 (문항당 10점, 만점 100점)")
        user_answers = []

        for idx, q in enumerate(questions):
            st.markdown(f"#### {q['question']}")
            
            # 힌트 제공 Expander
            with st.expander("💡 힌트 보기"):
                st.info(q["hint"])

            # 5지 선다 라디오 버튼
            choice = st.radio(
                f"문항 {idx+1}번 정답 선택:",
                options=list(range(1, 6)),
                format_func=lambda x: q["options"][x-1],
                key=f"q_{idx+1}"
            )
            user_answers.append(choice)
            st.write("")

        submit_btn = st.form_submit_button("🏁 형성평가 제출하기", use_container_width=True)

    # 제출 결과 처리
    if submit_btn:
        score = 0
        correct_list = []
        
        for idx, q in enumerate(questions):
            if user_answers[idx] == q["answer"]:
                score += 10
                correct_list.append(True)
            else:
                correct_list.append(False)

        # DB 저장
        save_score(st.session_state['userid'], user_answers, score)

        st.balloons()
        st.success(f"🎉 평가가 완료되었습니다! **{st.session_state['userid']}**님의 점수: **{score} / 100점**")

        # 결과 및 정답/해설 확인
        st.subheader("🔍 채점 결과 및 정답 해설")
        for idx, q in enumerate(questions):
            status = "✅ 정답" if correct_list[idx] else "❌ 오답"
            with st.expander(f"문항 {idx+1} 채점 결과: {status} (선택한 답: {user_answers[idx]}번 / 정답: {q['answer']}번)"):
                st.write(f"**정답:** {q['options'][q['answer']-1]}")
                st.write(f"**해설:** {q['explanation']}")

    st.write("---")

    # ==========================================
    # 5. 과거 응시 이력 확인 (DB 조회)
    # ==========================================
    st.subheader("📊 나의 형성평가 응시 이력")
    history_df = get_user_history(st.session_state['userid'])

    if not history_df.empty:
        # 보기 쉽게 컬럼명 변경
        history_df.columns = [
            "1번", "2번", "3번", "4번", "5번", 
            "6번", "7번", "8번", "9번", "10번", 
            "총점", "응시 일시"
        ]
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("아직 응시한 이력이 없습니다. 위의 형성평가를 제출해 보세요!")