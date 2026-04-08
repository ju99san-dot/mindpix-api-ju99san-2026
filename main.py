response = sdk.payment().create(payment_data)
payment = response["response"]

print("RESPOSTA MP:", payment)

pix = payment.get("point_of_interaction", {}).get("transaction_data", {})

return {
    "pix_copia_cola": pix.get("qr_code"),
    "qr_code_base64": pix.get("qr_code_base64")
}
from fastapi import FastAPI
import mercadopago
import os

app = FastAPI()

MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")

sdk = mercadopago.SDK(MP_ACCESS_TOKEN)

@app.get("/")
async def root():
    return {"status": "API rodando 🚀"}

@app.post("/criar-pix")
async def criar_pix(valor: float):
    payment_data = {
        "transaction_amount": valor,
        "description": "Pagamento Adalo Mind",
        "payment_method_id": "pix",
        "payer": {
            "email": "teste@email.com"
        }
    }

    response = sdk.payment().create(payment_data)
    payment = response["response"]

    return {
        "pix_copia_cola": payment["point_of_interaction"]["transaction_data"]["qr_code"],
        "qr_code_base64": payment["point_of_interaction"]["transaction_data"]["qr_code_base64"]
    }
