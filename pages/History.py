import streamlit as st
import pandas as pd    
import sqlite3
st.set_page_config(page_title="History",layout="wide")

with st.sidebar:
    st.title("Current Bankroll")
    st.metric(label="Current money",value=f"${st.session_state.bankroll:,.2f}")
    
conn = sqlite3.connect(r"data\bets.db")
cs = conn.cursor()
bet_query = "SELECT * FROM BETS"
bets_df = pd.read_sql(bet_query,conn)
bets_df = bets_df.iloc[::-1].reset_index(drop=True)
parlay_query = "SELECT * FROM PARLAY"
parlay_df = pd.read_sql(parlay_query,conn)
parlay_df = parlay_df.iloc[::-1].reset_index(drop=True)
st.subheader("BETS:")
for idx,row in enumerate(bets_df.itertuples()):
    status = ":green[WON]" if row.team_bet_on == row.winner else ":red[LOST]"
    row_header = f"{row.home_team} vs {row.away_team} ---------- {status}"
    with st.expander(label=row_header,expanded=False):
        c1,c2 = st.columns([2,1])
        with c1:
            st.markdown(f"Bet Amount: {row.bet_amount}$")
            st.markdown(f"Choice: {row.team_bet_on}")
            st.markdown(f"Winner: {row.winner}")
        with c2:
            st.markdown(f"Total Payout: {row.payout}$")
            
st.subheader("PARLAYS:")
for idx,row in enumerate(parlay_df.itertuples()):
    status = ":green[WON]" if row.WON == "True" else ":red[LOST]"
    row_header = f"{row.LEGS}-parlay ------ {status}"
    with st.expander(label=row_header,expanded=False):
        m1,m2 = st.columns([2,1])
        with m1:
            st.write(f"Amount Bet: {row.BET}$")
            st.write(f"Payout: {row.PAYOUT:.2f}$")