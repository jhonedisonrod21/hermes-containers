# mailpit

Buzón SMTP falso para desarrollo local. `notification-service` envía los correos
aquí (SMTP en `localhost:1025`) y se ven en la UI web (`http://localhost:8025`)
sin salir a un proveedor real.

## Uso

```bash
cd mailpit && cp .env.example .env && docker compose up -d
# UI: http://localhost:8025  ·  SMTP: localhost:1025
```

El `notification-service` (perfil local) apunta su `spring.mail` a `localhost:1025`.
Los correos quedan capturados en el volumen `hermes_mailpit_data`.
