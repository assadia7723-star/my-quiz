# -*- coding: utf-8 -*-
import os
import sys

# [인코딩 방어 코드] 시스템 출력 표준을 UTF-8로 강제 지정
os.environ["PYTHONIOENCODING"] = "utf-8"
if hasattr(sys, "stdout") and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import streamlit as st
from openai import OpenAI

# 1. 화면 설정
st.set_page_config(
    page_title="완독 확인 독서 퀴즈 생성기",
    page_icon="📚",
    layout="centered"
)

st.title("📚 완독 확인 독서 퀴즈 생성기")
st.caption("책 제목만 입력하면 아이가 책을 읽었는지 확인하는 퀴즈를 만들어줍니다.")

# 2. 비밀 열쇠(API Key) 불러오기
api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    with st.sidebar:
        st.warning("API Key 설정이 필요합니다.")
        api_key = st.text_input("OpenAI API Key 직접 입력", type="password")

# 3. 책 제목 입력창
book_title = st.text_input("책 제목을 입력하세요", placeholder="예: 호랑이를 부탁해")

# 4. 퀴즈 생성 버튼
if st.button("퀴즈 생성하기", type="primary", use_container_width=True):
    if not api_key:
        st.error("API Key가 필요합니다. Secrets 설정을 확인해 주세요.")
    elif not book_title.strip():
        st.warning("책 제목을 입력해 주세요.")
    else:
        with st.spinner("책 내용을 분석하여 퀴즈를 만들고 있습니다..."):
            try:
                client = OpenAI(api_key=api_key)
                
                system_prompt = """[역할]
너는 아동 및 청소년 도서 전문 교육자이자 독서 지도사야. 
사용자가 '책 제목'을 제공하면, 아이가 그 책을 실제 완독했는지 확인하기 위한 '맞춤형 독서 퀴즈 세트'를 생성해야 해.

[출력 규칙]
1. 입력받은 책 제목을 바탕으로 아래 3가지 영역의 퀴즈를 작성해줘.
   - 1구역: [줄거리 확인] 단답형 또는 주관식 2문제 (책을 읽지 않으면 알 수 없는 주요 사건)
   - 2구역: [디테일 확인] 3지 선다형 객관식 2문제 (주요 등장인물, 행동, 배경 등)
   - 3구역: [생각해보기] 서술형 1문제 (책의 결말이나 교훈에 대한 아이의 생각)
2. 각 문제 아래에는 학부모가 채점할 수 있도록 <정답 및 완독 확인 포인트>를 반드시 함께 제공해줘.
3. 책 내용을 모르거나 불분명할 경우, 추측해서 만들지 말고 "해당 도서의 상세 정보를 찾을 수 없습니다."라고 답변해줘."""

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"책 제목: [{book_title.strip()}] 바탕으로 완독 확인 퀴즈를 만들어주세요."}
                    ]
                )
                
                result = response.choices[0].message.content
                st.success("퀴즈 생성 완료!")
                st.markdown("---")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
