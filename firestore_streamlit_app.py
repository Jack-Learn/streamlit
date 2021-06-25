# 架設網站
# streamlit  firestore_streamlit_app.py

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

# 定義網頁
st.set_page_config(
    page_title= '跟著機器人來復健',
    page_icon="random",
    layout="centered",
    initial_sidebar_state="collapsed",
)



# 首頁
def home():

    st.title('首頁')

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


def info2friestore(user_id, password, birth_year, name):

    docs = {'birth year': birth_year,
            'name': name,
            'password': password}

    if birth_year == '' or name == '':
        st.error('註冊失敗')

    else:
        try:
            doc_ref = db.collection('users').document(user_id)    
            doc_ref.set(docs)    
            st.info('註冊成功')
        except:
            st.error('註冊失敗')


# 註冊頁面
def register():

    user_id = st.text_input('帳號')
    password = st.text_input('密碼')
    birth_year = st.text_input('出生年')
    name = st.text_input('姓名')
    button_1_click = st.button('註冊')

    if button_1_click:
        info2friestore(user_id, password, birth_year, name)

if __name__ == '__main__':
    
    # 左邊導航欄    
    website = st.sidebar.radio(
        '導航欄',
        ('首頁', '使用者註冊'))
    
    if website == '首頁':
        home()

    elif website == '使用者註冊':
        register()