import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email Configuration
email_address = "aadichadha@gmail.com"
email_password = "eeoi odag olix nnfc"  # Your app-specific password
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Title and File Upload
st.title("Baseball Metrics Analyzer")
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

# Function to send an email
def send_email(recipient_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(email_address, email_password)
            server.send_message(msg)
            st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

if uploaded_file:
    # Load the data
    df = pd.read_csv(uploaded_file)

    # Check for necessary columns
    has_bat_speed = "Bat Speed (mph)" in df.columns
    has_exit_velocity = "Velo" in df.columns

    report_body = "<h2>Baseball Metrics Report</h2>"

    if has_bat_speed:
        # Average Bat Speed
        player_avg_bat_speed = df["Bat Speed (mph)"].mean()

        # Top 10% Bat Speed and related metrics
        top_10_percent_bat_speed = df["Bat Speed (mph)"].quantile(0.90)
        top_10_percent_swings = df[df["Bat Speed (mph)"] >= top_10_percent_bat_speed]

        # Average Attack Angle on Top 10% Bat Speed Swings
        if "Attack Angle" in df.columns and not top_10_percent_swings.empty:
            avg_attack_angle_top_10 = top_10_percent_swings["Attack Angle"].mean()
            report_body += f"<p>Average Attack Angle (Top 10% Bat Speed Swings): {avg_attack_angle_top_10:.2f}°</p>"
        else:
            report_body += "<p><em>Not enough data to calculate average attack angle for top 10% bat speed swings.</em></p>"

        # Average Time to Contact
        if "Time to Contact" in df.columns:
            avg_time_to_contact = df["Time to Contact"].mean()
            report_body += f"<p>Average Time to Contact: {avg_time_to_contact:.2f} seconds</p>"
        else:
            report_body += "<p><em>Time to Contact data is not available.</em></p>"

        report_body += f"<p>Player Average Bat Speed: {player_avg_bat_speed:.2f} mph</p>"
        report_body += f"<p>Top 10% Bat Speed: {top_10_percent_bat_speed:.2f} mph</p>"

    if has_exit_velocity:
        # Average Exit Velocity
        player_avg_exit_velocity = df["Velo"][df["Velo"] > 0].mean()  # Ignore zero values

        # Top 8% Exit Velocity and related metrics
        top_8_percent_exit_velocity = df["Velo"].quantile(0.92)
        top_8_percent_swings = df[df["Velo"] >= top_8_percent_exit_velocity]

        # Average Launch Angle on Top 8% Exit Velocity Swings
        if "Launch Angle" in df.columns and not top_8_percent_swings.empty:
            avg_launch_angle_top_8 = top_8_percent_swings["Launch Angle"].mean()
            report_body += f"<p>Average Launch Angle (Top 8% Exit Velocity Swings): {avg_launch_angle_top_8:.2f}°</p>"
        else:
            report_body += "<p><em>Launch Angle data is not available for top 8% exit velocity swings.</em></p>"

        # Average Distance on Top 8% Exit Velocity Swings
        if "Distance" in df.columns and not top_8_percent_swings.empty:
            avg_distance_top_8 = top_8_percent_swings["Distance"].mean()
            report_body += f"<p>Average Distance (Top 8% Exit Velocity Swings): {avg_distance_top_8:.2f} ft</p>"
        else:
            report_body += "<p><em>Distance data is not available for top 8% exit velocity swings.</em></p>"

        report_body += f"<p>Player Average Exit Velocity: {player_avg_exit_velocity:.2f} mph</p>"
        report_body += f"<p>Top 8% Exit Velocity: {top_8_percent_exit_velocity:.2f} mph</p>"

    # Display the report
    st.write("### Metrics Report")
    st.markdown(report_body, unsafe_allow_html=True)

    # Option to email the report
    st.write("### Email the Report")
    recipient_email = st.text_input("Enter the recipient's email address:")
    if st.button("Send Report"):
        if recipient_email:
            send_email(recipient_email, "Baseball Metrics Report", report_body)
        else:
            st.error("Please enter a valid email address.")
