from bs4 import BeautifulSoup
import urllib
from distutils.filelist import findall
import requests
from lxml import etree
Taxon_to_Accession_id = {}
taxon_id = [29292]
url='https://www.ncbi.nlm.nih.gov/genome/?term=txid29292%5BOrganism:noexp%5D'
res=requests.get('https://www.ncbi.nlm.nih.gov/genome/?term=txid' + str(taxon_id[0])+'[Organism:noexp]', timeout=1000)
errors2 = []
html = res.text.encode('utf-8')
xp = etree.HTML(html)
table = xp.xpath('//table[@class="GenomeList2"]')
if table:
    host_ncid=table[0].xpath('tbody/tr[1]/td[3]/a/text()')[0]
    print(host_ncid)



# /html/body/div[1]/div[1]/form/div[1]/div[4]/div/div[5]/div/div[2]/table[2]/tbody/tr/td/div[3]/div/div/div/table/tbody/tr[1]/td[3]/a

# soup = BeautifulSoup(contents, "html.parser")
# # print(soup)
# m_name = []
# if soup.find_all('table', class_='GenomeList2') == []:
#     errors2.append(str(taxon_id)+'\n')
# else:
#     for tag in soup.find_all('table', class_='GenomeList2'):
#         mm = tag.find('tbody')
#         for ii in mm.findAll('a', target='_blank'):
#             m_name.append(ii.contents[0])
#         for m in m_name:
#             if m != '.':
#                 Taxon_to_Accession_id[taxon_id[0]] = str(m)
#                 break
# print(Taxon_to_Accession_id)
# print(m_name)
