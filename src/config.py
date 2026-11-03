#mongo config
MONGO_URI = "mongodb://127.0.0.1:27017"
MONGO_BDD = "bdd_de_test"
MONGO_COLLECTION_DOC = 'documents'
MONGO_COLLECTION_MD = "marker_extraction"
MONGO_COLLECTION_IMAGES = "images"
MONGO_COLLECTION_METADATA_MD = "meta-data_marker"
THRESHOLD = 12_000_000  #seuil de taille à partir duquel onswitch vers gridfs. Ici 12 Mo
OUTPUT_DIR = "output"


#IA config
MAX_SECTION_LENGTH = 1000
SUMMARY_RATIO = 0.2     # 20 % de chaque section
MIN_WORDS = 30
SYSTEM_SUMMARY = """Tu es un assistant qui résume des cours en français.

Tu reçois un extrait d'un document plus long. Ton résumé sera mis bout à bout avec ceux des autres extraits pour former le résumé du document complet. Donc :
- Résume uniquement le contenu de cet extrait, sans introduction ni conclusion générale.
- N'écris jamais « cet extrait », « cette section » ni « dans ce passage » : énonce directement les idées.
- Conserve les définitions, les termes techniques, les chiffres, les commandes et les exemples essentiels.
- N'ajoute aucune information absente du texte.
- Utilise des phrases courtes ou des puces, et garde les titres de l'extrait s'il y en a.
- Longueur : environ {target_words} mots.
- Réponds uniquement avec le résumé."""