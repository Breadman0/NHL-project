import os
import sqlite3
import sys
from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from utils.styling import inject_custom_css
inject_custom_css()

st.set_page_config(page_title="The Hockey Telegraph", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = BASE_DIR / "images"
STATIC_DIR = BASE_DIR / "static"

sys.path.append(str(BASE_DIR))
os.chdir(str(BASE_DIR))

font_path = STATIC_DIR / "Monocraft.ttf"
if font_path.exists():
    try:
        fm.fontManager.addfont(str(font_path))
        font_name = fm.FontProperties(fname=str(font_path)).get_name()
        plt.rcParams["font.family"] = font_name
    except Exception:
        plt.rcParams["font.family"] = "DejaVu Sans"
else:
    plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False

DATA_DIR.mkdir(exist_ok=True)



st.markdown('<div class="monocraft-app">', unsafe_allow_html=True)

## WIN loss calc:
connection = sqlite3.connect(str(DATA_DIR / "bets.db"))
conn = connection.cursor()
bet_q = """ SELECT team_bet_on , winner
            FROM BETS

"""
parlay_q = """SELECT WON
            FROM PARLAY

"""

try:
    bet_df = pd.read_sql_query(bet_q, connection)
except Exception:
    bet_df = pd.DataFrame(columns=["team_bet_on", "winner"])

try:
    parlay_df = pd.read_sql_query(parlay_q, connection)
except Exception:
    parlay_df = pd.DataFrame(columns=["WON"])

won, lost = 0, 0
for _, row in enumerate(bet_df.itertuples()):
    if getattr(row, "winner", None) == getattr(row, "team_bet_on", None):
        won += 1
    else:
        lost += 1
for _, row in enumerate(parlay_df.itertuples()):
    if getattr(row, "WON", None) is True:
        won += 1
    else:
        lost += 1

bankroll_path = DATA_DIR / "bankroll.txt"
log_roll_path = DATA_DIR / "log_roll.txt"

if not bankroll_path.exists() or bankroll_path.stat().st_size == 0:
    bankroll_path.write_text("1000.0", encoding="utf-8")

if not log_roll_path.exists():
    log_roll_path.write_text("", encoding="utf-8")

if "bankroll" not in st.session_state:
    st.session_state.bankroll = float(bankroll_path.read_text(encoding="utf-8").strip())

st.markdown(
    """
    <style>
    section.stMain .block-container {
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<hr>',unsafe_allow_html=True)
right,center,left = st.columns([2,6,2],border=True)
with center:
    st.markdown('<h1 style="text-align: center; padding-top: 30px; font-family: serif; font-size: 4rem;">The Tribune</h1>', unsafe_allow_html=True)
    r, c, l, m, n = st.columns([4, 4, 4, 5, 4])
    with l:
        st.image(str(IMAGES_DIR / "nhl_logo.png"), width=200)
with left:
    st.markdown('<h3 style="font-family:serif;">&emsp;LATE CITY&emsp;&ensp;EDITION</h3><p>FIVE CENTS In Manhattan,<br>Brooklyn and The Bronx <br>| TEN CENTS Elsewhere</p>', unsafe_allow_html=True)
with right:
    st.markdown('<h5>WEATHER<h5><p style="font-size:15px;">Today: Fair , Moderate winds</p><p style="font-size:15px;">Tomorrow : Clear Expected<h6>Vol. LXXXVII No. 29,407 | (Copyright, 1927, New York Tribune Inc.)</h6>', unsafe_allow_html=True)

cols = st.columns(41)
for i in range(41):
    with cols[i]:
        img_path = IMAGES_DIR / "NHL Logos" / f"image ({i + 1}).png"
        st.image(str(img_path), width=80)
    
st.markdown('<hr>',unsafe_allow_html=True)    
r1,c1,l1 = st.columns([3,3,3])

with c1:
    st.markdown('<h4 style="text-align: center; padding-top: 5px; font-family: serif;">"God Bless America"</h4>', unsafe_allow_html=True)
with l1:
    r2, c2, l2 = st.columns([6, 6, 5])
    with l2:
        st.image(str(IMAGES_DIR / "canon2.png"), width=100)
with r1:
    st.image(str(IMAGES_DIR / "canon1.png"), width=100)
st.markdown('<h6 style="text-align: center; padding-top: 10px;">Vol. I • June 2026</h6>', unsafe_allow_html=True)


main, sidebar = st.columns([7, 3],border=True)


with main:
    with st.container(height=1000):
        bg = "#F5F1E8"
        accent = "#7C5B3B"
        accent_secondary = "#B78C53"
        accent_tertiary = "#C47A4A"
        grid_color = "#D7C6A8"
        text_color = "#4F3E2A"

        fig, ax = plt.subplots()
        with log_roll_path.open("r", encoding="utf-8") as r:
            lines = r.read().splitlines()
            lines = [float(val) for val in lines if val]

        x_vals = list(range(1, len(lines) + 1))
        fig.patch.set_facecolor(bg)
        ax.set_facecolor(bg)
        ax.plot(x_vals, lines, '-o', color=accent, linewidth=2.2, markersize=4)
        ax.grid(True, color=grid_color, alpha=0.8)
        ax.set_title("Bankroll History", color=text_color)
        ax.tick_params(colors=text_color)
        for spine in ax.spines.values():
            spine.set_color(grid_color)
        st.pyplot(fig)

        fig1, ax1 = plt.subplots()
        labels = ['Won', 'Lost']
        sizes = [won, lost]
        explode = [0.1, 0]
        colors = [accent, accent_secondary]
        fig1.patch.set_facecolor(bg)
        ax1.set_facecolor(bg)
        ax1.pie(
            sizes,
            explode=explode,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            shadow=True,
            startangle=140,
            textprops={'color': text_color}
        )
        ax1.set_title("Win-Loss Ratio", color=text_color)
        ax1.axis('equal')
        st.pyplot(fig1)
        
        lines_np = np.array(lines)
        profit_np = np.diff(lines_np)
        cum_sum = np.cumsum(profit_np)
        roi = (cum_sum / 1000) * 100
        fig2, ax2 = plt.subplots()
        fig2.patch.set_facecolor(bg)
        ax2.set_facecolor(bg)
        ax2.plot(x_vals[:-1], roi, '-o', linewidth=2.2, color=accent_secondary, markersize=4)
        ax2.axhline(0, color=accent_tertiary, linestyle='--', linewidth=1.5, alpha=0.8)
        ax2.grid(2, color=grid_color, alpha=0.8)
        ax2.set_title("ROI Chart", color=text_color)
        ax2.tick_params(colors=text_color)
        for spine in ax2.spines.values():
            spine.set_color(grid_color)
        st.pyplot(fig2)
        
        profit_net = np.sum(profit_np[profit_np>0])
        loss_net = np.sum(profit_np[profit_np<0])
        net = profit_net+loss_net
        colo = ""
        if net > 0:
            colo = "green"
        elif net == 0:
            colo ="grey"
        else:
            colo ="red"
        p,n,l = st.columns([2,2,2])
        with p:
            st.markdown("<h4 style='text-align:center;'>PROFIT:</h4>",unsafe_allow_html=True)
            st.markdown(f"<h5 style='color:green;text-align:center;'>{profit_net:.2f}$</h5>",unsafe_allow_html=True)
            
        with n:
            st.markdown("<h4 style='text-align:center;'>NET:</h4>",unsafe_allow_html=True)
            st.markdown(f"<h5 style='color:{colo};text-align:center;'>{net:.2f}$</h5>",unsafe_allow_html=True)
        with l:
            st.markdown("<h4 style='text-align:center;'>LOSS:</h4>",unsafe_allow_html=True)
            st.markdown(f"<h5 style='color:red;text-align:center;'>{loss_net:.2f}$</h5>",unsafe_allow_html=True)

with sidebar:
    with st.container(height=1000):
        st.image(str(IMAGES_DIR / "n1.png"))
        st.write("Staal scores 2, Hurricanes top Golden Knights in Game 4, even Stanley Cup Final")
        st.image(str(IMAGES_DIR / "n2.png"))
        st.write("Hertl breaks tie late, Golden Knights edge Hurricanes in Game 1 of Cup Final")
        st.image(str(IMAGES_DIR / "n3.png"))
        st.write("Hurricanes win Stanley Cup with Game 6 shutout against Golden Knights")
        st.image(str(IMAGES_DIR / "n4.png"))
        st.write("McKenna signs entry-level contract with Maple Leafs ")
        st.image(str(IMAGES_DIR / "n5.png"))
        st.write("Carlsson gets offer sheet from Flyers; Ducks can match")

st.markdown('</div>', unsafe_allow_html=True)

with st.sidebar:
    st.title("Current Bankroll")
    st.metric(label="Current money", value=f"${st.session_state.bankroll:,.2f}")