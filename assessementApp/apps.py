from django.apps import AppConfig


class AssessementappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assessementApp'

    def ready(self):
       import assessementApp.signals 
        
    


    

