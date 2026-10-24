import streamlit as st
import pandas as pd

st.set_page_config(page_title="Реабілітаційний Асистент v0.13", layout="wide")

CATEGORIES = [
    "Стопи", "Литки", "ЗПС (задня поверхня стегна)", "ППС (передня поверхня стегна)",
    "ВПС (внутрішня поверхня стегна)", "ЗовПС (зовнішня поверхня стегна)", "ЯГ (сідниці)",
    "Квадрати", "Пресс", "Найширша", "Клубов (клубовопоперековий)", "Ромби",
    "Трапеція", "Шия", "Плечі", "Кисті та передпліччя", "Грудні", "Дихання", "Сколіоз"
]

data = [
    {"id": 1, "name": "23 нб", "category": "ЯГ (сідниці)", "action": "Укріплення", "description": "Укріплення сідниць (ЯГ)"},
    {"id": 2, "name": "Др на ч", "category": "Клубов (клубовопоперековий)", "action": "Укріплення та Розтяжка", "description": "Укріплення клубовопоперекового, розтяжка клуб., розтяжка прессу, укріплення ППС"},
    {"id": 3, "name": "20 нб", "category": "ППС (передня поверхня стегна)", "action": "Розтяжка", "description": "Розтяжка ППС"},
    {"id": 4, "name": "21 бок", "category": "ВПС (внутрішня поверхня стегна)", "action": "Укріплення", "description": "Укріплення внутрішньої поверхні стегна"},
    {"id": 5, "name": "28", "category": "ЗПС (задня поверхня стегна)", "action": "Укріплення та Розтяжка", "description": "Укріплення ЗПС, розтяжка ЗПС"},
    {"id": 6, "name": "7 вб", "category": "Найширша", "action": "Укріплення та Мобілізація", "description": "Укріплення найширшого м'яза, тракція грудного відділу"},
    {"id": 7, "name": "Пила от", "category": "Найширша", "action": "Комплекс", "description": "Укріплення найширшого, розтяжка ЗПС, розтяжка ЯГ, укріплення ЯГ, розтяжка квадратних м'язів"},
    {"id": 8, "name": "Шифт гвх", "category": "Сколіоз", "action": "Корекція грудного відділу", "description": "Корекція грудного відділу при сколіозі"},
    {"id": 9, "name": "23-2 сколіоз", "category": "Сколіоз", "action": "Корекція поперекового відділу", "description": "Корекція поперекового відділу при сколіозі"},
    {"id": 10, "name": "22 стоя", "category": "ЗовПС (зовнішня поверхня стегна)", "action": "Укріплення", "description": "Укріплення зовнішньої поверхні стегна, укріплення ЯГ"}
]

df = pd.DataFrame(data)

st.title("🩺 Асистент підбору реабілітаційних вправ (Версія 0.13)")
st.markdown("Зручний підбір вправ із синхронізованим керуванням програмою пацієнта.")

if "selected_exercises" not in st.session_state:
    st.session_state.selected_exercises = []

name_to_row = {row['name']: row for _, row in df.iterrows()}

# --- БІЧНА ПАНЕЛЬ ---
st.sidebar.header("📋 Програма пацієнта")
selected_count = len(st.session_state.selected_exercises)
st.sidebar.markdown(f"**Обрано вправ:** {selected_count} / ~20")

if selected_count > 0:
    if st.sidebar.button("🗑️ Очистити всю програму"):
        for ex_name in st.session_state.selected_exercises:
            if ex_name in name_to_row:
                r_id = name_to_row[ex_name]['id']
                st.session_state[f"ex_v13_{r_id}"] = False
        st.session_state.selected_exercises = []
        st.rerun()
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Склад програми:**")
    for ex_name in st.session_state.selected_exercises:
        col_s1, col_s2 = st.sidebar.columns([4, 1])
        col_s1.text(f"• {ex_name}")
        if col_s2.button("❌", key=f"del_{ex_name}"):
            if ex_name in name_to_row:
                r_id = name_to_row[ex_name]['id']
                st.session_state[f"ex_v13_{r_id}"] = False
            st.session_state.selected_exercises.remove(ex_name)
            st.rerun()
else:
    st.sidebar.info("Програма поки що порожня. Обирайте вправи нижче.")

st.sidebar.markdown("---")
st.sidebar.header("🔍 Навігація по базі")
selected_category = st.sidebar.selectbox("Оберіть розділ (категорію):", ["Всі розділи"] + CATEGORIES)

sub_action = "Всі"
if selected_category not in ["Всі розділи", "Дихання", "Сколіоз"]:
    sub_action = st.sidebar.radio("Оберіть підрозділ:", ["Всі", "Укріплення", "Розтяжка", "Інше / Комплекс"])
elif selected_category == "Сколіоз":
    sub_action = st.sidebar.selectbox("Напрямок корекції:", ["Всі", "Корекція грудного відділу", "Корекція поперекового відділу"])

keyword = st.sidebar.text_input("Або пошук за ключовим словом:")

filtered_df = df.copy()

if keyword:
    filtered_df = filtered_df[
        filtered_df['name'].str.contains(keyword, case=False, na=False) |
        filtered_df['category'].str.contains(keyword, case=False, na=False) |
        filtered_df['description'].str.contains(keyword, case=False, na=False)
    ]
    st.subheader(f"Результати пошуку за запитом: '{keyword}' ({len(filtered_df)})")
else:
    if selected_category != "Всі розділи":
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
        
    if sub_action != "Всі" and selected_category not in ["Всі розділи"]:
        if sub_action in ["Укріплення", "Розтяжка"]:
            filtered_df = filtered_df[filtered_df['action'].str.contains(sub_action, case=False, na=False) | filtered_df['description'].str.contains(sub_action, case=False, na=False)]
        else:
            filtered_df = filtered_df[filtered_df['action'].str.contains(sub_action, case=False, na=False)]
            
    st.subheader(f"Розділ: {selected_category} {f'➔ {sub_action}' if sub_action != 'Всі' else ''}")

if filtered_df.empty:
    st.info("У цьому розділі поки немає вправ у тестовій базі.")
else:
    for idx, row in filtered_df.iterrows():
        with st.expander(f"🔹 {row['name']} (Категорія: {row['category']})"):
            st.write(f"**Опис / Дія:** {row['description']}")
            st.write(f"**Тип:** {row['action']}")
            
            def on_checkbox_change(r_name=row['name'], widget_key=f"ex_v13_{row['id']}"):
                if st.session_state[widget_key]:
                    if r_name not in st.session_state.selected_exercises:
                        st.session_state.selected_exercises.append(r_name)
                else:
                    if r_name in st.session_state.selected_exercises:
                        st.session_state.selected_exercises.remove(r_name)

            is_checked = row['name'] in st.session_state.selected_exercises
            st.checkbox(
                f"Додати у програму пацієнта ({row['name']})", 
                value=is_checked, 
                key=f"ex_v13_{row['id']}",
                on_change=on_checkbox_change
            )

st.sidebar.markdown("---")
st.sidebar.markdown("*Версія 0.13 — Синхронізоване керування програмою.*")
