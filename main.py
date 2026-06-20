import streamlit as st
from app.dashboard import show_dashboard
from app.predictor import show_predictor

import os
import subprocess

model_path = os.path.join("model", "best_model.pkl")
if not os.path.exists(model_path):
    print("Training model...")
    subprocess.run(["python", "model/train.py"], check=True)

st.set_page_config(
    page_title= 'WC 2026 Analytics',
    page_icon= "⚽",
    layout='wide'
)

st.markdown("""
    <style>
        /* Make standings table full width and responsive */
        table {
            width: 100% !important;
            font-size: 1rem;
        }
        th, td {
            text-align: center !important;
            padding: 12px 8px !important;
            vertical-align: middle !important;
        }
        /* Left align the Club column */
        td:nth-child(2) {
            text-align: left !important;
        }
        /* Add subtle row hover effect */
        tbody tr:hover {
            background-color: rgba(255, 255, 255, 0.05);
        }
        /* Make flag images align properly */
        img {
            vertical-align: middle !important;
            margin-right: 8px !important;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title('⚽ WC 2026 Analytics')
page = st.sidebar.radio(
    'Navigate',  ['Live Dashboard', ' Match Predictor']
)

if page == 'Live Dashboard':
    show_dashboard()
else:
    show_predictor()