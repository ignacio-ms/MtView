function string_API_request(id) {
    getSTRING(
        'https://string-db.org',
        {
            'species': '3880',  // Medicago truncatula species id
            'identifiers': [id],
            'network_flavor': 'evidence',
            'block_structure_pics_in_bubbles': 1,
            'caller_identity': 'mtview.herokuapp.com'
        }
    );
}

function reformat_graph() {
    const logo = document.getElementById('svg_string_logo');
    if (logo != null)
        logo.parentNode.removeChild(logo);
}