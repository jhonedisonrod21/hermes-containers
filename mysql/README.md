# Hermes Calendar — MySQL (local dev)

Imagen MySQL 8.4 para desarrollo local de Hermes Calendar. Crea una base de datos
**por contexto acotado** y el usuario de aplicación `hermes_app`:

| Base | Servicios |
|------|-----------|
| `HERMES_IAM`      | auth-server, identity-service, tenant-service |
| `HERMES_CALENDAR` | catalog-service, scheduling-service, integration-hub-service |
| `HERMES_COMMERCE` | payment-service, notification-service |

> En MySQL el *schema* **es** la base de datos. Cada grupo de servicios posee su
> propia base; dentro de ella cada servicio gestiona sus tablas con Flyway (su
> propio `flyway_schema_history_*`). Ver `ARCHITECTURE.md` en el proyecto.

## Uso

```bash
cp .env.example .env        # ajusta credenciales si lo necesitas
docker compose up -d --build
docker compose ps           # espera a que el healthcheck quede "healthy"
```

Conexión:

| Parámetro | Valor por defecto |
|-----------|-------------------|
| Host      | `localhost`       |
| Puerto    | `3306`            |
| Bases     | `HERMES_IAM`, `HERMES_CALENDAR`, `HERMES_COMMERCE` |
| Usuario   | `hermes_app`      |
| Password  | `hermes_app_local`|
| JDBC URL  | `jdbc:mysql://localhost:3306/HERMES_IAM` (según grupo) |

Cliente rápido:

```bash
docker exec -it hermes-calendar-mysql \
  mysql -u hermes_app -phermes_app_local HERMES_IAM
```

## Detener / limpiar

```bash
docker compose down          # detiene, conserva los datos (volumen)
docker compose down -v       # detiene y BORRA el volumen hermes_mysql_data
```

## Notas

- Charset por defecto `utf8mb4` / `utf8mb4_unicode_ci` y zona horaria `UTC`
  (ver `conf.d/hermes.cnf`), alineado con cómo los servicios Hermes persisten
  fechas (`OffsetDateTime` normalizado a UTC).
- Los scripts de `init/` solo se ejecutan en el **primer** arranque, cuando el
  volumen de datos está vacío. Si cambias el script, recrea el volumen con
  `docker compose down -v`.
- Las credenciales de este `.env` son **solo para desarrollo local**. No las uses
  en entornos compartidos.
