# app_groq.py
import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    st.set_page_config(page_title="🔐 Clé API manquante", page_icon="⚠️")
    st.title("🔐 Clé API GROQ manquante")
    st.error("Ajoute ta clé dans un fichier `.env` : `GROQ_API_KEY=...`")
    st.stop()

client = Groq(api_key=API_KEY)

# 🎨 Page config + Titre stylé
st.set_page_config(page_title="✨ Chatbot IA Ultime", page_icon="💎", layout="wide")

# 💫 CSS sombre et élégant
st.markdown("""
<style>
/* Fond sombre cosmique */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 10% 20%, #0a0a0a, #1b1b2f, #2c2c44);
    color: #e0e0e0;
    font-family: 'Segoe UI', system-ui, sans-serif;
}

/* Titre animé */
.title {
    text-align: center;
    font-size: 3rem;
    margin: 25px 0;
    background: linear-gradient(90deg, #6b5b95, #feb47b, #355c7d);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-weight: 900;
    animation: glow 2s infinite alternate;
    text-shadow: 0 0 8px rgba(255,255,255,0.1);
}

@keyframes glow {
    from { text-shadow: 0 0 10px #fff, 0 0 15px #6b5b95; }
    to   { text-shadow: 0 0 15px #fff, 0 0 25px #355c7d, 0 0 30px #feb47b; }
}

/* Messages utilisateur */
.user-msg {
    background: linear-gradient(135deg, #3e3e50, #5c5c7a);
    color: #fff;
    padding: 16px 20px;
    border-radius: 24px 24px 6px 24px;
    margin: 14px 0;
    text-align: right;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    max-width: 85%;
    margin-left: auto;
    font-size: 1.05rem;
    line-height: 1.5;
    border: 1px solid rgba(255,255,255,0.05);
}

/* Messages bot */
.bot-msg {
    background: linear-gradient(135deg, #2c3e50, #34495e);
    color: #f0f0f0;
    padding: 16px 20px;
    border-radius: 24px 24px 24px 6px;
    margin: 14px 0;
    text-align: left;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    max-width: 85%;
    margin-right: auto;
    font-size: 1.05rem;
    line-height: 1.5;
    border: 1px solid rgba(255,255,255,0.05);
}

/* Input stylé */
.stChatInput input {
    background: rgba(30, 30, 50, 0.7);
    color: #fff;
    border: 1px solid rgba(134, 168, 231, 0.3);
    border-radius: 30px;
    padding: 14px 24px;
    font-size: 1.1rem;
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
}

.stChatInput input:focus {
    border-color: #6b5b95;
    box-shadow: 0 0 0 3px rgba(107,91,149,0.4);
    outline: none;
}

/* Footer discret */
.footer {
    text-align: center;
    color: rgba(255,255,255,0.4);
    font-size: 0.85rem;
    margin-top: 30px;
    padding: 10px;
}

/* Cacher le footer Streamlit par défaut */
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

# 🌟 Footer
st.markdown('<div class="footer">✨ Chatbot IA Ultime • Clé API sécurisée</div>', unsafe_allow_html=True)
