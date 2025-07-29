import streamlit as st
from auth import login_user, logout, get_logged_in_user
from agents.nutrition_agent import run_nutrition_agent
from agents.suggestion_agent import suggestion_agent
from pdf_ingestion import ingest_pdf
from diary_db import (
    init_db,
    log_chat,
    log_meal,
    log_meal_diary,
    fetch_meal_diary,
    clear_meal_diary,
    insert_entry,
    get_chat_history
)
from tools.rag_tool import rag_tool

import os
import base64
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()
init_db()

st.set_page_config("Nutrition Assistant", layout="wide")

# ---- Sidebar ----
with st.sidebar:
    st.title("🍽️ NutriMate AI")
    if "user" not in st.session_state:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", key="login_button"):
            if login_user(username, password):
                st.session_state.user = username
                st.success(f"Welcome, {username}")
            else:
                st.error("Invalid credentials.")
    else:
        st.write(f"👤 Logged in as: `{st.session_state.user}`")
        if st.button("Logout", key="logout_button"):
            logout()
            st.success("Logged out.")
            st.rerun()

if "user" not in st.session_state:
    st.stop()

# ---- Main Tabs ----
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 Chat", "📄 PDF Upload", "📜 History", "📊 Diary", "🌟 Suggestion"
])

# ---- Chat Interface ----
with tab1:
    st.header("🤖 AI Nutrition Chat Assistant")
    question = st.text_input("Ask anything about your diet, health, meals…", key="chat_question")
    if st.button("Ask", key="ask_button"):
        if question:
            response = run_nutrition_agent(question, st.session_state.user)
            st.markdown(f"**Response:**\n\n{response}")
        else:
            st.warning("Please ask a question.")

# ---- PDF Upload ----
with tab2:
    st.header("📄 Upload Diet/Health PDFs")
    pdf = st.file_uploader("Upload your PDF", type=["pdf"], key="pdf_uploader")
    if pdf and st.button("Ingest PDF", key="ingest_pdf_button"):
        ingest_pdf(pdf, user_id=st.session_state.user)
        st.success("PDF content indexed for chat.")

# ---- Chat History ----
with tab3:
    st.header("📜 Your Prompt Logs")
    logs = fetch_meal_diary(st.session_state.user)
    for prompt, resp, timestamp in logs[::-1]:
        st.markdown(f"🕒 *{timestamp}*")
        st.markdown(f"**You:** {prompt}")
        st.markdown(f"**Assistant:** {resp}")
        st.markdown("---")

# ---- Meal Diary ----
with tab4:
    st.header("📊 Meal Diary")
    with st.form("log_form"):
        food = st.text_input("Food Item", key="food_input")
        calories = st.number_input("Calories", 0.0, key="calories_input")
        protein = st.number_input("Protein (g)", 0.0, key="protein_input")
        fat = st.number_input("Fat (g)", 0.0, key="fat_input")
        carbs = st.number_input("Carbs (g)", 0.0, key="carbs_input")
        submitted = st.form_submit_button("Log Meal")
        if submitted:
            insert_entry(st.session_state.user, food, calories, protein, fat, carbs)
            st.success("Logged!")

    st.subheader("🍱 Your Meals Today")
    rows = get_chat_history(st.session_state.user)
    if rows:
        st.table(rows)

        df = pd.DataFrame(rows, columns=["Food", "Calories", "Protein", "Fat", "Carbs", "Time"])
        total_macros = df[["Protein", "Fat", "Carbs"]].sum()
        fig = px.pie(
            values=total_macros,
            names=["Protein", "Fat", "Carbs"],
            title="Macronutrient Distribution"
        )
        st.plotly_chart(fig)

        if st.button("🧹 Clear Diary", key="clear_diary_button"):
            clear_meal_diary(st.session_state.user)
            st.success("Diary cleared.")
            st.rerun()
    else:
        st.info("No meals logged yet.")

# ---- Suggestion Agent ----
with tab5:
    st.header("🌟 Get Meal Suggestions")
    food_item = st.text_input("Enter any food/meal to improve", key="suggestion_input")
    if st.button("Suggest", key="suggest_button"):
        suggestion = suggestion_agent(food_item)
        st.markdown(suggestion)
