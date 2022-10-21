function display_molecule(pdb) {
    let elem = $('#af-container');
    let config = { backgroundColor: 'white', lowerZoomLimit:50, upperZoomLimit: 500 };
    let viewer = $3Dmol.createViewer(elem, config);
    let rendering = false;
    let skip = false;

    const pae_colorscheme = function (atom) {
        if (atom.b >= 90)
            return '#0053D6'
        else if (atom.b < 90 && atom.b >= 70)
            return '#65CBF3';
        else if (atom.b < 70 && atom.b >= 50)
            return '#FFDB13';
        return '#FF7D45';
    }

    const glob_model = viewer.addModel(pdb, "pdb", {keepH: true, assignBonds: true});
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
        if (rendering){
            viewer.setStyle({}, {'cartoon': {colorfunc: pae_colorscheme, 'arrows': true}});

            const prev_model = viewer.getModel(1);
            if (prev_model.selectedAtoms({resi: atom.resi}).length !== 0){
                viewer.zoomTo({}, 500);
                viewer.zoom(1, 1000);

                rendering = false;
                skip = true;
                viewer.render();
            }
            viewer.removeModel(1);
        }
        if (!skip){
            rendering = true;

            const new_atoms = viewer.selectedAtoms({resi: atom.resi, expand: 7});
            const model = viewer.addModel();
            model.addAtoms(new_atoms);
            model.setStyle({}, {stick: {radius: .15}, sphere: {radius: .2}});

            viewer.enableFog(true);
            glob_model.setStyle({resi: atom.resi, expand: 7}, {'cartoon': {colorfunc: pae_colorscheme, 'arrows': true, opacity: .85}});
            viewer.zoomTo({resi: atom.resi, expand: 7}, 700);
            viewer.render();
        }
        skip = false;
    });
    viewer.setHoverable({}, true,
        function(atom,viewer) {
           if(!atom.label) {
                atom.label = viewer.addLabel(atom.resn + ": " + atom.atom + '\n' + atom.b + '% confident', {position: atom, backgroundColor: 'mintcream', fontColor:'black'});
           }
       },
       function(atom) {
           if(atom.label) {
                viewer.removeLabel(atom.label);
                delete atom.label;
           }
        }
    );
    viewer.render();
    viewer.zoom(1, 1000);
}