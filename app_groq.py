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

# 💫 CSS ULTRA-BEAU : dégradés, animations, ombres portées, coins arrondis, typo fluide
st.markdown("""
<style>
/* Fond cosmique animé */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 10% 20%, #0f0c29, #302b63, #24243e);
    color: white;
    font-family: 'Segoe UI', system-ui, sans-serif;
}

/* Titre animé */
.title {
    text-align: center;
    font-size: 3rem;
    margin: 25px 0;
    background: linear-gradient(90deg, #ff7e5f, #feb47b, #86a8e7, #91eae4);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-weight: 900;
    animation: glow 2s infinite alternate;
    text-shadow: 0 0 10px rgba(255,255,255,0.1);
}

@keyframes glow {
    from { text-shadow: 0 0 10px #fff, 0 0 20px #ff7e5f; }
    to   { text-shadow: 0 0 20px #fff, 0 0 30px #86a8e7, 0 0 40px #91eae4; }
}

/* Messages utilisateur */
.user-msg {
    background: linear-gradient(135deg, #ff7e5f, #feb47b);
    color: white;
    padding: 16px 20px;
    border-radius: 24px 24px 6px 24px;
    margin: 14px 0;
    text-align: right;
    box-shadow: 0 6px 20px rgba(255, 126, 95, 0.3);
    max-width: 85%;
    margin-left: auto;
    font-size: 1.05rem;
    line-height: 1.5;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Messages bot */
.bot-msg {
    background: linear-gradient(135deg, #86a8e7, #91eae4);
    color: #0f0f14;
    padding: 16px 20px;
    border-radius: 24px 24px 24px 6px;
    margin: 14px 0;
    text-align: left;
    box-shadow: 0 6px 20px rgba(134, 168, 231, 0.3);
    max-width: 85%;
    margin-right: auto;
    font-size: 1.05rem;
    line-height: 1.5;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Input stylé comme un vrai chat moderne */
.stChatInput input {
    background: rgba(20, 20, 35, 0.7);
    color: white;
    border: 1px solid rgba(134, 168, 231, 0.5);
    border-radius: 30px;
    padding: 14px 24px;
    font-size: 1.1rem;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.stChatInput input:focus {
    border-color: #91eae4;
    box-shadow: 0 0 0 3px rgba(145, 234, 228, 0.4);
    outline: none;
}

/* Footer discret */
.footer {
    text-align: center;
    color: rgba(255,255,255,0.5);
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

# ✨ Saisie utilisateur — fluide, sans bug
if prompt := st.chat_input("Parle-moi..."):
    # Ajout + affichage immédiat utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user-msg">👤 {prompt}</div>', unsafe_allow_html=True)

    # Appel API avec modèle actif
    with st.spinner("✨ Réflexion en cours..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # ✅ Officiellement actif (remplaçant de llama3-8b-8192)
                messages=st.session_state.messages
            )
            bot_reply = response.choices[0].message.content.strip()
        except Exception as e:
            st.error(f"⚠️ Erreur : {e}")
            bot_reply = "Désolé, je ne peux pas répondre pour le moment."

    # Ajout + affichage réponse
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.markdown(f'<div class="bot-msg">🤖 {bot_reply}</div>', unsafe_allow_html=True)

# 🌟 Footer
st.markdown('<div class="footer">✨ Conçu pour être le plus beau chatbot du monde • Clé API sécurisée</div>', unsafe_allow_html=True)