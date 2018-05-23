from pprint import pprint
from urllib.parse import urlparse

import kubernetes
import pytest
import yaml

from .k8s_wrappers import *
from .util import *

# Tests

@pytest.fixture
def core_api():
    kubernetes.config.load_kube_config()
    return CoreV1Api()

@pytest.fixture
def extensions_v1beta1_api():
    kubernetes.config.load_kube_config()
    return ExtensionsV1beta1Api()

def namespace():
    # load_kube_config doesn’t set a namespace, or retrieve one from the context
    return "default"

def test_listing_pods_does_not_raise(core_api):
    pods = core_api.list_namespaced_pod(namespace(), _request_timeout=1).items
    assert len(pods) > 0

def test_hello_world(core_api, extensions_v1beta1_api):
    app_name = f'timestamp-test-{int(time.time())}'

    deployment_spec, service_spec = (replace_dict_values(spec, timestamp=app_name)
                                     for spec in yaml.load_all(read('timestamp-svc.yaml')))

    with Deployment(namespace(), deployment_spec, extensions_v1beta1_api) \
            as deployment:
        with Service(namespace(), service_spec, core_api) as service:
            w = kubernetes.watch.Watch()
            for event in w.stream(core_api.list_namespaced_endpoints,
                                  namespace=namespace(),
                                  field_selector=f"metadata.name={app_name}"):
                # print("Got event:")
                # pprint(event)
                if len(event["object"].subsets) != 0:
                    break

            hostname = urlparse(kubernetes.client.configuration.host).hostname
            timestamp_port = next(port.node_port
                                  for port in service.spec.ports
                                  if port.name == app_name)
            print(f"{app_name} listening on {hostname} port {timestamp_port}")

            response = try_connect_until_timeout(hostname, timestamp_port)

            assert response.startswith(b'Timestamp service: ')
