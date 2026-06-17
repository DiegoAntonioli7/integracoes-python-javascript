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

lsof -ti:8001 | xargs kill -9 2>/dev/null || true

echo "==> Instalando dependências SOAP Python..."
cd "$ROOT/soap/python-spyne-soap"
"$PYTHON3" -m pip install -r requirements.txt -q

echo "==> Subindo servidor SOAP Python na porta 8001..."
"$PYTHON3" app.py &
SERVER_PID=$!

echo "==> Aguardando servidor iniciar..."
sleep 3

echo "==> Executando Locust..."
cd "$ROOT"
mkdir -p "$ROOT/soap/results"
"$PYTHON3" -m locust -f locust/soap_python_locust.py --host http://localhost:8001 --users 20 --spawn-rate 20 --headless --run-time 60s --stop-timeout 5 --csv="$ROOT/soap/results/soap_python"

kill $SERVER_PID 2>/dev/null
