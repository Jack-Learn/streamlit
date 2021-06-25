import time
import streamlit as st
import numpy as np
import pandas as pd

st.title('我的第一個應用程式')

st.write("嘗試創建**表格**：")  # **XX** -> XX 會粗體

# 建立dataframe
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

# 在網頁繪製表格
df 


# 建立dataframe
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

# 在網頁繪製折線圖
st.line_chart(chart_data)


# 勾選框
if st.checkbox('顯示地圖圖表'):

    # 建立dataframe
    map_data = pd.DataFrame(
        np.random.randn(100, 2) / [50, 50] + [22.7, 120.3],
        columns=['lat', 'lon'])
    # 在網頁繪製地圖
    st.map(map_data)

# 下拉式選單
option = st.sidebar.selectbox(  # sidebar 顯示於邊條
    '你喜歡哪種動物？',
    ['狗', '貓', '鸚鵡', '天竺鼠'])

# 不打 st.write()也能正常顯示
st.sidebar.write('你的答案：', option)

left_column, right_column = st.beta_columns(2)
left_column.write("這是左邊欄位。")
right_column.write("這是右邊欄位。")

input  = st.text_input('輸入框', '輸入')