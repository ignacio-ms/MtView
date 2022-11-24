function exp_visibility() {
    const experiment_div = document.getElementById('experiment-div');
    const pae_div = document.getElementById('pae-div');
    const pae_legend_div = document.getElementById('pae-info-div');
    const efp_legend_div = document.getElementById('efp-leg-div');
    const interaction_legend_div = document.getElementById('interaction-legend-div');

    const ccby_div = document.getElementById('cc-license-div');
    const ccby_ref = document.getElementById('cc-references');

    const radio_bttns = document.querySelectorAll('input[name="window-rb"]');
    for (const btt of radio_bttns){
        if (btt.value === 'taxonomy' && btt.checked){
            ccby_div.style.display = "grid";
            ccby_ref.innerHTML = "<a href='https://academic.oup.com/nar/article/49/D1/D480/6006196' target='_blank' style='font-style: italic'>UniProt</a>";
        }

        if (btt.value === 'boxplot'){
            experiment_div.style.display = btt.checked ? "block" : "none";
            experiment_div.style.height = btt.checked ? "auto" : 0;

            if (btt.checked) ccby_div.style.display = "none";
        }

        if (btt.value === 'molecule'){
            pae_div.style.display = btt.checked ? "block" : "none";
            pae_div.style.height = btt.checked ? "auto" : 0;

            pae_legend_div.style.display = btt.checked ? "block" : "none";
            pae_legend_div.style.height = btt.checked ? "auto" : 0;

            if (btt.checked){
                ccby_div.style.display = "grid";
                ccby_ref.style.display = "grid";
                ccby_ref.innerHTML = "" +
                    "<a href='https://doi.org/10.1038/s41586-021-03819-2' target='_blank' style='font-style: italic'>Alphafold</a>" +
                    "<a href='https://doi.org/10.1093/nar/gkab1061' target='_blank' style='font-style: italic'>AlphafoldDB</a>";
            }
        }

        if (btt.value === 'eFP'){
            efp_legend_div.style.display = btt.checked ? "block" : "none";
            efp_legend_div.style.height = btt.checked ? "auto" : 0;

            if (btt.checked) ccby_div.style.display = "none";
        }

        if (btt.value === 'interactions'){
            interaction_legend_div.style.display = btt.checked ? "block" : "none";
            interaction_legend_div.style.height = btt.checked ? "auto" : 0;

            if (btt.checked){
                ccby_div.style.display = "grid";
                ccby_ref.innerHTML = "<a href='https://doi.org/10.1093/nar/gky1131' target='_blank' style='font-style: italic'>STRING</a>";
            }
        }
    }
}
