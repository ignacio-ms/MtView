function exp_visibility() {
    const experiment_div = document.getElementById('experiment-div');
    const pae_div = document.getElementById('pae-div');
    const pae_legend_div = document.getElementById('pae-info-div');
    const efp_legend_div = document.getElementById('efp-leg-div');
    const interaction_legend_div = document.getElementById('interaction-legend-div');

    const radio_bttns = document.querySelectorAll('input[name="window-rb"]');
    for (const btt of radio_bttns){
        if (btt.value === 'boxplot'){
            experiment_div.style.visibility = btt.checked ? "visible" : "hidden";
            experiment_div.style.height = btt.checked ? "auto" : 0;
        }

        if (btt.value === 'molecule'){
            pae_div.style.visibility = btt.checked ? "visible" : "hidden";
            pae_div.style.height = btt.checked ? "auto" : 0;
            pae_legend_div.style.visibility = btt.checked ? "visible" : "hidden";
            pae_legend_div.style.height = btt.checked ? "auto" : 0;
        }

        if (btt.value === 'eFP'){
            efp_legend_div.style.visibility = btt.checked ? "visible" : "hidden";
            efp_legend_div.style.height = btt.checked ? "auto" : 0;
        }

        if (btt.value === 'interactions'){
            reformat_graph();

            interaction_legend_div.style.visibility = btt.checked ? "visible" : "hidden";
            interaction_legend_div.style.height = btt.checked ? "auto" : 0;
        }
    }
}
