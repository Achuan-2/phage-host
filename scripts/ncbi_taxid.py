from ete3 import NCBITaxa
from Bio import Entrez
Entrez.email = "achuan-2@outlook.com"


ncbi = NCBITaxa()


def get_desired_ranks(taxid, desired_ranks):
    lineage = ncbi.get_lineage(taxid)
    lineage2ranks = ncbi.get_rank(lineage)
    ranks2lineage = dict((rank, taxid)
                         for (taxid, rank) in lineage2ranks.items())
    print(ranks2lineage)
    return {'{}_id'.format(rank): ranks2lineage.get(rank, '<not present>') for rank in desired_ranks}


def get_taxid(name):
    ncbi = NCBITaxa()
    id = ncbi.get_name_translator([name])[name][-1]
    return id

# def main(taxids, desired_ranks, path):
#     with open(path, 'w') as csvfile:
#         fieldnames = ['{}_id'.format(rank) for rank in desired_ranks]
#         writer = csv.DictWriter(csvfile, delimiter='\t', fieldnames=fieldnames)
#         writer.writeheader()
#         for taxid in taxids:
#             writer.writerow(get_desired_ranks(taxid, desired_ranks))


if __name__ == '__main__':
    # taxids = [1204725, 2162,  1300163, 420247]
    host_name = 'Alkalihalobacillus alcalophilus ATCC 27647 = CGMCC 1.3604'
    taxid = get_taxid(host_name)
    print(taxid)
    desired_ranks = ['superkingdom', 'phylum', 'class',
                    'order', 'family', 'genus', 'species','stain']
    
    lineage = get_desired_ranks(taxid, desired_ranks)
    print(get_desired_ranks(taxid, desired_ranks))

    # print(get_taxid('Synechococcus sp. WH8109'))
    # main(taxids, desired_ranks, path)




# def get_tax_id(species):
#     """to get data from ncbi taxomomy, we need to have the taxid. we can
#     get that by passing the species name to esearch, which will return
#     the tax id"""
#     species = species.replace(' ', "+").strip()
#     search = Entrez.esearch(term=species, db="taxonomy", retmode="xml")
#     record = Entrez.read(search)
#     return record['IdList'][0]


# def get_tax_data(taxid):
#     """once we have the taxid, we can fetch the record"""
#     search = Entrez.efetch(id=taxid, db="taxonomy", retmode="xml")
#     return Entrez.read(search)

# species_list = ['Helicobacter pylori 26695', 'Thermotoga maritima MSB8', 'Deinococcus radiodurans R1', 'Treponema pallidum subsp. pallidum str. Nichols', 'Aquifex aeolicus VF5', 'Archaeoglobus fulgidus DSM 4304']

# taxid_list = [] # Initiate the lists to store the data to be parsed in
# data_list = []
# lineage_list = []

# print('parsing taxonomic data...') # message declaring the parser has begun

# for species in species_list:
#     print ('\t'+species) # progress messages

#     taxid = get_tax_id(species) # Apply your functions
#     data = get_tax_data(taxid)
#     lineage = {d['Rank']:d['ScientificName'] for d in data[0]['LineageEx'] if d['Rank'] in ['phylum']}

#     taxid_list.append(taxid) # Append the data to lists already initiated
#     data_list.append(data)
#     lineage_list.append(lineage)

# print('complete!')
# print(lineage_list)
