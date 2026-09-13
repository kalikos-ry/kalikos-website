# Kalikos website (kalikos.org)

This is the code for the Kalikos website, a community-driven platform for sharing and discussing news, events, and other content related to the Kalikos community.

# Development

## Local development setup

Install [uv](https://docs.astral.sh/uv/), then sync dependencies:

```bash
uv sync
```

Create a `.env` file. Copy from `.env-dev` and add the local development specific settings.

## To update dependencies

Add or change dependencies in [`pyproject.toml`](pyproject.toml), or use:

```bash
uv add package-name
uv add 'package-name==1.2.3'
```

Then refresh the lockfile and environment:

```bash
uv lock
uv sync
```

## Copy data
TBD: Copy database data from the production server and media files from the production server.

The default location for media files is `media/`.

## Running the project
```bash
uv run python manage.py runserver
```
