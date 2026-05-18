import os
import json

try:
    from ibm_watson import NaturalLanguageUnderstandingV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from ibm_watson.natural_language_understanding_v1 import (
        Features,
        EntitiesOptions,
        KeywordsOptions,
        CategoriesOptions,
        ConceptsOptions,
        EmotionOptions,
        RelationsOptions,
        SemanticRolesOptions,
        SentimentOptions,
        SyntaxOptions,
    )
except Exception:  # IBM Watson is optional for the public demo.
    NaturalLanguageUnderstandingV1 = None
    IAMAuthenticator = None
    Features = EntitiesOptions = KeywordsOptions = CategoriesOptions = ConceptsOptions = None
    EmotionOptions = RelationsOptions = SemanticRolesOptions = SentimentOptions = SyntaxOptions = None


def login():
    watson_apikey = os.getenv('WATSON_APIKEY') or os.getenv('WATSON_NLU_APIKEY')
    watson_instance_url = os.getenv('WATSON_INSTANCE_URL') or os.getenv('WATSON_NLU_URL')

    if not NaturalLanguageUnderstandingV1 or not IAMAuthenticator:
        raise RuntimeError('IBM Watson SDK is not installed')
    if not watson_apikey or not watson_instance_url:
        raise RuntimeError('IBM Watson NLU credentials are not configured')

    authenticator = IAMAuthenticator(watson_apikey)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator,
    )
    natural_language_understanding.set_service_url(watson_instance_url)
    return natural_language_understanding


def analyzeText(client, text):
    response = client.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
            keywords=KeywordsOptions(emotion=True, sentiment=True, limit=2),
            categories=CategoriesOptions(limit=100),
            concepts=ConceptsOptions(limit=100),
            emotion=EmotionOptions(),
            relations=RelationsOptions(),
            semantic_roles=SemanticRolesOptions(keywords=True, entities=True),
            sentiment=SentimentOptions(),
            syntax=SyntaxOptions(sentences=True),
        )
    ).get_result()
    return json.dumps(response, indent=2)
