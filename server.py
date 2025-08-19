import importlib
import os
import sys
import uuid
import socket
import subprocess
import threading
importlib.util.find_spec("requests") or subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", "requests"])
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
# 检查 requests 是否已安装

# ========== 配置 ==========
NAME = os.getenv("NAME", socket.gethostname())
PORT = int(os.getenv("PORT", "3000"))  # HTTP 服务端口
DOMAIN = os.getenv("DOMAIN", "no_domain")
RAW_UUID = os.getenv("uuid", "") or str(uuid.uuid4()) # 变量uuid，若不配置则随机生成uuid
HAS_UUID = bool(os.getenv("uuid"))
HAS_DOMAIN = bool(os.getenv("DOMAIN"))
UUID = RAW_UUID.replace("-", "")
SUBTXT = os.path.expanduser("~/agsb/jh.txt")
ARGOSB_PATH = os.path.expanduser("~/agsb/argosb.sh")
ARGOSB_URL = "https://raw.githubusercontent.com/lucas8864/agsb-docker/refs/heads/main/argosb.sh"

# 额外需要传递的环境变量（保持原样）
VMPT = os.getenv("vmpt", "29344")
HYPT = os.getenv("hypt", "12345")
ARGO = os.getenv("argo", "y")
AGN = os.getenv("agn", "") #CF固定域名
AGK = os.getenv("agk", "") #CF隧道token

# vlessURL 拼接
vlessURL = (
    f"vless://{RAW_UUID}@{DOMAIN}:443?encryption=none&security=tls"
    f"&sni={DOMAIN}&fp=chrome&type=ws&host={DOMAIN}&path=%2F#Vl-ws-tls-{NAME}"
    if HAS_UUID and HAS_DOMAIN else ""
)

# ========== HTTP 服务 ==========
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                f"🟢部署成功 (Python版)\n\n\n\n查看节点信息路径：/你的uuid或者/subuuid\n\n".encode("utf-8")
            )
        elif self.path == f"/{RAW_UUID}":
            result = vlessURL
            if os.path.exists(SUBTXT):
                with open(SUBTXT, "r", encoding="utf-8") as f:
                    data = f.read().strip()
                    if data:
                        result = f"{vlessURL}\n{data}" if vlessURL else data
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(result.encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write("❌Not Found：路径错误！！！\n\n查看节点信息路径：/你的uuid或者/subuuid".encode("utf-8"))

# ========== 下载 argosb.sh ==========
def download_argosb():
    os.makedirs(os.path.dirname(ARGOSB_PATH), exist_ok=True)
    print(f"⬇️ 下载 argosb.sh from {ARGOSB_URL}")
    try:
        r = requests.get(ARGOSB_URL, timeout=15)
        if r.status_code == 200:
            with open(ARGOSB_PATH, "w", encoding="utf-8") as f:
                f.write(r.text)
            os.chmod(ARGOSB_PATH, 0o755)
            print(f"✅ argosb.sh 已下载到 {ARGOSB_PATH}")
        else:
            print(f"⚠️ 下载失败 status={r.status_code}")
    except Exception as e:
        print(f"❌ 下载 argosb.sh 出错: {e}")

# ========== 启动 argosb.sh ==========
def run_argosb():
    if not os.path.exists(ARGOSB_PATH):
        download_argosb()

    if os.path.exists(ARGOSB_PATH):
        print(f"🚀 Running {ARGOSB_PATH} ...")
        env = os.environ.copy()
        # 保证这些变量传给 argosb.sh
        env.update({
            "uuid": RAW_UUID,
            "vmpt": VMPT,
            "hypt": HYPT,
            "argo": ARGO,
            "agn": AGN,
            "agk": AGK,
        })
        process = subprocess.Popen(
            ["sh", ARGOSB_PATH],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        for line in process.stdout:
            sys.stdout.write(line)
        for line in process.stderr:
            sys.stderr.write(line)
        process.wait()
        print(f"Script finished with code {process.returncode}")
    else:
        print(f"❌ argosb.sh not found at {ARGOSB_PATH} (下载失败)")

# ========== 主程序 ==========
if __name__ == "__main__":
    print(f"✅ HTTP server listening on port {PORT}")
    print(f"💣 VLESS 节点信息: \n{vlessURL}\n" if vlessURL else "⚠️ No VLESS URL generated.")

    # 异步启动 argosb.sh
    threading.Thread(target=run_argosb, daemon=True).start()

    # 启动 HTTP 服务
    server = HTTPServer(("0.0.0.0", PORT), RequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        server.server_close()
