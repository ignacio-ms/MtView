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
        viewer.setStyle({}, {'cartoon': {colorfunc: pae_colorscheme, 'arrows': true}});
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

            let new_atoms = [];
            let new_atoms_resi = [];

            const new_selection = viewer.selectedAtoms({resi: atom.resi, expand: 5});
            new_selection.forEach(function (atom) {
                let resi = atom.resi;
                if (!new_atoms_resi.includes(resi)){
                    new_atoms_resi.push(resi);
                    viewer.selectedAtoms({resi: resi}).forEach(function (n_atom) {
                        new_atoms.push(n_atom);
                    })
                }
            })

            const model = viewer.addModel();
            model.addAtoms(new_atoms);
            model.setStyle({}, {stick: {radius: .15}, sphere: {radius: .2}});

            viewer.enableFog(true);
            glob_model.setStyle({resi: new_atoms_resi}, {'cartoon': {colorfunc: pae_colorscheme, 'arrows': true, opacity: .85}});
            viewer.zoomTo({resi: new_atoms_resi}, 700);
            viewer.render();
        }
        skip = false;
    });
    viewer.setHoverable({}, true,
        function(atom,viewer) {
           if(!atom.label) {
                atom.label = viewer.addLabel(atom.atom + ' | ' + atom.resn + ": " + atom.resi + '\n' + atom.b + '% confident', {position: atom, backgroundColor: 'mintcream', fontColor:'black'});
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

    const pae_div = $('#pae-div');
    pae_div.on('plotly_selected', function (event, points) {
        const init = parseInt(points.range.y[0]);
        const fin = parseInt(points.range.y[1]);

        let sel_range = [];
        for (let i = init; i <= fin; i++) sel_range.push(i);

        viewer.zoomTo({}, 500);
        viewer.zoom(1, 1000);
        viewer.setStyle({}, {'cartoon': {color: '#ECF3FD', 'arrows': true}});
        viewer.setStyle({resi: sel_range}, {'cartoon': {color: '#0053D6', 'arrows': true}});
        viewer.render();
    })

    pae_div.on('plotly_click', function () {
        viewer.zoomTo({}, 500);
        viewer.zoom(1, 1000);
        viewer.setStyle({}, {'cartoon': {colorfunc: pae_colorscheme, 'arrows': true}});
        viewer.render();
    })
}