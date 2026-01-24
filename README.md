# Kalikos website (kalikos.org)

This is the code for the Kalikos website, a community-driven platform for sharing and discussing news, events, and other content related to the Kalikos community.

# Development

## Local development setup

```bash
python -m venv .venv
source .venv/bin/activate # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file. Copy from `.env-dev` and add the local development specific settings.

## To update dependencies

Update `requirements.in` with the new dependencies.

```bash
pip install pip-tools
pip-compile requirements.in
pip install -r requirements.txt
```

## Copy data
TBD: Copy database data from the production server and media files from the production server.

The default location for media files is `media/`.