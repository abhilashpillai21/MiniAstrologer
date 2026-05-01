from supabase import create_client
import os

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def login_user(email, password):
    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })
    return response


def signup_user(email, password):
    response = supabase.auth.sign_up({
        "email": email,
        "password": password
    })
    return response

def insert_data(email, prompt, full_response):
    supabase.table("usage_logs").insert(
    {
        "user_email": email,
        "question": prompt,
        "answer": full_response
    }).execute()
    