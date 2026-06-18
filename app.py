import os
import pandas as pd
import streamlit as st

from analyzer import detect_outliers, find_strong_correlations
from insights import generate_insights
from report_generator import create_report
from visualizer import create_histograms, create_boxplots, create_scatter_plot

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AutoViz Dashboard", layout="wide")

os.makedirs("generated_charts", exist_ok=True)
# ---------------- UI STYLE ----------------
# ---------------- UI STYLE ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(
        135deg,
        #ff9966,
        #ff5e62
    );
}

/* Main Title */
h1 {
    color: white !important;
    text-align: center;
    font-weight: bold;
}

/* Headings */
h2, h3 {
    color: white !important;
}

/* Metric Cards */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.15);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

/* Buttons */
.stButton > button {
    background: white;
    color: #ff5e62 !important;
    border-radius: 12px;
    border: none;
    font-weight: bold;
    width: 100%;
    height: 45px;
}

.stButton > button:hover {
    background: #fff3f3;
    transition: 0.3s;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.12);
}

</style>
""", unsafe_allow_html=True)

st.title("🌅 AutoViz Analytics Dashboard")

st.markdown(
    """
    <div style='text-align:center;
                color:white;
                font-size:18px;
                margin-bottom:20px;'>
        Automated Data Analysis • Visualizations • Insights • PDF Reporting
    </div>
    """,
    unsafe_allow_html=True
)
# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio(
    "📌 Navigation",
    ["Upload Data", "EDA Summary", "Visualizations", "Insights", "Report"]
)

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    rows, cols = df.shape
    missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()

    correlations = find_strong_correlations(df)
    outliers = detect_outliers(df)
    insights = generate_insights(df, correlations, outliers)

    # ---------------- UPLOAD TAB ----------------
    if menu == "Upload Data":

        st.subheader("📁 Dataset Preview")
        st.dataframe(df.head())

    # ---------------- EDA SUMMARY ----------------
    elif menu == "EDA Summary":

        st.subheader("📊 Dataset Overview")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rows", rows)
        col2.metric("Columns", cols)
        col3.metric("Missing Values", missing)
        col4.metric("Duplicates", duplicates)

        st.subheader("📌 Data Types")
        st.write(df.dtypes)

        st.subheader("📈 Statistical Summary")
        st.dataframe(df.describe())

    # ---------------- VISUALIZATIONS ----------------
    elif menu == "Visualizations":

        st.subheader("📊 Histograms")

        if st.button("Generate Histograms"):
            create_histograms(df)
            for file in os.listdir("generated_charts"):
                if file.endswith("_hist.png"):
                    st.image(f"generated_charts/{file}")

        st.subheader("📦 Boxplots")

        if st.button("Generate Boxplots"):
            create_boxplots(df)
            for file in os.listdir("generated_charts"):
                if file.endswith("_box.png"):
                    st.image(f"generated_charts/{file}")

        st.subheader("📉 Scatter Plot")

        numeric_cols = df.select_dtypes(include="number").columns

        if len(numeric_cols) >= 2:

            x_axis = st.selectbox("X Axis", numeric_cols)
            y_axis = st.selectbox("Y Axis", numeric_cols, index=1)

            if st.button("Generate Scatter Plot"):
                create_scatter_plot(df, x_axis, y_axis)
                st.image("generated_charts/scatter.png")

    # ---------------- INSIGHTS ----------------
    elif menu == "Insights":

        st.subheader("🧠 Key Insights")

        if insights:
            for i in insights:
                st.success(i)
        else:
            st.info("No insights available.")

        st.subheader("🔗 Strong Correlations")

        if correlations:
            for c1, c2, val in correlations:
                st.write(f"🔗 {c1} ↔ {c2} = {val}")
        else:
            st.write("No strong correlations found.")

        st.subheader("🚨 Outliers")

        if outliers:
            for o in outliers:
                st.warning(o)
        else:
            st.write("No significant outliers found.")

    # ---------------- REPORT ----------------
    elif menu == "Report":

        st.subheader("📄 Generate PDF Report")

        summary = {
            "Rows": rows,
            "Columns": cols,
            "Missing Values": missing,
            "Duplicate Rows": duplicates
        }

        if st.button("Generate Report"):

            pdf_file = create_report(
                summary,
                correlations,
                outliers,
                insights
            )

            st.success("Report Generated!")

            with open(pdf_file, "rb") as f:
                st.download_button(
                    "⬇ Download PDF Report",
                    f,
                    file_name="AutoViz_Report.pdf",
                    mime="application/pdf"
                )

    # ---------------- CSV DOWNLOAD ----------------
    st.sidebar.subheader("⬇ Download Data")

    csv = df.to_csv(index=False)

    st.sidebar.download_button(
        "Download CSV",
        csv,
        "dataset.csv",
        "text/csv"
    )

else:
    st.info("📤 Please upload a CSV file to start analysis.")
    st.markdown("---")
st.markdown(
    """
    <div style='text-align:center; color:lightgray;'>
        🚀 AutoViz Analytics Dashboard | Built with Python, Pandas & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)