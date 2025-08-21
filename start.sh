#!/bin/bash

function _init_(){
echo "[init] Node.js version:"
node -v
echo "[init] Python version:"
python3 -V
}


function _check_(){
if lsof -i TCP:${PORT} -sTCP:LISTEN >/dev/null 2>&1; then
    echo "端口 ${PORT} 已被占用，程序退出。"
    exit 1
fi
}



function st_index(){

if [ -f "index.js" ]; then
  echo "[start] Running Node app..."
  node index.js
fi

}

function st_server(){
if [ -f "server.py" ]; then
  echo "[start] Running Python app..."
  python3 server.py
else
  echo "[start] No Python app found, keeping container alive..."
  tail -f /dev/null
fi
}

_init_ && check
#st_index
st_server

tail -f /dev/null
