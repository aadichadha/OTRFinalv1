import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Title and Introduction
st.title("Baseball Metrics Analyzer")
st.write("Upload your Bat Speed and Exit Velocity CSV files to generate a comprehensive report.")

# File Uploads
bat_speed_file = st.file_uploader("Upload Bat Speed (mph) File", type="csv")
exit_velocity_file = st.file_uploader("Upload Exit Velocity File", type="csv")

# Ask for Player Level
player_level = st.selectbox("Select Player Level", ["Youth", "High School", "College", "Indy", "Affiliate", "Professional"])

# Benchmarks Based on Level
benchmarks = {
    "Youth": {"Avg EV": 58.4, "Top 8th EV": 70.19, "Avg BatSpeed": 49.21, "90th% BatSpeed": 52.81},
    "High School": {"Avg EV": 74.54, "Top 8th EV": 86.75, "Avg BatSpeed": 62.64, "90th% BatSpeed": 67.02},
    "College": {"Avg EV": 81.57, "Top 8th EV": 94.44, "Avg BatSpeed": 67.53, "90th% BatSpeed": 72.54},
    "Indy": {"Avg EV": 85.99, "Top 8th EV": 98.12, "Avg BatSpeed": 69.2, "90th% BatSpeed": 74.04},
    "Affiliate": {"Avg EV": 85.49, "Top 8th EV": 98.71, "Avg BatSpeed": 70.17, "90th% BatSpeed": 75.14},
    "Professional": {"Avg EV": 94.3, "Top 8th EV": 104.5, "Avg BatSpeed": 78.2, "90th% BatSpeed": 82.3}
}

# Initialize Metrics
bat_speed_metrics = ""
exit_velocity_metrics = ""

# Process Bat Speed File
if bat_speed_file:
    df_bat_speed = pd.read_csv(bat_speed_file, skiprows=20)
    df_bat_speed.columns = df_bat_speed.columns.str.strip()
    bat_speed_data = df_bat_speed.iloc[:, 7]

    # Calculate Bat Speed Metrics
    bat_speed_avg = bat_speed_data.mean()
    bat_speed_top_10 = bat_speed_data.quantile(0.90)
    bat_speed_benchmark = benchmarks[player_level]["Avg BatSpeed"]
    top_10_benchmark = benchmarks[player_level]["90th% BatSpeed"]
    bat_speed_metrics = (
        "### Bat Speed (mph) Metrics\n"
        f"- **Average Bat Speed:** {bat_speed_avg:.2f} mph (Benchmark: {bat_speed_benchmark} mph)\n"
        f"- **Top 10% Bat Speed:** {bat_speed_top_10:.2f} mph (Benchmark: {top_10_benchmark} mph)"
    )

# Process Exit Velocity File
if exit_velocity_file:
    df_exit_velocity = pd.read_csv(exit_velocity_file, skiprows=20)
    df_exit_velocity.columns = df_exit_velocity.columns.str.strip()
    exit_velocity_data = df_exit_velocity.iloc[:, 7]

    # Filter out zero values
    exit_velocity_data = exit_velocity_data[exit_velocity_data > 0]

    # Calculate Exit Velocity Metrics
    exit_velocity_avg = exit_velocity_data.mean()
    exit_velocity_top_8 = exit_velocity_data.quantile(0.92)
    ev_benchmark = benchmarks[player_level]["Avg EV"]
    top_8_benchmark = benchmarks[player_level]["Top 8th EV"]
    exit_velocity_metrics = (
        "### Exit Velocity Metrics\n"
        f"- **Average Exit Velocity:** {exit_velocity_avg:.2f} mph (Benchmark: {ev_benchmark} mph)\n"
        f"- **Top 8% Exit Velocity:** {exit_velocity_top_8:.2f} mph (Benchmark: {top_8_benchmark} mph)"
    )

# Display Results
st.write("## Calculated Metrics")
if exit_velocity_metrics:
    st.markdown(exit_velocity_metrics)
if bat_speed_metrics:
    st.markdown(bat_speed_metrics)

# Email Configuration
email_address = "aadichadha@gmail.com"
email_password = "eeoi odag olix nnfc"  # Your app-specific password
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Option to Email the Report
st.write("## Email the Report")
recipient_email = st.text_input("Enter Email Address")
if st.button("Send Report"):
    if recipient_email:
        # Combine the reports for both files
        report = f"{exit_velocity_metrics}\n\n{bat_speed_metrics}"
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = recipient_email
        msg['Subject'] = "Baseball Metrics Report"
        msg.attach(MIMEText(report, 'plain'))

        # Send the email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_address, email_password)
                server.send_message(msg)
            st.success("Report sent successfully!")
        except Exception as e:
            st.error(f"Failed to send email: {e}")
    else:
        st.error("Please enter a valid email address.")
