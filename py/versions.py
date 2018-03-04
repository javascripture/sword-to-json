def lookup_version(version):
    versions = {
        'Darby': 'DARBY',
        'ESV2011': 'ESV',
        'GodsWord': 'GW',
        'Jubilee2000': 'JUB',
        'NETfree': 'NET'
    }

    return versions[version] if versions.get(version) else version
