import re
import unidecode
import unicodedata


OPERATION_TYPES = {
    'SELL': 'en-venta',
    'RENT': 'en-renta',
    'SHARE': 'compartir'
}


PROPERTY_TYPES = {
    'APARTMENT': 'departamentos',
    'HOUSE': 'casas',
    'LOTS': 'terreno',
    'ROOMS': 'cuarto',
    'STORE': 'local',
    'WAREHOUSE': 'bodega',
    'OFFICE': 'oficina',
    'BUILDING': 'edificio',
    'HOTEL': 'hotel',
    'RANCH': 'rancho'
}


def normalize_string(string_to_normalize):
    return unidecode.unidecode(string_to_normalize)


def normalize_as_url(url):
    normalize_url = normalize_string(url.lower())
    return re.sub(r'\s', '-', normalize_url)


def property_vip_url(property_ad):
    property_url = "/{}/{}/{}/{}".format(
        PROPERTY_TYPES[property_ad['property_type']],
        OPERATION_TYPES[property_ad['operation_type']],
        slugify(property_ad['title']),
        property_ad['pk']
    )

    return property_url


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode(
            'ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[\s]+', '-', value)
