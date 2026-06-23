# pse-simulator

Banco PSE **simulado** para desarrollo local de Hermes. Reemplaza al proveedor real
(Wompi/PayU) mientras no haya credenciales: lista bancos, abre una transacción, muestra
una página de banco con **Aprobar/Rechazar** y envía a Hermes el **webhook firmado**
(HMAC-SHA256 con el secreto de eventos del tenant) tal como haría el proveedor.

## Uso
```bash
cd pse-simulator && cp .env.example .env && docker compose up -d --build   # http://localhost:8099
```

## Endpoints
- `GET  /pse/financial_institutions` — lista de bancos.
- `POST /pse/transactions` — crea transacción, devuelve `redirectUrl` a la página del banco.
- `GET  /pse/bank/{txid}` — página del banco (Aprobar/Rechazar).
- `POST /pse/bank/{txid}/approve|decline` — firma y envía el webhook, redirige al `returnUrl`.

El contenedor llama al webhook del payment-service en el host vía `host.docker.internal`
(configurable con `WEBHOOK_URL`). No es para producción (estado en memoria).
