import matplotlib.pyplot as plt

# Simulando impacto de SAI sobre a temperatura média global
years = list(range(2024, 2050))
temperature_no_sai = [x * 0.02 + 1 for x in range(len(years))]
temperature_with_sai = [x * 0.01 + 0.5 for x in range(len(years))]

plt.plot(years, temperature_no_sai, label='Sem SAI')
plt.plot(years, temperature_with_sai, label='Com SAI')
plt.xlabel('Ano')
plt.ylabel('Aumento da Temperatura (°C)')
plt.title('Impacto Simulado de SAI sobre a Temperatura Global')
plt.legend()
plt.show()
