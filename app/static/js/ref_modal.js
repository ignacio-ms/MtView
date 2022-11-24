function open_modal() {
    const modal = document.getElementById('citation-modal');
    const body = document.getElementById('citation-modal-body');
    const span = document.getElementById('modal-close');

    const radio_bttns = document.querySelectorAll('input[name="window-rb"]');
    for (const btt of radio_bttns){
        switch (btt.value) {
            case 'taxonomy':
                if (btt.checked){
                    body.innerHTML = "The data came from UniProt" +
                        "<a href='https://www.uniprot.org/uniprot/G7KTP8_MEDTR' target='_blank'>" +
                        "    <img src='https://version-11-5.string-db.org/images/uniprot_logo_small.png' width='42' height='19' style='vertical-align:middle;border:0;' alt='UniProt'>" +
                        '</a><br>'+
                        "<br>"+
                        "Citation<br>"+
                        "Authot: The UniProt Consortium<br>"+
                        "Title: UniProt: the universal protein knowledgebase in 2021<br>"+
                        "In:49.D1(2020) - pp:D480-D489<br>"+
                        "<a href='https://academic.oup.com/nar/article/49/D1/D480/6006196' style='font-style: italic' target='_blank'>Ref</a><br>"+
                        "<br>"+
                        "<div id='cc-license-div' style='position: absolute; bottom: 10px; right: 10px'>"+
                        "    <a href='https://creativecommons.org/licenses/by/4.0/' target='_blank'>"+
                        "        <img src='../static/SVGs/ccby.svg' alt='ccvy'>"+
                        "        </a>"+
                        "</div>";
                }
                break;

            case 'boxplot':
                if (btt.checked){
                    body.innerHTML = "The data came from MtExpress"+
                        "<a href='https://medicago.toulouse.inrae.fr/MtExpress' target='_blank'>"+
                        "    <img src='../static/SVGs/mtexpress_logo.png' width='42' height='19' style='vertical-align:middle;border:0;' alt='MtExpress'>"+
                        "</a><br>"+
                        "<br>"+
                        "Citation<br>"+
                        "Authot: Sebastien Carrere<br>"+
                        "Title: MtExpress, a Comprehensive and Curated RNAseq-based Gene Expression Atlas for the Model Legume Medicago truncatula<br>"+
                        "In:62.9(2021) - pp:1494-1500<br>"+
                        "<a href='https://doi.org/10.1093/pcp/pcab110' style='font-style: italic' target='_blank'>Ref</a><br>"+
                        "<br>"+
                        "Data based on RNA-seq experiments aged from 2013 to 2022, normalized in both tmm and log2_tmm normalization methods."+
                        "<br>"+
                        "<div id='cc-license-div' style='position: absolute; bottom: 10px; right: 10px'>"+
                        "    <a href='https://creativecommons.org/licenses/by/4.0/' target='_blank'>"+
                        "        <img src='../static/SVGs/ccby.svg' alt='ccvy'>"+
                        "    </a>"+
                        "</div>";
                }
                break;

            case 'eFP':
                if (btt.checked){
                    body.innerHTML = "The data came from MtSSPdb"+
                        "<a href='https://mtsspdb.zhaolab.org/atlas-internal/3880/transcript/profile/0' target='_blank'>"+
                        "    <img src='../static/SVGs/nri_logo.png' width='42' height='19' style='vertical-align:middle;border:0;' alt='NRI'>"+
                        "</a><br>"+
                        "<br>"+
                        "Noble Research Institute<br>"+
                        "Developed by The Zao Bioinformatics Lab<br><br>"+
                        "Data downloaded in raw counts and self normalized in tmm and log2_tmm normalization methods using edgeR."+
                        "<br>";
                }
                break;

            case 'molecule':
                if (btt.checked){
                    body.innerHTML = "The data came from AlphafoldDB"+
                        "<a href='https://alphafold.com/' target='_blank'>"+
                        "    <img src='../static/SVGs/ap_logo.png' width='70' height='19' style='vertical-align:middle;border:0;' alt='Alphafold'>"+
                        "</a><br>"+
                        "<br>"+
                        "DB Citation<br>"+
                        "Authot: Mihaly Varadi<br>"+
                        "Title: AlphaFold Protein Structure Database: massively expanding the structural coverage of protein-sequence space with high-accuracy models<br>"+
                        "In:50.D1(2022) - pp:D439-D444<br>"+
                        "<a href='https://doi.org/10.1093/nar/gkab1061' style='font-style: italic' target='_blank'>Ref</a><br>"+
                        "<br>"+
                        "Method Citation<br>"+
                        "Authot: John Jumper<br>"+
                        "Title: Highly accurate protein structure prediction with AlphaFold<br>"+
                        "In:596(2021) - pp:583-589<br>"+
                        "<a href='https://doi.org/10.1038/s41586-021-03819-2' style='font-style: italic' target='_blank'>Ref</a><br>"+
                        "<br>"+
                        "AI prediction method using DeepLearning techniques.<br>"+
                        "Data downloaded from AlphafoldDB (.pdb) and displayed using 3DMol library."+
                        "<br>"+
                        "<div id='cc-license-div' style='position: absolute; bottom: 10px; right: 10px'>"+
                        "   <a href='https://creativecommons.org/licenses/by/4.0/' target='_blank'>"+
                        "       <img src='../static/SVGs/ccby.svg' alt='ccvy'>"+
                        "   </a>"+
                        "</div>";
                }
                break;

            case 'interactions':
                if (btt.checked){
                    body.innerHTML = "The data came from STRING"+
                        "<a href='https://string-db.org/cgi/input?sessionId=benin4UPqn31&input_page_show_search=on' target='_blank'>"+
                        "    <img src='../static/SVGs/string_logo.png' width='70' height='19' style='vertical-align:middle;border:0;' alt='STRING'>"+
                        "</a><br>"+
                        "<br>"+
                        "Citation<br>"+
                        "Authot: Damian Szklarczyk<br>"+
                        "Title: STRING v11: protein-protein association networks with increased coverage, supporting functional discovery in genome-wide experimental datasets<br>"+
                        "In:47.D1(2019) - pp:D607-D613<br>"+
                        "<a href='https://doi.org/10.1093/nar/gky1131' style='font-style: italic' target='_blank'>Ref</a><br>"+
                        "<br>"+
                        "<div id='cc-license-div' style='position: absolute; bottom: 10px; right: 10px'>"+
                        "    <a href='https://creativecommons.org/licenses/by/4.0/' target='_blank'>"+
                        "        <img src='../static/SVGs/ccby.svg' alt='ccvy'>"+
                        "    </a>"+
                        "</div>";
                }
                break;
        }
    }

    modal.style.display = "block";
    span.onclick = function () { modal.style.display = "none"; }

    window.addEventListener('click', function (event) {
        if (event.target === modal) modal.style.display = "none";
    });
}