# app_groq.py
import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not GROQ_API_KEY:
    st.set_page_config(page_title="🔐 Clé API GROQ manquante", page_icon="⚠️")
    st.title("🔐 Clé API GROQ manquante")
    st.error("Ajoute ta clé dans un fichier `.env` : `GROQ_API_KEY=...`")
    st.stop()

if not OPENAI_API_KEY:
    st.warning("⚠️ La clé OpenAI est manquante pour la génération d'images.")
    # tu peux continuer, juste la génération d'image sera désactivée

client = Groq(api_key=GROQ_API_KEY)

# 🎨 Page config
st.set_page_config(page_title="✨ Chatbot IA Ultime", page_icon="💎", layout="wide")

# 💫 CSS sombre et élégant
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 10% 20%, #0f0c29, #1c1c2e, #121212);
    color: white;
    font-family: 'Segoe UI', system-ui, sans-serif;
}
.title {
    text-align: center;
    font-size: 3rem;
    margin: 25px 0;
    background: linear-gradient(90deg, #6e56cf, #9b59b6, #34495e, #2c3e50);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-weight: 900;
    animation: glow 2s infinite alternate;
    text-shadow: 0 0 10px rgba(255,255,255,0.1);
}
@keyframes glow {
    from { text-shadow: 0 0 10px #fff, 0 0 20px #6e56cf; }
    to   { text-shadow: 0 0 20px #fff, 0 0 30px #34495e, 0 0 40px #2c3e50; }
}
.user-msg {
    background: linear-gradient(135deg, #6e56cf, #9b59b6);
    color: white;
    padding: 16px 20px;
    border-radius: 24px 24px 6px 24px;
    margin: 14px 0;
    text-align: right;
    box-shadow: 0 6px 20px rgba(110, 86, 207, 0.3);
    max-width: 85%;
    margin-left: auto;
    font-size: 1.05rem;
    line-height: 1.5;
}
.bot-msg {
    background: linear-gradient(135deg, #34495e, #2c3e50);
    color: #f0f0f0;
    padding: 16px 20px;
    border-radius: 24px 24px 24px 6px;
    margin: 14px 0;
    text-align: left;
    box-shadow: 0 6px 20px rgba(52, 73, 94, 0.3);
    max-width: 85%;
    margin-right: auto;
    font-size: 1.05rem;
    line-height: 1.5;
}
.stChatInput input {
    background: rgba(30, 30, 50, 0.7);
    color: white;
    border: 1px solid rgba(52, 73, 94, 0.5);
    border-radius: 30px;
    padding: 14px 24px;
    font-size: 1.1rem;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}
.stChatInput input:focus {
    border-color: #9b59b6;
    box-shadow: 0 0 0 3px rgba(155, 89, 182, 0.4);
    outline: none;
}
.footer {
    text-align: center;
    color: rgba(255,255,255,0.5);
    font-size: 0.85rem;
    margin-top: 30px;
    padding: 10px;
}
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">💎 Chatbot IA Ultime</div>', unsafe_allow_html=True)

# 🧠 Historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Tu es un assistant brillant, créatif et élégant."}
    ]

# 💬 Affichage des messages existants
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">👤 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

# ✨ Saisie texte
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
            st.error(f"⚠️ Erreur Chat : {e}")
            bot_reply = "Désolé, je ne peux pas répondre pour le moment."

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.markdown(f'<div class="bot-msg">🤖 {bot_reply}</div>', unsafe_allow_html=True)

# 🎨 Génération d'image
st.markdown("<hr><h3 style='color:white;'>🎨 Générateur d'images</h3>", unsafe_allow_html=True)
if img_prompt := st.text_input("Écris l'image que tu veux générer :"):
    if OPENAI_API_KEY:
        import openai
        openai.api_key = OPENAI_API_KEY
        with st.spinner("🖌️ Création de l'image..."):
            try:
                result = openai.images.generate(
                    model="gpt-image-1",
                    prompt=img_prompt,
                    size="1024x1024"
                )
                image_url = result.data[0].url
                st.image(image_url, caption=img_prompt)
            except Exception as e:
                st.error(f"⚠️ Erreur Image : {e}")
    else:
        st.warning("Clé OpenAI manquante : impossible de générer une image.")

# 🌟 Footer
st.markdown('<div class="footer">✨ Conçu avec style et élégance • Clés API sécurisées</div>', unsafe_allow_html=True)
