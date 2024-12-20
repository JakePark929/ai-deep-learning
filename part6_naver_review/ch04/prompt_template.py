prompt_template = """다음은 영화에 대한 리뷰들 입니다. 리뷰 내용을 종합적으로 요약해주세요.
1) 아래 json 양식 처럼 응답해 주세요.
{{
    "summary": "이 영화는..."
}}

```reviews
{reviews}
"""

prompt_template_langchain="""다음은 영화에 대한 리뷰들 입니다. 리뷰 내용을 종합적으로 요약해주세요.

{format_instructions}

```reviews
{reviews}
"""