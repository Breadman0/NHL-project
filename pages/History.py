from pathlib import Path

import pandas as pd
import sqlite3
import streamlit as st

st.set_page_config(page_title="History", layout="wide")

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
STATIC_DIR = ROOT_DIR / "static"
DATA_DIR.mkdir(exist_ok=True)

st.markdown(
    """
    <style>
    @font-face {
        font-family: 'Monocraft';
        src: url('/app/static/Monocraft.ttf') format('truetype');
        font-display: swap;
    }
    @font-face {
        font-family: 'Material Symbols';
        src: url('/app/static/MaterialSymbols-Regular.ttf') format('truetype');
        font-display: swap;
    }
    body, html, .stApp, .main, .block-container, .element-container {
        font-family: 'Segoe UI', Roboto, Arial, sans-serif !important;
        line-height: 1.4 !important;
    }
    .stApp *:not([class*="material-symbol"]):not([data-testid*="Icon"]):not([data-testid*="icon"]):not([data-baseweb="icon"]):not(svg):not(svg *) {
        font-family: 'Monocraft', 'Courier New', monospace !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="monocraft-app">', unsafe_allow_html=True)

bets_db_path = DATA_DIR / "bets.db"

with st.sidebar:
    st.title("Current Bankroll")
    st.metric(label="Current money", value=f"${st.session_state.bankroll:,.2f}")

bets_df = pd.DataFrame()
parlay_df = pd.DataFrame()

if bets_db_path.exists():
    try:
        conn = sqlite3.connect(str(bets_db_path))
        bet_query = "SELECT * FROM BETS"
        bets_df = pd.read_sql(bet_query, conn)
        bets_df = bets_df.iloc[::-1].reset_index(drop=True)
        parlay_query = "SELECT * FROM PARLAY"
        parlay_df = pd.read_sql(parlay_query, conn)
        parlay_df = parlay_df.iloc[::-1].reset_index(drop=True)
        conn.close()
    except sqlite3.DatabaseError:
        st.warning("Unable to read history data from data/bets.db.")
else:
    st.warning("History database not found: data/bets.db")

st.subheader("BETS:")
if not bets_df.empty:
    for idx, row in enumerate(bets_df.itertuples()):
        status = ":green[WON]" if row.team_bet_on == row.winner else ":red[LOST]"
        row_header = f"{row.home_team} vs {row.away_team} ---------- {status}"
        with st.expander(label=row_header, expanded=False):
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"Bet Amount: {row.bet_amount}$")
                st.markdown(f"Choice: {row.team_bet_on}")
                st.markdown(f"Winner: {row.winner}")
            with c2:
                st.markdown(f"Total Payout: {row.payout}$")
else:
    st.write("No bet history available.")

st.subheader("PARLAYS:")
if not parlay_df.empty:
    for idx, row in enumerate(parlay_df.itertuples()):
        status = ":green[WON]" if row.WON == "True" else ":red[LOST]"
        row_header = f"{row.LEGS}-parlay ------ {status}"
        with st.expander(label=row_header, expanded=False):
            m1, m2 = st.columns([2, 1])
            with m1:
                st.write(f"Amount Bet: {row.BET}$")
                st.write(f"Payout: {row.PAYOUT:.2f}$")
else:
    st.write("No parlay history available.")

st.markdown('</div>', unsafe_allow_html=True)