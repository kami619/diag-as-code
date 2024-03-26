from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx
from diagrams.onprem.client import Users
from diagrams.generic.network import Router

graph_attr = {
    "fontsize": "32",
    "bgcolor": "lightyellow"
}

with Diagram("Cloud35 Scale Lab Architechture", show=False, graph_attr=graph_attr):
    external_user = [Users("External User"),]
    internet_gateway = Router("Internet Gateway")
    external_user >> internet_gateway

    with Cluster("OpenShift Cluster"):
        with Cluster("Control Plane Nodes"):
            control_plane_nodes = [Server("Control Plane Node 1"),
                                   Server("Control Plane Node 2"),
                                   Server("Control Plane Node 3")]

        with Cluster("Worker Plane Nodes"):
            worker_nodes = [Server("Worker Node 1"),
                            Server("Worker Node 2"),
                            Server("Worker Node 3")]
        
        # Representing the Ingress Load Balancer
        ingress_lb = Nginx("Ingress Load Balancer")
        internet_gateway >> ingress_lb

        ingress_lb >> worker_nodes

    # External DB positioned outside the cluster for clarity
    db = PostgreSQL("External DB (PostgreSQL)")

    with Cluster("Load Generators"):
        load_gens = [Server("Load Gen 1"),
                     Server("Load Gen 2"),
                     Server("Load Gen 3")]
    load_gens >> internet_gateway

    # Connection from the OpenShift Cluster to the External DB
    for wn in worker_nodes:
        wn >> db
