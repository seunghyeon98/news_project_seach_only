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
    # output_text = response.choices[0].message.content.replace("\'", '')
    output_text = response.choices[0].message.content
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
      - type: List[dict]
      - 종합한 내용이 어떤 산업과 연관이 있고, 왜 연관이 있는지를 담은 정보
      - <산업> : 기사와 연관된 산업
      - <설명> : 기사와 연관된 산업이 왜 연관이 있는지를 설명
      - key : value
        'industry' : <산업>
        'description' : <설명>

    - oracle
      - type: List[str]
      - 종합한 내용에서 어떤 insight를 얻을 수 있을지, 예를 들어 투자할 산업, 기업, 새로운 기회와 같은 것을 종합한 내용을 리스트업해서 list로 담아줘.
    * Output은 JSON 형식으로 작성해줘.
    {
      "report_title": <str>,
      "main_text": <str>,
      "relate": [{'industry':<산업>, 'description':<설명>}],
      "oracle": [<str1>, <str2>, <str3>]
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
    print(type(json_obj))
    print(json_obj)
    return json_obj

    try:
        json_obj = json.loads(report)
        print("Generated report structure:", json.dumps(json_obj, ensure_ascii=False, indent=2))
        return json_obj
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print("Raw response:", report)
        # 에러 발생 시 기본 구조 반환
        return {
            "report_title": "Error generating report",
            "main_text": "An error occurred while generating the report.",
            "relate": [],
            "oracle": []
        }

    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
        generate_report(query)
    else:
        print("No search term provided")
