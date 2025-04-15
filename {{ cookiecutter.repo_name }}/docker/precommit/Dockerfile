# Creates a dockerfile with pre-commit preconfigured.
# Can be used to reduce time for linting stage.

FROM python:3.9-slim-buster

ENV PRE_COMMIT_VERSION 3.0.4

# Install git and curl for pre-commit and uv installation
RUN apt-get update \
  && apt-get install -y --no-install-recommends git curl \
  && apt-get purge -y --auto-remove \
  && rm -rf /var/lib/apt/lists/*

# Install uv and add to PATH
RUN curl -fsSL https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Create project directories
RUN mkdir /tmp/pre-commit && mkdir /project && cd /tmp/pre-commit \
  && git init .

# Install pre-commit using uv
RUN cd /tmp/pre-commit \
  && uv pip install --system pre-commit==${PRE_COMMIT_VERSION}

# Copy pre-commit config
ARG src=".pre-commit-config.yaml"
COPY ${src} /tmp/pre-commit/.pre-commit-config.yaml

# Install and run pre-commit hooks
RUN cd /tmp/pre-commit \
  && uv run pre-commit install \
  && uv run pre-commit run

# Set working directory for when container is run
WORKDIR /project

# Add a default CMD that runs pre-commit
CMD ["uv", "run", "pre-commit", "run", "--all-files", "--show-diff-on-failure", "--color", "always"]
