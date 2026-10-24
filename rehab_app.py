import streamlit as st
import pandas as pd

st.set_page_config(page_title="Реабілітаційний Асистент v0.14", layout="wide")

CATEGORIES = [
    "Стопи", "Литки", "ЗПС (задня поверхня стегна)", "ППС (передня поверхня стегна)",
    "ВПС (внутрішня поверхня стегна)", "ЗовПС (зовнішня поверхня стегна)", "ЯГ (сідниці)",
    "Квадрати", "Пресс", "Найширша", "Клубов (клубовопоперековий)", "Ромби",
    "Трапеція", "Шия", "Плечі", "Кисті та передпліччя", "Грудні", "Дихання", "Сколіоз"
]

# Повна база вправ з експорту Telegram-каналу «Спина+. Методичка»
raw_exercises = [
    {"id": 1, "name": "ТР 1 СК", "category": "Плечі", "action": "Укріплення", "description": "ТР 1 СК Вихідне положення: сидячи на лаві (лава під кутом 45 градусів). Упор ногами в тренажер, одягаємо м'яку ручку на руку, - рука рівна, долоню повернути вгору. З видихом тягнемо лікоть убік, трохи вище за 90 градусів, повертаючи пензель, потім повільно відпускаємо руку у вихідне положення."},
    {"id": 2, "name": "Тр 2 Ск", "category": "Плечі", "action": "Укріплення", "description": "Тр 2 Ск Вихідне положення: сидячи на лаві (лава під кутом 45 градусів). Упор ногами в тренажер, одягаємо м'яку ручку на руку, рука рівна долоня повернути убік, повільно відводимо пряму руку убік, потім повертаємо у вихідне положення. М'язи: середній пучок дельти, підостна."},
    {"id": 3, "name": "Тр 3 ск", "category": "Плечі", "action": "Укріплення", "description": "Тр 3 ск Вихідне положення: сидячи на лаві (лава під кутом 45 градусів). Упораючи ногами в тренажер, одягаємо м'яку ручку на великий палець і стискаємо м'яку ручку чотирма пальцями, потім відводимо пряму руку назад великим пальцем вниз і повертаємо назад у вихідне положення."},
    {"id": 4, "name": "Тр 1 лежачи", "category": "Плечі", "action": "Укріплення", "description": "Тр 1 лежачи Початкове положення: лежачи на підлозі з упором ніг у тренажер під 90 градусів. Одягаємо м'яку ручку на руку, рука рівна долоня повернути вгору, з видихом тягнемо лікоть убік, трохи вище за 90 градусів, повертаючи кисть. Потім повільно відпускаємо руку у вихідне положення."},
    {"id": 5, "name": "Тр 2 лежа", "category": "Плечі", "action": "Укріплення", "description": "Исходное положение: лежа на полу с упором ног в тренажер под 90 градусов. Одеваем мягкую ручку на руку, рука ровная ладонь повернуть в сторону, медленно отводим прямую руку в сторону, затем отпускаем в исходное положение Мышцы: средний пучок дельты подостная"},
    {"id": 6, "name": "Тр 3 лежа", "category": "Плечі", "action": "Укріплення", "description": "Исходное положение: лежа на полу с упором ног в тренажер под 90 градусов, одеваем мягкую ручку на большой палец и сжимаем мягкую ручку четырьмя пальцами, затем отводим прямую руку назад большим пальцем вниз и возвращаем обратно в исходное положение Мышцы: передний пучок дельты, подостная"},
    {"id": 7, "name": "Тр 1 двумя руками", "category": "Плечі", "action": "Укріплення", "description": "Исходное положение: лежа на полу ногами упор в тренажер( угол ног 90 градусов). Цепляем две цепочки с верхнего блока, цепляем мягкие ручки на цепочки и одеваем каждую из ручек по отдельности на руки, затем сгибаем руки в локтях и тянем в сторону чуть выше угла 90, и медленно отпускаем"},
    {"id": 8, "name": "Тр 2 двумя руками", "category": "Плечі", "action": "Укріплення", "description": "Исходное положение: лежа на полу ногами упор в тренажер( угол ног 90 градусов). Цепляем две цепочки с верхнего блока, цепляем мягкие ручки и одеваем каждую из ручек по отдельности на руки, ладони смотрят друг на друга и с выдохом позволим руки в стороны на уровне плечей"},
    {"id": 9, "name": "Тр 3 двумя руками", "category": "Плечі", "action": "Укріплення", "description": "Исходное положение: лежа на полу ногами упор в тренажер( угол ног 90 градусов) цепляем две цепочки с верхнего блока, цепляем мягкие ручки и одеваем каждую из ручек по отдельности на руки, и с выдохом тянем прямые руки за голову, затем возвращаем в исходное положение"},
    {"id": 10, "name": "Пул ск", "category": "Грудні", "action": "Укріплення", "description": "Пул ск / Базова вправа на блоках для опрацювання верхнього регіону корпусу та найширших/грудних м'язів."}
]

# Автоматичне розширення та підключення повного масиву з каналу
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
st.sidebar.markdown("*Версія 0.14 — Повна база з Telegram-каналу.*")
