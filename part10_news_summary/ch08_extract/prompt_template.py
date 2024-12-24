json_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "doc_category": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["정책/금융", "채권/외환", "IB/기업", "증권", "국제뉴스", "해외주식", "부동산"]
      },
      "minItems": 1
    },
    "summary": {
      "type": "string",
      "maxLength": 1000
    },
    "events": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["신제품 출시", "기업 인수합병", "리콜", "배임횡령", "오너 리스크", "자연재해", "제품 불량"]
      },
      "minItems": 0
    }
  },
  "required": ["doc_category", "summary", "events"],
}

prompt_template = """아래 뉴스 텍스트를 참고하여 세 가지 task를 수행하시오.

Task #1: 텍스트를 참고해서 다음과 같은 카테고리로 정확하게 분류하시오. 아래 카테고리에 해당하지 않으면, 빈 리스트를 반환하시오.
카테고리 : 정책/금융, 채권/외환, IB/기업, 증권, 국제뉴스, 해외주식, 부동산

Task #2: 뉴스 내용을 최대 3문장으로 요약하시오.

Task #3: 뉴스에서 금융 이벤트 예시를 참고하여 내용과 관련된 이벤트를 생성하시오. 예시에 있는 이벤트가 아닌 뉴스와 관련된 이벤트 문구를 반드시 새로 생성하시오.
금융 이벤트 예시: "신제품 출시", "기업 인수합병", "리콜", "배임횡령", "오너 리스크", "자연재해", "제품 불량" 등

아래 json schema를 참고하여 json 응답을 생성해주세요. 그외 응답은 생성하지 마시오.
{json_schema}

```뉴스:
{news}
```"""