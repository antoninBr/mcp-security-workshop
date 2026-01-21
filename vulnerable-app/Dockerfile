# Vulnerable Demo App - Dockerfile
# Exercise 05: Container Poisoning

FROM node:14

# ⚠️ SECURITY ISSUE: Running as root (no USER directive)
WORKDIR /app

# Copy package files
COPY package*.json ./

# ⚠️ SECURITY ISSUE: Installing dependencies as root
RUN npm install

# Copy application files
COPY . .

# ⚠️ SECURITY ISSUE: Exposing .env file with secrets
# Should use build args or runtime secrets instead

# ⚠️ SECURITY ISSUE: No healthcheck
EXPOSE 3000

CMD ["node", "index.js"]
