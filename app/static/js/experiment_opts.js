function exp_visibility() {
    const experiment_div = document.getElementById('experiment-div');
    const radio_bttns = document.querySelectorAll('input[name="window-rb"]');
    for (const btt of radio_bttns){
        if (btt.value === 'boxplot'){
            experiment_div.style.visibility = btt.checked ? "visible" : "hidden";
            break;
        }
    }
}
