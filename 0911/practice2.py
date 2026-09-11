from dotenv import load_dotenv
import os

from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# stream()은 응답이 생성되는 동안 이벤트를 하나씩 전달함.
# 텍스트 delta 이벤트가 오면 생성된 텍스트 조각을 바로 출력함.
# 여기서의 이벤트는 일종의 청크랑 비슷한거라고 생각하면 됨.
with client.responses.stream(
    model="gpt-5-mini",
    input="한국 레전드 축구선수 4명을 순위별로 이름만 알려줘.",
) as stream:

    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
