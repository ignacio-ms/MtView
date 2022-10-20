function display_molecule(pdb) {
    let elem = $('#af-container');
    let config = { backgroundColor: 'white' };
    let viewer = $3Dmol.createViewer(elem, config);

    let color_scale = [];
    color_scale.push({r:0,g:83,b:214});
    color_scale.push({r:101,g:203,b:243});
    color_scale.push({r:255,g:219,b:19});
    color_scale.push({r:255,g:125,b:69});

    viewer.addModel(pdb, "pdb");
    viewer.setStyle({},
        {
            'cartoon': {
                'colorscheme': {
                    'prop':'b',
                    'gradient': 'roygb'
                    ,'min':50,'max':90
                },
                'arrows': true
            }
        }
    );
    viewer.zoomTo();
    viewer.render();
    viewer.zoom(1, 1000);
}