#!/usr/bin/env bash
# Lanza el análisis estático/vulnerabilidades de uno o todos los repos
# contra la instancia SonarQube local (http://localhost:9001).
#
#   ./scan.sh              -> escanea los 5 backends + el front
#   ./scan.sh hermes-infra -> escanea solo ese repo
#   ./scan.sh hermes-front -> solo el front (requiere `npm install` en hermes-front)
#
# Los backends usan el plugin Gradle; hermes-front (SPA TS/JS) usa sonar-scanner (npm).
# El token se lee de hermes-containers/sonarqube/.analysis-token (no versionado).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
TOKEN_FILE="$HERE/.analysis-token"

[ -f "$TOKEN_FILE" ] || { echo "Falta $TOKEN_FILE (genera un token de análisis en Sonar)"; exit 1; }
TOKEN="$(cat "$TOKEN_FILE")"
HOST="${SONAR_HOST_URL:-http://localhost:9001}"

REPOS=(hermes-platform-shared hermes-security hermes-calendar hermes-commerce hermes-infra hermes-front)
[ $# -gt 0 ] && REPOS=("$@")

for repo in "${REPOS[@]}"; do
  echo "==================== $repo ===================="
  if [ "$repo" = "hermes-front" ]; then
    # SPA TS/JS: el análisis lo hace sonar-scanner (devDependency), no Gradle.
    ( cd "$ROOT/$repo" && SONAR_TOKEN="$TOKEN" npm run sonar -- -Dsonar.host.url="$HOST" )
  else
    ( cd "$ROOT/$repo" && ./gradlew sonar -Dsonar.token="$TOKEN" -Dsonar.host.url="$HOST" --console=plain )
  fi
done

echo "Listo. Revisa los resultados en $HOST"
