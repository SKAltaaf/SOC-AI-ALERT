       
import streamlit as st
from datetime import datetime
import requests
import json

st.set_page_config(
    page_title="AI SOC Alert Triage Assistant",
    page_icon="🛡️",
    layout="wide"
)

# Demo security alerts
alerts = {
    "ALT-001 — Repeated Failed Logins": {
        "type": "Authentication",
        "severity": "High",
        "target": "analyst01",
        "source_ip": "192.0.2.45",
        "failed_attempts": 18,
        "description": "Multiple failed login attempts against one account.",
        "evidence": [
            "18 failed login attempts",
            "Target account: analyst01",
            "Source IP: 192.0.2.45",
            "Successful login after failures: Unknown"
        ],
        "recommendations": [
            "Review authentication logs and event timestamps.",
            "Check whether a successful login followed the failures.",
            "Determine whether other accounts were targeted.",
            "Verify the activity with the account owner."
        ]
    },
    "ALT-002 — Unusual Login Time": {
        "type": "Authentication",
        "severity": "Medium",
        "target": "finance_user",
        "source_ip": "198.51.100.24",
        "failed_attempts": 3,
        "description": "A login occurred at an unusual time.",
        "evidence": [
            "Login time: 02:15 UTC",
            "Target account: finance_user",
            "Three associated failed attempts in this simulation",
            "User's normal schedule: Unknown"
        ],
        "recommendations": [
            "Verify the user's normal working hours and timezone.",
            "Confirm whether the user recognizes the login.",
            "Review surrounding authentication events.",
            "Look for other unusual account activity."
        ]
    },
    "ALT-003 — Suspicious Process": {
        "type": "Endpoint",
        "severity": "Critical",
        "target": "WORKSTATION-07",
        "source_ip": "203.0.113.17",
        "failed_attempts": 0,
        "description": "An endpoint reported an unusual process.",
        "evidence": [
            "Endpoint: WORKSTATION-07",
            "Process reputation: Unknown",
            "Parent process: Not supplied",
            "File hash: Not supplied"
        ],
        "recommendations": [
            "Collect the process name, path and command line.",
            "Review the parent process and process ancestry.",
            "Check the file hash using trusted security tools.",
            "Review related endpoint and network events."
        ]
    }
}

st.title("🛡️ AI-Powered SOC Alert Triage Assistant")
st.caption("Cybersecurity portfolio project | Simulated data only")

# Summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Alerts", len(alerts))
col2.metric("High / Critical", sum(
    1 for alert in alerts.values()
    if alert["severity"] in ["High", "Critical"]
))
col3.metric("Data Source", "Demo")

st.subheader("Alert Severity Overview")

severity_counts = {
    severity: sum(
        1 for item in alerts.values()
        if item["severity"] == severity
    )
    for severity in ["Critical", "High", "Medium", "Low"]
}

st.bar_chart(severity_counts)


st.divider()


# Filter alerts by severity
severity_filter = st.selectbox(
    "Filter by Severity",
    ["All", "Critical", "High", "Medium", "Low"]
)

filtered_alerts = {
    name: details
    for name, details in alerts.items()
    if severity_filter == "All"
    or details["severity"] == severity_filter
}

if not filtered_alerts:
    st.warning("No alerts match this severity.")
    st.stop()

selected = st.selectbox(
    "Select an alert",
    list(filtered_alerts.keys())
)
alert = filtered_alerts[selected]


# Alert details
st.subheader("Alert Details")



status_key = f"status_{selected}"

if status_key not in st.session_state:
    st.session_state[status_key] = "New"

alert_status = st.selectbox(
    "Investigation Status",
    ["New", "Investigating", "Closed"],
    key=status_key
)

st.caption("Investigation status is retained for this Streamlit session.")



st.caption(
    "Demo status only — it is not saved to a database "
    "and may reset when the app session restarts."
)

left, right = st.columns(2)

