from app.models import efp, taxonomy, molecule


taxonomy = taxonomy.Taxonomy()
taxonomy.set_experiments()
taxonomy.set_gene_names()
taxonomy.get_dataset_info()

efp = efp.efp(taxonomy)
efp.read_tissues()
efp.read_symbiosis()

molecule = molecule.Molecule()
