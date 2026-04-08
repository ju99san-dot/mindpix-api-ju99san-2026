from fastapi import FastAPI, HTTPException, Body
import mercadopago
import os

app = FastAPI()

# Pega token do Railway
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")

if not MP_ACCESS_TOKEN:
    raise Exception("MP_ACCESS_TOKEN não definido!")

# Inicia Mercado Pago
sdk = mercadopago.SDK(MP_ACCESS_TOKEN)


# Rota básica
@app.get("/")
async def root():
    return {"status": "API rodando 🚀"}


# Criar PIX (funciona com Adalo e /docs)
@app.post("/criar-pix")
async def criar_pix(valor: float = Body(...)):

    try:
        payment_data = {
            "transaction_amount": valor,
            "description": "Pagamento via API",
            "payment_method_id": "pix",
            "payer": {
                "email": "teste@teste.com"
            }
        }

        response = sdk.payment().create(payment_data)
        payment = response["response"]

        print("RESPOSTA MP:", payment)

        pix = payment.get("point_of_interaction", {}).get("transaction_data", {})

        return {
            "status": "ok",
            "pix_copia_cola": pix.get("qr_code"),
            "qr_code_base64": pix.get("qr_code_base64")
        }

    except Exception as e:
        print("ERRO:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# Criar link de pagamento
@app.post("/criar-link")
async def criar_link(valor: float = Body(...)):

    try:
        preference_data = {
            "items": [
                {
                    "title": "Pagamento",
                    "quantity": 1,
                    "unit_price": valor
                }
            ]
        }

        response = sdk.preference().create(preference_data)
        link = response["response"]["init_point"]

        return {
            "status": "ok",
            "link_pagamento": link
        }

    except Exception as e:
        print("ERRO:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
