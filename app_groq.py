import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# 🔐 Chargement de la clé API
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    st.set_page_config(page_title="🔐 Clé API manquante", page_icon="⚠️")
    st.title("🔐 Clé API GROQ manquante")
    st.error("Ajoute ta clé dans un fichier `.env` : `GROQ_API_KEY=...`")
    st.stop()

client = Groq(api_key=API_KEY)

# 🎨 Configuration de la page
st.set_page_config(page_title="💬 Chatbot IA Ultime", page_icon="💎", layout="wide")

# 💫 Nouveau thème CSS
st.markdown("""
<style>
body {
    font-family: 'Segoe UI', sans-serif;
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom right, #1e1e2f, #2a2a3d);
    color: #f0f0f0;
}
.title {
    text-align: center;
    font-size: 2.8rem;
    margin: 30px 0 10px;
    font-weight: bold;
    color: #ffffff;
    text-shadow: 0 0 10px #6b5b95;
}
.user-msg, .bot-msg {
    padding: 16px 20px;
    margin: 12px 0;
    border-radius: 20px;
    max-width: 80%;
    font-size: 1.05rem;
    line-height: 1.5;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.05);
}
.user-msg {
    background: #4b4b6b;
    color: #fff;
    margin-left: auto;
    text-align: right;
}
.bot-msg {
    background: #3a3a55;
    color: #e0e0e0;
    margin-right: auto;
    text-align: left;
}
.stChatInput input {
    background: rgba(40, 40, 60, 0.8);
    color: #fff;
    border: 1px solid #6b5b95;
    border-radius: 30px;
    padding: 14px 24px;
    font-size: 1.1rem;
    width: 100%;
}
.stChatInput input:focus {
    border-color: #feb47b;
    box-shadow: 0 0 0 3px rgba(254,180,123,0.4);
    outline: none;
}
.footer {
    text-align: center;
    color: rgba(255,255,255,0.4);
    font-size: 0.85rem;
    margin-top: 40px;
    padding: 10px;
}
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">💎 Chatbot IA Ultime</div>', unsafe_allow_html=True)

# 🧠 Initialisation historique
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Tu es un assistant brillant, créatif, et toujours élégant dans tes réponses."}
    ]

# 💬 Affichage des messages
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">👤 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

# ✨ Saisie utilisateur
if prompt := st.chat_input("Parle-moi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user-msg">👤 {prompt}</div>', unsafe_allow_html=True)

    with st.spinner("✨ Réflexion en cours..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=st.session_state.messages
            )
            bot_reply = response.choices[0].message.content.strip()
        except Exception as e:
            st.error(f"⚠️ Erreur : {e}")
            bot_reply = "Désolé, je ne peux pas répondre pour le moment."

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.markdown(f'<div class="bot-msg">🤖 {bot_reply}</div>', unsafe_allow_html=True)
