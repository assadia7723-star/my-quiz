# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import streamlit as st
from google import genai

# 페이지 기본 설정
st.set_page_config(
    page_title="완독 확인 독서 퀴즈 생성기 (무료)",
    page_icon="📚",
    layout="centered"
)

st.title("📚 완독 확인 독서 퀴즈 생성기")
st.caption("Google Gemini 무료 AI를 활용하여 책 완독 확인 퀴즈를 생성합니다.")

# 1. Gemini API Key 불러오기
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    with st.sidebar:
        st.warning("Secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
        api_key = st.text_input("Google Gemini API Key 직접 입력", type="password")

# 2. 책 제목 입력
book_title = st.text_input("책 제목을 입력하세요", placeholder="예: 어린 왕자")

# 3. 퀴즈 생성 버튼
if st.button("무료로 퀴즈 생성하기", type="primary", use_container_width=True):
    if not api_key:
        st.error("Google Gemini API Key가 필요합니다. Secrets 설정 또는 사이드바에 입력해 주세요.")
    elif not book_title.strip():
        st.warning("책 제목을 입력해 주세요.")
    else:
        with st.spinner("Gemini 무료 AI가 퀴즈를 만들고 있습니다..."):
            try:
                # Google Gemini 클라이언트 생성
                client = genai.Client(api_key=str(api_key).strip())
                
                prompt = (
                    f"너는 아동 및 청소년 도서 전문 교육자야.\n"
                    f"책 제목: [{book_title.strip()}]\n"
                    f"위 책을 아이가 진짜 완독했는지 검증하기 위한 독서 퀴즈 세트를 만들어줘.\n\n"
                    f"[출력 구성]\n"
                    f"1. 줄거리 확인 문제 2개 (주관식/단답형)\n"
                    f"2. 디테일 확인 문제 2개 (3지 선다형 객관식)\n"
                    f"3. 생각해보는 서술형 문제 1개\n"
                    f"4. 각 문제 밑에 <정답 및 완독 확인 포인트> 작성"
                )

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                st.success("퀴즈 생성 완료!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
