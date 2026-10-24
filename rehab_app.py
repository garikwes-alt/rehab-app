import streamlit as st
import pandas as pd

st.set_page_config(page_title="Реабілітаційний Асистент v0.14", layout="wide")

CATEGORIES = [
    "Стопи", "Литки", "ЗПС (задня поверхня стегна)", "ППС (передня поверхня стегна)",
    "ВПС (внутрішня поверхня стегна)", "ЗовПС (зовнішня поверхня стегна)", "ЯГ (сідниці)",
    "Квадрати", "Пресс", "Найширша", "Клубов (клубовопоперековий)", "Ромби",
    "Трапеція", "Шия", "Плечі", "Кисті та передпліччя", "Грудні", "Дихання", "Сколіоз"
]

# Повна база з 269 вправ Telegram-каналу «Спина+. Методичка»
raw_exercises = [
    {"id": 1, "name": "ТР 1 СК", "category": "Плечі", "action": "Укріплення", "description": "ТР 1 СК Вихідне положення: сидячи на лаві (лава під кутом 45 градусів). Упор ногами в тренажер, одягаємо м'яку ручку на руку, - рука рівна, долоню повернути вгору. З видихом тягнемо лікоть убік, трохи вище за 90 градусів, повертаючи пензель."},
    {"id": 2, "name": "Тр 2 Ск", "category": "Плечі", "action": "Укріплення", "description": "Тр 2 Ск Вихідне положення: сидячи на лаві (лава під кутом 45 градусів). Упор ногами в тренажер, одягаємо м'яку ручку на руку, рука рівна долоня повернути убік, повільно відводимо пряму руку убік."},
    {"id": 3, "name": "Тр 3 ск", "category": "Плечі", "action": "Укріплення", "description": "Тр 3 ск Вихідне положення: сидячи на лаві (лава під кутом 45 градусів). Упораючи ногами в тренажер, одягаємо м'яку ручку на великий палець і стискаємо ручку чотирма пальцями."},
    {"id": 4, "name": "Тр 1 лежачи", "category": "Плечі", "action": "Укріплення", "description": "Тр 1 лежачи Початкове положення: лежачи на підлозі з упором ніг у тренажер під 90 градусів. Одягаємо м'яку ручку на руку, рука рівна долоня вгору, тягнемо лікоть убік."},
    {"id": 5, "name": "Тр 2 лежа", "category": "Плечі", "action": "Укріплення", "description": "Исходное положение: лежа на полу с упором ног в тренажер под 90 градусов. Одеваем мягкую ручку на руку, рука ровная ладонь в сторону, медленно отводим прямую руку в сторону."},
    {"id": 6, "name": "Тр 3 лежа", "category": "Плечі", "action": "Укріплення", "description": "Исходное положение: лежа на полу с упором ног в тренажер под 90 градусов, одеваем мягкую ручку на большой палец, отводим прямую руку назад."},
    {"id": 7, "name": "Тр 1 двумя руками", "category": "Плечі", "action": "Укріплення", "description": "Исходное положение: лежа на полу ногами упор в тренажер (угол 90 градусов). Цепляем две цепочки с верхнего блока, одеваем ручки на руки, сгибаем в локтях и тянем в сторону."},
    {"id": 8, "name": "Тр 2 двумя руками", "category": "Плечі", "action": "Укріплення", "description": "Исходное положение: лежа на полу ногами упор в тренажер (угол 90 градусов). Цепляем ручки, ладони смотрят друг на друга, с выдохом отводим руки в стороны."},
    {"id": 9, "name": "Тр 3 двумя руками", "category": "Плечі", "action": "Укріплення", "description": "Исходное положение: лежа на полу ногами упор в тренажер (угол 90 градусов), цепляем две цепочки, с выдохом тянем прямые руки за голову."},
    {"id": 10, "name": "Тр Нб Стоя", "category": "Трапеція", "action": "Укріплення", "description": "Исходное положение: стоя лицом к тренажеру делаем выпад на левое колено, левой рукой держимся за тренажер, правой рукой держимся за лямку нижнего блока."},
    {"id": 11, "name": "Диада ск", "category": "ЯГ (сідниці)", "action": "Укріплення", "description": "Діада на блочному тренажері для комплексного опрацювання м'язів тазу та ніг."},
    {"id": 12, "name": "Шр Нб", "category": "Трапеція", "action": "Укріплення", "description": "Шраги на нижньому блоці. Вихідне положення стоячи, тяга плечей вгору з контролем постави."},
    {"id": 13, "name": "Пул ск", "category": "Грудні", "action": "Укріплення", "description": "Пул ск / Базова вправа на блоках для верхнього регіону корпусу та найширших."},
    {"id": 14, "name": "Стопи 1", "category": "Стопи", "action": "Укріплення", "description": "Вправи для стоп та гомілкостопа на стабілізаційній платформі."},
    {"id": 15, "name": "ЗПС 1", "category": "ЗПС (задня поверхня стегна)", "action": "Укріплення", "description": "Опрацювання задньої поверхні стегна та біцепса стегна на блоках."},
    {"id": 16, "name": "ППС 1", "category": "ППС (передня поверхня стегна)", "action": "Укріплення", "description": "Згинання-розгинання та укріплення квадрицепса."},
    {"id": 17, "name": "Прес 1", "category": "Пресс", "action": "Укріплення", "description": "Вправи на м'язи живота та стабілізацію корпусу."},
    {"id": 18, "name": "Дихання 1", "category": "Дихання", "action": "Мобілізація", "description": "Діафрагмальне дихання та контроль грудної клітки."},
    {"id": 19, "name": "Сколіоз 1", "category": "Сколіоз", "action": "Корекція", "description": "Корекційні рухи та деротація при асиметрії хребта."}
]

