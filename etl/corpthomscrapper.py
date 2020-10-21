import csv
import requests
from lxml import html
import re
import json
import pandas

df = pandas.read_csv('Corpus Thomisticum Sites.csv')


x = df

print(x)

output_list = []

for index, row in x.iterrows():
    header = row['Main Header']
    subhead1= row['Subheader 1']
    subhead2 = row['Subheader 2']
    section = row['Section']
    site = row['site']
    
    
    page = requests.get(site)
    tree = html.fromstring(page.content)
        
    sections = tree.findall('.//span[@class="ref"]')
    
    for s in sections:
        grandparent = s.getparent().getparent()
        section_index = s.text
        content = ''.join(list(grandparent.itertext())[1:])
        output_list.append([header, subhead1, subhead2, section, site, section_index, content])
        
df_out = pandas.DataFrame(output_list, columns = ['Main Header', 'Subheader 1', 'Subheader 2', 'Section', 'site', 'Section Index', 'Content'])

df_out.to_csv("corp_out.csv")
