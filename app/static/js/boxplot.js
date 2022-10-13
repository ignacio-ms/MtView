$(document).ready(function () {
    $('#experiment-div').change(function () {

        let selected_btt;
        const radio_bttns = document.querySelectorAll('input[name="mode-rb"]');
        for (const btt of radio_bttns){
            if (btt.checked){
                selected_btt = btt;
                break;
            }
        }

        let selected_exps = [];
        $('#experiments-dd option').each(function (i) {
            if (this.selected === true){
                selected_exps.push(this.value);
            }
        })

        $.ajax({
            url: '/boxplot',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                    'exp_selected': selected_exps,
                    'norm_selected': selected_btt.value
            }),
            success: function (data) {
                Plotly.newPlot('boxplot-div', data);
            }
        });
    })
})
