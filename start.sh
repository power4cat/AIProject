#!/bin/zsh
set -e
root=$(cd "$(dirname "$0")";pwd)
cd "$root"
NoBrowser=0
# 参数解析
if [[ "$1" == "-NoBrowser" ]];then
  NoBrowser=1
fi
port=8000
url="http://localhost:$port"
echo "========================================="
echo "  AI Robot 一键启动（本地 Ollama 模式）"
echo "========================================="

#1 .env
if [ ! -f ".env" ];then
  cp ".env.example" ".env"
  echo "[1/6] 已生成 .env（请按需检查密钥/模型）"
else
  echo "[1/6] .env 已存在"
fi

#2 虚拟环境 mac路径 .venv/bin/python
py="$root/.venv/bin/python"
if [ ! -f "$py" ];then
  echo "[2/6] 创建虚拟环境 .venv ..."
  python3 -m venv .venv
  if [ ! -f "$py" ];then
    echo "创建 .venv 失败，请先安装 Python3.10+"
    exit 1
  fi
fi
echo "[2/6] 虚拟环境就绪"

#3 安装依赖
echo "[3/6] 检查核心依赖 ..."
$py -m pip install -q -r requirements.txt
echo "[3/6] 依赖就绪"

#4 读取.env 获取模型
GetEnvValue(){
  key=$1
  line=$(grep "^${key}=" .env | head -1)
  value=${line#*=}
  echo "$value"
}
llmModel=$(GetEnvValue "AIROBOT_LLM_MODEL")
embModel=$(GetEnvValue "AIROBOT_EMBEDDING_MODEL")

echo "[4/6] 检测Ollama..."
if curl -s --connect-timeout 3 http://127.0.0.1:11434/api/tags >/dev/null;then
  echo "[4/6] Ollama在线，请确认模型已pull"
else
  echo "⚠️[4/6] Ollama未运行！先启动Ollama，执行 ollama pull $llmModel && ollama pull $embModel"
fi

#5 端口占用检测
if lsof -i :$port >/dev/null;then
  echo "[5/6] 端口 $port 已有服务运行，打开控制台"
  if [ $NoBrowser -eq 0 ];then
    open "$url/dashboard"
  fi
  exit 0
fi
echo "[5/6] 端口 $port 空闲"

#6 启动uvicorn后台运行
logDir="$root/.logs"
mkdir -p "$logDir"
outLog="$logDir/uvicorn.out.log"
errLog="$logDir/uvicorn.err.log"

echo "[6/6] 启动uvicorn，日志：.logs/uvicorn.*.log"
nohup $py -m uvicorn app.main:app --host 127.0.0.1 --port $port > "$outLog" 2>"$errLog" &
pid=$!

ok=0
for ((i=0;i<40;i++));do
  sleep 1
  if curl -s --connect-timeout 2 "$url/health" >/dev/null ;then
    ok=1
    break
  fi
done
if [ $ok -eq 0 ];then
  echo "服务启动超时，请查看日志 $errLog"
  exit 1
fi

echo "✅服务已启动"
echo "控制台: $url/dashboard"
echo "指标:   $url/api/v1/stats"
if [ $NoBrowser -eq 0 ];then
  open "$url/dashboard"
fi