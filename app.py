import streamlit as st
import random
import hashlib
import time
import os

# --------------------------------------------------------------------------
# [시스템] 데이터 로더
# --------------------------------------------------------------------------
@st.cache_data
def load_data_from_files():
    text_files = ["bible.txt", "sutra.txt", "literature.txt", "talmud.txt", "lyrics.txt", "poetry.txt"]
    combined_texts = []
    image_urls = []

    for file in text_files:
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
                combined_texts.extend(lines)
    
    if os.path.exists("images.txt"):
        with open("images.txt", "r", encoding="utf-8") as f:
            image_urls = [line.split()[0] for line in f.readlines() if line.strip()]
    
    if not image_urls:
        image_urls = ["https://images.unsplash.com/photo-1518098268026-4e140130aa11?w=800"]

    return combined_texts, image_urls

# --------------------------------------------------------------------------
# [로직] 운명의 연금술
# --------------------------------------------------------------------------
def get_oracle_result(user_question, text_pool, image_pool):
    if not text_pool:
        return "데이터가 없습니다.", image_pool[0]

    fate_seed = f"{user_question}_{time.time()}"
    hash_obj = hashlib.sha256(fate_seed.encode())
    seed_int = int(hash_obj.hexdigest(), 16)
    
    random.seed(seed_int)
    return random.choice(text_pool), random.choice(image_pool)

# --------------------------------------------------------------------------
# [화면] UI 구성
# --------------------------------------------------------------------------
st.set_page_config(page_title="The Oracle", page_icon="📖", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@300;500;700&display=swap');
    
    /* 1. 배경: 차분한 미색 (Paper Tone) */
    .stApp {
        background-color: #f9f9f7;
        color: #2c2c2c;
        font-family: 'Noto Serif KR', serif;
    }

    /* 2. 헤더 타이틀 */
    .header-container {
        padding: 50px 0 30px 0;
        text-align: center;
        margin-bottom: 20px;
    }
    .main-title {
        font-size: 36px;
        color: #1a1a1a;
        font-weight: 700;
        letter-spacing: -1px;
        margin-bottom: 15px;
    }
    .sub-title {
        font-size: 15px;
        color: #666;
        line-height: 1.8;
        font-weight: 300;
        font-style: italic;
    }

    /* 3. 입력창 디자인 */
    .stTextInput > div > div > input {
        background-color: transparent !important;
        color: #111 !important;
        text-align: left;
        border: none;
        border-bottom: 1px solid #aaa;
        border-radius: 0px;
        font-family: 'Noto Serif KR', serif;
        font-size: 18px;
        padding: 10px 5px;
        transition: all 0.3s;
    }
    .stTextInput > div > div > input:focus {
        border-bottom: 1px solid #1a1a1a;
        box-shadow: none;
    }

    /* 4. 버튼 디자인 (기본 좌측 정렬) */
    .stButton > button {
        background-color: #1a1a1a;
        color: #ffffff;
        border: none;
        border-radius: 0px;
        padding: 12px 30px;
        font-size: 14px;
        font-weight: 500;
        letter-spacing: 0.5px;
        margin-top: 15px;
        transition: background 0.3s;
    }
    .stButton > button:hover {
        background-color: #555;
        color: #fff;
    }

    /* 5. 결과 카드 (엽서 스타일) */
    .result-frame {
        background-color: #ffffff;
        padding: 20px 20px 40px 20px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.05);
        margin-top: 40px;
        text-align: center;
        animation: fadeUp 1.0s ease-out;
    }
    .result-img {
        width: 100%;
        max-height: 400px;
        object-fit: cover;
        margin-bottom: 30px;
        filter: grayscale(20%);
    }
    .result-text {
        font-size: 21px;
        line-height: 1.7;
        color: #111;
        font-weight: 500;
        word-break: keep-all;
        padding: 0 10px;
    }
    .result-source {
        font-size: 12px;
        color: #999;
        margin-top: 25px;
        font-family: sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: block;
    }

    /* 6. 하단 가이드 */
    .guide-text {
        margin-top: 50px;
        text-align: center;
        color: #888;
        font-size: 13px;
        font-weight: 300;
        border-top: 1px solid #e0e0e0;
        padding-top: 20px;
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 데이터 로드
texts, images = load_data_from_files()

# ==============================================================================
# [Header] 제목과 도입부
# ==============================================================================
st.markdown("""
<div class='header-container'>
    <div class='main-title'>The Literary Oracle</div>
    <div class='sub-title'>
        우연은 신이 서명하지 않은 기적입니다.<br>
        당신의 질문을 문장으로 남겨주세요.
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# [Input] 질문 입력 및 버튼
# ==============================================================================
with st.form("question_form"):
    user_question = st.text_input("", placeholder="이곳에 질문을 입력하세요")
    
    # 버튼 (기본 좌측 정렬로 복귀)
    submitted = st.form_submit_button("신탁 확인하기")

# ==============================================================================
# [Result] 결과 화면
# ==============================================================================
if submitted:
    if not user_question:
        st.warning("질문을 입력하지 않으면 문은 열리지 않습니다.")
    elif not texts:
        st.error("데이터 파일이 비어있습니다.")
    else:
        with st.spinner("페이지를 넘기는 중..."):
            time.sleep(1.2)
            raw_text, result_img = get_oracle_result(user_question, texts, images)
            
            # 출처 분리 로직
            if "(" in raw_text and ")" in raw_text:
                parts = raw_text.rsplit("(", 1)
                main_text = parts[0].strip()
                source_text = parts[1].replace(")", "").strip()
            else:
                main_text = raw_text
                source_text = "Unknown Source"

        # 결과물 출력 (엽서 스타일)
        st.markdown(f"""
        <div class='result-frame'>
            <img src='{result_img}' class='result-img'>
            <div class='result-text'>
                “{main_text}”
            </div>
            <span class='result-source'>{source_text}</span>
        </div>
        """, unsafe_allow_html=True)

        # 해석 가이드
        st.markdown("""
        <div class='guide-text'>
            이 문장은 정답이 아닙니다. 거울입니다.<br>
            읽는 순간 당신의 마음에 떠오른 감정, 그것이 당신의 해답입니다.
        </div>
        """, unsafe_allow_html=True)

else:
    # 초기 화면 하단 문구
    st.markdown("""
    <div class='guide-text' style='border-top: none;'>
        Curated for your serendipity.
    </div>
    """, unsafe_allow_html=True)