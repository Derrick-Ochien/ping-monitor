# Ping Monitor

This Python script pings multiple network addresses associated with different departments and visualizes the results using Matplotlib.

## Setup

1. Clone this repository to your local machine.
2. Ensure you have Python installed.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Modify the `config.json` file to add or remove departments and their corresponding IP addresses.
5. Run the script using `python ping_monitor.py`.

## Configuration (config.json)

```json
{
    "departments": {
        "COUNTY COMMISSIONER (MANAGEMENT VLAN 10)": "10.62.0.1",
        "TREASURY (MANAGEMENT VLAN 10)": "10.62.0.33",
        "CRD (MANAGEMENT VLAN 10)": "10.62.0.41",
        "EDUCATION (MANAGEMENT VLAN 10)": "10.62.0.49",
        "HOSPITAL (MANAGEMENT VLAN 10)": "10.62.0.73",
        "TOM MBOYA UNIVERSITY (MANAGEMENT VLAN 10)": "10.62.0.97",
        "COUNTY ASSEMBLY (MANAGEMENT VLAN 10)": "10.62.0.121",
        "PROBATION (MANAGEMENT VLAN 10)": "10.62.0.89",
        "KNA (MANAGEMENT VLAN 10)": "10.62.0.113"
    }
}
