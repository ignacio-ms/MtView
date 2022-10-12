from app.models import efp, taxonomy


taxonomy = taxonomy.Taxonomy()
efp = efp.efp()
efp.read_data()
