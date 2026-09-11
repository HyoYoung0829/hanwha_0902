from dotenv import load_dotenv
import os

from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트 생성
client = OpenAI(api_key=api_key)

# 간단한 API 호출
response = client.responses.create(
    model="gpt-5-mini",
    input="호날두와 메시중 누가 축구를 더 잘하나요? 이름만 답하세요.",
)

print(response.output_text)
