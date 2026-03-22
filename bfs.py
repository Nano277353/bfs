import streamlit as st
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

# ─── Configuración de página ───────────────────────────────────────────────
st.set_page_config(
    page_title="BFS · Red Social",
    page_icon="🔗",
    layout="wide"
)

# ─── Estilos ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

.stApp {
    background: #0d0d0d;
    color: #f0f0f0;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.03em;
}

.titulo-principal {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.6rem;
    color: #f0f0f0;
    letter-spacing: -0.04em;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}

.subtitulo {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #555;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

.resultado-box {
    background: #111;
    border: 1px solid #222;
    border-left: 3px solid #00ff88;
    border-radius: 6px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
}

.ruta-step {
    display: inline-block;
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 4px;
    padding: 4px 12px;
    margin: 3px;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: #f0f0f0;
}

.ruta-step.highlight {
    background: #003322;
    border-color: #00ff88;
    color: #00ff88;
}

.ruta-arrow {
    color: #444;
    margin: 0 2px;
    font-size: 0.8rem;
}

.metric-card {
    background: #111;
    border: 1px solid #222;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    text-align: center;
}

.metric-num {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #00ff88;
    line-height: 1;
}

.metric-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 4px;
}

.stButton > button {
    background: #00ff88 !important;
    color: #0d0d0d !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.5rem 1.5rem !important;
    width: 100%;
}

.stButton > button:hover {
    opacity: 0.85 !important;
    color: #0d0d0d !important;
}

label, .stSelectbox label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
    color: #555 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Algoritmo BFS ─────────────────────────────────────────────────────────
def encontrar_ruta_bfs(grafo, inicio, objetivo):
    cola = deque([[inicio]])
    visitados = set([inicio])
    while cola:
        camino = cola.popleft()
        nodo_actual = camino[-1]
        if nodo_actual == objetivo:
            return camino
        for vecino in grafo.get(nodo_actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                cola.append(nuevo_camino)
    return None

# ─── Datos de la red ───────────────────────────────────────────────────────
red_social = {
    'Tu':      ['Ana', 'Beto'],
    'Ana':     ['Tu', 'Carlos', 'Diana'],
    'Beto':    ['Tu', 'Elena'],
    'Carlos':  ['Ana'],
    'Diana':   ['Ana', 'Facundo'],
    'Elena':   ['Beto'],
    'Facundo': ['Diana'],
}

# ─── Visualización del grafo ───────────────────────────────────────────────
def dibujar_grafo(red, ruta=None):
    G = nx.Graph()
    for nodo, vecinos in red.items():
        for v in vecinos:
            G.add_edge(nodo, v)

    ruta_set = set(ruta) if ruta else set()
    ruta_edges = set()
    if ruta and len(ruta) > 1:
        for i in range(len(ruta) - 1):
            ruta_edges.add((ruta[i], ruta[i+1]))
            ruta_edges.add((ruta[i+1], ruta[i]))

    pos = nx.spring_layout(G, seed=42, k=2.5)

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#0d0d0d')
    ax.set_facecolor('#0d0d0d')

    # Aristas normales
    normal_edges = [(u, v) for u, v in G.edges() if (u, v) not in ruta_edges]
    nx.draw_networkx_edges(G, pos, edgelist=normal_edges,
                           edge_color='#2a2a2a', width=1.5, ax=ax)

    # Aristas de la ruta
    ruta_edge_list = [(u, v) for u, v in G.edges() if (u, v) in ruta_edges]
    if ruta_edge_list:
        nx.draw_networkx_edges(G, pos, edgelist=ruta_edge_list,
                               edge_color='#00ff88', width=2.5, ax=ax)

    # Nodos normales
    normal_nodes = [n for n in G.nodes() if n not in ruta_set]
    nx.draw_networkx_nodes(G, pos, nodelist=normal_nodes,
                           node_color='#1e1e1e', node_size=700,
                           edgecolors='#333', linewidths=1.5, ax=ax)

    # Nodos en la ruta
    ruta_nodes = [n for n in G.nodes() if n in ruta_set]
    if ruta_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=ruta_nodes,
                               node_color='#003322', node_size=800,
                               edgecolors='#00ff88', linewidths=2, ax=ax)

    nx.draw_networkx_labels(G, pos, font_color='#f0f0f0',
                            font_size=9, font_family='monospace', ax=ax)
    ax.axis('off')
    plt.tight_layout(pad=0.5)
    return fig

# ─── Layout principal ──────────────────────────────────────────────────────
st.markdown('<p class="titulo-principal">BFS · Red Social</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo">Búsqueda por amplitud · Ruta más corta</p>', unsafe_allow_html=True)

col_panel, col_grafo = st.columns([1, 2], gap="large")

with col_panel:
    st.markdown("#### Configurar búsqueda")
    nodos = list(red_social.keys())

    inicio = st.selectbox("Nodo de inicio", nodos, index=0)
    objetivo = st.selectbox("Nodo objetivo", nodos, index=nodos.index('Facundo'))

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    buscar = st.button("Ejecutar BFS")

    st.markdown("---")

    # Métricas de la red
    G_info = nx.Graph()
    for n, vecinos in red_social.items():
        for v in vecinos:
            G_info.add_edge(n, v)

    mc1, mc2 = st.columns(2)
    with mc1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-num">{G_info.number_of_nodes()}</div>
            <div class="metric-label">Nodos</div>
        </div>""", unsafe_allow_html=True)
    with mc2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-num">{G_info.number_of_edges()}</div>
            <div class="metric-label">Conexiones</div>
        </div>""", unsafe_allow_html=True)

with col_grafo:
    ruta_resultado = None

    if buscar:
        if inicio == objetivo:
            st.warning("El nodo de inicio y objetivo son el mismo.")
        else:
            ruta_resultado = encontrar_ruta_bfs(red_social, inicio, objetivo)

        if ruta_resultado:
            ruta_html = ""
            for i, nodo in enumerate(ruta_resultado):
                es_extremo = (nodo == inicio or nodo == objetivo)
                cls = "ruta-step highlight" if es_extremo else "ruta-step"
                ruta_html += f'<span class="{cls}">{nodo}</span>'
                if i < len(ruta_resultado) - 1:
                    ruta_html += '<span class="ruta-arrow">→</span>'

            st.markdown(f"""
            <div class="resultado-box">
                <div style="font-size:0.65rem;color:#555;text-transform:uppercase;
                            letter-spacing:0.1em;margin-bottom:0.6rem;">
                    Ruta encontrada · {len(ruta_resultado) - 1} salto(s)
                </div>
                {ruta_html}
            </div>""", unsafe_allow_html=True)
        elif buscar and inicio != objetivo:
            st.markdown("""
            <div class="resultado-box" style="border-left-color:#ff4444;">
                Sin ruta disponible entre los nodos seleccionados.
            </div>""", unsafe_allow_html=True)

    fig = dibujar_grafo(red_social, ruta=ruta_resultado)
    st.pyplot(fig, use_container_width=True)

    if not buscar:
        st.markdown("""
        <div style="font-family:'Space Mono',monospace;font-size:0.7rem;
                    color:#333;text-align:center;margin-top:0.5rem;">
            Selecciona nodos y ejecuta BFS para ver la ruta resaltada
        </div>""", unsafe_allow_html=True)