function display_molecule(pdb) {
    let elem = $('#af-container');
    let config = { backgroundColor: 'white' };
    let viewer = $3Dmol.createViewer(elem, config);
    let rendering = false;

    const pae_colorscheme = function (atom) {
        if (atom.b >= 90)
            return '#0053D6'
        else if (atom.b < 90 && atom.b >= 70)
            return '#65CBF3';
        else if (atom.b < 70 && atom.b >= 50)
            return '#FFDB13';
        return '#FF7D45';
    }

    viewer.addModel(pdb, "pdb");
    viewer.setStyle({},
        {
            'cartoon': {
                colorfunc: pae_colorscheme,
                'arrows': true
            }
        }
    );
    viewer.zoomTo();
    viewer.setClickable({}, true, function (atom, _viewer, _event, _container) {
        if (rendering)
            viewer.removeModel(viewer.getModel());
        rendering = true;

        const new_atoms = viewer.selectedAtoms({resi: atom.resi, expand: 10});
        const model = viewer.addModel();
        model.addAtoms(new_atoms);
        model.setStyle({}, {stick: {radius: .15}});

        viewer.enableFog(true);
        viewer.zoomTo({resi: atom.resi, expand: 10}, 1000);
        viewer.render();
    });
    viewer.enableContextMenu({}, true);
    viewer.render();
    viewer.zoom(1, 1000);
}