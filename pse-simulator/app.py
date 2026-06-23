"""
Simulador de banco PSE para desarrollo de Hermes.

Reemplaza al proveedor real (Wompi/PayU) en local: lista bancos, abre una "transacción",
muestra una página de banco con botones Aprobar/Rechazar y, al decidir, envía a Hermes el
webhook FIRMADO (HMAC-SHA256 con el secreto de eventos del tenant) tal como haría el proveedor.

No es para producción: estado en memoria, un solo proceso.
"""
import hashlib
import hmac
import json
import os
import uuid

import requests
from flask import Flask, redirect, request

app = Flask(__name__)

# A dónde enviar el webhook de confirmación (el payment-service de Hermes).
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "http://host.docker.internal:8084/webhooks/fake_pse")
# Base pública del simulador (a la que el navegador del usuario es redirigido).
SELF_BASE_URL = os.environ.get("SELF_BASE_URL", "http://localhost:8099")

# Bancos de ejemplo (códigos ilustrativos al estilo PSE).
BANKS = [
    {"code": "1007", "name": "Bancolombia"},
    {"code": "1051", "name": "Davivienda"},
    {"code": "1013", "name": "BBVA Colombia"},
    {"code": "1001", "name": "Banco de Bogotá"},
    {"code": "1507", "name": "Nequi"},
    {"code": "1551", "name": "Daviplata"},
]

# Transacciones en memoria: txid -> {...}
TX = {}


@app.get("/health")
def health():
    return {"status": "UP"}


@app.get("/pse/financial_institutions")
def financial_institutions():
    return app.response_class(json.dumps(BANKS), mimetype="application/json")


@app.post("/pse/transactions")
def create_transaction():
    body = request.get_json(force=True, silent=True) or {}
    txid = "pse_" + uuid.uuid4().hex
    TX[txid] = {
        "id": txid,
        "amount": body.get("amount"),
        "currency": body.get("currency"),
        "bank": body.get("financialInstitutionCode"),
        "reference": body.get("reference"),
        "events_secret": body.get("eventsSecret") or "",
        "return_url": body.get("returnUrl") or SELF_BASE_URL,
        "status": "PENDING",
    }
    return {
        "id": txid,
        "status": "PENDING",
        "redirectUrl": f"{SELF_BASE_URL}/pse/bank/{txid}",
    }


@app.get("/pse/bank/<txid>")
def bank_page(txid):
    tx = TX.get(txid)
    if not tx:
        return ("Transacción no encontrada", 404)
    return f"""
    <html><head><meta charset="utf-8"><title>Banco simulado · PSE</title></head>
    <body style="font-family:Arial;max-width:480px;margin:40px auto;color:#172033">
      <div style="border:1px solid #E3E8F0;border-radius:8px;overflow:hidden">
        <div style="background:#0D347A;color:#fff;padding:16px 24px"><b>Banco simulado</b> · PSE</div>
        <div style="padding:24px">
          <p>Vas a autorizar un pago en Hermes Agenda.</p>
          <p><b>Monto:</b> {tx['amount']} {tx['currency']}<br/>
             <b>Transacción:</b> {txid}</p>
          <form method="post" action="{SELF_BASE_URL}/pse/bank/{txid}/approve" style="display:inline">
            <button style="background:#1F9D55;color:#fff;border:0;padding:12px 22px;border-radius:8px;cursor:pointer">Aprobar pago</button>
          </form>
          <form method="post" action="{SELF_BASE_URL}/pse/bank/{txid}/decline" style="display:inline;margin-left:8px">
            <button style="background:#D64545;color:#fff;border:0;padding:12px 22px;border-radius:8px;cursor:pointer">Rechazar</button>
          </form>
        </div>
      </div>
    </body></html>
    """


@app.post("/pse/bank/<txid>/approve")
def approve(txid):
    return _finish(txid, "PAID")


@app.post("/pse/bank/<txid>/decline")
def decline(txid):
    return _finish(txid, "FAILED")


def _finish(txid, status):
    tx = TX.get(txid)
    if not tx:
        return ("Transacción no encontrada", 404)
    tx["status"] = status
    _send_webhook(tx, status)
    return redirect(f"{tx['return_url']}?ref={txid}&status={status}", code=302)


def _send_webhook(tx, status):
    payload = {"eventId": "evt_" + uuid.uuid4().hex, "providerReference": tx["id"], "status": status}
    raw = json.dumps(payload).encode("utf-8")
    signature = hmac.new(tx["events_secret"].encode("utf-8"), raw, hashlib.sha256).hexdigest()
    try:
        resp = requests.post(
            WEBHOOK_URL,
            data=raw,
            headers={"Content-Type": "application/json", "X-Payment-Signature": signature},
            timeout=5,
        )
        app.logger.info("webhook %s -> %s (%s)", tx["id"], resp.status_code, status)
    except Exception as exc:  # noqa: BLE001
        app.logger.warning("webhook %s failed: %s", tx["id"], exc)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8099)
