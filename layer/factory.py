from constants import CLUSTER_LAYER_NAME
from constants import FAST_TRACK_LAYER_NAME
from constants import NONOVERLAP_LAYER_NAME
from constants import OVERLAP_LAYER_NAME
from constants import REPORT_LAYER_NAME

from .layers import ClusterLayer
from .layers import FastTrackLayer
from .layers import NonOverlapLayer
from .layers import OverlapLayer
from .layers import ReportLayer


class LayerFactory:
    def __init__(self, gis):
        self.gis = gis

    # TODO: Use dictionary instead of if-else soup
    # TODO: Figure out best way to pass
    # TODO: Remove color from class creation call
    def generate_layer(self, layer_name):
        if layer_name == REPORT_LAYER_NAME:
            layer_title = self._generate_title(REPORT_LAYER_NAME)
            return ReportLayer(self.gis, layer_title, "Mapa de Costas-2024", None)

        elif layer_name == OVERLAP_LAYER_NAME:
            layer_title = self._generate_title(OVERLAP_LAYER_NAME)
            return OverlapLayer(self.gis, layer_title, "Mapa de Costas-2024", "red")

        elif layer_name == NONOVERLAP_LAYER_NAME:
            layer_title = self._generate_title(NONOVERLAP_LAYER_NAME)
            return NonOverlapLayer(
                self.gis, layer_title, "Mapa de Costas-2024", "green"
            )

        elif layer_name == CLUSTER_LAYER_NAME:
            layer_title = self._generate_title(CLUSTER_LAYER_NAME)
            return ClusterLayer(self.gis, layer_title, "Mapa de Costas-2024", "green")

        elif layer_name == FAST_TRACK_LAYER_NAME:
            layer_title = self._generate_title(FAST_TRACK_LAYER_NAME)
            return FastTrackLayer(self.gis, layer_title, "Mapa de Costas-2024", "green")
        else:
            raise Exception(f"{layer_name} not yet implemented!")

    def _generate_title(self, layer_name):
        """
        Maps layer title to presentation Name
        """
        TITLE_MAP = {
            REPORT_LAYER_NAME: "Observaciones",
            OVERLAP_LAYER_NAME: "Reservas Peligrando",
            NONOVERLAP_LAYER_NAME: "Reservas",
            CLUSTER_LAYER_NAME: "Hot spots",
            FAST_TRACK_LAYER_NAME: "Fast Track",
        }
        return TITLE_MAP[layer_name]
