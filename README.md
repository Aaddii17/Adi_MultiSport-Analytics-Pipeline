# 🏏⚽ AdiSports: Unified Multi-Sport Analytics Pipeline

[![Live Demo](https://img.shields.io/badge/Live_Dashboard-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://adi-sports-247.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)]()

AdiSports is an end-to-end data engineering and analytics platform designed to bridge the gap between static historical archives and real-time live event tracking. The system features a decoupled, dual-module architecture that processes millions of rows of legacy cricket data while simultaneously managing live network streams for global football matches.

## 🚀 Key Features

* **Real-Time Football Center:** Tracks live global matches, daily schedules, and recent results via the LiveScore REST API.
* **Deep Historical Cricket Analytics:** Processes ball-by-ball Indian Premier League (IPL) data from 2008 through the 2026 season.
* **Dynamic On-the-Fly Aggregation:** Bypasses static summary tables by mathematically calculating match winners, Orange Caps, Purple Caps, and MVP awards directly from delivery-level transactional data.
* **Fault-Tolerant API Routing:** Implements strict Time-to-Live (TTL) memory caching (`@st.cache_data`) and dynamic JSON parsing to mitigate HTTP 429 rate limits.
* **Global Standardization Layer:** Automatically resolves severe schema mismatches and standardizes legacy team franchises.

## 🛠️ Technology Stack

* **Language:** Python
* **Data Processing & ETL:** Pandas, Apache Parquet
* **Frontend UI:** Streamlit
* **Data Visualization:** Plotly Express
* **API Integration:** Requests, LiveScore API (via RapidAPI)

## 👨‍💻 Developers

This platform was developed as an In-House Practical Training (NTCC) project for the Bachelor of Technology in Computer Science and Engineering (Data Science) degree at Amity University, Noida.

* **Aditya Singh Tanwar**
* **Taavish Mehra**
