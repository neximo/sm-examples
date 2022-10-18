import os
from concurrent.futures import ProcessPoolExecutor
from elasticsearch_dsl import Q

import os

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search




from helpers import batch_from_iter, chunks
from seo import property_vip_url
from settings import (SECTION_URLS, HELP_URLS)

from urls import create_all_paths, limit_amenities_combinations_or_none
from sitemap import RooSiteMap, UrlSiteMap

DOMAIN_NAME = os.environ.get('DOMAIN_NAME', 'neximo.mx')
ENV = os.environ.get('ENV', 'production')
ES_HOST = os.environ.get('ES_HOST', 'http://127.0.0.1:9100')


BUCKET = "{}.external.neximo.mx".format(ENV)
DOMAIN_SITEMAP = 'https://www.{}'.format(DOMAIN_NAME)
NOT_MARKETABLE_STATUS = [
    "PAUSED",
    "ARCHIVED",
    "PENDING_FOR_DELETE"
]
SITEMAP_HASH_NAME = "_neximo"
LIMIT_AMENITIES_COMBINATIONS = limit_amenities_combinations_or_none()

ROOT_SITEMAP_FILE_NAME = 'sitemap{}.xml'.format(SITEMAP_HASH_NAME)
CHILD_SITEMAP_FILE_PREFIX = "child_sitemap_"
SITEMAP_DIRECTORY = "sitemap"
MAX_URLS_PER_SITEMAP = 50_000  # Google limits to 50,000 urls by file

ALLOWED_PUBLIC_PROPERTY_AD_STATUS = [
    'PUBLISHED',
    'CLAIMED',
    'ARCHIVED',
]

def new_search_client():
    client = Elasticsearch(hosts=[ES_HOST], timeout=300)
    s = Search(using=client)
    return s



def _add_domain(path_url):
    return "{}{}".format(DOMAIN_SITEMAP, path_url)


def flush(all_urls, last_sitemap_number_created):
    sitemap = UrlSiteMap(
        filename=f'{CHILD_SITEMAP_FILE_PREFIX}{last_sitemap_number_created}{SITEMAP_HASH_NAME}.xml',
        children=all_urls
    )
    sitemap.upload()
    sitemap_url = _add_domain(f'/{sitemap.filename}')
    print(f'{sitemap_url} uploaded')
    return sitemap_url


def all_urls_for(property_ad):
    if property_ad['status'] == "PUBLISHED":
        for url in create_all_paths(
            property_ad=property_ad,
            limit_amenities_combinations=LIMIT_AMENITIES_COMBINATIONS
        ):
            yield url
    yield property_vip_url(property_ad=property_ad)


