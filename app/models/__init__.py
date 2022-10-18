from app.models import efp, taxonomy


taxonomy = taxonomy.Taxonomy()
taxonomy.set_gene_names()

efp = efp.efp()
