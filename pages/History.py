from pathlib import Path
import pandas as pd
import sqlite3
import streamlit as st
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime
import string
import random 
import os 
from utils.styling import inject_custom_css
inject_custom_css()
st.set_page_config(page_title="History", layout="wide")

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
STATIC_DIR = ROOT_DIR / "static"
DATA_DIR.mkdir(exist_ok=True)

def generate_ticket_id(length=8):
    characters = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(characters, k=length))
    return f"TRB-{random_part}"

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
                if st.button("Generate Betting Slip",key=f"bet_{row.winner}_{row.Index}"):
                    pages_dir = os.path.dirname(os.path.abspath(__file__))
                    env = Environment(loader=FileSystemLoader(pages_dir))
                    template = env.get_template("the-tribune-straight-bet.html")
                    html_content = template.render(
                        ticket_id = generate_ticket_id(),
                        date_time = datetime.today().strftime('%Y-%m-%d'),
                        team_1 = row.home_team,
                        team_2 = row.away_team,
                        choice = row.team_bet_on,
                        odds = "BAD FOR YOU" if row.team_bet_on  != row.winner else float(round(row.payout/row.bet_amount,2)),
                        money_bet = f"${row.bet_amount}",
                        expected_payout = f"${round(row.payout,2)}" if row.team_bet_on == row.winner else "$0"
                    )
                    pdf_bytes = HTML(string=html_content).write_pdf()
                    st.download_button(
                        label="📥 Download Slip PDF",
                        data=pdf_bytes,
                        file_name=f"betting_slip.pdf",
                        mime="application/pdf"
                    )
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
            with m2:
                if st.button("Generate Betting Slip",key=f"bet_{row.PAYOUT}_{row.Index}"):
                    pages_dir = os.path.dirname(os.path.abspath(__file__))
                    env = Environment(loader=FileSystemLoader(pages_dir))
                    template = env.get_template("the-tribune-parlay.html")
                    html_content = template.render(
                        legs_1 = row.LEGS,
                        ticket_id = generate_ticket_id(),
                        date = datetime.today().strftime('%Y-%m-%d'),
                        legs = row.LEGS,
                        amount_bet = f"${row.BET}",
                        payout = f"${float(round(row.PAYOUT,2))}"
                    )
                    pdf_bytes = HTML(string=html_content).write_pdf()
                    st.download_button(
                        label="📥 Download Slip PDF",
                        data=pdf_bytes,
                        file_name=f"betting_slip.pdf",
                        mime="application/pdf"
                    )
else:
    st.write("No parlay history available.")

st.markdown('</div>', unsafe_allow_html=True)