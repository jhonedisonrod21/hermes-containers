# hermes-containers

Contenedores de apoyo para el desarrollo local de Hermes. Un repositorio, varios
servicios independientes (cada uno con su `compose.yml`).

| Carpeta | Imagen | Puerto host | Para qué |
|---------|--------|-------------|----------|
| `mysql/` | MySQL 8.4 | 3306 | Bases `HERMES_IAM`, `HERMES_CALENDAR`, `HERMES_COMMERCE` |
| `mailpit/` | Mailpit | 1025 / 8025 | Buzón SMTP falso para `notification-service` (SMTP + UI web) |
| `sonarqube/` | SonarQube Community | 9001 | Análisis estático de código |

## Uso

```bash
# Base de datos (necesaria para el stack)
cd mysql && cp .env.example .env && docker compose up -d --build

# Buzón SMTP falso (para notificaciones por correo en local)
cd mailpit && cp .env.example .env && docker compose up -d   # UI: http://localhost:8025

# Análisis estático (opcional)
cd sonarqube && cp .env.example .env && docker compose up -d --build   # UI: http://localhost:9001
```

## Notas
- Los `.env` (con credenciales) están **gitignorados**; en el repo solo va
  `.env.example`. Cópialo a `.env` antes de levantar.
- SonarQube usa su **propio** PostgreSQL interno (definido en su `compose.yml`),
  independiente de la base `HERMES_*` de la aplicación.
- SonarQube requiere en el host: `sudo sysctl -w vm.max_map_count=262144`.

Ver `../HERMES-POLYREPO.md` para el stack completo.
