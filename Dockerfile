# Node.js 20 Alpine
FROM node:20-alpine

# 运行环境
ENV HOME=/home/node
ENV PORT=8080

WORKDIR /app

# 安装运行所需工具
RUN apk add --no-cache \
    bash \
    curl \
    wget \
    python3 \
    py3-pip \
    py3-requests \
    net-tools \
    lsof \
    ca-certificates \
    openssl \
    procps

# 先复制依赖文件，利用 Docker 缓存
COPY package.json package-lock.json ./

# 安装 Node 依赖
RUN npm ci --omit=dev \
    && npm cache clean --force

# 复制项目文件
COPY index.js /app/index.js
COPY argosb.sh /home/node/agsb/argosb.sh

# 设置权限
RUN chmod +x /home/node/agsb/argosb.sh \
    && chown -R node:node /app /home/node/agsb

# 使用 node 用户运行
USER node

# Cloud Run HTTP 端口
EXPOSE 8080

# Cloud Run 启动入口
CMD ["node", "index.js"]
