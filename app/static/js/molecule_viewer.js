function display_molecule(pdb) {
    let elem = $('#af-container');
    let config = { backgroundColor: 'white' };
    let viewer = $3Dmol.createViewer(elem, config);

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