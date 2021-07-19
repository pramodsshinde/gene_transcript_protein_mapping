import sys
import pandas as pd

df_gene = pd.read_csv("ensembl90_Gene_HGNC.csv")
df_syno = pd.read_csv("ensembl90_synonyms.csv")
df_summary = pd.read_csv("entrez_gene_summary.csv")


#print(df_summary)
#print(df_gene)
#print(df_syno)

df_temp = df_gene.merge(df_syno, on='versioned_ensembl_gene_id', how='left')
#print(df_temp)

df_final = df_temp.merge(df_summary, on='display_label', how='left')

df_final.to_csv('Ensembl_Gene_Mapping.tsv', index=False,  sep ='\t')