FROM node:20

# Install essential packages: Git, build tools, Python, SQLite3, PostgreSQL client libs, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    make \
    build-essential \
    g++ \
    python3 \
    sqlite3 libsqlite3-dev \
    libpq-dev \
    libtool \
    autoconf \
    automake \
    openssh-client \
 && rm -rf /var/lib/apt/lists/*

# Enable Corepack so we can use Yarn v4 (Backstage’s default yarn)
RUN corepack enable

# For reliable file watching on mounted volumes (optional)
ENV CHOKIDAR_USEPOLLING=true
ENV NODE_ENV=development

# Set the working directory for the project
WORKDIR /workspace

# Switch to the non-root 'node' user for safety
USER node
