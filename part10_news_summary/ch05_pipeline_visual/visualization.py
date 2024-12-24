import os

from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from pymongo import MongoClient

load_dotenv()
MONGO_INITDB_HOST = os.getenv('MONGO_INITDB_HOST')
MONGO_INITDB_PORT = int(os.getenv('MONGO_INITDB_PORT'))
MONGO_INITDB_ROOT_USERNAME  = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD  = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

mongo_client = MongoClient(
    host=MONGO_INITDB_HOST, 
    port=MONGO_INITDB_PORT,
    username=MONGO_INITDB_ROOT_USERNAME,
    password=MONGO_INITDB_ROOT_PASSWORD,
    authSource='admin'
)

db = mongo_client['project1']
collection = db['NewsAnalysis1']

data = list(collection.find())

# 데이터를 저장할 리스트
rows = []

# 데이터 처리
for item in data:
    for analysis in item.get('analysis', []):  # 'analysis' 리스트 순회
        organization = analysis.get('company')  # 'company' 값 가져오기
        sentiments = analysis.get('sentiment', [])  # 'sentiment' 리스트 가져오기
        seendate = analysis.get('seendate')  # 'seendate' 값 가져오기

        # sentiment 개별 항목을 행으로 추가
        for sentiment in sentiments:
            rows.append({
                "organization": organization,
                "positive": sentiment.get('positive', 0),
                "negative": sentiment.get('negative', 0),
                "neutral": sentiment.get('neutral', 0),
                "seendate": seendate
            })

# 리스트를 데이터프레임으로 변환
df = pd.DataFrame(rows)

# seendate를 datetime 형식으로 변환 후 정렬
df['seendate'] = pd.to_datetime(df['seendate'])
df = df.sort_values(by='seendate')

# 같은 날짜와 시간에 대해 평균을 계산
df_grouped = df.groupby(['organization', df['seendate'].dt.floor('T')])[['positive', 'negative', 'neutral']].mean().reset_index()

# 기업명 리스트 자동 생성
organization_list = df['organization'].unique().tolist()

# 결과 출력
# print(df)
print(df_grouped.to_string())

# title
st.title("기업별 날짜에 따른 감성지수 변화")

# 기업선택
organization = st.selectbox("기업을 선택하세요", organization_list)

# 선택한 기업의 데이터 필터링
selected_df = df_grouped.loc[df_grouped['organization'] == organization].set_index('seendate')

# 감성 지수 차트
st.line_chart(selected_df[['positive', 'negative', 'neutral']])

mongo_client.close()