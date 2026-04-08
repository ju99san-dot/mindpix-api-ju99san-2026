from fastapi import FastAPI
import requests
import os

app = FastAPI()

MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")

@app.post("/criar-link")
def criar_link(valor: float):
    url = "https://api.mercadopago.com/checkout/preferences"

    headers = {
        "Authorization": f"Bearer {MP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "items": [
            {
                "title": "Pagamento",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": valor
            }
        ]
    }

    response = requests.post(url, json=body, headers=headers)

    data = response.json()

    return {
        "status": "ok",
        "link_pagamento": data.get("init_point")
    }
