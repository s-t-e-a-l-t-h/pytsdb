from pytsdb import aggregators
from pytsdb import config
from pytsdb import put
import warnings


class TsdbConnector(object):
    def __init__(self, host, port, *args, **kwargs):
        self._host = host
        self._port = port
        self._protocol = kwargs.get('protocol', 'http')
        self._config = self.parameters_serializer()

    def get_aggregators(self):
        """
        This endpoint simply lists the names of implemented aggregation functions used in timeseries queries.
        :return:  json (list)
        """
        return aggregators.aggregators(**self._config)

    def get_config(self):
        """
        This endpoint returns information about the running configuration of the TSD.
        It is read only and cannot be used to set configuration options.
        :return: json
        """
        return config.tsdb_configuration(**self._config)

    def put(self, data, **kwargs):
        """
        Metric has to be created or enable tsd.core.auto_create_metrics

        :param data: json like dict or list of json like dicts
        :param kwargs: dict
        :return: requests response
        """
        params = self._config
        summary = kwargs.get('summary', False)
        details = kwargs.get('details', False)
        sync = kwargs.get('sync', False)
        sync_timeout = kwargs.get('sync_timeout', 0) if sync else False

        params.update(
            {
                'data': data,
                'summary': summary,
                'details': details,
                'sync': sync,
                'sync_timeout': sync_timeout,
            }
        )

        if isinstance(sync_timeout, int) and not sync:
            warnings.warn('Argument sync_timeout has no effect without sync set to True')

        return put.put(**params)

    def parameters_serializer(self):
        return {
            'host': self._host,
            'port': self._port,
            'protocol': self._protocol
        }


def connect(host, port, *args, **kwargs):
    return TsdbConnector(host, port, args, kwargs)
