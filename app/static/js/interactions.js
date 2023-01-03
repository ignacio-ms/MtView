function string_API_request(id) {
    $('#loading-string-div').show();
    getSTRING(
        'https://version-11-5.string-db.org',
        {
            'species': '3880',
            'identifiers': [id],
            'network_flavor': 'evidence',
            'block_structure_pics_in_bubbles': 1
        }
    );
}