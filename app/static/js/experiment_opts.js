function exp_visibility() {
    const experiment_div = document.getElementById('experiment-div');
    const pae_div = document.getElementById('pae-div');
    const pae_legend_div = document.getElementById('pae-info-div');
    const efp_legend_div = document.getElementById('efp-leg-div');
    const interaction_legend_div = document.getElementById('interaction-legend-div');

    const radio_bttns = document.querySelectorAll('input[name="window-rb"]');
    for (const btt of radio_bttns){
        switch (btt.value) {
            case 'boxplot':
                experiment_div.style.display = btt.checked ? "block" : "none";
                experiment_div.style.height = btt.checked ? "auto" : 0;
                break;

            case 'eFP':
                efp_legend_div.style.display = btt.checked ? "block" : "none";
                efp_legend_div.style.height = btt.checked ? "auto" : 0;
                break;

            case 'molecule':
                pae_div.style.display = btt.checked ? "block" : "none";
                pae_div.style.height = btt.checked ? "auto" : 0;

                pae_legend_div.style.display = btt.checked ? "block" : "none";
                pae_legend_div.style.height = btt.checked ? "auto" : 0;
                break;

            case 'interactions':
                interaction_legend_div.style.display = btt.checked ? "block" : "none";
                interaction_legend_div.style.height = btt.checked ? "auto" : 0;
                break;
        }
    }
}
