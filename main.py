response = sdk.payment().create(payment_data)
    payment = response["response"]

    print("RESPOSTA MP:", payment)

    pix = payment.get("point_of_interaction", {}).get("transaction_data", {})

    return {
        "pix_copia_cola": pix.get("qr_code"),
        "qr_code_base64": pix.get("qr_code_base64")
    }


@app.post("/criar-link")
async def criar_link(valor: float):

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
        "link_pagamento": link
    }
