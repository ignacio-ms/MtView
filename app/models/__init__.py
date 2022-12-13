from app.models import efp, taxonomy, molecule, expression


taxonomy = taxonomy.Taxonomy()
taxonomy.set_gene_names()

expression = expression.Expression()
expression.set_experiments()
expression.get_dataset_info()

efp = efp.efp(expression)
efp.read_tissues()

molecule = molecule.Molecule()
