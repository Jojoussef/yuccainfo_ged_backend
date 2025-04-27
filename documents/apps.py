from django.apps import AppConfig
from transformers import pipeline

class DocumentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'documents'
    classifier = None

    def ready(self):
        # load zero-shot classifier once
        DocumentsConfig.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=-1,
        )
    
