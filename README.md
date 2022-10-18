# sm-examples

This shows how we created our urls

We have some urls that are always added to our sitemap, urls like our FAQs, Contact Us, About Us, etc.


## Data shape
This scripts expects a json with the following shape:

```json
{
  "address": "text",
  "age": "integer",
  "amenities":
  [
    {
      "amenity_type": "text",
      "description": "text",
      "id": "integer",
      "name": "text",
      "pk": "integer"
    }
  ],
  "apt_number": "text",
  "archived_at": "date",
  "bathrooms": "float",
  "bedrooms": "integer",
  "broker":
  {
    "about": "text",
    "active_plan": "text",
    "avatar": "text",
    "blocked_at": "date",
    "blocked_reason": "text",
    "deleted_at": "date",
    "email": "text",
    "first_name": "text",
    "full_name": "text",
    "has_paid": "boolean",
    "id": "integer",
    "is_searchable": "boolean",
    "last_name": "text",
    "mailbox_email": "text",
    "pk": "integer",
    "primary_telephone": "text",
    "second_last_name": "text",
    "second_telephone": "text",
    "status": "text",
    "telephone": "text",
    "top_producer": "text"
  },
  "campaigns":
  {
    "active": "boolean",
    "id": "integer",
    "name": "text",
    "pk": "integer"
  },
  "city": "text",
  "construction_area": "float",
  "country": "text",
  "created_at": "date",
  "deleted_at": "date",
  "description": "text",
  "development_type": "text",
  "district": "text",
  "half_bathrooms": "float",
  "has_sale_commission_tax": "boolean",
  "id": "integer",
  "images_json":
  {
    "image_type": "text",
    "order": "integer",
    "status": "text",
    "url": "text"
  },
  "land_type": "text",
  "lat": "text",
  "lng": "text",
  "maintenance_fee":
  {
    "amount": "double",
    "currency": "text"
  },
  "mandate_type": "text",
  "neighborhood": "text",
  "operation_type": "text",
  "parking_spaces": "integer",
  "pk": "integer",
  "postal_code": "text",
  "price":
  {
    "amount": "double",
    "currency": "text"
  },
  "property_status": "text",
  "property_type": "text",
  "sale_commission_days": "integer",
  "sale_commission_percentage": "text",
  "sale_gross_commission":
  {
    "amount": "double",
    "currency": "text"
  },
  "sale_total_commission":
  {
    "amount": "double",
    "currency": "text"
  },
  "sale_type": "text",
  "show_full_location": "boolean",
  "state": "text",
  "status": "text",
  "status_documentation": "text",
  "status_documentation_approved_at": "date",
  "status_documentation_changed_at": "date",
  "status_documentation_pending_signature_at": "date",
  "status_documentation_rejected_at": "date",
  "street": "text",
  "street_number": "text",
  "surface_area": "float",
  "title": "text",
  "updated_at": "date",
  "url": "text",
  "video_url": "text",
  "virtual_tour_url": "text"
}
```


## Process

We use elasticsearch to query our listing data, then we create all the possible urls for a given listing, 
the only thing that we limit is the amount to amenities to include, because with each amenity we need a lot of urls.

### Query data

We query our elasticsearch index for all the pages that we want to add to our sitemap

We have few restrictions, those are following:

**Exclude listings from inactive agents**: so only active users, 
**we also exclude the users that have not given us permission** to show their listings: is_searchable: true

```python
active_broker = Q(
    "nested",
    path="broker",
    query=Q("term", broker__status="ACTIVE")
)
is_searchable = Q(
    "nested",
    path="broker",
    query=Q("term", broker__is_searchable=True)
)
```

**Include publishable listing**, the one with the following statues:

```python
ALLOWED_PUBLIC_PROPERTY_AD_STATUS = [
    'PUBLISHED',
    'CLAIMED',
    'ARCHIVED',
]

published_ad = Q("terms", status=ALLOWED_PUBLIC_PROPERTY_AD_STATUS)
```

**Exclude unpublishable properties**: the ones with the following statues:

```python
NOT_MARKETABLE_STATUS = [
    "PAUSED",
    "ARCHIVED",
    "PENDING_FOR_DELETE"
]

marketable = ~Q("terms", property_status=NOT_MARKETABLE_STATUS)
```

So the final query is:

```python
q = active_broker & is_searchable & published_ad & marketable

for property_ad in self.es.index('property_ad').query(q).source(['id']).scan():
    self.property_ids.append(property_ad.id)
```

We get the ids first because we process them in batches, so we don't have to load all the data in memory.


### Generate URLs
For each property we always generate the following urls:

```python
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
```

property_type_paths will give you:
`/casa`, `/departamento`, `/terreno`, `/local`, etc. see `PROPERTY_TYPES` inside `seo.py` 

operation_type_paths the same idea as above; but for:
```python
OPERATION_TYPES = {
    'SELL': 'en-venta',
    'RENT': 'en-renta',
    'SHARE': 'compartir'
}
```

locations_paths will give you:
`/estado/municipio/colonia` and `/estado/municipio` and `/estado`

combine_multiple_paths, will give you as many combinations about characteristics of the property, like: with garden, 
with pool, with garage, etc. see `AMENITIES` inside `urls/amenities.py`

For example if you have a property with the following amenities: `['garden', 'rood-garden', 'balcony']`

You will get;

`[ /con-balcon, /con-balcon-con-jardin /con-balcon-con-jardin-con-roof-garden ]`


Finally, we create another permutation of the previous urls: `combine_multiple_paths(paths=list(filter(None, all_paths)`
