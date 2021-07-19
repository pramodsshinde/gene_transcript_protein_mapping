from Bio import Entrez
import sys
import pandas as pd

Entrez.email = "pshinde@lji.org"

def retrieve_annotation(id_list):

    """Annotates Entrez Gene IDs using Bio.Entrez, in particular epost (to
    submit the data to NCBI) and esummary to retrieve the information.
    Returns a list of dictionaries with the annotations."""

    request = Entrez.epost("gene", id=",".join(id_list))
    try:
        result = Entrez.read(request)
    except RuntimeError as e:
        # FIXME: How generate NAs instead of causing an error with invalid IDs?
        print("An error occurred while retrieving the annotations.")
        print("The error returned was" + e)
        sys.exit(-1)

    webEnv = result["WebEnv"]
    queryKey = result["QueryKey"]
    data = Entrez.esummary(db="gene", webenv=webEnv, query_key=queryKey)
    annotations = Entrez.read(data)

    print("Retrieved " + str(len(annotations)) +" annotations for  " + str(len(id_list)) + "  genes")

    return(annotations)

def print_data(annotation):
    for gene_data in annotation:
        #print(gene_data)
        gene_id = gene_data["Id"]
        gene_symbol = gene_data["NomenclatureSymbol"]
        gene_name = gene_data["Description"]

        print(
            gene_id,
            gene_symbol,
            gene_name,
        )


df_entrez_file = pd.read_csv("ensembl90_Entrez.csv")
entrez_ids = df_entrez_file['dbprimary_acc'].tolist()
entrez_ids  = [str(x) for x in entrez_ids ]

## Breaks array into sub-arrays
arr = [entrez_ids[i:i + 10000] for i in range(0, len(entrez_ids), 10000)]

lst = []
for list in arr:

    records = retrieve_annotation(list)

    for record in records["DocumentSummarySet"]['DocumentSummary']:
        
        gene_id = record.attributes['uid']
        gene_summary = ''

        if record['Summary'][0:12] != 'DISCONTINUED':
            gene_summary = record['Summary']
        
        val = {'gene_id': int(gene_id), 'gene_summary': gene_summary}
        lst.append(val)


df_annotation = pd.DataFrame(lst, columns=['gene_id', 'gene_summary'])
df_summary = df_entrez_file.merge(df_annotation, left_on='dbprimary_acc', right_on='gene_id')

df_summary.drop(columns=['gene_id'])
df_summary.to_csv('entrez_gene_summary.csv', index=False)