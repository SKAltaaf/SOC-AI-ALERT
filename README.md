# AI-Powered SOC Alert Triage Assistant

A cybersecurity portfolio project that uses a locally running large language model to assist with Security Operations Center (SOC) alert triage.

## Overview

The application provides a Streamlit dashboard for reviewing simulated security alerts. It sends the selected alert's evidence to a local Qwen3 4B model through Ollama and displays an AI-generated assessment to support human investigation.

## Features

- Interactive dashboard with simulated security alerts
- Alert severity filtering
- Alert evidence and details
- Local AI-assisted alert analysis using Ollama and Qwen3 4B
- Risk reasoning, uncertainties, and recommended investigation steps
- Investigation status tracking during the current app session
- Downloadable text-based triage reports

## Technology Stack

- Python
- Streamlit
- Ollama
- Qwen3 4B
- Requests

## Requirements

- Python
- Ollama installed and running
- The `qwen3:4b` model downloaded locally

## Run Locally

1. Clone this repository:

   ```bash
   git clone https://github.com/SKAltaaf/SOC-AI-ALERT.git
   cd SOC-AI-ALERT
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start Ollama and download the model if needed:

   ```bash
   ollama pull qwen3:4b
   ```

5. Run the dashboard:

   ```bash
   python -m streamlit run app.py
   ```

6. Open the local URL displayed in the terminal.

## Limitations

- All alert data is simulated.
- AI assessments may be inaccurate and require human verification.
- Live Splunk integration is not implemented.
- Investigation status is not persisted to a database.
- The application does not automatically block accounts or perform response actions.

## Future Improvements

- Integrate with Splunk or another SIEM
- Add real log ingestion and parsing
- Improve alert prioritization and evidence correlation
- Add persistent investigation records
- Expand testing and error handling

## Disclaimer

This project is intended for educational and portfolio demonstration purposes. Validate all AI-generated findings against reliable security evidence before taking action.
