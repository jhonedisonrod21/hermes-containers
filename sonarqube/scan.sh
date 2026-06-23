#!/usr/bin/env bash
# Lanza el análisis estático/vulnerabilidades de uno o todos los repos backend
# contra la instancia SonarQube local (http://localhost:9001).
#
#   ./scan.sh              -> escanea los 5 repos backend
#   ./scan.sh hermes-infra -> escanea solo ese repo
#
# El token se lee de hermes-containers/sonarqube/.analysis-token (no versionado).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
TOKEN_FILE="$HERE/.analysis-token"

[ -f "$TOKEN_FILE" ] || { echo "Falta $TOKEN_FILE (genera un token de análisis en Sonar)"; exit 1; }
TOKEN="$(cat "$TOKEN_FILE")"
HOST="${SONAR_HOST_URL:-http://localhost:9001}"

REPOS=(hermes-platform-shared hermes-security hermes-calendar hermes-commerce hermes-infra)
[ $# -gt 0 ] && REPOS=("$@")

for repo in "${REPOS[@]}"; do
  echo "==================== $repo ===================="
  ( cd "$ROOT/$repo" && ./gradlew sonar -Dsonar.token="$TOKEN" -Dsonar.host.url="$HOST" --console=plain )
done

echo "Listo. Revisa los resultados en $HOST"
