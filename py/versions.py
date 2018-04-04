versions = {
    'ASV': {'name': 'American Standard Version'},
    'Darby': {'name': 'Darby Translation', 'abbr': 'DARBY'},
    'ESV2011': {'name': 'English Standard Version 2011', 'abbr': 'ESV'},
    'GodsWord': {'name': 'God\'s Word Translation', 'abbr': 'GW'},
    'Jubilee2000': {'name': 'Jubilee Bible 2000', 'abbr': 'JUB'},
    'KJV': {'name': 'Authorized King James Version'},
    'LEB': {'name': 'Lexham English Bible'},
    'NETfree': {'name': 'New English Translation', 'abbr': 'NET'},
    'WEB': {'name': 'World English Bible'},
    'engWMB2015eb': {'name': 'World Messianic Bible', 'abbr': 'WMB'},
    'YLT': {'name': 'Young\'s Literal Translation'}
}


def lookup_version_abbr(version):
    return versions[version]['abbr'] if versions.get(version) and versions.get(version).get('abbr') else version


def lookup_version_name(version):
    return versions[version]['name'] if versions.get(version) and versions.get(version).get('name') else None
