import streamlit as st
import os
import pandas as pd   
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import matplotlib.font_manager as fm
import sys


st.set_page_config(

    page_title="The Hockey Telegraph",

    layout="wide"

)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

font_path ="static/Monocraft.ttf" 
fm.fontManager.addfont(font_path)
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rcParams['font.family'] = font_name
plt.rcParams['axes.unicode_minus'] = False
##WIN loss calc:
connection = sqlite3.connect('data/bets.db')
conn = connection.cursor()
bet_q = """ SELECT team_bet_on , winner
            FROM BETS

"""
parlay_q = """SELECT WON
            FROM PARLAY

"""

bet_df = pd.read_sql_query(bet_q,connection)
parlay_df = pd.read_sql(parlay_q,connection)
won,lost = 0,0
for idx,row in enumerate(bet_df.itertuples()):
    if row.winner == row.team_bet_on:
        won+=1
    else:
        lost+=1
for idx,row in enumerate(parlay_df.itertuples()):
    if row.WON == True:
        won +=1
    else:
        lost +=1
##############################
path = r"data/bankroll.txt"
if not os.path.exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("1000.0")
path2 = r"data\log_roll.txt"
if not os.path.exists(path):
    os.makedirs(os.path.dirname(path) , exist_ok=True)
    with open(path,"w") as f:
        f.write(st.session_state.bankroll)


st.markdown(

    """

    <style>

    @font-face {

        font-family: 'CanterburyFont';

        src: url('app/static/Canterbury.ttf') format('truetype');

        font-weight: normal;

        font-style: normal;

    }

    @font-face {

        font-family: 'basker-bold';

        src: url('app/static/Baskervville-Bold.ttf') format('truetype');

        font-weight: normal;

        font-style: normal;

    }

    section.stMain .block-container {

        padding-top: 1rem;

    }

    </style>

    """,

    unsafe_allow_html=True

)

st.markdown('<hr>',unsafe_allow_html=True)
right,center,left = st.columns([2,6,2],border=True)
with center:
    st.markdown('<h1 style="text-align: center; padding-top: 30px; font-family: \'CanterburyFont\', serif; font-size: 4rem;">The Tribune</h1>', unsafe_allow_html=True)
    r,c,l,m,n = st.columns([4,4,4,5,4])
    with l:
        st.image(r"images\nhl_logo.png",width=200)
with left:
    st.markdown('<h3 style="font-family:\'basker-bold\',serif;">&emsp;LATE CITY&emsp;&ensp;EDITION</h3><p>FIVE CENTS In Manhattan,<br>Brooklyn and The Bronx <br>| TEN CENTS Elsewhere</p>',unsafe_allow_html=True)
with right:
    st.markdown('<h5>WEATHER<h5><p style="font-size:15px;">Today: Fair , Moderate winds</p><p style="font-size:15px;">Tomorrow : Clear Expected<h6>Vol. LXXXVII No. 29,407 | (Copyright, 1927, New York Tribune Inc.)</h6>',unsafe_allow_html=True)

cols = st.columns(41)
for i in range(41):
    with cols[i]:
        img_path = rf"images\NHL Logos\image ({i + 1}).png"
        st.image(img_path,width=80)
    
st.markdown('<hr>',unsafe_allow_html=True)    
r1,c1,l1 = st.columns([3,3,3])

with c1:
    st.markdown('<h4 style="text-align: center; padding-top: 5px; font-family: \'basker-bold\', serif;">"God Bless America"</h4>', unsafe_allow_html=True)
with l1:
    r2,c2,l2 = st.columns([6,6,5])
    with l2:
        st.image(r"images\canon2.png",width=100)
with r1:
    st.image(r"images\canon1.png",width = 100)
st.markdown('<h6 style="text-align: center; padding-top: 10px;">Vol. I • June 2026</h6>', unsafe_allow_html=True)


main, sidebar = st.columns([7, 3],border=True)


with main:
    with st.container(height=1000):
        fig,ax = plt.subplots()
        fig.patch.set_facecolor('#F5F1E8')
        ax.set_facecolor('#F5F1E8')
        with open(path2,"r") as r:
            lines = r.read().splitlines()
            lines = [float(val) for val in lines if val]
        
            
        x_vals = list(range(1,len(lines)+1))
        ax.plot(x_vals,lines,'-o',color='green',linewidth=2)
        ax.grid(True)
        ax.set_title("Bankroll History")
        st.pyplot(fig)
            
        fig1,ax1 = plt.subplots()
        fig1.patch.set_facecolor('#F5F1E8')
        ax1.set_facecolor('#F5F1E8')
        
        labels = ['Won','Lost']
        sizes = [won,lost]
        explode = [0.1,0]
        colors = ['#1f77b4', '#ff7f0e']
        plt.pie(
            sizes,
            explode=explode,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            shadow=True,
            startangle=140
        )
        ax1.set_title("Win-Loss Ratio")
        ax1.axis('equal')
        st.pyplot(fig1)
        ##
        lines_np = np.array(lines)
        profit_np = np.diff(lines_np)
        cum_sum = np.cumsum(profit_np)
        roi = (cum_sum/1000)*100
        fig2,ax2 = plt.subplots()
        fig2.patch.set_color('#F5F1E8')
        ax2.set_facecolor('#F5F1E8')
        ax2.plot(x_vals[:-1],roi,'-o',linewidth=2)
        ax2.axhline(0, color='green', linestyle='--', linewidth=1.5, alpha=0.7)
        ax2.grid(2)
        ax2.set_title("ROI Chart")
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
        st.image(r"images\n1.png")
        st.write("Staal scores 2, Hurricanes top Golden Knights in Game 4, even Stanley Cup Final")
        st.image(r"images\n2.png")
        st.write("Hertl breaks tie late, Golden Knights edge Hurricanes in Game 1 of Cup Final")
        st.image(r"images\n3.png")
        st.write("Hurricanes win Stanley Cup with Game 6 shutout against Golden Knights")
        st.image(r"images\n4.png")
        st.write("McKenna signs entry-level contract with Maple Leafs ")
        st.image(r"images\n5.png")
        st.write("Carlsson gets offer sheet from Flyers; Ducks can match")
        
if 'bankroll' not in st.session_state:
    with open(path,"r") as w:
        st.session_state.bankroll = float(w.read().strip())
    
with st.sidebar:
    st.title("Current Bankroll")
    st.metric(label="Current money",value=f"${st.session_state.bankroll:,.2f}")