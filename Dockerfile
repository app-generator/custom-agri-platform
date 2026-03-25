# ==========================================
# STAGE 1: Frontend Builder (Node)
# ==========================================
FROM node:18-bullseye-slim AS frontend-builder

WORKDIR /app

COPY package.json package-lock.json* yarn.lock* ./

RUN yarn install --frozen-lockfile

COPY . .
RUN yarn build


# ==========================================
# STAGE 2: Final Production Image (Python)
# ==========================================
FROM python:3.11.5-slim 

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Bikin user & group DI SINI (Stage 2) dengan explicit UID 1000
RUN groupadd -g 1000 appgroup \
 && useradd -u 1000 -g appgroup -d /home/appuser -m appuser

# Install OS dependencies wajib
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps duluan biar layer ke-cache
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy sisa code backend dari host LANGSUNG dengan chown (Save layer size)
COPY --chown=appuser:appgroup . .

# COPY hasil build Webpack/Assets dari STAGE 1 langsung dengan chown
COPY --chown=appuser:appgroup --from=frontend-builder /app/static ./static
COPY --chown=appuser:appgroup --from=frontend-builder /app/webpack-stats.json ./

# Expose port (Opsional cuma buat dokumentasi image)
EXPOSE 5005

# Drop privilege ke non-root user buat security
USER appuser

# CMD murni cuma jalanin server
# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "config.wsgi"]
