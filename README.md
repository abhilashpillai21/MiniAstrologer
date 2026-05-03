# Mini Astrology App

Mini Astrology App is a learning project that combines Streamlit, OpenAI, ChromaDB, and Supabase to let users upload a birth chart text file and ask questions about it.

The app uses a simple RAG pipeline: it chunks the uploaded chart text, creates embeddings, retrieves the most relevant chunks, and sends that context to an OpenAI model to generate a grounded answer.

## Project Goal

This project is built to learn how AI products work end to end:

- User authentication with Supabase
- RAG using embeddings and vector search
- OpenAI model calls
- Chat-style user experience
- Conversation history
- Basic admin analytics

The long-term goal is to turn this into a helpful assistant for people who want to understand birth chart information through a conversational interface.

## Features

The app currently includes the following core features needed for a simple authenticated RAG-based chat experience:

- Email/password login and signup using Supabase Auth
- Upload a `.txt` birth chart file
- Ask questions about the uploaded chart
- Retrieve relevant chart sections using ChromaDB
- Generate answers with OpenAI
- Save question and answer history per user
- Show recent user questions in the sidebar
- Admin dashboard with basic usage analytics

## Tech Stack

This project uses following lightweight Python-based stack that is beginner-friendly while still covering real AI app concepts:

- Python
- Streamlit
- OpenAI API
- ChromaDB
- Supabase
- Pandas

## How It Works

At a high level, the app follows the following basic RAG workflow from file upload to grounded answer generation:

1. A user logs in or creates an account.
2. The user uploads a birth chart text file.
3. The app splits the file into overlapping text chunks.
4. Each chunk is embedded using an OpenAI embedding model.
5. ChromaDB stores and searches the embedded chunks.
6. When the user asks a question, the app retrieves the most relevant chunks.
7. The retrieved context, question, and recent conversation history are sent to OpenAI.
8. The answer is shown in the chat UI and saved to Supabase.

## Project Structure

The codebase is intentionally small and organized around the main parts of the app: UI, authentication, retrieval, analytics, and helpers.

```text
MiniAstrologer/
+-- frontend.py        # Main Streamlit app and user interface
+-- auth.py            # Supabase login, signup, and usage history functions
+-- vectordb.py        # ChromaDB, embeddings, retrieval, and OpenAI response logic
+-- dashboard.py       # Admin dashboard and usage analytics
+-- utils.py           # Shared helper functions
+-- requirements.txt   # Python dependencies
+-- runtime.txt        # Python runtime version
+-- JupyterNotes/      # Learning notes and experiments
```

## Environment Variables

This project uses environment variables for secrets and model configuration. In GitHub Codespaces, these can be stored in Codespaces secrets.

Required variables:

```env
OPENAI_API_KEY=
OPENAI_API_MODEL=
OPENAI_EMBEDDED_MODEL=
SUPABASE_URL=
SUPABASE_KEY=
```

Recommended future variable:

```env
ADMIN_EMAILS=
```

Do not commit real secret values to GitHub.

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run frontend.py
```

Then open the local Streamlit URL shown in the terminal.

## Current Limitations

Since this is a learning project, there are still several areas that need improvement before it becomes a more polished product.

- Only `.txt` uploads are supported.
- Admin email is currently hard-coded in `frontend.py`.
- There are no automated tests yet.
- The RAG pipeline is simple and can be improved with better chunking, evaluation, and citation handling.
- Error handling is still basic.
- The UI is functional but can be made more polished.

## Improvement Roadmap

The next improvements are focused on making the app easier to use, easier to maintain, and more useful as an AI product.

- Move admin email configuration to an environment variable
- Add PDF upload support
- Add feedback buttons for answers, such as helpful or not helpful
- Add tests for chunking and retrieval helpers
- Improve source citations in answers
- Add cost and usage tracking
- Add a clearer onboarding flow for first-time users
- Add product analytics such as uploads, repeat usage, and unanswered questions

## Learning Notes

This is a beginner-friendly AI product project. It is useful for learning both technical and product management concepts:

- How RAG works
- How authentication fits into an AI app
- How user history can improve context
- How to think about hallucination and answer quality
- How to track whether users are getting value from the product

## Status

This project is actively being built as a learning project.
