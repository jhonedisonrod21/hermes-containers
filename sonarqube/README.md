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

## Analizar el proyecto (Gradle)

1. En SonarQube: **My Account → Security → Generate Token** (tipo *Project Analysis*).
2. Añade el plugin al `build.gradle` raíz del proyecto:

   ```groovy
   plugins {
       id 'org.sonarqube' version '5.1.0.4882'
   }

   sonar {
       properties {
           property 'sonar.host.url', 'http://localhost:9001'
           property 'sonar.projectKey', 'hermes-calendar-platform'
           property 'sonar.projectName', 'Hermes Calendar Platform'
       }
   }
   ```

3. Ejecuta el análisis (los reports de cobertura JaCoCo, si los activas, se
   recogen automáticamente):

   ```bash
   ./gradlew build sonar \
     -Dsonar.token=TU_TOKEN \
     -Dsonar.host.url=http://localhost:9001
   ```

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
