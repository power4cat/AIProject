#!/bin/zsh
set -e
port=8000

echo "🔍 正在查找端口 $port 的uvicorn进程..."
# 获取PID（mac lsof）
pid=$(lsof -t -i :$port)

if [[ -z "$pid" ]]; then
  echo "✅ 没有找到运行在 $port 端口的服务，无需停止"
  exit 0
fi

echo "🛑 找到进程PID: $pid，准备停止服务"
kill "$pid"

# 等待2秒优雅退出
sleep 2

# 二次检查进程是否还存活
stillAlive=$(lsof -t -i :$port || true)
if [[ -n "$stillAlive" ]]; then
  echo "⚠️进程未正常退出，强制杀死"
  kill -9 "$stillAlive"
fi

echo "✅ AI Robot 服务已停止"