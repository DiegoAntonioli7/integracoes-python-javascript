#!/bin/bash
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "==> Instalando dependências GraphQL JavaScript..."
cd "$ROOT/graphql/javascript-apollo-graphql"
npm install --silent

echo "==> Subindo servidor GraphQL JavaScript na porta 3003..."
npm start &
SERVER_PID=$!

echo "==> Aguardando servidor iniciar..."
sleep 3

echo "==> Executando Locust..."
cd "$ROOT"
mkdir -p "$ROOT/graphql/results"
locust -f locust/graphql_javascript_locust.py --host http://localhost:3003 --csv="$ROOT/graphql/results/graphql_javascript"

kill $SERVER_PID 2>/dev/null
