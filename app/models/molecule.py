import requests
import py3Dmol


accession_id = 'A0A396IUP1'
pymol_url = f'https://3dmol.csb.pitt.edu/viewer.html?url=https://alphafold.ebi.ac.uk/files/AF-{accession_id}-F1-model_v3.pdb'
pymol_url_comp = f'https://3dmol.csb.pitt.edu/viewer.html?url=https://alphafold.ebi.ac.uk/files/AF-{accession_id}-F1-model_v3.pdb&select=all&style=cartoon:style~rectangle,color~spectrum,arrows~true;line:hidden~true,linewidth~5,colorscheme~Jmol;stick:hidden~true'
url = f'https://alphafold.ebi.ac.uk/files/AF-{accession_id}-F1-model_v3.pdb'
res = requests.get(url)
