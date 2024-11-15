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
    # Load the file using the original, working code logic
    df_bat_speed = pd.read_csv(bat_speed_file, skiprows=20)
    df_bat_speed.columns = df_bat_speed.columns.str.strip()

    # Original Bat Speed Metrics
    bat_speed_data = df_bat_speed["Bat Speed (mph)"]
    player_avg_bat_speed = bat_speed_data.mean()
    top_10_percent_bat_speed = bat_speed_data.quantile(0.90)
    top_10_percent_swings = df_bat_speed[bat_speed_data >= top_10_percent_bat_speed]

    # New Metric: Average Attack Angle for Top 10% Bat Speed Swings
    avg_attack_angle_top_10 = None
    if "Attack Angle" in df_bat_speed.columns:
        avg_attack_angle_top_10 = top_10_percent_swings["Attack Angle"].mean()

    # New Metric: Average Time to Contact
    avg_time_to_contact = None
    if "Time to Contact" in df_bat_speed.columns:
        avg_time_to_contact = df_bat_speed["Time to Contact"].mean()

    # Format Bat Speed Metrics
    bat_speed_benchmark = benchmarks[player_level]["Avg BatSpeed"]
    top_90_benchmark = benchmarks[player_level]["90th% BatSpeed"]
    bat_speed_metrics = (
        "### Bat Speed Metrics\n"
        f"- **Player Average Bat Speed:** {player_avg_bat_speed:.2f} mph (Benchmark: {bat_speed_benchmark} mph)\n"
        f"- **Top 10% Bat Speed:** {top_10_percent_bat_speed:.2f} mph (Benchmark: {top_90_benchmark} mph)\n"
    )
    if avg_attack_angle_top_10 is not None:
        bat_speed_metrics += f"- **Average Attack Angle (Top 10% Bat Speed Swings):** {avg_attack_angle_top_10:.2f}°\n"
    if avg_time_to_contact is not None:
        bat_speed_metrics += f"- **Average Time to Contact:** {avg_time_to_contact:.2f} seconds\n"

# Process Exit Velocity File
if exit_velocity_file:
    # Load the file using the original, working code logic
    df_exit_velocity = pd.read_csv(exit_velocity_file, skiprows=20)
    df_exit_velocity.columns = df_exit_velocity.columns.str.strip()

    # Original Exit Velocity Metrics
    exit_velocity_data = df_exit_velocity["Velo"]
    exit_velocity_avg = exit_velocity_data[exit_velocity_data > 0].mean()  # Ignore zero values
    top_8_percent_exit_velocity = exit_velocity_data.quantile(0.92)
    top_8_percent_swings = df_exit_velocity[exit_velocity_data >= top_8_percent_exit_velocity]

    # New Metric: Average Launch Angle for Top 8% Exit Velocity Swings
    avg_launch_angle_top_8 = None
    if "Launch Angle" in df_exit_velocity.columns:
        avg_launch_angle_top_8 = top_8_percent_swings["Launch Angle"].mean()

    # New Metric: Average Distance for Top 8% Exit Velocity Swings
    avg_distance_top_8 = None
    if "Distance" in df_exit_velocity.columns:
        avg_distance_top_8 = top_8_percent_swings["Distance"].mean()

    # Format Exit Velocity Metrics
    ev_benchmark = benchmarks[player_level]["Avg EV"]
    top_8_benchmark = benchmarks[player_level]["Top 8th EV"]
    exit_velocity_metrics = (
        "### Exit Velocity Metrics\n"
        f"- **Average Exit Velocity:** {exit_velocity_avg:.2f} mph (Benchmark: {ev_benchmark} mph)\n"
        f"- **Top 8% Exit Velocity:** {top_8_percent_exit_velocity:.2f} mph (Benchmark: {top_8_benchmark} mph)\n"
    )
    if avg_launch_angle_top_8 is not None:
        exit_velocity_metrics += f"- **Average Launch Angle (Top 8% Exit Velocity Swings):** {avg_launch_angle_top_8:.2f}°\n"
    if avg_distance_top_8 is not None:
        exit_velocity_metrics += f"- **Average Distance (Top 8% Exit Velocity Swings):** {avg_distance_top_8:.2f} ft\n"

# Display Results
st.write("## Calculated Metrics")
if bat_speed_metrics:
    st.markdown(bat_speed_metrics)
if exit_velocity_metrics:
    st.markdown(exit_velocity_metrics)

