import streamlit as st
import os


path = r"C:\Users\pytho\Documents\nhl\project\data\bankroll.txt"
if not os.path.exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("1000.0")

st.set_page_config(

    page_title="The Hockey Telegraph",

    layout="wide"

)



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
        st.image(r"C:\Users\pytho\Documents\nhl\project\images\nhl_logo.png",width=200)
with left:
    st.markdown('<h3 style="font-family:\'basker-bold\',serif;">&emsp;LATE CITY&emsp;&ensp;EDITION</h3><p>FIVE CENTS In Manhattan,<br>Brooklyn and The Bronx <br>| TEN CENTS Elsewhere</p>',unsafe_allow_html=True)
with right:
    st.markdown('<h5>WEATHER<h5><p style="font-size:15px;">Today: Fair , Moderate winds</p><p style="font-size:15px;">Tomorrow : Clear Expected<h6>Vol. LXXXVII No. 29,407 | (Copyright, 1927, New York Tribune Inc.)</h6>',unsafe_allow_html=True)

cols = st.columns(41)
for i in range(41):
    with cols[i]:
        img_path = rf"C:\Users\pytho\Documents\nhl\project\images\NHL Logos\image ({i + 1}).png"
        st.image(img_path,width=80)
    
st.markdown('<hr>',unsafe_allow_html=True)    
r1,c1,l1 = st.columns([3,3,3])

with c1:
    st.markdown('<h4 style="text-align: center; padding-top: 5px; font-family: \'basker-bold\', serif;">"God Bless America"</h4>', unsafe_allow_html=True)
with l1:
    r2,c2,l2 = st.columns([6,6,5])
    with l2:
        st.image(r"C:\Users\pytho\Documents\nhl\project\images\canon2.png",width=100)
with r1:
    st.image(r"C:\Users\pytho\Documents\nhl\project\images\canon1.png",width = 100)
st.markdown('<h6 style="text-align: center; padding-top: 10px;">Vol. I • June 2026</h6>', unsafe_allow_html=True)


main, sidebar = st.columns([7, 3],border=True)


with main:

    st.write("Main article")


with sidebar:

    st.image(r"C:\Users\pytho\Documents\nhl\project\images\n1.png")
    st.write("Staal scores 2, Hurricanes top Golden Knights in Game 4, even Stanley Cup Final")
    st.image(r"C:\Users\pytho\Documents\nhl\project\images\n2.png")
    st.write("Hertl breaks tie late, Golden Knights edge Hurricanes in Game 1 of Cup Final")
    st.image(r"C:\Users\pytho\Documents\nhl\project\images\n3.png")
    st.write("Hurricanes win Stanley Cup with Game 6 shutout against Golden Knights")
if 'bankroll' not in st.session_state:
    with open(path,"r") as w:
        st.session_state.bankroll = float(w.read().strip())
    
with st.sidebar:
    st.title("Current Bankroll")
    st.metric(label="Current money",value=f"${st.session_state.bankroll:,.2f}")