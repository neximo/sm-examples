from itertools import combinations, product
from pprint import pp
from .constants import AMOUNT_RANGES, MAX_EXACT_SEARCH_COUNT, PRICE_LABELS


def parse_num(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return value


def amount_range(amount):
    """
      Return: tuple - (lower_bound, upper_bound)
    """

    if amount < AMOUNT_RANGES[0]:
        return None, AMOUNT_RANGES[0]

    if amount >= AMOUNT_RANGES[-1]:
        return AMOUNT_RANGES[-1], None

    for index, bound in enumerate(AMOUNT_RANGES):
        if amount < bound:
            return AMOUNT_RANGES[index - 1], bound


def bedrooms_paths(bedrooms):
    if bedrooms >= MAX_EXACT_SEARCH_COUNT:
        return(f'con-mas-de-{bedrooms}-habitaciones-cuartos',)
    if bedrooms == 1:
        return ('con-1-habitacion-cuarto', 'con-mas-de-1-habitacion-cuarto')
    return (f'con-{bedrooms}-habitaciones-cuartos',
            f'con-mas-de-{bedrooms}-habitaciones-cuartos')


def parking_spaces_paths(parking_spaces):
    if parking_spaces >= MAX_EXACT_SEARCH_COUNT:
        return(f'con-mas-de-{parking_spaces}-estacionamientos',)
    if parking_spaces == 1:
        return ('con-1-estacionamiento', 'con-mas-de-1-estacionamiento')
    return (f'con-{parking_spaces}-estacionamientos',
        f'con-mas-de-{parking_spaces}-estacionamientos')


def bathrooms_paths(bathrooms):
    if bathrooms >= MAX_EXACT_SEARCH_COUNT:
        return(f'con-mas-de-{bathrooms}-banos',)
    if bathrooms == 1:
        return ('con-1-bano', 'con-mas-de-1-bano')
    return (f'con-{bathrooms}-banos', f'con-mas-de-{bathrooms}-banos')


def half_bathrooms_paths(half_bathrooms):
    if half_bathrooms >= MAX_EXACT_SEARCH_COUNT:
        return(f'con-mas-de-{half_bathrooms}-medios-banos',)
    if half_bathrooms == 1:
        return ('con-1-medio-bano', 'con-mas-de-1-medio-bano')
    return (f'con-{half_bathrooms}-medio-bano', f'con-mas-de-{half_bathrooms}-medio-bano')


def price_paths(price):
    price_label = PRICE_LABELS.get(price['currency'])
    lower_bound, upper_bound = amount_range(price['amount'])

    if lower_bound and upper_bound:
        return (
            f'de-{lower_bound}-a-{upper_bound}-{price_label}',
            f'desde-{lower_bound}-{price_label}',
            f'hasta-{upper_bound}-{price_label}',
        )

    if lower_bound:
        return (
            f'desde-{lower_bound}-{price_label}',
            f'hasta-{lower_bound}-{price_label}',
        )

    if upper_bound:
        return (
            f'desde-{upper_bound}-{price_label}',
            f'hasta-{upper_bound}-{price_label}',
        )


AMENITIES = [
    {
        'name': 'bedrooms',
        'build_paths': bedrooms_paths
    },
    {'name': 'parking_spaces', 'build_paths': parking_spaces_paths},
    {'name': 'bathrooms', 'build_paths': bathrooms_paths},
    {'name': 'half_bathrooms', 'build_paths': half_bathrooms_paths},
    {'name': 'Alberca', 'build_paths': lambda value: ('con-alberca',)},
    {'name': 'Rango de Precio', },
    {'name': 'Precio mínimo', },
    {'name': 'Precio máximo', },
    {'name': 'price', 'build_paths': price_paths},
    {'name': 'Elevador', 'build_paths': lambda value: ('con-elevador',)},
    {
        'name': 'Seguridad/guardia',
        'build_paths': lambda value: ('con-seguridad-guardia',)},
    {
        'name': 'Intercomunicador',
        'build_paths': lambda value: ('con-intercomunicador',)},
    {
        'name': 'Cocina equipada',
        'build_paths': lambda value: ('con-cocina-equipada',)},
    {
        'name': 'Armarios empotrados',
        'build_paths': lambda value: ('con-armario',)
    },
    {'name': 'Gimnasio', 'build_paths': lambda value: ('con-gimnasio',)},
    {
        'name': 'Aire acondicionado',
        'build_paths': lambda value: ('con-aire-acondicionado',)},
    {'name': 'Calefaccion', 'build_paths': lambda value: ('con-calefaccion',)},
    {
        'name': 'Cuarto de servicio',
        'build_paths': lambda value: ('con-cuarto-de-servicio',)
    },
    {'name': 'Balcon', 'build_paths': lambda value: ('con-balcon',)},
    {'name': 'Terraza', 'build_paths': lambda value: ('con-terraza',)},
    {
        'name': 'Estacionamiento para visitas',
        'build_paths': lambda value: ('con-estacionamiento-para-visitas',)
    },
    {
        'name': 'Área de Juegos Infantiles',
        'build_paths': lambda value: ('con-juegos-infantiles',)
    },
    {'name': 'Jardín', 'build_paths': lambda value: ('con-jardin',)},
    {'name': 'Jacuzzi', 'build_paths': lambda value: ('con-jacuzzi',)},
    {'name': 'Roof garden', 'build_paths': lambda value: ('con-roof-garden',)},
]


PROPERTY_CHARACTERISTICS_AS_AMENITIES = (
    'bedrooms',
    'parking_spaces',
    'bathrooms',
    'halfBathrooms',
    'price',
)


def amenity_paths(property_ad):
    """
    Return:
        Iterable of iterables

    Example:
        amenity_paths(property_ad=property_ad)
        >>> (
                ('con-3-habitaciones-cuartos', 'con-mas-de-3-habitaciones-cuartos,),
                ('con-alberca',),
                ('de-4000000-a-4500000-pesos', 'desde-4000000-pesos', 'hasta-4500000-pesos',)
            )
    """
    if not property_ad['amenities']:
        return tuple()

    property_amenities_name = tuple(
        map(lambda amenity: amenity['name'], property_ad['amenities']))
    property_amenities = set(property_amenities_name + PROPERTY_CHARACTERISTICS_AS_AMENITIES)

    amenity_values = {}
    amenities_paths = []

    for property_name in PROPERTY_CHARACTERISTICS_AS_AMENITIES:
        if property_name in property_ad and property_ad[property_name]:
            amenity_values[property_name] = parse_num(
                property_ad[property_name])

    for amenity in AMENITIES:
        amenity_name = amenity.get('name')
        if amenity_name in property_amenities:
            amenity_value = amenity_values.get(amenity_name, True)
            build_paths = amenity.get('build_paths')

            if amenity_value and build_paths:
                amenities_paths.append(build_paths(amenity_value))

    return amenities_paths
