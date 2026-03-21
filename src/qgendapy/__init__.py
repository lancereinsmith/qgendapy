from importlib.metadata import version

from qgendapy.client import AsyncQGendaClient, QGendaClient
from qgendapy.odata import OData

__version__ = version("qgendapy")

__all__ = ["AsyncQGendaClient", "OData", "QGendaClient", "__version__"]
