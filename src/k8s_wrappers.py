from kubernetes.client import CoreV1Api, ExtensionsV1beta1Api

_FOREGROUND_PROPAGATION_DELETE_OPTIONS = {
    "kind": "DeleteOptions",
    "apiVersion": "v1",
    "propagationPolicy": "Foreground"
}

class Deployment:
    """
    Context manager for Kubernetes deployments in unit tests: deletes deployment
    on __exit__.
    """

    def __init__(self, namespace, spec, extensions_v1beta1_api):
        self.namespace = namespace
        self.spec = spec
        self.extensions_v1beta1_api = extensions_v1beta1_api

        self.deployment = None

    def __enter__(self):
        self.deployment = self.extensions_v1beta1_api.create_namespaced_deployment(
            self.namespace, self.spec)
        return self.deployment

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.deployment is None:
            return
        self.extensions_v1beta1_api.delete_namespaced_deployment(
            self.deployment.metadata.name, self.namespace,
            _FOREGROUND_PROPAGATION_DELETE_OPTIONS)

class Service:
    def __init__(self, namespace, spec, core_api: CoreV1Api):
        self.namespace = namespace
        self.spec = spec
        self.core_api = core_api

        self.service = None

    def __enter__(self):
        self.service = self.core_api.create_namespaced_service(
            self.namespace, self.spec)
        return self.service

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.service is None:
            return
        self.core_api.delete_namespaced_service(
            self.service.metadata.name,
            self.namespace)
