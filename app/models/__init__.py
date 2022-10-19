from app.models import efp, taxonomy, molecule


taxonomy = taxonomy.Taxonomy()
taxonomy.set_gene_names()

efp = efp.efp()
molecule = molecule.Molecule()
