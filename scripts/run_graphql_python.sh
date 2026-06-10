#!/bin/bash
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

PYTHON3=""
for candidate in \
  "/Library/Frameworks/Python.framework/Versions/3.14/bin/python3.14" \
  "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13" \
  "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12" \
  "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11" \
  "$(which python3.14 2>/dev/null)" \
  "$(which python3.13 2>/dev/null)" \
  "$(which python3.12 2>/dev/null)" \
  "$(which python3 2>/dev/null)"; do
  if [ -n "$candidate" ] && [ -x "$candidate" ] && "$candidate" -c "import locust" 2>/dev/null; then
    PYTHON3="$candidate"
    break
  fi
done

if [ -z "$PYTHON3" ]; then
  echo "ERRO: locust nao encontrado em nenhum Python."
  echo "Instale com: /Library/Frameworks/Python.framework/Versions/3.14/bin/pip3 install locust"
  exit 1
fi
echo "==> Usando $PYTHON3"

lsof -ti:8002 | xargs kill -9 2>/dev/null || true

echo "==> Instalando dependências GraphQL Python..."
cd "$ROOT/graphql/python-strawberry-graphql"
"$PYTHON3" -m pip install -r requirements.txt -q

echo "==> Subindo servidor GraphQL Python na porta 8002..."
"$PYTHON3" -m uvicorn app:app --port 8002 &
SERVER_PID=$!

echo "==> Aguardando servidor iniciar..."
sleep 3

echo "==> Executando Locust..."
cd "$ROOT"
mkdir -p "$ROOT/graphql/results"
"$PYTHON3" -m locust -f locust/graphql_python_locust.py --host http://localhost:8002 --csv="$ROOT/graphql/results/graphql_python"

kill $SERVER_PID 2>/dev/null
