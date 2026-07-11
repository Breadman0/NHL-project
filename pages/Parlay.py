from pathlib import Path

import numpy as np
import pandas as pd
import sqlite3
import streamlit as st

st.set_page_config(page_title="Parlay Tab", layout="wide")

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
STATIC_DIR = ROOT_DIR / "static"
DATA_DIR.mkdir(exist_ok=True)

events_db_path = DATA_DIR / "events.db"
bets_db_path = DATA_DIR / "bets.db"
bankroll_path = DATA_DIR / "bankroll.txt"
log_roll_path = DATA_DIR / "log_roll.txt"

st.markdown(
    """
    <style>
    @font-face {
        font-family: 'Monocraft';
        src: url('/static/Monocraft.ttf') format('truetype');
        font-display: swap;
    }
    @font-face {
        font-family: 'Material Symbols';
        src: url('/static/MaterialSymbols-Regular.ttf') format('truetype');
        font-display: swap;
    }
    body, html, .stApp, .main, .block-container, .element-container {
        font-family: 'Segoe UI', Roboto, Arial, sans-serif !important;
        line-height: 1.4 !important;
    }
    .monocraft-app, .monocraft-app *:not(.material-icons):not([class*="material-symbol"]):not([data-testid="stIcon"]) {
        font-family: 'Monocraft', 'Courier New', monospace !important;
    }
    .material-icons, [class*="material-symbol"], [data-testid="stIcon"] {
        font-family: 'Material Symbols', 'Segoe UI Symbol', sans-serif !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="monocraft-app">', unsafe_allow_html=True)

if not bankroll_path.exists() or bankroll_path.stat().st_size == 0:
    bankroll_path.write_text("1000.0", encoding="utf-8")

if not log_roll_path.exists():
    log_roll_path.write_text("", encoding="utf-8")

if "parlay" not in st.session_state:
    st.session_state.parlay = []

with st.sidebar:
    st.title("Current Bankroll")
    st.metric(label="Current money", value=f"${st.session_state.bankroll:,.2f}")


def write_money():
    bankroll_path.write_text(str(st.session_state.bankroll), encoding="utf-8")
    with log_roll_path.open("a", encoding="utf-8") as a:
        a.write(str(st.session_state.bankroll) + "\n")

if "deleted" not in st.session_state:
    st.session_state.deleted = ":red[Entry Deleted]"
if "del_ind" not in st.session_state:
    st.session_state.del_ind = set()

cn = None
if events_db_path.exists():
    try:
        cn = sqlite3.connect(str(events_db_path))
    except sqlite3.DatabaseError:
        st.warning("Unable to open events database.")
else:
    st.warning("Event database not found: data/events.db")

df = pd.DataFrame()
if cn is not None and st.session_state.parlay:
    placeholder = ",".join(["?"] * len(st.session_state.parlay))
    sql_query = f"SELECT * FROM EVENTS WHERE game_id IN ({placeholder})"
    try:
        df = pd.read_sql_query(sql_query, cn, params=st.session_state.parlay)
        df = df.drop_duplicates(subset=["game_id"], keep="first")
    except sqlite3.DatabaseError:
        st.warning("Unable to read parlay event records.")
        df = pd.DataFrame()
elif not st.session_state.parlay:
    st.write(":red[Empty Parlay]")

bet_cal = []
if not df.empty:
    for idx, row in enumerate(df.itertuples()):
        if idx in st.session_state.del_ind:
            continue

        row_header = f"⏰ {row.time},{row.date} | {row.home_team} vs {row.away_team}"
        with st.expander(label=row_header, expanded=False):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**📍 Venue:** {row.venue}")
                st.markdown(
                    f"📊 **Market Odds:** Home: `{row.odds_1}` | Away: `{row.odds_y}` "
                )

                choice = st.radio(
                    "Select the Bet:",
                    [row.home_team, row.away_team],
                    key=f"r_{row.game_id}",
                )
                if idx in st.session_state.del_ind:
                    bet_cal.append(
                        [
                            idx,
                            choice,
                            row.odds_1 if choice == row.home_team else row.odds_y,
                            row.WINNER,
                            "Deleted",
                        ]
                    )
                else:
                    bet_cal.append(
                        [
                            idx,
                            choice,
                            row.odds_1 if choice == row.home_team else row.odds_y,
                            row.WINNER,
                        ]
                    )

            with c2:
                if st.button("Delete Entry", key=f"k_{row.game_id}"):
                    st.write(st.session_state.deleted)
                    st.session_state.del_ind.add(idx)
                    st.rerun()

if cn is not None:
    cn.commit()
    cn.close()

cm = sqlite3.connect(str(bets_db_path))
cr = cm.cursor()
cr.execute(
    """
    CREATE TABLE IF NOT EXISTS PARLAY(
        BET REAL,
        PAYOUT REAL,
        WON TEXT,
        LEGS INTEGER
    )
    """
)

st.markdown('</div>', unsafe_allow_html=True)

bet_cal = [sub for sub in bet_cal if len(sub) == 4]
bet_cal = np.array(bet_cal, dtype=object)
row_odds = 1.00
money_bet = st.number_input(
    "Bet Wager:",
    min_value=0.00,
    max_value=float(st.session_state.bankroll),
    step=5.00,
)
if st.button("Confirm Parlay"):
    if bet_cal.size > 0:
        for i in range(len(bet_cal)):
            if bet_cal[i][3] == bet_cal[i][1]:
                row_odds = row_odds * float(bet_cal[i][2])
            else:
                st.write(":red[Parlay Lost]")
                st.write(f"*** Match {i+1}::")
                st.write(f"Choice:{bet_cal[i][1]}")
                st.write(f"Winner:{bet_cal[i][3]}")
                row_odds = 0.00
        sql_query = """
        INSERT INTO PARLAY(BET,PAYOUT,WON,LEGS)
        VALUES(?,?,?,?)
        """
        cr.execute(
            sql_query,
            (
                money_bet,
                row_odds * money_bet,
                "True" if row_odds != 0 else "False",
                len(bet_cal),
            ),
        )
        cm.commit()
        cr.close()
        if row_odds != 0.00:
            st.write(":green[Parlay Won]")
            st.write(f"Total Payout: {row_odds * money_bet:.2f}$")
            st.session_state.bankroll = st.session_state.bankroll + (row_odds * money_bet)
            write_money()
        else:
            st.write("Total Payout: 0$")
            st.session_state.bankroll = st.session_state.bankroll - money_bet
            write_money()
    else:
        st.write("Check Parlay again")