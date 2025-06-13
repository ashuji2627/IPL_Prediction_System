# 🏏 IPL Prediction System

An interactive and intelligent web application that predicts the winning probability of an ongoing IPL match using real-time match stats. Built with **Streamlit** and a **machine learning pipeline**, this project combines data science and engaging UI to bring an immersive experience for cricket enthusiasts.

<!--![Screenshot](screenshots/ipl_ui.png)  Replace with actual path in your repo -->

---

## 🚀 Features

- 🎯 Real-time win probability prediction using machine learning
- ⚡ Animated probability bars and pie chart visualization
- 🧢 Team logo integration
- 🏟️ Venue-based dynamics
- 🖼️ Custom IPL-themed background
- 🌙 Light/Dark mode toggle for personalized appearance
- 🖥️ Responsive and user-friendly interface

---

## 📊 Prediction Factors (Modules)

This application relies on multiple **real-time match features** to predict the outcome using a trained ML model:

| **Factor**               | **Description** |
|--------------------------|-----------------|
| 🏏 **Batting Team**       | Team currently batting. |
| 🆚 **Bowling Team**       | Team currently bowling. |
| 📍 **Host City**          | Venue affects conditions and team performance. |
| 🎯 **Target Score**       | Total runs to chase in the innings. |
| ⚾ **Current Score**       | Runs scored by the batting team so far. |
| ⏱️ **Overs Completed**    | Number of overs completed. |
| ❌ **Wickets Fallen**     | Wickets lost so far. |
| 🔢 **Runs Left**          | Target - Current Score. |
| 🎯 **Balls Left**         | Total balls remaining in the innings (120 - overs × 6). |
| 📈 **Current Run Rate (CRR)** | Runs per over so far (Score ÷ Overs). |
| 📉 **Required Run Rate (RRR)** | Runs required per over ((Runs Left × 6) ÷ Balls Left). |

These parameters are fed into a trained pipeline model (`pipe.pkl`) which outputs the **win probabilities** for both teams.

---
## 📚 Technologies Used

- **Frontend & UI**: Streamlit + Custom CSS
- **Backend Logic**: Python & scikit-learn
- **Model File**: Trained ML Pipeline (`pipe.pkl`)
- **Visualization**: Matplotlib
- **Assets**: PIL for image handling, base64 for background encoding


