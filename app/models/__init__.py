from app.models import efp, taxonomy, molecule


taxonomy = taxonomy.Taxonomy()
taxonomy.set_experiments()
taxonomy.set_gene_names()
taxonomy.get_dataset_info()

efp = efp.efp()
molecule = molecule.Molecule()
