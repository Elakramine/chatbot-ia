# app_groq.py
import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import openai

# 🔐 Chargement des clés API
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not GROQ_API_KEY or not OPENAI_API_KEY:
    st.set_page_config(page_title="🔐 Clés API manquantes", page_icon="⚠️")
    st.title("🔐 Clés API manquantes")
    st.error("Ajoute GROQ_API_KEY et OPENAI_API_KEY dans ton fichier `.env`")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)
openai.api_key = OPENAI_API_KEY

# 🎨 Page config + titre
st.set_page_config(page_title="✨ Chatbot & Image IA", page_icon="💎", layout="wide")
st.markdown("""
<style>
body {background: #1a1a2e; color:white; font-family: 'Segoe UI', sans-serif;}
.title {text-align:center; font-size:3rem; margin:20px 0; color:#91eae4; font-weight:900;}
.user-msg {background:#ff7e5f; padding:12px 18px; border-radius:20px; margin:10px 0; text-align:right; max-width:80%; margin-left:auto;}
.bot-msg {background:#86a8e7; padding:12px 18px; border-radius:20px; margin:10px 0; text-align:left; max-width:80%; margin-right:auto; color:#0f0f14;}
.stButton button {background:#91eae4; color:#0f0f14; border-radius:20px; padding:8px 18px;}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="title">💎 Chatbot & Image IA</div>', unsafe_allow_html=True)

# 🧠 Historique
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Tu es un assistant brillant, créatif et élégant."}
    ]

# 💬 Chat
chat_col, image_col = st.columns(2)

with chat_col:
    st.subheader("💬 Chat IA")
    for msg in st.session_state.messages[1:]:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-msg">👤 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-msg">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

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
                st.error(f"⚠️ Erreur Chat: {e}")
                bot_reply = "Désolé, je ne peux pas répondre pour le moment."
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.markdown(f'<div class="bot-msg">🤖 {bot_reply}</div>', unsafe_allow_html=True)

# 🖼 Génération d'image
with image_col:
    st.subheader("🖼 Génération d'image")
    image_prompt = st.text_input("Décris l'image que tu veux générer")
    if st.button("Générer l'image"):
        if image_prompt:
            with st.spinner("🖌 Création de l'image en cours..."):
                try:
                    result = openai.Image.create(
                        prompt=image_prompt,
                        n=1,
                        size="512x512"
                    )
                    image_url = result['data'][0]['url']
                    st.image(image_url, use_column_width=True)
                except Exception as e:
                    st.error(f"⚠️ Erreur Image: {e}")
        else:
            st.warning("💡 Écris un prompt pour générer l'image.")

