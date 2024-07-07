'''
search_news.py로부터 유저의 검색을 통해 수집된 기사들을 바탕으로 보고서를 만드는 용.
보고서가 만들어지면 news_report.json으로 저장됨.
'''

import sys
import json
from openai import OpenAI
from search_news import fetch_and_process_articles
import os
# Load OpenAI API key
from dotenv import load_dotenv

load_dotenv()



client = OpenAI(
    # This is the default and can be omitted
    api_key= os.getenv('OPENAI_API_KEY')
)


def llm_answer_request(instruction, prompt, model):
    messages = [{"role": "system", "content": instruction},
                {"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        response_format= {"type": "json_object"}

    )
    # output_text = response.choices[0].message['content']
    # output_text = response.choices[0]['message']['content']
    output_text = response.choices[0].message.content.replace("\'", '')
    return output_text
    

def generate_prompt(searched_news):
    instruction = """
    - 너는 유저가 뉴스 기사들을 입력하면 하나의 보고서로 종합하는 보고서 작성 BOT이야.
    - 출력은 한국어로 작성하고, JSON으로 출력해줘.
    - 보고서에 들어갈 사항은 다음과 같아.
    - report_title
      - type: str
      - 종합한 내용을 하나의 주제로 표시할 제목
    - main_text   
      - type: str
      - 뉴스 기사들의 내용을 하나의 내용으로 종합한 내용
    - relate
      - type: str
      - 종합한 내용이 어떤 산업과 연관이 있는지에 대한 내용
    - oracle
      - type: <List>
      - 종합한 내용에서 어떤 insight를 얻을 수 있을지, 예를 들어 투자할 산업, 기업, 새로운 기회와 같은 것을 종합한 내용을 리스트업해서 list로 담아줘.
    * Output은 JSON 형식으로 작성해줘.
    {
      "report_title": "<str>",
      "main_text": "<str>",
      "relate": "<str>",
      "oracle": ["<str1>", "<str2>", "<str3>"]
    }
    """
    prompt = f"""
    * 뉴스 기사
    {json.dumps(searched_news, ensure_ascii=False, indent=4)}
    """
    ans = llm_answer_request(instruction, prompt, model='gpt-4o')
    return ans

def generate_report(query):
    # query 대한 뉴스 검색하기.
    searched_news = fetch_and_process_articles(query)

    # 검색된 뉴스 기사들을 바탕으로 보고서 생성
    report = generate_prompt(searched_news)
    json_obj = json.loads(report)
    # print(type(json_obj))
    return json_obj
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
        generate_report(query)
    else:
        print("No search term provided")
