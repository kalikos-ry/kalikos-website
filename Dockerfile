FROM python:3.13-bullseye
SHELL ["/bin/bash", "-c"]
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 0
RUN apt-get update \
 && apt-get install -y --force-yes \
 nano gettext chrpath libssl-dev libxft-dev \
 libfreetype6 libfreetype6-dev libfontconfig1 libfontconfig1-dev \
 && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /code/
COPY ./code/pyproject.tom[l] ./code/uv.loc[k] ./code/requirements.tx[t] /code/
RUN if [ -f "pyproject.toml" ]; then \
      UV_PROJECT_ENVIRONMENT=/usr/local uv sync --frozen; \
    elif [ -f "requirements.txt" ]; then \
      uv pip install --system gunicorn && uv pip install --system -r requirements.txt; \
    else \
      echo "ERROR: No pyproject.toml or requirements.txt found" && exit 1; \
    fi
COPY ./code/ /code/
COPY ./env/ /env/
RUN source /env/envs_export.sh && if [ -n "$BUILD_COMMAND" ]; then eval $BUILD_COMMAND; fi
RUN source /env/envs_export.sh && if [ -f "manage.py" ]; then if [ "$DISABLE_COLLECTSTATIC" == "1" ]; then echo "collect static disabled"; else echo "Found manage.py, running collectstatic" && python manage.py collectstatic --noinput; fi; else echo "No manage.py found. Skipping collectstatic."; fi;
RUN useradd -ms /bin/bash code
USER code