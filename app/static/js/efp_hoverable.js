function efp_hover() {
    const efp_legend = document.getElementById('efp-leg-plot-div');
    let prev_colors;

    efp_legend.on('plotly_hover', function (data) {
        const selected = data.points[0].data.marker.color;
        prev_colors = {
            'flower_fill': document.getElementById('flower_fill').style.fill,
            'leaf_bud_fill': document.getElementById('leaf_bud_fill').style.fill,
            'leaf_fill': document.getElementById('leaf_fill').style.fill,
            'petiole_fill': document.getElementById('petiole_fill').style.fill,
            'stem_fill': document.getElementById('stem_fill').style.fill,
            'root_fill': document.getElementById('root_fill').style.fill,
            'small_pod_fill': document.getElementById('small_pod_fill').style.fill,
            'medium_pod_fill': document.getElementById('medium_pod_fill').style.fill,
            'large_pod_fill': document.getElementById('large_pod_fill').style.fill,
            'mature_nodule_fill': document.getElementById('mature_nodule_fill').style.fill,
            'nodule_4d_fill': document.getElementById('nodule_4d_fill').style.fill,
            'nodule_10d_fill': document.getElementById('nodule_10d_fill').style.fill,
            'nodule_14d_fill': document.getElementById('nodule_14d_fill').style.fill,
            'nodule_0d_fill': document.getElementById('nodule_0d_fill').style.fill,
            'nitrate_nodule_12h_fill': document.getElementById('nitrate_nodule_12h_fill').style.fill,
            'nitrate_nodule_48h_fill': document.getElementById('nitrate_nodule_48h_fill').style.fill,
            // 'intra_nodule_fill': document.getElementById('intra_nodule_fill').style.fill
        };

        for (let tissue in prev_colors){
            if (selected === '#ffffff') break;
            if (rgb2hex(prev_colors[tissue]) !== selected){
                document.getElementById(tissue).style.fill = '#ffffff';
            }
        }

    }).on('plotly_unhover', function () {
        for (let tissue in prev_colors){
            document.getElementById(tissue).style.fill = prev_colors[tissue];
        }
    });
}

function rgb2hex(rgb) {
    rgb = rgb.slice(
        rgb.indexOf("(") + 1,
        rgb.indexOf(")")
    ).split(", ");

    return "#" + (1 << 24 | rgb[0] << 16 | rgb[1] << 8 | rgb[2]).toString(16).slice(1);
}
