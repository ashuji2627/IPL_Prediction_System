import streamlit as st
import pandas as pd
# import pickle
from PIL import Image
import base64
import matplotlib.pyplot as plt
import pickle
import time




# ========== Background Styling ==========
def set_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    page_bg = f"""
    <style>
    html, body {{
        max-width: 100%;
        overflow-x: hidden;
    }}

    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .block-container {{
        background-color: rgba(0, 0, 0, 0.75);
        border-radius: 15px;
        padding: 1.5rem;
        margin: auto;
        max-width: 95%;
    }}

    @media only screen and (max-width: 768px) {{
        .stSelectbox, .stNumberInput {{
            width: 100% !important;
        }}
    }}

    h1, h2, h3 {{
        color: #FFD700;
        text-align: center;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

# ========== Call Background ==========
set_bg_from_local("Background_Image.png")

# ========== Load Model ==========
try:
    with open("pipe.pkl", "rb") as file:
        pipe = pickle.load(file)
except Exception as e:
    st.error("❌ Model file not found or can't be loaded.")

teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
         'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
         'Rajasthan Royals', 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
          'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Sharjah', 'Mohali', 'Bengaluru']

# ========== Dark Mode Toggle ==========
st.sidebar.markdown("## ⚙️ Preferences")
dark_mode = st.sidebar.checkbox("🌙 Enable Dark Mode")

if dark_mode:
    st.markdown("""
    <style>
    .stApp {{ background-color: #1e1e1e; }}
    h1, h2, h3, label, .css-1v0mbdj, .css-ffhzg2 {{ color: #ffffff !important; }}
    .css-1v0mbdj:hover, .css-ffhzg2:hover {{ color: #ffd700 !important; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>\U0001F3CF IPL Prediction System</h1>", unsafe_allow_html=True)

# ========== Team Selection ==========
st.markdown("### \U0001F46D Select Teams and Venue")
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('Batting Team 🟢', sorted(teams))
    try:
        bat_logo = Image.open(f"team_logos/{batting_team}.png")
        st.image(bat_logo, width=100)
    except:
        st.info(f"Logo not found for {batting_team}")

with col2:
    bowling_team = st.selectbox('Bowling Team 🔴', sorted(teams))
    try:
        bowl_logo = Image.open(f"team_logos/{bowling_team}.png")
        st.image(bowl_logo, width=100)
    except:
        st.info(f"Logo not found for {bowling_team}")

selected_city = st.selectbox('📍 Host City', sorted(cities))

# ========== Match Inputs ==========
st.markdown("### \U0001F4CA Match Situation")
col3, col4 = st.columns(2)
with col3:
    target = st.number_input("🎯 Target Score", min_value=1)
    overs = st.number_input("🕒 Overs Completed", min_value=0.1, max_value=20.0, step=0.1)

with col4:
    score = st.number_input("📈 Current Score", min_value=0)
    wickets_out = st.number_input("💥 Wickets Out", min_value=0, max_value=10)

# ========== Prediction Button ==========
if st.button("🔮 Predict Probability"):
    if overs == 0 or (120 - overs * 6) <= 0:
        st.warning("⚠️ Invalid overs or balls left.")
    else:
        runs_left = target - score
        balls_left = 120 - (overs * 6)
        wickets = 10 - wickets_out
        crr = score / overs
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

        valid_teams = [
          'Sunrisers Hyderabad', 'Mumbai Indians',
          'Royal Challengers Bangalore', 'Kolkata Knight Riders',
          'Kings XI Punjab', 'Chennai Super Kings',
          'Rajasthan Royals', 'Delhi Capitals'
        ]

        valid_cities = [
           'Hyderabad', 'Pune', 'Rajkot', 'Indore', 'Bangalore', 'Mumbai',
           'Kolkata', 'Delhi', 'Chandigarh', 'Kanpur', 'Jaipur', 'Chennai',
           'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion', 'East London',
           'Johannesburg', 'Kimberley', 'Bloemfontein', 'Ahmedabad', 'Cuttack',
           'Nagpur', 'Dharamsala', 'Visakhapatnam', 'Raipur', 'Ranchi',
           'Abu Dhabi', 'Sharjah', 'Mohali', 'Bengaluru'
        ]



        # Example input fields
        batting_team = st.selectbox("Batting Team", valid_teams)
        bowling_team = st.selectbox("Bowling Team", [team for team in valid_teams if team != batting_team])
        city = st.selectbox("City", valid_cities)

        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [selected_city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [wickets],
            'total_runs_x': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        # st.write("Input Columns:", input_df.columns.tolist())
        # st.write(input_df)

        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]

        st.markdown("### 📈 Winning Probabilities")

        # Animated Bar
        progress_win = st.progress(0, text=f"{batting_team} Win Probability")
        progress_loss = st.progress(0, text=f"{bowling_team} Win Probability")
        for i in range(0, int(win*100)+1, 2):
            progress_win.progress(i / 100.0, text=f"{batting_team}: {i}%")
            time.sleep(0.01)
        for j in range(0, int(loss*100)+1, 2):
            progress_loss.progress(j / 100.0, text=f"{bowling_team}: {j}%")
            time.sleep(0.01)

        st.success(f"🟢 {batting_team} – {round(win*100)}%")
        st.error(f"🔴 {bowling_team} – {round(loss*100)}%")

        # Pie Chart
        labels = [batting_team, bowling_team]
        sizes = [win * 100, loss * 100]
        colors = ['#00cc96', '#EF553B']
        fig1, ax1 = plt.subplots(figsize=(4, 4))  # smaller pie chart
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax1.axis('equal')
        st.pyplot(fig1)

# ========== Footer ==========
st.markdown("""
<hr>
<p style='text-align:center; color:white; font-size:18px;'>
🔥 Teams: SRH • MI • RCB • KKR • KXIP • CSK • RR • DC
</p>
""", unsafe_allow_html=True)
