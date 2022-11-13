$(document).ready(function () {
    $('#efp-leg-div').change(function () {
        let selected_btt;
        const radio_bttns = document.querySelectorAll('input[name="efp-mode-rb"]');
        for (const btt of radio_bttns){
            if (btt.checked){
                selected_btt = btt;
                break;
            }
        }

        $.ajax({
            url: '/efp',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                    'norm_selected': selected_btt.value
            }),
            success: function (data) {
                Plotly.newPlot('efp-leg-plot-div', JSON.parse(data['plot']));

                const colors = JSON.parse(data['colors']);
                for (const id in colors){
                    let tissue_path = document.getElementById(id);
                    tissue_path.style.fill = colors[id];
                }

                const vals = JSON.parse(data['vals']);
                for (const id in vals){
                    let val_path = document.getElementById(id + '_tip');
                    val_path.textContent = val_path.textContent.replace(/-?\d+\.\d+/g, vals[id]);
                    console.log(val_path.textContent);
                }

                efp_hover();
            }
        });
    })
})
