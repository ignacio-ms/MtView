experiments = ['SRP362799', 'ERP126041', 'SRP013555', 'SRP139359', 'SRP212693', 'SRP159219', 'SRP230996', 'SRP363570', 'SRP161571', 'SRP189439']
norm_methods = ['log2_tmm', 'tmm']

del_list = [
    r' \(.*?\)', r' \[.*?\]', r' \{.*?\}',
    'FUNCTION: ', 'TISSUE SPECIFICITY: ', 'INDUCTION: ', 'SUBCELLULAR LOCATION: '
]

colors = ['slategray', '#ffa400', 'crimson']

analysis_tools = {
    'Taxonomy': 'taxonomy', 'Expression values': 'boxplot',
    'eFP': 'eFP', 'Molecule viewer': 'molecule'
}

img_labels = [
    'flower', 'leaf_bud', 'leaf', 'petiole', 'stem', 'root',
    'small_pod', 'medium_pod', 'large_pod',
    'mature_nodule', 'nodule_4d', 'nodule_10d', 'nodule_14d', 'nodule_0d',
    'nitrate_nodule_12h', 'nitrate_nodule_48h',
]

color_scale = ['#0053D6', '#ECF3FD']
