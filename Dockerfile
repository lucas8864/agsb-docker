FROM node:22-bookworm-slim
WORKDIR /app
RUN apt-get update && \
    apt-get install -y \
    bash \
    curl \
    wget \
    ca-certificates \
    net-tools \
    lsof \
    openssl \
    procps
    && rm -rf /var/lib/apt/lists/*   
    
COPY package*.json ./
RUN npm install --omit=dev

COPY index.js /app/index.js
COPY argosb.sh /home/node/agsb/argosb.sh

RUN chmod +x /home/node/agsb/argosb.sh && \
    chown -R node:node /app /home/node/agsb

USER node

CMD ["node", "/app/index.js"]
