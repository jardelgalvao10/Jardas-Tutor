import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# 1. CONFIGURAÇÕES INICIAIS
load_dotenv()

# Pegamos a chave primeiro e guardamos na variável
chave_openai = st.secrets["OPENAI_API_KEY"]

# Agora usamos a variável para criar o cliente da OpenAI
client_openai = OpenAI(api_key=chave_openai)

st.set_page_config(
    page_title="Jardas Seu tutor de Inglês",
    page_icon="🤖", 
    layout="centered")

st.title("Olá sou o Jardas...")

# --- MELHORIA 1: MEMÓRIA DE CONVERSA ---
# Inicializa o histórico se ele não existir
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {"role": "system", "content": "Você é o Jardas, um tutor de inglês nativo, amigável e paciente. "
                                     "Seu objetivo é ajudar o usuário a praticar inglês. "
                                     "Sempre responda em inglês, mas se o usuário estiver com muita dificuldade, "
                                     "explique brevemente em português entre parênteses. "
                                     "Corrija os erros gramaticais do usuário de forma gentil."}
    ]

# --- MELHORIA 2: FUNÇÃO DE VOZ OTIMIZADA ---
def falar(texto):
    try:
        from elevenlabs.client import ElevenLabs
        api_key = os.getenv("ELEVENLABS_API_KEY").strip()
        client_el = ElevenLabs(api_key=api_key)
        
        # Usando a voz 'Adam' (ID: pNInz6obpgDQGcFmaJgB) que é excelente para tutores
        audio_generator = client_el.text_to_speech.convert(
            text=texto,
            voice_id="pNInz6obpgDQGcFmaJgB", 
            model_id="eleven_multilingual_v2"
        )
        
        audio_bytes = b"".join(audio_generator)
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
        
    except Exception as e:
        st.error(f"Erro na voz: {e}")

# --- INTERFACE DE CHAT ---
# Exibe o histórico de mensagens
for mensagem in st.session_state.mensagens:
    if mensagem["role"] != "system":
        with st.chat_message(mensagem["role"]):
            st.markdown(mensagem["content"])

# Entrada do usuário
if prompt := st.chat_input("Say something to Alex..."):
    # Adiciona fala do usuário ao histórico
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta do Alex (OpenAI)
    with st.chat_message("assistant"):
        resposta_placeholder = st.empty()
        
        # Chamada com memória (enviamos todo o histórico)
        response = client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.mensagens
        )
        
        full_response = response.choices[0].message.content
        resposta_placeholder.markdown(full_response)
        
        # Adiciona resposta ao histórico e fala
        st.session_state.mensagens.append({"role": "assistant", "content": full_response})
        falar(full_response)

# Botão lateral para limpar a memória
if st.sidebar.button("Limpar Histórico de Conversa"):
    st.session_state.mensagens = [st.session_state.mensagens[0]]
    st.rerun()