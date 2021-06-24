# 引用必要套件
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import streamlit as st

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt 

# 引用私密金鑰
# path/to/serviceAccount.json 請用自己存放的路徑
cred = credentials.Certificate('./key/scoring-physical-fitness-firebase-adminsdk-kdyfc-816162a01b.json')

try:
    # 初始化firebase，注意不能重複初始化
    firebase_admin.initialize_app(cred)

except:
    pass

# 初始化firestore
db = firestore.client()


# 查詢所有使用者
docs = db.collection('users').stream()
users_list = [doc.id for doc in docs]
# print(users_list)

user_id = st.selectbox('選擇使用者', users_list)

# 查詢使用者個人資料
doc_ref = db.collection('users').document(user_id)
docs = doc_ref.get().to_dict()

st.write('使用者名稱：', docs['name'])


# 查詢歷史分數
time_list = []
score_list = []
collection  = db.collection('users').document(user_id).collection('historical score')
for doc in collection.stream():
    left_column, right_column = st.beta_columns(2)
    _time = doc.id
    left_column.write(_time)
    doc_ref = db.collection('users', user_id, 'historical score').document(_time)
    score = doc_ref.get().to_dict()['score']
    right_column.write(score)

    time_list.append(datetime.strptime(_time, '%Y-%m-%d, %H:%M:%S'))
    score_list.append(score)


time_list = time_list[-10:]
score_list = score_list[-10:]
# 根據時間間隔畫圖
fig, ax = plt.subplots() 
score_df = pd.DataFrame(index=time_list, columns=['score'], data=score_list) 
ax.plot(score_df.index, score_df.values)
plt.xticks([time for time in time_list], score_df.index, rotation=45) 
st.pyplot(fig)