# 使用 Node 20 alpine 镜像
FROM node:20-alpine

ENV  HOME=/home/node
ARG  uuid=$uuid
ARG  vmpt=$vmpt
ARG  hypt=$hypt
ARG  PORT=$PORT
ARG  argo=$argo
ARG  agn=$agn
ARG  agk=$agk

WORKDIR /app

# 安装依赖 & 下载脚本
RUN apk add --no-cache curl bash wget python3 py3-pip net-tools lsof \
 && npm install -g npm@11.5.2 \
 && curl -LOs https://github.com/lucas8864/agsb-docker/raw/refs/heads/main/argosb.sh \
 && curl -LOs https://github.com/lucas8864/agsb-docker/raw/refs/heads/main/index.js \
 && curl -LOs https://github.com/lucas8864/agsb-docker/raw/refs/heads/main/package.json \
 && curl -LOs https://github.com/lucas8864/agsb-docker/raw/refs/heads/main/package-lock.json \
 && curl -LOs https://github.com/lucas8864/agsb-docker/raw/refs/heads/main/package-lock.json \
 && curl -LOs https://github.com/lucas8864/agsb-docker/raw/refs/heads/main/server.py \
 && curl -LOs https://github.com/lucas8864/agsb-docker/raw/refs/heads/main/start.sh \
 && chmod +x argosb.sh start.sh server.py \
 && npm install --production ws \
 && npm cache clean --force

# 创建运行目录并移动脚本
RUN mkdir -p "$HOME/agsb" \
 && mv argosb.sh "$HOME/agsb/argosb.sh" \
 && chmod -R 777 "$HOME/agsb"

# 给 node 用户权限
RUN mkdir -p /app/node_modules "$HOME/bin" \
 && chmod -R 777 /app "$HOME/bin" \
 && ifconfig eth0 && netstat -antp \
 && cat start.sh

# 切换到 node 用户
USER node

# 暴露端口
EXPOSE 7860

# 采用start.sh启动web服务
#CMD ["node", "index.js"]
CMD ["bash", "-c", "./start.sh"]
