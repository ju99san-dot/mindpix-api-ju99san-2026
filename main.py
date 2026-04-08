from fastapi import FastAPI
import mercadopago
import os

app = FastAPI()

# Pega o token do Railway (variável de ambiente)
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")

# Inicia SDK do Mercado Pago
sdk = mercadopago.SDK(MP_ACCESS_TOKEN)


# Rota de teste
@app.get("/")
async def root():
    return {"status": "API rodando 🚀"}


# Rota para criar PIX
@app.post("/criar-pix")
async def criar_pix(valor: float):

    payment_data = {
        "transaction_amount": valor,
        "description": "Pagamento via API",
        "payment_method_id": "pix",
        "payer": {
            "email": "teste@email.com"
        }
    }

    # Cria pagamento
    response = sdk.payment().create(payment_data)
    payment = response["response"]

    print("RESPOSTA MP:", payment)

    # Pega dados do PIX com segurança
    pix = payment.get("point_of_interaction", {}).get("transaction_data", {})

    return {
        "pix_copia_cola": pix.get("qr_code"),
        "qr_code_base64": pix.get("qr_code_base64")
    }
