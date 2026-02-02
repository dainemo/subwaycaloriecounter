import streamlit as st
import pandas as pd

# 1. 시트별로 데이터 따로 불러오기
# 샌드위치 메뉴가 있는 시트
main_df = pd.read_excel('KORSubwayNutrition.csv', sheet_name='Sandwiches')

# 토핑과 소스가 있는 시트
topping_df = pd.read_excel('KORSubwayNutrition.csv', sheet_name='Toppings')

st.title("서브웨이 칼로리 카운터")

# --- 메인 메뉴 선택 (Sheet1 데이터 사용) ---
st.subheader("1. 메인 메뉴를 골라주세요")
selected_main = st.selectbox("메뉴 선택", main_df['Item'].unique())
main_cal = main_df[main_df['Item'] == selected_main]['Pure_Calorie'].values[0]
main_protein = main_df[main_df['Item'] == selected_main]['Protein'].values[0]
main_sodium = main_df[main_df['Item'] == selected_main]['Sodium'].values[0]


# --- 토핑 선택 (Sheet2 데이터 사용) ---
st.subheader("2. 추가 토핑/소스를 골라주세요")
selected_toppings = st.multiselect("토핑 선택", topping_df['Item'].unique())
# 선택한 토핑들의 칼로리만 쏙쏙 더하기
topping_cal = topping_df[topping_df['Item'].isin(selected_toppings)]['Calorie(kcal)'].sum()
topping_protein = topping_df[topping_df['Item'] == selected_toppings]['Protein(g)'].sum()
topping_sodium = topping_df[topping_df['Item'] == selected_toppings]['Sodium(mg)'].sum()


# --- 최종 결과 ---
total_cal = main_cal + topping_cal
total_pro = main_protein + topping_protein
total_sod = main_sodium + topping_sodium

st.divider()
st.header(" 총 칼로리: {total_cal} kcal / 493 kcal
              총 단백질: {total_pro} g / 34 g
              총 나트륨: {total_sod} mg / 650 mg")
