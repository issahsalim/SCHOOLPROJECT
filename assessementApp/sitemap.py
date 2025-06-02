from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class StaticViewsSitemap(Sitemap):
    changefreq='daily'
    priority= 0.8
    
    def items(self):
        return ['home']  
    

    def location(self, item):
        return reverse(item) 
    
 
 