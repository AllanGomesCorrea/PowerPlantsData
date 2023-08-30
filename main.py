#Código para analises de dados
#Retirado dados de: https://datasets.wri.org/dataset/globalpowerplantdatabase

import pandas as pd
import matplotlib.pyplot as plt

file_name = 'global_power_plant_database.csv'

df_raw = pd.read_csv(file_name, encoding= 'utf-8', delimiter=',')

#df_raw.info()
#df_raw.head(10)

#As colunas desejadas a serem trabalhadas
select_columns = [
    'country_long',
    'capacity_mw',
    'primary_fuel',
    'other_fuel1',
    'other_fuel2',
    'other_fuel3',
    'generation_gwh_2013',
    'generation_gwh_2014',
    'generation_gwh_2015',
    'generation_gwh_2016',
    'generation_gwh_2017',
    'generation_gwh_2018',
    'generation_gwh_2019',
    'estimated_generation_gwh_2013',
    'estimated_generation_gwh_2014',
    'estimated_generation_gwh_2015',
    'estimated_generation_gwh_2016',
    'estimated_generation_gwh_2017',
]

df_selected = df_raw[select_columns].copy()

#Explorar os dados

#1 Quantidade de usinas por país e mostrar as top 10
power_plants = df_selected.country_long.value_counts()

plt.barh(power_plants.head(10).index[::-1], power_plants.head(10).values[::-1])
plt.xlabel('Usinas de energia')
plt.ylabel('Países')
plt.title('Top 10 países')
plt.show()

#2 Total de energia MW gerada por país e a média.
MW_generated = df_selected.groupby('country_long')['capacity_mw'].sum()
MW_generated = MW_generated.sort_values(ascending=False)
MW_generated_mean = df_selected.groupby('country_long')['capacity_mw'].mean()
MW_generated_mean = MW_generated_mean.sort_values(ascending=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
ax1.barh(MW_generated.head(10).index[::-1], MW_generated.head(10).values[::-1])
ax1.set_xlabel('Megawatts (MW)')
ax1.set_ylabel('Países')
ax1.set_title('Geração total de energia (MW)')

ax2.barh(MW_generated_mean.head(10).index[::-1], MW_generated_mean.head(10).values[::-1])
ax2.set_xlabel('Megawatts (MW)')
ax2.set_ylabel('Países')
ax2.set_title('Geração média de energia (MW)')
plt.tight_layout()
plt.show()

#3 Quantidade de primary fuel
primary_fuel = df_selected.primary_fuel.value_counts()

plt.figure(figsize=(10, 5))
plt.pie(primary_fuel.values, labels=primary_fuel.index, autopct='%1.1f%%')
plt.title('Fontes de energia')

#4 Média de energia gerada por ano 2013-2017 com o que foi dado
generate2013_mean = df_selected.generation_gwh_2013.dropna().values.mean()
generate2014_mean = df_selected.generation_gwh_2014.dropna().values.mean()
generate2015_mean = df_selected.generation_gwh_2015.dropna().values.mean()
generate2016_mean = df_selected.generation_gwh_2016.dropna().values.mean()
generate2017_mean = df_selected.generation_gwh_2017.dropna().values.mean()
generate2018_mean = df_selected.generation_gwh_2018.dropna().values.mean()
generate2019_mean = df_selected.generation_gwh_2019.dropna().values.mean()

list_mean = [generate2013_mean, generate2014_mean, generate2015_mean, generate2016_mean, generate2017_mean, generate2018_mean, generate2019_mean]
list_date = ['2013', '2014', '2015', '2016', '2017', '2018', '2019']

plt.figure(figsize=(10, 5))
plt.bar(list_date, list_mean)
plt.xlabel('Anos')
plt.ylabel('GWh')
plt.title('Média de energia gerada (GWh) por ano')
plt.show()

#5 Quantidade de usinas Hydro nos EUA que estão a baixo da capacidade média
sources = df_selected.groupby(['country_long', 'primary_fuel'])['capacity_mw']
num_fuel = df_selected.groupby(['country_long'])['primary_fuel']
hydro_Eua_mean = sources.get_group(('United States of America', 'Hydro')).mean()
hydro_Eua_num = num_fuel.get_group('United States of America') == 'Hydro'
hydro_Eua_num = hydro_Eua_num.sum()

sources_comp = sources.get_group(('United States of America', 'Hydro')) < hydro_Eua_mean
total_sources_below = sources_comp.sum()

plt.figure(figsize=(10, 5))
plt.pie([total_sources_below, hydro_Eua_num-total_sources_below], autopct='%1.1f%%')
plt.title(f'Usinas Hydro nos EUA menores que a média {hydro_Eua_mean:.2f}')
plt.legend([f'{total_sources_below} menores que a média',f'{hydro_Eua_num-total_sources_below} maiores ou igual a Média'] ,bbox_to_anchor=(1.6, 0.9))
plt.show()