# 💌 GratiGlow – Aesthetic Gratitude Journal with Streamlit
import streamlit as st
import sqlite3
import pandas as pd
import datetime
import random
import plotly.express as px

# 🌸 Setup page config
st.set_page_config(page_title="GratiGlow Journal", page_icon="💌", layout="centered")
st.title("💖 GratiGlow – Your Soft Gratitude Space")

# 🌼 Connect to SQLite
conn = sqlite3.connect('gratitude_journal.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        entry TEXT,
        mood TEXT,
        mood_score INTEGER
    )
''')
conn.commit()

# 🧠 Mood to Score Mapping
mood_map = {
    "😊 Happy": 5,
    "😌 Calm": 4,
    "😐 Okay": 3,
    "😞 Low": 2,
    "😰 Anxious": 1
}

# 💌 Quote Pool
quotes = [
    "Gratitude turns what we have into enough 🌟",
    "Today is a gift, that’s why it’s called the present 🎁",
    "Small steps every day 💖",
    "You are doing your best, and that’s beautiful 🌷",
    "Peace begins with a grateful heart 💕"
]

# ✨ Tabs
tab1, tab2 = st.tabs(["📔 Add Entry", "📊 Mood Tracker"])

# 📔 Add Entry Tab
with tab1:
    st.subheader("Write Today’s Gratitude")
    entry = st.text_area("What are you grateful for today? ✨", placeholder="Ex: I'm grateful for a peaceful walk in the morning 🌅")
    mood = st.selectbox("How do you feel right now?", list(mood_map.keys()))
    if st.button("Save Entry 💾"):
        if entry.strip():
            today = datetime.date.today().strftime("%Y-%m-%d")
            mood_score = mood_map[mood]
            cursor.execute('INSERT INTO journal (date, entry, mood, mood_score) VALUES (?, ?, ?, ?)',
                           (today, entry, mood, mood_score))
            conn.commit()
            st.success("Entry saved! 💖")
        else:
            st.warning("Please write something you're grateful for.")

    st.markdown("---")
    st.markdown(f"#### 💬 Quote of the Day")
    st.info(random.choice(quotes))

# 📊 Mood Tracker Tab
with tab2:
    st.subheader("Your Mood Journey 🌈")
    df = pd.read_sql_query('SELECT * FROM journal', conn)
    if len(df) == 0:
        st.info("No entries yet. Add your first gratitude above!")
    else:
        st.dataframe(df[['date', 'entry', 'mood']].sort_values(by='date', ascending=False))
        mood_chart = px.line(df, x='date', y='mood_score', markers=True, title="🌈 Mood Over Time")
        st.plotly_chart(mood_chart, use_container_width=True)

        mood_counts = df['mood'].value_counts().reset_index()
        mood_counts.columns = ['Mood', 'Count']
        pie_chart = px.pie(mood_counts, names='Mood', values='Count', title="🧁 Mood Distribution")
        st.plotly_chart(pie_chart, use_container_width=True)

# 🧁 Footer
st.markdown("""
---
Made with 💌 by Ananya Singh  
*Gratitude is the gentle art of counting blessings.*
""")
