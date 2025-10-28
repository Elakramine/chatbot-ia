import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# 🔐 Chargement des clés API
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not GROQ_API_KEY:
    st.set_page_config(page_title="🔐 Clé API GROQ manquante", page_icon="⚠️")
    st.title("🔐 Clé API GROQ manquante")
    st.error("Ajoute ta clé dans un fichier `.env` : `GROQ_API_KEY=...`")
    st.stop()

client_groq = Groq(api_key=GROQ_API_KEY)

if OPENAI_API_KEY:
    import openai
    openai.api_key = OPENAI_API_KEY

# 🎨 Configuration de la page
st.set_page_config(page_title="💬 Chatbot IA Ultime", page_icon="💎", layout="wide")

# 💫 Thème CSS élégant
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom right, #1a1a2e, #16213e);
    color: #f0f0f0;
    font-family: 'Segoe UI', sans-serif;
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
    background: #2e2e4d;
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

# 🧠 Choix du mode IA
mode = st.sidebar.radio("🧠 Choisis ton IA :", ["💬 Llama (Groq)", "💬 OpenAI (GPT)", "🎨 Générateur d'image"])

# 🧠 Historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Tu es un assistant brillant, créatif et élégant."}
    ]

# 💬 Mode Chat
if mode in ["💬 Llama (Groq)", "💬 OpenAI (GPT)"]:
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
                if mode == "💬 Llama (Groq)":
                    response = client_groq.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=st.session_state.messages
                    )
                    bot_reply = response.choices[0].message.content.strip()
                else:
                    if not OPENAI_API_KEY:
                        st.error("⚠️ Clé OpenAI manquante.")
                        bot_reply = "Désolé, je ne peux pas répondre sans clé OpenAI."
                    else:
                        response = openai.ChatCompletion.create(
                            model="gpt-4",
                            messages=st.session_state.messages
                        )
                        bot_reply = response.choices[0].message["content"].strip()
            except Exception as e:
                st.error(f"⚠️ Erreur Chat : {e}")
                bot_reply = "Désolé, je ne peux pas répondre pour le moment."

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.markdown(f'<div class="bot-msg">🤖 {bot_reply}</div>', unsafe_allow_html=True)

# 🎨 Mode Image
elif mode == "🎨 Générateur d'image":
    st.markdown("### 🎨 Décris l'image que tu veux générer :")
    img_prompt = st.text_input("🖌️ Prompt image")
    if img_prompt and OPENAI_API_KEY:
        with st.spinner("🖼️ Génération de l'image..."):
            try:
                result = openai.Image.create(
                    prompt=img_prompt,
                    n=1,
                    size="1024x1024"
                )
                image_url = result["data"][0]["url"]
                st.image(image_url, caption=img_prompt)
            except Exception as e:
                st.error(f"⚠️ Erreur Image : {e}")
    elif img_prompt:
        st.warning("⚠️ Clé OpenAI manquante : impossible de générer une image.")

# 🌟 Footer
st.markdown('<div class="footer">✨ Conçu avec style et élégance • IA sélectionnable • Clés sécurisées</div>', unsafe_allow_html=True)

