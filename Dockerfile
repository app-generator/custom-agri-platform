# ==========================================
# STAGE 1: Frontend Builder (Node)
# ==========================================
FROM node:18-bullseye-slim AS frontend-builder

RUN groupadd -r appgroup \
 && useradd -r -g appgroup -d /home/appuser -m appuser

WORKDIR /app

# Copy config NPM dulu biar ke-cache sama Docker
COPY package.json package-lock.json* yarn.lock* ./
# Pake npm ci lebih cepat dan strict dibanding npm i buat CI/CD
#RUN npm install
RUN yarn install

# Copy sisa source code buat di-compile Webpack
COPY . .
#RUN npm run build
RUN yarn build


# ==========================================
# STAGE 2: Final Production Image (Python)
# ==========================================
# Pake versi -slim biar image sizenya drop drastis dari 1GB jadi ~200MB
FROM python:3.11.5-slim 

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install OS dependencies wajib buat compile psycopg2 (Postgres client)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps duluan biar layer ke-cache
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy sisa code backend dari host
COPY . .

# COPY hasil build Webpack/Assets dari STAGE 1
# (Asumsi hasil build lari ke folder static atau dist, disesuaikan aja)
COPY --from=frontend-builder /app/static ./static
# Kalo webpack nulis file json buat Django, copy juga (liat dari screenshot lo ada webpack-stats.json)
COPY --from=frontend-builder /app/webpack-stats.json ./

RUN chown -R appuser:appgroup /app /home/appuser

# Expose port (Opsional cuma buat dokumentasi image)
EXPOSE 5005

# CMD murni cuma jalanin server. 
# Migrasi dan collectstatic udah di-handle sama 'command' di docker-compose.yml
# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "config.wsgi"]

USER appuser
