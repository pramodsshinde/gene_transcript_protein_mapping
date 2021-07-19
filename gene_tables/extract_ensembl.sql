### MYSQL ENSEMBL 90

### Retrieve Gene table
select g.biotype, g.seq_region_strand, g.seq_region_start, g.seq_region_end, 
CONCAT(g.stable_id,'.' ,g.version) AS versioned_ensembl_gene_id, g.description, g.canonical_transcript_id, x.display_label 
from gene g join xref x on g.display_xref_id=x.xref_id where g.stable_id like 'ENS%';


### Retrieve gene synonyms
select CONCAT(stable_id,'.',version) AS versioned_ensembl_gene_id, group_concat(syns.synonym) as synonym
from( select g.stable_id, g.version, s.synonym from
xref x, external_synonym s, gene g, xref x2
where g.display_xref_id = x2.xref_id
and x.xref_id = s.xref_id
and x.display_label = x2.display_label) syns group by stable_id;

### Retrive Entrez id : HGNC
select dbprimary_acc, display_label from xref where external_db_id=1300;