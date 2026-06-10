#!/bin/bash
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "==> Instalando dependências REST JavaScript..."
cd "$ROOT/rest/javascript-express-rest"
npm install --silent

echo "==> Subindo servidor REST JavaScript na porta 3001..."
npm start &
SERVER_PID=$!

echo "==> Aguardando servidor iniciar..."
sleep 3

echo "==> Executando Locust..."
cd "$ROOT"
mkdir -p "$ROOT/rest/results"
locust -f locust/rest_javascript_locust.py --host http://localhost:3001 --csv="$ROOT/rest/results/rest_javascript"

kill $SERVER_PID 2>/dev/null