def xml(property_ad_ids):
    es_client = new_search_client()
    q = Q("terms", id=property_ad_ids)

    # property_ads = es_client.index('property_ad').query(q).scan()

    property_ads = [
        {
            "address": "Prol. Hidalgo 259  , Adolfo López Mateos , 05280 Cuajimalpa de Morelos, Ciudad de México, México",
            "age": 12,
            "amenities":
                [
                    {
                        "amenity_type": "AMENITY",
                        "description": "",
                        "id": 2,
                        "name": "Seguridad privada",
                        "pk": 2
                    },
                    {
                        "amenity_type": "AMENITY",
                        "description": "",
                        "id": 3,
                        "name": "Área de juegos infantiles",
                        "pk": 3
                    },
                    {
                        "amenity_type": "AMENITY",
                        "description": "",
                        "id": 4,
                        "name": "Gimnasio",
                        "pk": 4
                    },
                    {
                        "amenity_type": "AMENITY",
                        "description": "",
                        "id": 23,
                        "name": "Salón de Fiestas",
                        "pk": 23
                    },
                    {
                        "amenity_type": "CHARACTERISTICS",
                        "description": "",
                        "id": 26,
                        "name": "Área de lavandería",
                        "pk": 26
                    },
                    {
                        "amenity_type": "AMENITY",
                        "description": "",
                        "id": 35,
                        "name": "Jardín",
                        "pk": 35
                    },
                    {
                        "amenity_type": "CHARACTERISTICS",
                        "description": "",
                        "id": 44,
                        "name": "Terraza",
                        "pk": 44
                    },
                    {
                        "amenity_type": "CHARACTERISTICS",
                        "description": "",
                        "id": 126,
                        "name": "Walk in closet",
                        "pk": 126
                    },
                    {
                        "amenity_type": "CHARACTERISTICS",
                        "description": "",
                        "id": 135,
                        "name": "Sala y Comedor",
                        "pk": 135
                    },
                    {
                        "amenity_type": "AMENITY",
                        "description": None,
                        "id": 140,
                        "name": "Piso Laminado",
                        "pk": 140
                    },
                    {
                        "amenity_type": "CHARACTERISTICS",
                        "description": None,
                        "id": 141,
                        "name": "Pet friendly",
                        "pk": 141
                    },
                    {
                        "amenity_type": "CHARACTERISTICS",
                        "description": None,
                        "id": 142,
                        "name": "Intercomunicador",
                        "pk": 142
                    }
                ],
            "apt_number": "",
            "bathrooms": 2.0,
            "bedrooms": 2,
            "broker":
                {
                    "active_plan": "FULL_SERVICE",
                    "avatar": "https://production-neximo.s3.amazonaws.com/users/2655/profile/affa94ecfb17.jpeg",
                    "blocked_at": None,
                    "blocked_reason": None,
                    "deleted_at": None,
                    "email": "mumuquedc@gmail.com",
                    "first_name": "DIANA",
                    "full_name": "DIANA CARRILLO ANGELES",
                    "id": 2655,
                    "is_searchable": True,
                    "last_name": "CARRILLO",
                    "mailbox_email": "diana.carrillo@neximo.mx",
                    "pk": 2655,
                    "primary_telephone": "+525540140012",
                    "second_last_name": "ANGELES",
                    "second_telephone": None,
                    "status": "ACTIVE",
                    "telephone": "+525540140012",
                    "top_producer": None
                },
            "campaigns":
                [],
            "city": "",
            "construction_area": 107.0,
            "country": "México",
            "created_at": "2022-10-13T14:20:48.449000+00:00",
            "deleted_at": None,
            "description": "<p>Bonita y acogedora casa en condominio, buena ubicación, atrás de Chedraui Cuajimalpa en agradable zona de varios fraccionamientos. Ideal para familias pequeñas, a sólo 15 minutos de Santa Fé, accesos a carretera México -Toluca en ambos sentidos, Bosques de las Lomas, Jesús del Monte e Interlomas. En la zona, a sólo 5 minutos, encontrarás tiendas de autoservicio, bancos y colegios.</p><p><br></p><p>La casa cuenta con 107 m2 de construcción más una terraza de 12 m2 aproximadamente. Muy buen aprovechamiento de espacios. Al llegar encontrarás hermosas jardineras que adornan la entrada de la casa y dan una única vista verde a la sala, en planta baja tiene un pequeño y lindo recibidor que da paso a la sala y comedor, los cuales cuentan con una cantina, a continuación llegará a la cocina integral abierta con dos despensas, al salir de la cocina se encuentra una acogedora terraza techada con jardín donde podrá pasar momentos inolvidables con sus seres queridos. También en este piso, se encuentra el medio baño de visitas y el área de lavado.</p><p><br></p><p>En la planta alta se encuentra otro recibidor con buena iluminación, la recámara principal con balcón, vestidor y baño propio, una recámara secundaria con opción a hacer una tercera recámara y un baño completo. Le corresponden dos lugares de estacionamiento.</p><p><br></p><p>El condominio cuenta con vigilancia 24 horas, salón de eventos para 60 personas, pequeño gimnasio y jardín con juegos infantiles, además de un excelente ambiente tranquilo y familiar.</p><p><br></p><p>MANTENIMIENTO: $1600</p><p>Mascotas permitidas</p><p><br></p><p>Excelente precio en la zona, que no se la ganen, llame ahora y pida su cita!</p>",
            "development_type": "NONE",
            "district": "Cuajimalpa de Morelos",
            "half_bathrooms": 1.0,
            "has_sale_commission_tax": False,
            "id": 157110,
            "images_json":
                [
                    {
                        "image_type": "GALLERY",
                        "order": 0,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/4505cf76098b.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 1,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/b23cc73d531e.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 2,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/bf0d33634b1c.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 3,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/c5923c511e27.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 4,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/8e436e7cd13b.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 5,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/d5ffc6b8bc71.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 6,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/a1e8cac8ff61.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 7,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/54f9ba2a1b23.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 8,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/34bd75de4cd8.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 9,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/ac02f1135902.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 10,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/4ac32e143694.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 11,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/5aa772ee9c10.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 12,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/30c217ab1fad.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 13,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/8bf7811588be.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 14,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/507b196cee35.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 15,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/ef27e9044841.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 16,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/054cb2b02a59.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 17,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/ff96364904e5.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 18,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/d94c6c66a627.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 19,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/df155f52fd7e.png"
                    },
                    {
                        "image_type": "GALLERY",
                        "order": 20,
                        "status": "SAVED",
                        "url": "https://production-neximo.s3.amazonaws.com/users/2655/properties/157110/af34b4f2f051.png"
                    }
                ],
            "land_type": "RESIDENTIAL",
            "lat": "19.3655258",
            "lng": "-99.2960123",
            "maintenance_fee": None,
            "mandate_type": "INTERMEDIATION",
            "neighborhood": "Adolfo López Mateos",
            "operation_type": "SELL",
            "parking_spaces": 2,
            "pk": 157110,
            "postal_code": "05280",
            "price":
                {
                    "amount": 3850000.0,
                    "currency": "MXN"
                },
            "property_status": "APPROVED",
            "property_type": "HOUSE",
            "sale_commission_days": None,
            "sale_commission_percentage": "0.04",
            "sale_gross_commission":
                {
                    "amount": 154000.0,
                    "currency": "MXN"
                },
            "sale_total_commission":
                {
                    "amount": 154000.0,
                    "currency": "MXN"
                },
            "sale_type": "OPEN",
            "show_full_location": True,
            "state": "Ciudad de México",
            "status": "PUBLISHED",
            "status_documentation": "PENDING_SIGNATURE",
            "status_documentation_approved_at": None,
            "status_documentation_changed_at": "2022-10-18T17:20:15.388000+00:00",
            "status_documentation_pending_signature_at": "2022-10-18T17:20:15.388000+00:00",
            "status_documentation_rejected_at": None,
            "street": "Prol. Hidalgo",
            "street_number": "259",
            "surface_area": 73.0,
            "title": "CASA EN VENTA CON TERRAZA CERCA DE SANTA FE CUAJIMALPA, CIUDAD DE MÉXICO",
            "updated_at": "2022-10-13T14:20:48.449000+00:00",
            "url": "/HOUSE/SELL/inmueble/157110",
            "video_url": "",
            "virtual_tour_url": ""
        }
    ]

    all_urls = set()

    for property_number, property_ad in enumerate(property_ads, start=1):
        for url in all_urls_for(property_ad):
            all_urls.add(_add_domain(url))

    return all_urls