with left:
    st.write("**Alert ID:**", selected.split(" — ")[0])
    st.write("**Alert type:**", alert["type"])
    st.write("**Severity:**", alert["severity"])
    st.write("**Target:**", alert["target"])

with right:
    st.write("**Source IP:**", alert["source_ip"])
    st.write("**Failed login attempts:**", alert["failed_attempts"])
    st.write("**Description:**", alert["description"])

st.subheader("Observed Evidence")
for item in alert["evidence"]:
    st.write(f"- {item}")

st.divider()

# Triage panel
st.header("🤖 AI-Assisted Alert Triage")
st.caption(
    "AI-powered triage uses the local Qwen3 4B model via Ollama. "
    "Alerts are simulated; live Splunk integration is not enabled."
)


if st.button("Analyze Selected Alert", type="primary"):
    st.subheader("AI-Generated Alert Assessment")

    with st.spinner("Qwen3 is analyzing the alert..."):
        try:
            prompt = f"""
You are a cautious SOC analyst assisting a human security analyst.

Analyze this simulated security alert using only the evidence provided.
Do not invent facts or claim that an attack is confirmed.
Distinguish observed evidence from possible explanations.
Do not recommend automatically blocking or disabling accounts.

Alert ID: {selected.split(" - ")[0]}
Alert type: {alert["type"]}
Severity: {alert["severity"]}
Target: {alert["target"]}
Source IP: {alert["source_ip"]}
Failed login attempts: {alert["failed_attempts"]}
Description: {alert["description"]}
Observed evidence: {json.dumps(alert["evidence"])}
Existing recommendations: {json.dumps(alert["recommendations"])}

Return these sections:
1. Summary
2. Risk assessment and reasoning
3. Evidence and uncertainty
4. Recommended investigation steps
5. What additional evidence is needed

Keep the answer practical and concise.
"""

            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "qwen3:4b",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "stream": False
                },
                timeout=180
            )

            response.raise_for_status()
            result = response.json()["message"]["content"]

            st.markdown(result)
             
            report = f"""SOC ALERT TRIAGE REPORT
=======================

Alert: {selected}
Type: {alert["type"]}
Severity in source alert: {alert["severity"]}
Target: {alert["target"]}
Source IP: {alert["source_ip"]}
Failed login attempts: {alert["failed_attempts"]}

OBSERVED EVIDENCE
{chr(10).join("- " + item for item in alert["evidence"])}

AI-GENERATED ASSESSMENT
{result}

EXISTING INVESTIGATION RECOMMENDATIONS
{chr(10).join("- " + step for step in alert["recommendations"])}

LIMITATIONS
This report uses simulated alert data and locally generated AI analysis.
Validate all findings against actual logs before taking action.
"""

            st.download_button(
                label="Download Incident Report",
                data=report,
                file_name=f"{selected.split(' - ')[0]}_triage_report.txt",
                mime="text/plain"
            )

            st.caption(
                "Generated locally using Qwen3 4B via Ollama. "
                "This is a simulated alert; verify findings before acting."
            )

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to Ollama. Open Ollama on your Mac "
                "and verify that the local model is available."
            )

        except requests.exceptions.Timeout:
            st.error(
                "The AI took too long to respond. Try again."
            )

        except (requests.exceptions.RequestException, KeyError, ValueError) as error:
            st.error(f"AI analysis failed: {error}")

    st.subheader("Recommended Investigation")
    for step in alert["recommendations"]:
        st.write(f"- {step}")

    st.warning(
        "Do not declare an incident based only on this demo assessment. "
        "Validate the evidence and follow your incident response process."
    )

# Project status
st.divider()
with st.expander("Project Scope and Limitations"):
    st.write("- All alerts are simulated examples.")
    st.write("- No real security logs are ingested.")
    st.write("- Local AI integration is enabled through Ollama (Qwen3 4B).")
    st.write("- Splunk integration is not enabled.")
    st.write("- No automated response actions are performed.")
