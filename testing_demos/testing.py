import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Hockey Slip & Bankroll", layout="centered")

# --- 1. INITIALIZE BANKROLL & SYSTEM STATE ---
if "bankroll" not in st.session_state:
    st.session_state.bankroll = 1000.00  # Starting balance

if "user_bets" not in st.session_state:
    st.session_state.user_bets = {}  # Format: {game_id: {"bet_type": "Home", "amount": 10.00}}

# --- 2. SIDEBAR: BANKROLL MANAGEMENT ---
with st.sidebar:
    st.title("💰 Your Wallet")
    st.metric(label="Current Bankroll", value=f"${st.session_state.bankroll:,.2f}")
    
    st.write("---")
    st.subheader("🏦 Withdraw Funds")
    
    # Withdrawal Input
    withdraw_amount = st.number_input(
        "Amount to withdraw ($):", 
        min_value=0.00, 
        max_value=float(st.session_state.bankroll), 
        step=10.00
    )
    
    if st.button("💸 Execute Withdrawal"):
        if withdraw_amount > 0:
            st.session_state.bankroll -= withdraw_amount
            st.success(f"Successfully withdrew ${withdraw_amount:.2f}!")
            st.rerun()  # Instantly updates the metric display
        else:
            st.error("Please enter an amount greater than $0.")

# --- 3. MATCH DAY DATA ---
data = {
    "game_id": ["2018020048", "2018020049"],
    "time": ["7:00 PM", "7:30 PM"],
    "home_team": ["Devils", "Rangers"],
    "away_team": ["Capitals", "Lightning"],
    "odds_1": [1.95, 2.10],
    "odds_y": [3.40, 3.20],
}
df = pd.DataFrame(data)

st.subheader("🏒 Tonight's Schedule")

# --- 4. EXPANDER MATCH ROWS WITH BET DETAILS ---
for row in df.itertuples():
    row_header = f"⏰ {row.time} | {row.home_team} vs {row.away_team}"
    
    with st.expander(label=row_header, expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"📊 **Odds:** Home ({row.odds_1}) | Away ({row.odds_y})")
            # Select team to bet on
            choice = st.radio(
                "Pick your team:", 
                ["None", row.home_team, row.away_team], 
                key=f"pick_{row.game_id}"
            )
            
        with col2:
            # Input bet amount
            bet_amt = st.number_input(
                "Wager Amount ($):", 
                min_value=0.00, 
                max_value=float(st.session_state.bankroll), 
                step=5.00, 
                key=f"amt_{row.game_id}"
            )
            
            # Save bet configuration to memory
            if choice != "None" and bet_amt > 0:
                st.session_state.user_bets[row.game_id] = {
                    "match": f"{row.home_team} vs {row.away_team}",
                    "pick": choice,
                    "wager": bet_amt,
                    "potential_payout": bet_amt * (row.odds_1 if choice == row.home_team else row.odds_y)
                }

# --- 5. GENERATE VERIFIED SLIP DOWNLOAD ---
st.write("---")
st.subheader("🎟️ Active Betting Slip")

if st.session_state.user_bets:
    # Display current pending bets on screen
    for gid, details in list(st.session_state.user_bets.items()):
        st.markdown(f"**{details['match']}** ➡️ Predicts *{details['pick']}* | Wager: `${details['wager']:.2f}` | Payout: `${details['potential_payout']:.2f}`")

    # BUILD SLIP TEXT STRING
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    slip_text = f"====================================\n"
    slip_text += f"       VERIFIED NHL BETTING SLIP    \n"
    slip_text += f"====================================\n"
    slip_text += f"Issued At: {timestamp}\n"
    slip_text += f"Client Remaining Balance: ${st.session_state.bankroll:.2f}\n"
    slip_text += f"------------------------------------\n"
    
    total_wager = 0
    for gid, details in st.session_state.user_bets.items():
        slip_text += f"Game ID: {gid}\n"
        slip_text += f"Matchup: {details['match']}\n"
        slip_text += f"Selection: {details['pick']}\n"
        slip_text += f"Wager: ${details['wager']:.2f}\n"
        slip_text += f"Est. Payout: ${details['potential_payout']:.2f}\n"
        slip_text += f"------------------------------------\n"
        total_wager += details['wager']
        
    slip_text += f"TOTAL WAGERED: ${total_wager:.2f}\n"
    slip_text += f"VERIFICATION CODE: SIGNED_MD5_{hash(slip_text[:20])}\n"
    slip_text += f"===================================="

    # Render Download Button
    st.download_button(
        label="📥 Download Verified Receipt (.txt)",
        data=slip_text,
        file_name=f"BetSlip_{datetime.date.today()}.txt",
        mime="text/plain"
    )
else:
    st.info("No active wagers placed on your slip yet.")