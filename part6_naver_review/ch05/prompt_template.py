prompt_template = """다음은 영화에 대한 리뷰들입니다.
1. 영화에 대해 긍정적이면 1, 부정적이면 0으로 평가해주세요.
2. 리뷰에서 긍정적인 키워드, 부정적인 키워드를 추출해주세요.
3. 리뷰 내용들을 종합적으로 요약해주세요.

```reviews
{reviews}
```"""