import os

from datetime import date

ENV = os.environ.get('ENV')
SITEMAP_DIRECTORY = "sitemap"
BUCKET = "{}.external.neximo.mx".format(ENV)


class Tag:
    tag = None
    tag_padding = 0
    newline_children = False

    def __init__(self, *args):
        self.children = args

    def __str__(self):
        children = ''.join([str(child) for child in self.children])
        tag_padding = ''.rjust(self.tag_padding, ' ')

        if self.tag_padding > 0 and self.newline_children:
            return  f'{tag_padding}<{self.tag}>\n{children}{tag_padding}</{self.tag}>\n'
        return f'{tag_padding}<{self.tag}>{children}</{self.tag}>\n'


class LocTag(Tag):
    tag = 'loc'
    tag_padding = 4

class LastmodTag(Tag):
    tag = 'lastmod'
    tag_padding = 4

class UrlTag(Tag):
    tag = 'url'
    tag_padding = 2
    newline_children = True


class SitemapTag(Tag):
    tag = 'sitemap'
    tag_padding = 2
    newline_children = True

    def __init__(self, loc, last_modified=None):
        if last_modified is None:
            last_modified = LastmodTag(date.today().isoformat())

        super().__init__(LocTag(loc), last_modified)


class BaseSiteMap:
    header = None
    footer = None
    tag_class = None

    def __init__(self, filename, children):
        tags = [
            str(self.tag_class(child))
            for child in children
        ]
        content = self.header
        content = content + ''.join(tags)
        content = content + self.footer

        self.filename = filename
        self.content = content

    def upload(self):
        print(f'Uploading {self.filename} to {BUCKET}')
        # fu = FileUploader(
        #     bucket=BUCKET,
        #     object_key=f'{SITEMAP_DIRECTORY}/{self.filename}',
        #     extra_params={
        #         'ACL': 'public-read',
        #         'ContentType': 'application/xml'
        #     }
        # )
        # fu.append(self.content)
        # fu.complete()


class RooSiteMap(BaseSiteMap):
    header = '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    footer = '</sitemapindex>'
    tag_class = SitemapTag


class UrlSiteMap(BaseSiteMap):
    header = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    footer = '</urlset>'
    tag_class = UrlTag

    def __init__(self, filename, children):
        tags = [
            str(self.tag_class(
                LocTag(child),
                LastmodTag(date.today().isoformat()),
            ))
            for child in children
        ]
        content = self.header
        content = content + ''.join(tags)
        content = content + self.footer

        self.filename = filename
        self.content = content

