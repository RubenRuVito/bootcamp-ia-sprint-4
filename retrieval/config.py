from __future__ import annotations

from typing import Callable

from data_utils import Movie
# from retrieval.indexing_pipeline_utils import get_synopsys_txt
from retrieval.indexing_pipeline_utils import get_synopsys_txt, get_dataMovies_transform_txt
# from retrieval.retrieval_pipeline_utils import clean_query_txt
from retrieval.retrieval_pipeline_utils import clean_query_txt, clean_query_txt_v2


class RetrievalExpsConfig:
    """
    Class to keep track of all the parameters used in the embeddings experiments.
    Any attribute created in this class will be logged to mlflow.

    Nota: cuando definimos atributos de tipo Callable, debemos usar `staticmethod` para que la función pueda ser llamada
    s
    """

    """
    Modelos "Sentence-similarity", "sentence-Transformer", Seleccionados para Experimentar:

    all-MiniLM-L6-v2 (91 MB)
    paraphrase-multilingual-MiniLM-L12-v2 (460 MB) *Seleccionado x metricas y tiempo de ejecución..
    intfloat/multilingual-e5-large (2.5 GB)
    intfloat/multilingual-e5-base (1.11 GB)

    Experimentos LAB_01: Testear los modelos sin modificar ni añadir funcionalidad..
    Experimentos LAB_02: Testear los modelos modificar y añadiendo funcionalidades al código..

    """

    def __init__(self):

        # Función a emplear para generar el texto a indexar con embeddings; Debe tomar como input un objeto `Movie` y devolver un string
        # self._text_to_embed_fn: Callable = get_synopsys_txt
        self._text_to_embed_fn: Callable = get_dataMovies_transform_txt

        # Parámetros para la generación de embeddings

        # self.model_name: str = "all-MiniLM-L6-v2"
        self.model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"
        # self.model_name: str = "intfloat/multilingual-e5-large"
        # self.model_name: str = "intfloat/multilingual-e5-base"
        # self.normalize_embeddings: bool = False  # Normalizar los embeddings a longitud 1 antes de indexarlos
        self.normalize_embeddings: bool = True

        # self._query_prepro_fn: Callable = clean_query_txt
        self._query_prepro_fn: Callable = clean_query_txt_v2

    ## NO MODIFICAR A PARTIR DE AQUÍ ##

    def text_to_embed_fn(self, movie: Movie) -> str:
        return self._text_to_embed_fn(movie)

    def query_prepro_fn(self, query: dict) -> str:
        return self._query_prepro_fn(query)

    @property
    def index_config_unique_id(self) -> str:
        return f"{self.model_name}_{self._text_to_embed_fn.__name__}_{self.normalize_embeddings}"

    @property
    def exp_params(self) -> dict:
        """
        Return the config parameters as a dictionary. To be used, for example, in mlflow logging
        """
        return {
            "model_name": self.model_name,
            "text_to_embed_fn": self._text_to_embed_fn.__name__,
            "normalize_embeddings": self.normalize_embeddings,
            "query_prepro_fn": self._query_prepro_fn.__name__,
        }
