#!/bin/bash
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "==> Instalando dependências SOAP JavaScript..."
cd "$ROOT/soap/javascript-node-soap"
npm install --silent

echo "==> Subindo servidor SOAP JavaScript na porta 3002..."
npm start &
SERVER_PID=$!

echo "==> Aguardando servidor iniciar..."
sleep 3

echo "==> Executando Locust..."
cd "$ROOT"
mkdir -p "$ROOT/soap/results"
locust -f locust/soap_javascript_locust.py --host http://localhost:3002 --users 100 --spawn-rate 20 --csv="$ROOT/soap/results/soap_javascript"

kill $SERVER_PID 2>/dev/null
