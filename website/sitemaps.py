from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):

    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "services",
            "one_ton_pickup",
            "pickup_delivery",
            "loading_labour",
            "about",
            "contact",
        ]

    def location(self, item):
        return reverse(item)