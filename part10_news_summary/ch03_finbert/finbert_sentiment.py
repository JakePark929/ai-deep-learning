from transformers import pipeline

def sentiment_analysis(text):
    pipe = pipeline("sentiment-analysis", model="ProsusAI/finbert")
    return pipe(text)

if __name__ == '__main__':
    # print(sentiment_analysis("Stock railed yesterday."))
    # print(sentiment_analysis("Tesla stock dropped 25%, but Meta railed 30%"))
    # print(sentiment_analysis("Meta railed 30%, but Tesla stock dropped 25%"))
    print(sentiment_analysis("Meta reported strong finalcial results for Q1 2024"))
    print(sentiment_analysis("Tesla released its financial results for Q1 2024, missing Wall Street expectations."))