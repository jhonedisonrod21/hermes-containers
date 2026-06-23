# Hermes Calendar — SonarQube Community (análisis estático)

SonarQube Community Edition para validación estática del código del proyecto
`hermes-calendar-platform`. Incluye su propio PostgreSQL como backend (SonarQube
**no soporta MySQL** para su almacenamiento interno — esto es independiente de la
base de datos `HERMES` de la aplicación).

## Requisito previo del host (Elasticsearch)

SonarQube embebe Elasticsearch, que exige aumentar un límite del kernel:

```bash
sudo sysctl -w vm.max_map_count=262144
# Para hacerlo permanente:
echo 'vm.max_map_count=262144' | sudo tee /etc/sysctl.d/99-sonarqube.conf
```

## Arranque

```bash
cp .env.example .env
docker compose up -d --build
docker compose logs -f sonarqube   # espera "SonarQube is operational"
```

UI: <http://localhost:9001>  · Credenciales iniciales: `admin` / `admin`
(te pedirá cambiarla en el primer login).

> El puerto del host es **9001** para no chocar con `hermes-auth-server`, que usa
> el 9000.

## Analizar el proyecto (polyrepo Gradle)

Hermes es un **polyrepo**: cada repo Gradle es un proyecto Sonar independiente
(`hermes-platform-shared`, `hermes-security`, `hermes-calendar`, `hermes-commerce`,
`hermes-infra`). El plugin `org.sonarqube` (v6.2.0.5505, compatible con Gradle 9.5 /
JDK 25) ya está aplicado en el `build.gradle` raíz de cada repo, con la `projectKey`
derivada del nombre del repo y la compilación atada al task `sonar`. **No hay que
tocar los `build.gradle`.**

### 1 · Token de análisis

Generado y guardado (sin versionar) en `.analysis-token`. Para regenerarlo:

```bash
curl -s -u admin:ADMIN_PASS -X POST "http://localhost:9001/api/user_tokens/generate" \
  --data-urlencode "name=hermes-gradle" --data-urlencode "type=GLOBAL_ANALYSIS_TOKEN" \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["token"])' > .analysis-token
```

### 2 · Lanzar el análisis

```bash
./scan.sh                 # los 5 repos backend, en orden de dependencias
./scan.sh hermes-infra    # solo un repo
```

`scan.sh` lee el token de `.analysis-token` y ejecuta `./gradlew sonar` en cada repo
(el task compila el bytecode antes de escanear). Manualmente, desde un repo concreto:

```bash
./gradlew sonar -Dsonar.token="$(cat ../hermes-containers/sonarqube/.analysis-token)"
```

> **Cobertura (JaCoCo):** no está activada. Sonar reporta bugs, vulnerabilidades,
> *security hotspots* y *code smells*, pero sin % de cobertura. Para añadirla habría
> que aplicar el plugin `jacoco` y exponer `xmlReport` en las convenciones comunes.
>
> **Front (`hermes-front`):** queda fuera de esta configuración (solo backend).

## Seguridad de la instancia

`admin/admin` es la credencial por defecto **solo para uso local**. En el primer login
la UI obliga a cambiarla; el token de análisis ya generado seguirá siendo válido.

## Detener / limpiar

```bash
docker compose down            # detiene, conserva análisis previos
docker compose down -v         # detiene y BORRA todos los volúmenes
```

## Notas

- Primer arranque tarda ~1-2 min (inicializa la base y Elasticsearch).
- Si el contenedor `sonarqube` reinicia en bucle, casi siempre es el
  `vm.max_map_count` del host (ver arriba) o RAM insuficiente (mín. ~2 GB libres).
- Credenciales de `.env` solo para uso local.
