import pandas as pd
import streamlit as st

def get_usage_logs(supabase):
    response = supabase.table("usage_logs").select("user_email, question, created_at").execute()
    return response.data

def render_dashboard(supabase):
    st.title("Admin Dashboard")

    data = get_usage_logs(supabase)

    if not data:
        st.write("No data yet")
        return None
    
    df = pd.DataFrame(data)
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["date"] = df["created_at"].dt.date

    col1, col2 = st.columns(2)

    col1.metric("Total Questions", len(df))
    col2.metric("Total Users", df["user_email"].nunique())

    st.subheader("Questions per Day")
    daily = df.groupby("date").size()
    st.line_chart(daily)

    st.subheader("Questions per User")
    user_counts = df.groupby("user_email").size().sort_values(ascending=False)
    st.bar_chart(user_counts)

    st.subheader("Recent Questions")
    st.dataframe(
        df[["created_at", "user_email", "question"]]
        .sort_values("created_at", ascending=False)
        .head(20)
    )

