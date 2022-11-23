norm_methods = ['log2_tmm', 'tmm']

del_list = [
    r' \(.*?\)', r' \[.*?\]', r' \{.*?\}',
    'FUNCTION: ', 'TISSUE SPECIFICITY: ', 'INDUCTION: ', 'SUBCELLULAR LOCATION: '
]

synonymous_ds = {
    'IMGA-Mt3.5.5-gene': 'v3.5',
    'JCVI-Mt4.0v2-gene': 'v4',
}

colors = ['slategray', '#ffa400', 'crimson']

analysis_tools = {
    'Taxonomy': 'taxonomy', 'Experiments': 'boxplot',
    'eFP': 'eFP', 'Molecule viewer': 'molecule', 'Interactions': 'interactions'
}

img_labels = [
    'flower', 'leaf_bud', 'leaf', 'petiole', 'stem', 'root',
    'small_pod', 'medium_pod', 'large_pod',
    'mature_nodule', 'nodule_4d', 'nodule_10d', 'nodule_14d', 'nodule_0d',
    'nitrate_nodule_12h', 'nitrate_nodule_48h',
]

null_img_labels = [
    'flower', 'leaf_bud', 'leaf', 'petiole', 'stem', 'root',
    'small_pod', 'medium_pod', 'large_pod'
]

color_scale = ['#0053D6', '#ECF3FD']

experiments = {
    'SRP371731': 'Tyrohova et. al.',
    'SRP220100': 'Hu et. al.',
    'SRP104107': 'Duan et. al.',
    'SRP201527': 'Man Ha et. al.',
    'SRP159219': 'Zhou et. al.',
    'SRP013555': 'Donà et. al.',
    'SRP306387': 'Dong et. al.',
    'SRP158577': 'Thomson et. al.',
    'SRP359128': 'Dong et. al.',
    'SRP149658': 'Cui et. al.',
    'SRP373618': 'Mahmood et. al.',
    'SRP348127': 'Kong et. al.',
    'SRP274101': 'Cheng et. al.',
    'SRP089710': 'Vu et. al.',
    'SRP290966': 'Chen et. al.',
    'SRP271410': 'Zinsmeister et. al.',
    'SRP109847': 'C de Bang et. al.',
    'SRP110041': 'C de Bang et. al.',
    'SRP098557': 'Liu et. al.',
    'SRP065519': 'Thatcher et. al.',
    'SRP261071': 'Camborde et. al.',
    'ERP010262': 'Mertens et. al.',
    'SRP166446': 'Pollier et. al.',
    'SRP161571': 'Boschiero et. al.',
    'ERP119454': 'Pollier et. al.',
    'SRP337984': 'Roy et. al.',
    'SRP276838': 'Wang et. al.',
    'SRP043103': 'Camps et. al.',
    'SRP097705': 'Feng et. al.',
    'SRP057298': 'Tang et. al.',
    'SRP189439': 'Fernández et. al.',
    'SRP099836': 'Luginbuehl et. al.',
    'SRP108590': 'Zeng et. al.',
    'SRP230996': 'karlo et. al.',
    'SRP372556': 'Cope et. al.',
    'SRP198429': 'Müller et. al.',
    'SRP275813': 'Wang et. al.',
    'SRP362799': 'Volpe et. al.',
    'SRP098561': 'García et. al.',
    'SRP078249': 'Afkhami et. al.',
    'SRP057198': 'Damiani et. al.',
    'SRP058185': 'Jardinaud et. al.',
    'SRP018396': 'Rose et. al.',
    'SRP050577': 'Larrainzar et. al.',
    'SRP187226': 'Poehlman et. al.',
    'SRP212795': 'traubenik et. al.',
    'SRP273143': 'Knaack et. al.',
    'SRP239907': 'Dong et. al.',
    'ERP105151': 'van Zeijl. al.',
    'SRP316040': 'Chakraborty et. al.',
    'ERP126011': 'Pervent et. al.',
    'ERP126041': 'Pervent et. al.',
    'ERP126042': 'Pervent et. al.',
    'SRP212693': 'Schiessl et. al.',
    'CNP0000354': 'Zhu et. al.',
    'SRP214687': 'Gao et. al.',
    'SRP009893': 'Boscari et. al.',
    'SRP028599': 'Roux et. al.',
    'SRP065884': 'Satgé et. al.',
    'SRP106216': 'Deng et. al.',
    'SRP290154': 'Xu et. al.',
    'SRP329890': 'Liu et. al.',
    'SRP124849': 'Trujillo et. al.',
    'SRP302539': 'Li et. al.',
    'SRP349933': 'Jardinaud et. al.',
    'SRP361663': 'Yu et. al.',
    'SRP349926': 'Jardinaud et. al.',
    'SRP139359': 'Michno et. al.',
    'SRP284140': 'Wang et. al.',
    'SRP077692': 'Michno et. al.',
    'ERP118927': 'Lambert et. al.',
    'SRP110143': 'C de Bang et. al.',
    'SRP363570': 'Sauviac et. al.',
    'SRP200112': 'Cui et. al.',
    'SRP186731': 'Sanko-Sawczenko et. al.',
    'SRP263069': 'Achom et. al.',
    'SRP229031': 'Benezech et. al.'
}
