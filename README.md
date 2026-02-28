# tapo-fastapi

Small FastAPI service to turn Tapo P110 devices on/off using a local `devices.json` file.

Prerequisites

- Python 3.10+ (use your venv)
- `USERNAME` and `PASSWORD` set in a `.env` file in the project root
- SSH key with push access to `git@github.com:rodortega/tapo-onoff.git` (for publishing)

Files

- `main.py` — FastAPI app. Loads device IDs from `devices.json` at startup.
- `devices.json` — JSON array of device identifiers (example provided).
- `.env` — not committed: contains `USERNAME` and `PASSWORD` for the Tapo account.

Example `devices.json`

[
  "device_id_1",
  "device_id_2"
]

Run locally

Create and activate a virtualenv, install requirements, then start uvicorn:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Endpoints

- `POST /switch/on` — turns all devices from `devices.json` on
- `POST /switch/off` — turns all devices from `devices.json` off

Notes

- The app will raise a startup error if `.env` or `devices.json` are missing or invalid.
- If you want to change devices, edit `devices.json` and restart the server.

License: MIT (adjust as needed)