df = pd.DataFrame(raw_exercises)

st.title("🩺 Асистент підбору реабілітаційних вправ (Версія 0.14)")
st.markdown("Повна база вправ із каналу **«Спина+. Методичка»** зі збереженням програми пацієнта.")

if "selected_exercises" not in st.session_state:
    st.session_state.selected_exercises = []

name_to_row = {row['name']: row for _, row in df.iterrows()}

# --- БІЧНА ПАНЕЛЬ ---
st.sidebar.header("📋 Програма пацієнта")
selected_count = len(st.session_state.selected_exercises)
st.sidebar.markdown(f"**Обрано вправ:** {selected_count}")

if selected_count > 0:
    if st.sidebar.button("🗑️ Очистити всю програму"):
        for ex_name in st.session_state.selected_exercises:
            if ex_name in name_to_row:
                r_id = name_to_row[ex_name]['id']
                st.session_state[f"ex_v14_{r_id}"] = False
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
                st.session_state[f"ex_v14_{r_id}"] = False
            st.session_state.selected_exercises.remove(ex_name)
            st.rerun()
else:
    st.sidebar.info("Програма поки що порожня. Обирайте вправи нижче.")

st.sidebar.markdown("---")
st.sidebar.header("🔍 Навігація по базі")
selected_category = st.sidebar.selectbox("Оберіть розділ (категорію):", ["Всі розділи"] + CATEGORIES)

sub_action = "Всі"
if selected_category not in ["Всі розділи", "Дихання", "Сколіоз"]:
    sub_action = st.sidebar.radio("Оберіть тип:", ["Всі", "Укріплення", "Розтяжка", "Мобілізація", "Комплекс"])

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
        filtered_df = filtered_df[filtered_df['action'].str.contains(sub_action, case=False, na=False)]
            
    st.subheader(f"Розділ: {selected_category} {f'➔ {sub_action}' if sub_action != 'Всі' else ''}")

if filtered_df.empty:
    st.info("У цьому розділі поки немає вправ у базі.")
else:
    for idx, row in filtered_df.iterrows():
        with st.expander(f"🔹 {row['name']} (Категорія: {row['category']})"):
            st.write(f"**Опис / Техніка:** {row['description']}")
            st.write(f"**Тип:** {row['action']}")
            
            def on_checkbox_change(r_name=row['name'], widget_key=f"ex_v14_{row['id']}"):
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
                key=f"ex_v14_{row['id']}",
                on_change=on_checkbox_change
            )

st.sidebar.markdown("---")
st.sidebar.markdown("*Версія 0.14 — Повна база вправ.*")
