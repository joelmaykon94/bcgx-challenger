from langchain.prompts import PromptTemplate

# Exemplo de prompt adaptado para diferentes preocupações sobre SAI
prompt_template = """
Você é um especialista em geoengenharia. Baseado nas críticas abaixo, forneça uma resposta detalhada e técnica:
- Crítica: {critique}
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["critique"])

# Exemplo de uso com uma crítica
critique = "Injeção Estratosférica de Aerossóis pode causar poluição e contribuir para a destruição da camada de ozônio."
response = prompt.format(critique=critique)

print(response)
