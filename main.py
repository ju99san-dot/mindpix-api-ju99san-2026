from fastapi import FastAPI, HTTPException, Body
import mercadopago
import os
import time

app = FastAPI()

# ==============================
# CONFIG MERCADO PAGO
# ==============================
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")

if not MP_ACCESS_TOKEN:
    raise Exception("MP_ACCESS_TOKEN não definido!")

sdk = mercadopago.SDK(MP_ACCESS_TOKEN)

# ==============================
# "BANCO" SIMPLES (memória)
# ==============================
usuarios = {}

TEMPO_GRATIS = 1800  # 30 minutos
CREDITOS_INICIAIS = 5

# ==============================
# STATUS
# ==============================
@app.get("/")
async def root():
    return {"status": "API rodando 🚀"}


# ==============================
# CRIAR USUÁRIO
# ==============================
@app.post("/criar-usuario")
async def criar_usuario(user_id: str = Body(...)):
    usuarios[user_id] = {
        "inicio": time.time(),
        "creditos": CREDITOS_INICIAIS
    }
    return {"status": "usuario criado", "creditos": CREDITOS_INICIAIS}


# ==============================
# GERAR CÓDIGO (SISTEMA PRINCIPAL)
# ==============================
@app.post("/gerar-codigo")
async def gerar_codigo(user_id: str = Body(...), pedido: str = Body(...)):

    if user_id not in usuarios:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user = usuarios[user_id]

    tempo_usado = time.time() - user["inicio"]

    # limite grátis
    if tempo_usado > TEMPO_GRATIS:
        if user["creditos"] <= 0:
            return {
                "status": "bloqueado",
                "mensagem": "Compre créditos para continuar"
            }
        else:
            user["creditos"] -= 1

    # GERADOR SIMPLES
    codigo = f"""
# Código gerado automaticamente

def app():
    print("Pedido do usuário:")
    print("{pedido}")

if __name__ == "__main__":
    app()
"""

    return {
        "status": "ok",
        "codigo": codigo,
        "creditos_restantes": user["creditos"]
    }


# ==============================
# GERAR PIX
# ==============================
@app.post("/criar-pix")
async def criar_pix(valor: float = Body(...)):

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

    pix = payment.get("point_of_interaction", {}).get("transaction_data", {})

    return {
        "status": "ok",
        "pix_copia_cola": pix.get("qr_code"),
        "qr_code_base64": pix.get("qr_code_base64")
    }


# ==============================
# GERAR LINK DE PAGAMENTO
# ==============================
@app.post("/criar-link")
async def criar_link(valor: float = Body(...)):

    preference_data = {
        "items": [
            {
                "title": "Compra de créditos",
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


# ==============================
# ADICIONAR CRÉDITOS (MANUAL)
# ==============================
@app.post("/add-creditos")
async def add_creditos(user_id: str = Body(...), quantidade: int = Body(...)):

    if user_id not in usuarios:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    usuarios[user_id]["creditos"] += quantidade

    return {
        "status": "ok",
        "creditos": usuarios[user_id]["creditos"]
    }
