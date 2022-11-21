function string_API_request(id) {
    $('#loading-string-div').show();
    getSTRING(
        'https://version-11-5.string-db.org',
        {
            'species': '3880',  // Medicago truncatula species id
            'identifiers': [id],
            'network_flavor': 'evidence',
            'block_structure_pics_in_bubbles': 1
        }
    );

}

// function reformat_graph() {
//     const logo = document.getElementById('svg_string_logo');
//     if (logo != null) logo.parentNode.removeChild(logo);
// }