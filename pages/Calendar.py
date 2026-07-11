import datetime
from pathlib import Path
import base64
import pandas as pd
import sqlite3
import streamlit as st

st.set_page_config(page_title="Events calendar", layout="wide")

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
    .stApp, .stApp *:not(.material-icons):not([class*="material-symbol"]):not([data-testid="stIcon"]) {
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

bankroll_path = DATA_DIR / "bankroll.txt"
log_roll_path = DATA_DIR / "log_roll.txt"
events_db_path = DATA_DIR / "events.db"
bets_db_path = DATA_DIR / "bets.db"

if not bankroll_path.exists() or bankroll_path.stat().st_size == 0:
    bankroll_path.write_text("1000.0", encoding="utf-8")

if not log_roll_path.exists():
    log_roll_path.write_text("", encoding="utf-8")

if "bankroll" not in st.session_state:
    try:
        st.session_state.bankroll = float(bankroll_path.read_text(encoding="utf-8").strip())
    except Exception:
        st.session_state.bankroll = 1000.0
        bankroll_path.write_text("1000.0", encoding="utf-8")

if "parlay" not in st.session_state:
    st.session_state.parlay = []

with st.sidebar:
    st.title("Current Bankroll")
    st.metric(label="Current money", value=f"${st.session_state.bankroll:,.2f}")

selected_date = st.date_input(
    label="Choose the Date",
    value=datetime.date(2018, 10, 3),
    min_value=datetime.date(2018, 10, 3),
    max_value=datetime.date(2019, 3, 10),
)


def write_money():
    bankroll_path.write_text(str(st.session_state.bankroll), encoding="utf-8")
    with log_roll_path.open("a", encoding="utf-8") as a:
        a.write(str(st.session_state.bankroll) + "\n")

selected_data = []
if events_db_path.exists():
    try:
        with sqlite3.connect(str(events_db_path)) as conn:
            cur = conn.cursor()
            date_value = selected_date.strftime("%Y-%m-%d")
            cur.execute("SELECT DISTINCT * FROM events WHERE DATE=?", (date_value,))
            selected_data = cur.fetchall()
    except sqlite3.DatabaseError:
        st.warning("Unable to read event data from the database.")
else:
    st.warning("Event database not found: data/events.db")

columns = [
    "id",
    "game_id",
    "date",
    "home_team",
    "away_team",
    "home_goals",
    "away_goals",
    "venue",
    "WINNER",
    "time",
    "odds_1",
    "odds_x",
    "odds_y",
]

if selected_data:
    df = pd.DataFrame(selected_data, columns=columns)
else:
    df = pd.DataFrame(columns=columns)

df = df.drop_duplicates(subset=["game_id"], keep="first")
num_rows = len(df)

connection = sqlite3.connect(str(bets_db_path))
cn = connection.cursor()
cn.execute(
    """
    CREATE TABLE IF NOT EXISTS BETS(
        match_id INTEGER,
        home_team TEXT,
        away_team TEXT,
        bet_amount REAL,
        team_bet_on TEXT,
        winner TEXT,
        payout REAL
    )
    """
)

if num_rows > 0:
    cols = st.columns(num_rows)
    for idx, row in enumerate(df.itertuples()):
        row_header = f"⏰ {row.time} | {row.home_team} vs {row.away_team}"
        with st.expander(label=row_header, expanded=False):
            sub1, sub2 = st.columns([2, 1])
            with sub1:
                st.markdown(f"**📍 Venue:** {row.venue}")
                st.markdown(
                    f"📊 **Market Odds:** Home: `{row.odds_1}` | Away: `{row.odds_y}` "
                )

                choice = st.radio(
                    "Select the Bet:",
                    [row.home_team, row.away_team, "Parlay"],
                    key=f"r_{row.game_id}",
                )

            with sub2:
                wager = st.number_input(
                    "Enter Wager Amount:",
                    min_value=0.00,
                    max_value=float(st.session_state.bankroll),
                    step=5.00,
                    key=f"amt_{row.game_id}",
                )
                if st.button("Place bet", key=f"_{row.game_id}"):
                    if choice == row.WINNER:
                        payout = wager * (row.odds_1 if choice == row.home_team else row.odds_y)
                        st.write(":green[WON]")
                        st.write(f"Total Payout: {payout:.2f}$")
                        st.session_state.bankroll += payout
                        write_money()
                        sql_query = """
                            INSERT INTO BETS(match_id,home_team,away_team,bet_amount,team_bet_on,winner,payout)
                            VALUES(?,?,?,?,?,?,?)
                        """
                        cn.execute(
                            sql_query,
                            (
                                row.game_id,
                                row.home_team,
                                row.away_team,
                                wager,
                                choice,
                                row.WINNER,
                                payout,
                            ),
                        )
                    elif choice == "Parlay":
                        st.session_state.parlay.append(row.game_id)
                        st.write(":green[Please access the Parlay Tab]")
                    else:
                        payout = 0.0
                        st.write(":red[LOST]")
                        st.write("Total Payout: 0$")
                        st.session_state.bankroll -= wager
                        write_money()
                        sql_query = """
                            INSERT INTO BETS(match_id,home_team,away_team,bet_amount,team_bet_on,winner,payout)
                            VALUES(?,?,?,?,?,?,?)
                        """
                        cn.execute(
                            sql_query,
                            (
                                row.game_id,
                                row.home_team,
                                row.away_team,
                                wager,
                                choice,
                                row.WINNER,
                                payout,
                            ),
                        )

else:
    st.write("No Scheduled Games For Today")

connection.commit()
cn.close()
st.markdown('</div>', unsafe_allow_html=True)
