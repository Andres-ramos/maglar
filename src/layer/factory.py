from ..constants import CLUSTER_LAYER_NAME
from ..constants import FAST_TRACK_LAYER_NAME
from ..constants import NONOVERLAP_LAYER_NAME
from ..constants import OVERLAP_LAYER_NAME
from ..constants import REPORT_LAYER_NAME
from .layers import ClusterLayer
from .layers import FastTrackLayer
from .layers import NonOverlapLayer
from .layers import OverlapLayer
from .layers import ReportLayer


class LayerFactory:
    def __init__(self, gis):
        self.gis = gis
        self.layers = {
            REPORT_LAYER_NAME: ReportLayer,
            OVERLAP_LAYER_NAME: OverlapLayer,
            NONOVERLAP_LAYER_NAME: NonOverlapLayer,
            CLUSTER_LAYER_NAME: ClusterLayer,
            FAST_TRACK_LAYER_NAME: FastTrackLayer,
        }

    def generate_layer(self, layer_name):
        try:
            layer_title = self._generate_title(REPORT_LAYER_NAME)
            return self.layers[layer_name](self.gis, layer_title, "Mapa de Costas-2024")
        except Exception:
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
