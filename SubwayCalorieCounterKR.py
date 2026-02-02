import streamlit as st
import pandas as pd


# 1. 시트별로 데이터 따로 불러오기
# 샌드위치 메뉴가 있는 시트
main_df = pd.read_excel('KORSubwayNutrition.xlsx', sheet_name='Sandwiches', engine='openpyxl')

# 토핑과 소스가 있는 시트
topping_df = pd.read_excel('KORSubwayNutrition.xlsx', sheet_name='Toppings', engine='openpyxl')

# 빈칸(NaN)이 있으면 모두 0으로 채워줘! (에러 방지 마법의 주문)
main_df = main_df.fillna(0)
topping_df = topping_df.fillna(0)

st.title("🥖 서브웨이 칼로리 카운터 🥖")

# --- 메인 메뉴 선택 (Sheet1 데이터 사용) ---
st.subheader("1. 메인 메뉴를 골라주세요")
selected_main = st.selectbox("메뉴 선택", main_df['Item'].unique())
main_cal = main_df[main_df['Item'] == selected_main]['Pure_Calorie'].values[0]
main_pro = main_df[main_df['Item'] == selected_main]['Protein'].values[0]
main_sod = main_df[main_df['Item'] == selected_main]['Sodium'].values[0]


# --- [1] 빵 선택 ---
bread_options = topping_df[topping_df['Category'] == 'Bread']['Item'].unique()
selected_bread = st.selectbox("1. 빵을 골라주세요", bread_options)
bread_data = topping_df[topping_df['Item'].isin([selected_bread])]

# --- [2] 치즈 선택 ---
cheese_options = topping_df[topping_df['Category'] == 'Cheese']['Item'].unique()
selected_cheese = st.selectbox("2. 치즈를 골라주세요", cheese_options)
cheese_data = topping_df[topping_df['Item'].isin([selected_cheese])]

# --- [3] 소스 선택 ---
sauce_options = topping_df[topping_df['Category'] == 'Sauce']['Item'].unique()
selected_sauce = st.multiselect("3. 소스를 골라주세요 (최대 2개)", sauce_options, max_selections=2)
sauce_data = topping_df[topping_df['Item'].isin(selected_sauce)]

# --- [최종 계산] 모든 선택된 데이터를 하나로 합쳐서 계산해요 ---
# 모든 데이터프레임을 하나로 합치는 기법! (리스트에 넣어서 합치기)
all_selected_toppings = pd.concat([bread_data, cheese_data, sauce_data])

total_topping_cal = all_selected_toppings['Calorie(kcal)'].sum()
total_topping_pro = all_selected_toppings['Protein(g)'].sum()
total_topping_sod = all_selected_toppings['Sodium(mg)'].sum()

# 최종 결과 합산
total_cal = main_cal + total_topping_cal
total_pro = main_pro + total_topping_pro
total_sod = main_sod + total_topping_sod



st.divider()


st.header(f"🔥 총 칼로리: {total_cal} kcal / 493 kcal")
st.header(f"🔥 총 단백질: {total_pro} g / 34 g")
st.header(f"🔥 총 나트륨: {total_sod} mg / 650 mg")
