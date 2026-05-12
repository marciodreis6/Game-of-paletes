import streamlit as st
import random

# =========================================
# CONFIGURAÇÕES INICIAIS
# =========================================

st.set_page_config(
    page_title="Cadê Meu Palete?",
    page_icon="📦",
    layout="wide"
)

# =========================================
# INICIALIZAÇÃO DO JOGO
# =========================================

if "estoque" not in st.session_state:
    st.session_state.estoque = 500
    st.session_state.orcamento = 9000
    st.session_state.perdas = 243
    st.session_state.dia = 1

    st.session_state.transportadoras = {
        "Carcará": 87,
        "Trend": 54,
        "IJ transporte": 63,
        "Frota propria": 39
    }

clientes = [
    "Atacadão",
    "Sendas",
    "WMS",
    "Atakarejo",
    "Avanço distribuidora"
]

mensagens_eventos = [
    "Motorista disse que esqueceu os pallets no cliente.",
    "Cliente informou que não encontrou os pallets.",
    "Motorista esqueceu de prestar contas na portaria.",
    "Motorista perdeu o comprovante de descarga.",
    "Transportadora jurou que devolveu tudo. Mentira provável.",
    "Auditoria pediu explicação sobre perdas.",
    "Tasker disse que perdeu a nota fiscal de palete."
]

# =========================================
# FUNÇÕES
# =========================================

def gerar_expedicao():
    cliente = random.choice(clientes)
    transportadora = random.choice(
        list(st.session_state.transportadoras.keys())
    )
    quantidade = random.randint(10, 30)

    return cliente, transportadora, quantidade


def evento_aleatorio():
    chance = random.randint(1, 100)

    if chance <= 35:
        evento = random.choice(mensagens_eventos)

        st.warning(f"⚠ EVENTO: {evento}")

        if "perdeu" in evento:
            st.session_state.estoque -= 6
            st.session_state.perdas += 6


# =========================================
# TÍTULO
# =========================================

st.title("📦 CADÊ MEU PALETE?")
st.caption("Sistema Corporativo de Controle Operacional")

# =========================================
# STATUS
# =========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Estoque",
    st.session_state.estoque
)

col2.metric(
    "Orçamento",
    f"R$ {st.session_state.orcamento}"
)

col3.metric(
    "Perdas",
    st.session_state.perdas
)

col4.metric(
    "Dia",
    st.session_state.dia
)

# =========================================
# TRANSPORTADORAS
# =========================================

st.subheader("🚚 Transportadoras Devendo")

for nome, saldo in st.session_state.transportadoras.items():
    st.write(f"**{nome}** → {saldo} pallets")

# =========================================
# EXPEDIÇÃO
# =========================================

st.subheader("📤 Nova Expedição")

cliente, transportadora, quantidade = gerar_expedicao()

st.info(f"""
CLIENTE: {cliente}

TRANSPORTADORA: {transportadora}

PALETS NECESSÁRIOS: {quantidade}
""")

col_a, col_b, col_c = st.columns(3)

# APROVAR
if col_a.button("✅ Aprovar envio"):

    if st.session_state.estoque >= quantidade:

        st.session_state.estoque -= quantidade

        st.session_state.transportadoras[
            transportadora
        ] += quantidade

        st.success("Carga liberada.")

        evento_aleatorio()

        st.session_state.dia += 1

    else:
        st.error("Estoque insuficiente.")

# NEGAR
if col_b.button("❌ Negar envio"):

    st.error("Cliente ficou puto com atraso.")

    st.session_state.dia += 1

# COMPRAR
if col_c.button("🛒 Comprar pallets"):

    qtd = 50
    custo = qtd * 31

    if st.session_state.orcamento >= custo:

        st.session_state.orcamento -= custo
        st.session_state.estoque += qtd

        st.success(f"Compra realizada: +{qtd} pallets")

    else:
        st.error("Orçamento insuficiente.")

# =========================================
# DEVOLUÇÃO
# =========================================

st.subheader("📥 Devoluções")

transportadora_dev = random.choice(
    list(st.session_state.transportadoras.keys())
)

divida = st.session_state.transportadoras[transportadora_dev]

if divida > 0:

    devolvidos = random.randint(0, divida)

    st.write(f"""
    TRANSPORTADORA: {transportadora_dev}

    DEVOLVIDOS: {devolvidos}

    PENDENTES: {divida - devolvidos}
    """)

    if devolvidos < divida:

        justificativa = random.choice(mensagens_eventos)

        st.warning(f"JUSTIFICATIVA: {justificativa}")

        col1, col2, col3 = st.columns(3)

        if col1.button("Aceitar perda"):

            perda = divida - devolvidos

            st.session_state.perdas += perda

            st.error(
                f"Você perdeu {perda} pallets igual um animal."
            )

        if col2.button("Cobrar"):

            st.success("Cobrança enviada.")

        if col3.button("Multar"):

            st.error(
                "Transportadora enviou comprovante claramente falso."
            )

    st.session_state.estoque += devolvidos

    st.session_state.transportadoras[
        transportadora_dev
    ] -= devolvidos

# =========================================
# CONDIÇÕES DE VITÓRIA E DERROTA
# =========================================

total_divida = sum(
    st.session_state.transportadoras.values()
)

# DERROTA 1 — ESTOQUE
if st.session_state.estoque <= 0:

    st.error("💀 GAME OVER — FALTA DE PALETS")

    st.write("""
    A fábrica parou completamente.

    Caminhões estão aguardando carga.

    O gerente entrou em colapso psicológico.
    """)

    st.stop()

# DERROTA 2 — ORÇAMENTO
if st.session_state.orcamento <= 0:

    st.error("💸 GAME OVER — FALÊNCIA OPERACIONAL")

    st.write("""
    A empresa ficou sem verba para comprar pallets.

    Diretoria culpou você imediatamente.
    """)

    st.stop()

# DERROTA 3 — AUDITORIA
if st.session_state.perdas >= 400:

    st.error("📋 GAME OVER — AUDITORIA REPROVADA")

    st.write("""
    Auditoria identificou descontrole operacional grave.

    Sumiram pallets demais.

    Alguém vai rodar nessa história.
    """)

    st.stop()

# DERROTA 4 — COLAPSO LOGÍSTICO
if total_divida >= 700:

    st.error("🚚 GAME OVER — COLAPSO LOGÍSTICO")

    st.write("""
    Transportadoras acumulam pallets demais.

    O pátio virou um caos absoluto.
    """)

    st.stop()

# =========================================
# VITÓRIA
# =========================================

if (
    st.session_state.dia >= 20
    and st.session_state.perdas < 100
    and st.session_state.estoque > 80
):

    st.success("🏆 OPERAÇÃO RECUPERADA")

    st.write("""
    Você conseguiu recuperar o controle operacional.

    As perdas foram reduzidas.

    A auditoria aprovou os resultados.

    Pela primeira vez em anos o setor de pallets
    não está pegando fogo.
    """)

    # RANK FINAL

    st.subheader("📊 AVALIAÇÃO FINAL")

    if st.session_state.perdas <= 50:

        rank = "S"

        status = "Lenda dos Pallets"

    elif st.session_state.perdas <= 80:

        rank = "A"

        status = "Especialista Operacional"

    else:

        rank = "B"

        status = "Sobreviveu ao inferno"

    st.write(f"RANK: {rank}")

    st.write(f"STATUS: {status}")

    st.write(f"PERDAS FINAIS: {st.session_state.perdas}")

    st.write(f"ESTOQUE FINAL: {st.session_state.estoque}")

    st.stop()
