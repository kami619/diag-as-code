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
    internet_gateway = Router("Public Network (lab dhcp)")
    external_user >> internet_gateway
    with Cluster("Private Network (Scale Lab Network 1)"):
        with Cluster("OpenShift Cluster"):
            with Cluster("Control Plane Nodes", direction="LR"):
                cnode1 = Server("Control Plane Node 1")
                cnode2 = Server("Control Plane Node 2")
                cnode3 = Server("Control Plane Node 3")
            cnode1 - cnode2 - cnode3
            with Cluster("Worker Plane Nodes"):
                worker_nodes = [Server("Worker Node 3"),
                                Server("Worker Node 2"),
                                Server("Worker Node 1")]
                ingress_lb = Nginx("Ingress Load Balancer")
            # Representing the Ingress Load Balancer
            internet_gateway >> ingress_lb
            ingress_lb >> worker_nodes
            db = PostgreSQL("External DB (PostgreSQL)")
            for wn in worker_nodes:
                wn >> db
        with Cluster("Load Generators"):
                load_gens = [Server("Load Gen 3"),
                            Server("Load Gen 2"),
                            Server("Load Gen 1")]
        load_gens >> ingress_lb