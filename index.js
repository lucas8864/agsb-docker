const http = require('http');
const fs = require('fs');
const os = require('os');
const net = require('net');
const path = require('path');
const { exec } = require('child_process');

const { WebSocket, createWebSocketStream } = require('ws');

const NAME = process.env.NAME || os.hostname();
const subtxt = path.join(os.homedir(), 'agsb', 'jh.txt');
const PORT = process.env.PORT || 3000;
const DOMAIN = process.env.DOMAIN || 'no_domain';
const rawUUID = process.env.uuid || 'subuuid';
const hasUUID = !!process.env.uuid;
const hasDOMAIN = !!process.env.DOMAIN;
const uuid = rawUUID.replace(/-/g, "");
const vlessURL = (hasUUID && hasDOMAIN)
  ? `vless://${rawUUID}@${DOMAIN}:443?encryption=none&security=tls&sni=${DOMAIN}&fp=chrome&type=ws&host=${DOMAIN}&path=%2F#Vl-ws-tls-${NAME}`
  : '';

const server = http.createServer((req, res) => {
  if (req.url === '/') {
    res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('🟢恭喜！部署成功！欢迎使用甬哥YGkkk-ArgoSB小钢炮脚本💣 【当前版本V25.8.8】\n\n查看节点信息路径：/你的uuid或者/subuuid');
  } else if (req.url === `/${rawUUID}`) {
    fs.readFile(subtxt, 'utf8', (err, data) => {
      const result = !err && data ? (vlessURL ? `${vlessURL}\n${data}` : data) : vlessURL;
      res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end(result);
    });
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('❌Not Found：路径错误！！！\n\n查看节点信息路径：/你的uuid或者/subuuid');
  }
});

server.listen(PORT, () => {
  console.log(`✅Server is running on port ${PORT}`);

  const argosbPath = path.join(os.homedir(), 'agsb', 'argosb.sh');
  if (fs.existsSync(argosbPath)) {
    const child = exec(`sh ${argosbPath}`);
    child.stdout.on('data', chunk => process.stdout.write(chunk));
    child.stderr.on('data', chunk => process.stderr.write(chunk));
    child.on('close', (code) => {
      console.clear();
      console.log(`🚀App is running`);

      if (hasUUID && hasDOMAIN) {
        const wss = new WebSocket.Server({ server });
        wss.on('connection', ws => {
          ws.once('message', msg => {
            if (!(msg instanceof Buffer)) msg = Buffer.from(msg);
            if (msg.length < 19) return;

            const [VERSION] = msg;
            const id = msg.slice(1, 17);
            if (!id.every((v, i) => v === parseInt(uuid.substr(i * 2, 2), 16))) return;

            const offset = msg.readUInt8(17);
            let i = 19 + offset;
            if (msg.length < i + 3) return;

            const port = msg.readUInt16BE(i);
            i += 2;
            const ATYP = msg.readUInt8(i++);
            let host = '';
            try {
              if (ATYP === 1) {
                host = msg.slice(i, i += 4).join('.');
              } else if (ATYP === 2) {
                const len = msg[i];
                host = new TextDecoder().decode(msg.slice(i + 1, i += 1 + len));
              } else if (ATYP === 3) {
                host = msg.slice(i, i += 16)
                  .reduce((s, b, j, a) => (j % 2 ? s.concat(a.slice(j - 1, j + 1)) : s), [])
                  .map(b => b.readUInt16BE(0).toString(16))
                  .join(':');
              } else return;
            } catch (err) { return; }

            ws.send(new Uint8Array([VERSION, 0]));
            const duplex = createWebSocketStream(ws);
            net.connect({ host, port }, function () {
              this.write(msg.slice(i));
              duplex.on('error', () => {}).pipe(this).on('error', () => {}).pipe(duplex);
            }).on('error', () => {});
          }).on('error', () => {});
        });
        console.log(`\n💣Vless-ws-tls节点分享: \n${vlessURL}\n`);
      }
    });
  } else {
    console.error(`argosb.sh not found at ${argosbPath}`);
  }
});
