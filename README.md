# Kalikos website (kalikos.org)

This is the code for the Kalikos website, a community-driven platform for sharing and discussing news, events, and other content related to the Kalikos community.

# Development

## Local development setup

```bash
python -m venv .venv
source .venv/bin/activate # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env-local` file. Copy from `.env-dev` and add the local development specific settings.

## To update dependencies

Update `requirements.in` with the new dependencies.

```bash
pip install pip-tools
pip-compile requirements.in
pip install -r requirements.txt
```

1. Set up environment `divio app setup kalikos -s test`
2. Run the project `divio project up`
3. Run migrations `docker-compose run --rm web python manage.py migrate`

## Syncing media and db
`divio app pull media` and `divio app pull db` to pull media and db from the server