import streamlit as st
import datetime
import pandas as pd 
import sqlite3
import os

st.set_page_config(page_title="Events calendar",layout="wide")

with st.sidebar:
    st.title("Current Bankroll")
    st.metric(label="Current money",value=f"${st.session_state.bankroll:,.2f}")

selected_date = st.date_input(
    label="Choose the Date",
    value=datetime.date(2018,10,3),
    min_value =datetime.date(2018,10,3),
    max_value=datetime.date(2019,3,10)
)
####Bankroll
path = r"data\bankroll.txt"
        
def write_money():
    with open(path,"w") as w:
        w.write(str(st.session_state.bankroll))
    with open('data\log_roll.txt',"a") as a:
        a.write(str(st.session_state.bankroll)+"\n")
#######
conn = sqlite3.connect(r'data\events.db')
c = conn.cursor()
date = selected_date.strftime("%Y-%m-%d")
c.execute('SELECT DISTINCT * FROM events WHERE DATE=?',(date,))
selected_data = c.fetchall()
c.close()
df = pd.DataFrame(selected_data,columns=["id","game_id",
  "date" ,
  "home_team" ,
  "away_team" ,
  "home_goals" ,
  "away_goals" ,
  "venue" ,
  "WINNER" ,
  "time" ,
  "odds_1" ,
  "odds_x" ,
  "odds_y"])
df = df.drop_duplicates(subset=["game_id"], keep="first")
num_rows = len(df)
connection = sqlite3.connect(r'data\bets.db')
cn = connection.cursor()
cn.execute("""
          CREATE TABLE IF NOT EXISTS BETS(
              match_id INTEGER,
              home_team TEXT,
              away_team TEXT,
              bet_amount REAL,
              team_bet_on TEXT,
              winner TEXT,
              payout REAL
          )
          
          
          """)
if 'parlay' not in st.session_state:
    st.session_state.parlay = []
if num_rows > 0:
    cols = st.columns(num_rows)
    for idx,row in enumerate(df.itertuples()):
            row_header = f"⏰ {row.time} | {row.home_team} vs {row.away_team}"
            with st.expander(label=row_header,expanded=False):
                sub1,sub2 = st.columns([2,1])
            with sub1:
                st.markdown(f"**📍 Venue:** {row.venue}")
                st.markdown(
                    f"📊 **Market Odds:** Home: `{row.odds_1}` | Away: `{row.odds_y}` "
                )
                
                choice = st.radio(
                    "Select the Bet:",
                    [row.home_team,row.away_team,"Parlay"],
                    key = f"r_{row.game_id}"
                )
            
            with sub2:
                wager = st.number_input(
                        "Enter Wager Amount:",
                        min_value = 0.00,
                        max_value = float(st.session_state.bankroll),
                        step = 5.00,
                        key = f"amt_{row.game_id}"
                    )
                if choice != None:
                    if st.button("Place bet",key=f"_{row.game_id}"):
                        if choice == row.WINNER:
                            st.write(":green[WON]")
                            st.write(f"Total Payout: {wager * (row.odds_1 if choice == row.home_team else row.odds_y):.2f}$")
                            st.session_state.bankroll = st.session_state.bankroll + (wager * (row.odds_1 if choice == row.home_team else row.odds_y))
                            write_money()
                            sql_query=("""
                                       INSERT INTO BETS(match_id,home_team,away_team,bet_amount,team_bet_on,winner,payout)
                                       VALUES(?,?,?,?,?,?,?)
                                       """)
                            cn.execute(sql_query,(
                                row.game_id,
                                row.home_team,
                                row.away_team,
                                wager,
                                choice,
                                row.WINNER,
                                wager * (row.odds_1 if choice == row.home_team else row.odds_y)
                            ))
                        elif choice == "Parlay":
                                st.session_state.parlay.append(row.game_id)
                                st.write(":green[Please access the Parlay Tab]")
                        else:
                            st.write(":red[LOST]")
                            st.write("Total Payout: 0$")
                            st.session_state.bankroll = st.session_state.bankroll-wager
                            write_money()
                            sql_query=("""
                                       INSERT INTO BETS(match_id,home_team,away_team,bet_amount,team_bet_on,winner,payout)
                                       VALUES(?,?,?,?,?,?,?)
                                       """)
                            cn.execute(sql_query,(
                                row.game_id,
                                row.home_team,
                                row.away_team,
                                wager,
                                choice,
                                row.WINNER,
                                wager * (row.odds_1 if choice == row.home_team else row.odds_y)
                            ))
                    
                    
                    
else:
    st.write("No Scheduled Games For Today")
connection.commit()
cn.close()
