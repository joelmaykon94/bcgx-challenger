def generate_response(question, user_type):
    if user_type == "cientista":
        return f"Como cientista, você provavelmente entende o impacto técnico do SAI. Aqui está uma explicação mais detalhada: {question}"
    elif user_type == "público geral":
        return f"Para o público geral: O SAI é uma técnica complexa, mas basicamente funciona assim: {question}"
    else:
        return "Desculpe, não consigo adaptar a resposta para esse tipo de usuário."

# Exemplo de resposta personalizada
user_type = "público geral"
question = "O que é Injeção Estratosférica de Aerossóis (SAI)?"
response = generate_response(question, user_type)

print(response)
