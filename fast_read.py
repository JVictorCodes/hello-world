import streamlit as st
import time
import re

# ==================================================
# CONFIGURAÇÃO DA PÁGINA
# ==================================================
st.set_page_config(
    page_title="FastRead",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================================
# CUSTOM CSS
# ==================================================
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    html, body {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .st-emotion-cache-zt5igj {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 100%;
    }
    
    body {
        background: linear-gradient(135deg, #0f1419 0%, #0a0e1a 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #0a0e1a 100%);
    }
    
    .header-title {
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    .header-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 16px;
        margin-bottom: 30px;
    }
    
    .fullscreen-word {
        text-align: center;
        font-size: 100px;
        font-weight: 700;
        color: white;
        line-height: 1.2;
        min-height: 180px;
        display: flex;
        align-items: center;
        justify-content: center;
        white-space: nowrap;
        overflow: visible;
        text-overflow: clip;
        word-break: keep-all;
        padding: 20px 0;
        width: 100%;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #3b82f6, #2563eb);
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 700;
        padding: 12px 24px;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(37, 99, 235, 0.4);
    }
    
    h1, h2, h3 {
        color: white;
    }
    
    .stTextArea textarea {
        background-color: #1a1f2e !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid #2d3748 !important;
    }
    
    .stSlider {
        color: white;
    }
    
    .stToggle {
        color: white;
    }
    
    .stProgress > div > div > div > div {
        background-color: #3b82f6;
    }
    
    label {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================================================
# STATE MANAGEMENT
# ==================================================
if "leitura_ativa" not in st.session_state:
    st.session_state.leitura_ativa = False

# ==================================================
# FUNÇÕES
# ==================================================
def limpar_texto(texto):
    """Remove espaços extras e limpa o texto"""
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()

def destacar_centro(palavra):
    """Destaca a letra central da palavra em negrito com HTML"""
    if len(palavra) <= 2:
        return f"<span style='font-weight: 700; color: #3b82f6;'>{palavra}</span>"
    
    meio = len(palavra) // 2
    return (
        palavra[:meio] + 
        f"<span style='font-weight: 700; color: #3b82f6;'>{palavra[meio]}</span>" + 
        palavra[meio+1:]
    )

# ==================================================
# RENDERIZAÇÃO TELA CHEIA (MODO LEITURA)
# ==================================================
if st.session_state.leitura_ativa:
    
    texto = st.session_state.texto_leitura
    velocidade = st.session_state.velocidade
    palavras_por_vez = st.session_state.palavras_por_vez
    modo_foco = st.session_state.modo_foco
    
    # Processar texto
    texto = limpar_texto(texto)
    palavras = texto.split()
    tempo_por_grupo = (60 / velocidade) * palavras_por_vez
    
    total_grupos = len(range(0, len(palavras), palavras_por_vez))
    
    # Espaçamento para deslocar para baixo
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    
    # Criar colunas para centralizar conteúdo (com mais espaço horizontal)
    col_left, col_center, col_right = st.columns([0.2, 1.6, 0.2])
    
    with col_center:
        # Criar placeholders únicos para atualização
        word_placeholder = st.empty()
        st.write("")
        progress_placeholder = st.empty()
        st.write("")
        control_placeholder = st.empty()
    
    # Loop principal de leitura
    for i in range(0, len(palavras), palavras_por_vez):
        
        # Extrair grupo de palavras
        grupo = palavras[i:i + palavras_por_vez]
        
        # Aplicar formatação (foco RSVP se ativado)
        if modo_foco:
            grupo_formatado = [destacar_centro(p) for p in grupo]
            texto_exibido = " ".join(grupo_formatado)
        else:
            texto_exibido = " ".join(grupo)
        
        # Calcular progresso
        atual = (i // palavras_por_vez) + 1
        percentual = min(atual / total_grupos, 1.0)
        
        # Limpar e atualizar palavra
        word_placeholder.empty()
        word_placeholder.markdown(f"<div class='fullscreen-word'>{texto_exibido}</div>", 
                       unsafe_allow_html=True)
        
        # Limpar e atualizar progresso
        progress_placeholder.empty()
        progress_placeholder.progress(percentual, text=f"📖 {atual} / {total_grupos}")
        
        # Limpar e atualizar controles
        control_placeholder.empty()
        with control_placeholder.container():
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("⏸ Pausar", use_container_width=True, key=f"pause_{i}"):
                    st.session_state.leitura_ativa = False
                    st.rerun()
        
        # Aguardar antes da próxima palavra
        time.sleep(tempo_por_grupo)
    
    # Tela de conclusão
    word_placeholder.empty()
    word_placeholder.markdown("<div class='fullscreen-word' style='color: #3b82f6;'>✓ Concluído!</div>", 
                   unsafe_allow_html=True)
    progress_placeholder.empty()
    
    st.write("")
    control_placeholder.empty()
    with control_placeholder.container():
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("← Voltar ao Menu", use_container_width=True, key="voltar"):
                st.session_state.leitura_ativa = False
                st.rerun()

# ==================================================
# INTERFACE PRINCIPAL
# ==================================================
else:
    
    # HEADER
    st.markdown("<h1 class='header-title'>⚡ FASTREAD</h1>", unsafe_allow_html=True)
    st.markdown("<div class='header-subtitle'>Treine velocidade, foco e retenção visual.</div>", 
               unsafe_allow_html=True)
    
    st.divider()
    
    # SEÇÃO DE TEXTO
    st.subheader("🗎 TEXTO")
    
    # Inicializar texto no session state se não existir
    if "texto_input" not in st.session_state:
        st.session_state.texto_input = ""
    
    texto = st.text_area(
        "Digite ou cole um texto",
        value=st.session_state.texto_input,
        placeholder="Cole ou escreva um texto para iniciar sua leitura dinâmica...",
        height=200,
        label_visibility="collapsed",
        on_change=lambda: st.session_state.update({"texto_input": st.session_state.texto_area})
    )
    
    # Atualizar session state conforme usuário digita
    if "texto_area" not in st.session_state or st.session_state.get("texto_area") != texto:
        st.session_state.texto_input = texto
    
    st.write("")
    
    # SEÇÃO DE CONFIGURAÇÕES
    st.subheader("⚙ CONFIGURAÇÕES")
    
    col1, col2 = st.columns(2)
    
    with col1:
        palavras_por_vez = st.slider(
            "Palavras por vez",
            min_value=1,
            max_value=8,
            value=2,
            help="Quantas palavras exibir por vez (1=máximo foco, 8=leitura natural)"
        )
    
    with col2:
        velocidade = st.slider(
            "Velocidade (PPM)",
            min_value=100,
            max_value=1200,
            value=500,
            step=50,
            help="Palavras Por Minuto (500=normal, 1200=muito rápido)"
        )
    
    modo_foco = st.toggle(
        "🎯 Modo Foco RSVP",
        value=True,
        help="Destaca a letra central de cada palavra para melhor leitura"
    )
    
    st.write("")
    
    # BOTÃO INICIAR
    iniciar = st.button(
        "▶ Iniciar Leitura",
        use_container_width=True,
        type="primary"
    )
    
    st.write("")
    st.divider()
    
    # SEÇÃO DE INFORMAÇÕES (FOOTER)
    st.write("")
    st.subheader("Por que usar FastRead?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### ⏱ FOCO TOTAL
        Elimine distrações e concentre-se em uma palavra de cada vez.
        """)
    
    with col2:
        st.markdown("""
        #### ⚡ MAIS VELOCIDADE
        Aumente sua velocidade de leitura com prática constante.
        """)
    
    with col3:
        st.markdown("""
        #### 🧠 MELHOR RETENÇÃO
        Treine seu cérebro para compreender e reter mais informações.
        """)
    
    # ==================================================
    # LÓGICA DE EXECUÇÃO
    # ==================================================
    if iniciar:
        if not texto.strip():
            st.error("❌ Digite um texto para começar!")
        elif len(texto.split()) < 1:
            st.error("❌ O texto precisa ter pelo menos uma palavra!")
        else:
            # Salvar configurações no estado
            st.session_state.texto_leitura = texto
            st.session_state.velocidade = velocidade
            st.session_state.palavras_por_vez = palavras_por_vez
            st.session_state.modo_foco = modo_foco
            st.session_state.leitura_ativa = True
            
            # Recarregar a página para exibir modo leitura
            st.rerun()