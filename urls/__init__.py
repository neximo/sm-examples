import os
from itertools import combinations, product
from seo import PROPERTY_TYPES, OPERATION_TYPES, normalize_as_url
from .amenities import amenity_paths

LIMIT_AMENITIES_COMBINATIONS = os.environ.get('LIMIT_AMENITIES_COMBINATIONS', '10')


def combine_paths(paths, separator="-", limit_combinations = None):
    """
    Args:
        paths: string iterable
    Return:
        string list
    Example:
        combine_paths(('con-jardin', 'con-jacuzzi', 'con-roof-garden'))
        >>>  [
                'con-jardin',
                'con-jacuzzi',
                'con-roof-garden',
                'con-jardin-con-jacuzzi',
                'con-jardin-con-roof-garden',
                'con-jacuzzi-con-roof-garden',
                'con-jardin-con-jacuzzi-con-roof-garden'
             ]
    """
    final_paths = set()
    limit = limit_combinations if limit_combinations else len(paths)
    for size in range(1, limit + 1):
        resulted_paths = [separator.join(p) for p in combinations(paths, size)]
        final_paths.update(resulted_paths)
    return final_paths


def combine_multiple_paths(paths, separator=None, limit_combinations=None):
    """
    Combine multiple paths without repeat between theirs.
    Any element in paths is a tupple and any element of any tupple can be combined with
    any element in other tupple except elements in the same tupple.s

    Args:
        paths - iterable of iterables
        separator - string - Useful separators can be '-' to join amenity paths or '/' to build URL
    Return:
        string list
    Example:
        combine_multiple_paths((
            ('con-alberca',),
            ('con-2-estacionamientos',),
            ('con-2-habitaciones-cuartos', 'con-mas-de-2-habitaciones-cuartos'),
            ('con-cuarto-de-servicio',),
            ('con-3-banos', 'con-mas-de-3-banos'),
            ('desde-5000000-pesos', 'hasta-5000000-pesos'),
        ))

        # It generates 215 unique combinations

        >>> [
                'con-alberca',
                'con-2-estacionamientos',
                'con-2-habitaciones-cuartos',
                'con-cuarto-de-servicio',
                'con-3-banos',
                'desde-5000000-pesos',
                'con-alberca-con-2-estacionamientos',
                'con-alberca-con-2-habitaciones-cuartos',
                'con-alberca-con-cuarto-de-servicio',
                'con-alberca-con-3-banos',
                'con-alberca-desde-5000000-pesos',
                ...
            ]
    """
    paths_combinations = set(product(*paths))
    unique_paths = set()

    for combination in paths_combinations:
        new_paths = [new_path for new_path in combine_paths(
            combination, separator=separator, limit_combinations=limit_combinations)]
        unique_paths.update(new_paths)
    return list(unique_paths)


def property_type_paths(property_type):
    property_type_url = PROPERTY_TYPES.get(property_type)
    if property_type_url:
        return property_type_url,
    return tuple()


def operation_type_paths(operation_type):
    operation_type_url = OPERATION_TYPES.get(operation_type)
    if operation_type_url:
        return operation_type_url,
    return tuple()


def locations_paths(state=None, district=None, neighborhood=None,):
    locations = list(map(normalize_as_url, filter(None, [neighborhood,  district, state])))
    paths = list()
    for index in range(len(locations)):
        paths.append('--'.join(locations[index:]))
    return paths


def create_all_paths(property_ad, limit_amenities_combinations=None):
    """
    Combine all available URL for any property Ad.
    URL format: /property-type/operation-type/location/amenities
    """
    all_paths = [
        property_type_paths(property_type=property_ad['property_type']),
        operation_type_paths(operation_type=property_ad['operation_type']),
        locations_paths(state=property_ad['state'], district=property_ad['district'], neighborhood=property_ad['neighborhood']),
        combine_multiple_paths(paths=amenity_paths(property_ad=property_ad), separator="-", limit_combinations=limit_amenities_combinations)
    ]

    for path in combine_multiple_paths(paths=list(filter(None, all_paths)), separator="/"):
        yield f'/{path}'

def limit_amenities_combinations_or_none():
    try:
        return int(LIMIT_AMENITIES_COMBINATIONS)
    except Exception as error:
        return None