def common_url():
    all_urls = set()
    common_path_url = set(SECTION_URLS + HELP_URLS)

    for path in common_path_url:
        all_urls.add(_add_domain(path))

    return all_urls


class NeximoSitemap:
    def __init__(self, *args, **kwargs):
        self.current_index = 0
        self.all_urls = common_url()

        self.last_sitemap_number_created = 0

        self.total_urls = 0
        self.sitemaps_urls = []
        self.property_ads = []
        self.property_ids = []

        try:
            self.es = new_search_client()
        except Exception as error:
            print(str(error))
            self.die('Unable to get an elasticsearch client.')

        print('Elastic search client created')

        self.load_property_ids()

    def load_property_ads(self):
        """Get all available property ads

            Returns:
                Generator
        """

        active_broker = Q(
            "nested",
            path="broker",
            query=Q("term", broker__status="ACTIVE")
        )

        published_ad = Q("terms", status=ALLOWED_PUBLIC_PROPERTY_AD_STATUS)

        marketable = ~Q("terms", property_status=NOT_MARKETABLE_STATUS)

        q = active_broker & published_ad & marketable

        for property_ad in self.es.index('property_ad').query(q).scan():
            self.property_ads.append(property_ad)

    def load_property_ids(self):
        """Get all available property ads

            Returns:
                Generator
        """
        self.property_ids.append(157110)

        """
                active_broker = Q(
                    "nested",
                    path="broker",
                    query=Q("term", broker__status="ACTIVE")
                )

                published_ad = Q("terms", status=ALLOWED_PUBLIC_PROPERTY_AD_STATUS)

                marketable = ~Q("terms", property_status=NOT_MARKETABLE_STATUS)

                q = active_broker & published_ad & marketable

                for property_ad in self.es.index('property_ad').query(q).source(['id']).scan():
                    self.property_ids.append(property_ad.id)
        """

    def get_all_urls_for_property(self, property_ad):
        for property_url in self.srp_urls(property_ad=property_ad):
            self.add_url(url=property_url)

    def get_vip_url(self, property_ad):
        property_url = self.vip_url(property_ad=property_ad)
        self.add_url(url=property_url)

    def srp_urls(self, property_ad):
        """GET SRP url"""
        return create_all_paths(property_ad=property_ad)

    def vip_url(self, property_ad):
        """Set vip urls"""
        yield property_vip_url(property_ad=property_ad)

    def add_url(self, url):
        self.all_urls.add(url)

    def flush(self):
        self.url_sitemap()
        self.last_sitemap_number_created += 1
        self.total_urls += len(self.all_urls)
        total_formated = '{:,}'.format(self.total_urls)
        print(f'Saved and uploaded {total_formated} URL')

    def url_sitemap(self, urls):
        """Create a sitemaps"""
        sitemap = UrlSiteMap(
            filename=f'{CHILD_SITEMAP_FILE_PREFIX}{self.last_sitemap_number_created}{SITEMAP_HASH_NAME}.xml',
            children=urls
        )
        sitemap.upload()
        self.sitemaps_urls.append(_add_domain(f'/{sitemap.filename}'))

    def save_root_sitemap(self):
        """Storage sitemaps at s3
        The root sitemap will be put at BUCKET/sitemap/ROOT_SITEMAP_FILE_NAME

        Example: production.external.neximo.mx/sitemap/root.xml
        """

        for urls in chunks(list(self.all_urls), MAX_URLS_PER_SITEMAP):
            self.url_sitemap(urls)
            self.last_sitemap_number_created += 1

        root_sitemap = RooSiteMap(
            filename=ROOT_SITEMAP_FILE_NAME,
            children=self.sitemaps_urls
        )
        # root_sitemap.upload()
        print(f'ROOT Sitemap {root_sitemap.filename} uploaded')

    def execute(self):
        print("Creating property ads paths...")

        batch_size = 30
        batch_num = 0

        with ProcessPoolExecutor(max_workers=1) as executor:
            for new_sitemaps_urls in executor.map(xml, list(chunks(self.property_ids, batch_size))):
                batch_num += 1
                print(new_sitemaps_urls)
                self.all_urls.update(new_sitemaps_urls)
                print(f"Batch ° {batch_num} | {len(new_sitemaps_urls)} new URL")
                all_urls = '{:,}'.format(len(self.all_urls))
                print(
                    f'{batch_num * batch_size} properties processed of {len(self.property_ids)} | {all_urls} unique URL')

        print("Finished property ads paths.")
        self.save_root_sitemap()
        return 'The sitemap for {} was generated'.format(DOMAIN_NAME)


if __name__ == '__main__':
    neximo_sitemap = NeximoSitemap()
    result = neximo_sitemap.execute()
    print(result)
