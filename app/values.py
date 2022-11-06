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
    'intra_nodule'
]

cmap = [
    '#ffffff', '#ffff00', '#ffee00', '#ffdd00', '#ffcc00',
    '#ffbb00', '#ffaa00', '#ff9900', '#ff8800', '#ff7700',
    '#ff6600', '#ff5500', '#ff4400', '#ff3300', '#ff2200',
    '#ff1100', '#ff0000',
]

color_scale = ['#0053D6', '#ECF3FD']
