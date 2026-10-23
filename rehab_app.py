
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Реабілітаційний Асистент v0.11", layout="wide")

# Список 19 категорій згідно з вимогами
CATEGORIES = [
    "Стопи",
    "Литки",
    "ЗПС (задня поверхня стегна)",
    "ППС (передня поверхня стегна)",
    "ВПС (внутрішня поверхня стегна)",
    "ЗовПС (зовнішня поверхня стегна)",
    "ЯГ (сідниці)",
    "Квадрати",
    "Пресс",
    "Найширша",
    "Клубов (клубовопоперековий)",
    "Ромби",
    "Трапеція",
    "Шия",
    "Плечі",
    "Кисті та передпліччя",
    "Грудні",
    "Дихання",
    "Сколіоз"
]

# Оновлені тестові дані з прив'язкою до нових категорій та дій (Укріплення / Розтяжка / Корекція)
data = [
    {
        "id": 1,
        "name": "23 нб",
        "category": "ЯГ (сідниці)",
        "action": "Укріплення",
        "description": "Укріплення сідниць (ЯГ)"
    },
    {
        "id": 2,
        "name": "Др на ч",
        "category": "Клубов (клубовопоперековий)",
        "action": "Укріплення та Розтяжка",
        "description": "Укріплення клубовопоперекового, розтяжка клубовопоперекового, розтяжка прессу, укріплення передньої поверхні стегна (ППС)"
    },
    {
        "id": 3,
        "name": "20 нб",
        "category": "ППС (передня поверхня стегна)",
        "action": "Розтяжка",
        "description": "Розтяжка ППС"
    },
    {
        "id": 4,
        "name": "21 бок",
        "category": "ВПС (внутрішня поверхня стегна)",
        "action": "Укріплення",
        "description": "Укріплення внутрішньої поверхні стегна"
    },
    {
        "id": 5,
        "name": "28",
        "category": "ЗПС (задня поверхня стегна)",
        "action": "Укріплення та Розтяжка",
        "description": "Укріплення задньої поверхні стегна (ЗПС), розтяжка ЗПС"
    },
    {
        "id": 6,
        "name": "7 вб",
        "category": "Найширша",
        "action": "Укріплення та Мобілізація",
        "id_secondary": "Грудні",
        "description": "Укріплення найширшого м'яза, тракція грудного відділу"
    },
    {
        "id": 7,
        "name": "Пила от",
        "category": "Найширша",
        "action": "Комплекс",
        "description": "Укріплення найширшого, розтяжка ЗПС, розтяжка ЯГ, укріплення ЯГ, розтяжка квадратних м'язів (Квадрати)"
    },
    {
        "id": 8,
        "name": "Шифт гвх",
        "category": "Сколіоз",
        "action": "Корекція грудного відділу",
        "description": "Корекція грудного відділу при сколіозі"
    },
    {
        "id": 9,
        "name": "23-2 сколіоз",
        "category": "Сколіоз",
        "action": "Корекція поперекового відділу",
        "description": "Корекція поперекового відділу при сколіозі"
    },
    {
        "id": 10,
        "name": "22 стоя",
        "category": "ЗовПС (зовнішня поверхня стегна)",
        "action": "Укріплення",
        "description": "Укріплення зовнішньої поверхні стегна, укріплення ЯГ"
    }
]

df = pd.DataFrame(data)

st.title("🩺 Асистент підбору реабілітаційних вправ (Версія 0.11)")
st.markdown("Оновлена структура з 19 категоріями та розділенням на «Укріплення» / «Розтяжка» для основних м'язових груп.")

# Бічна панель навігації та фільтрації
st.sidebar.header("Навігація по базі")
selected_category = st.sidebar.selectbox("Оберіть розділ (категорію):", ["Всі розділи"] + CATEGORIES)

# Фільтрація підкатегорій (Укріплення / Розтяжка) для категорій 1-17
sub_action = "Всі"
if selected_category not in ["Всі розділи", "Дихання", "Сколіоз"]:
    sub_action = st.sidebar.radio("Оберіть підрозділ:", ["Всі", "Укріплення", "Розтяжка", "Інше / Комплекс"])
elif selected_category == "Сколіоз":
    sub_action = st.sidebar.selectbox("Напрямок корекції:", ["Всі", "Корекція грудного відділу", "Корекція поперекового відділу"])

# Пошук за ключовим словом
keyword = st.sidebar.text_input("Або пошук за ключовим словом:")

# Логіка фільтрації
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
            st.write(гф := f"**Тип:** {row['action']}")
            st.checkbox(f"Додати у програму пацієнта ({row['name']})", key=f"ex_v11_{row['id']}")

st.sidebar.markdown("---")
st.sidebar.markdown("*Версія 0.11 — Режим відшліфування структури.*")
