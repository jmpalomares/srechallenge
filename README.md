# Srechallenge flask app
Simple app in flask to GET a response based in a query parameter defined in the URL.

The customer will connect to the endpoint with a saludation query in the URL and it will receive a response.


    curl -X GET http://localhost:5000/srechallenge?saludation=Hi
    {"data":"Hi there!"}

    HTTP/1.1 200 OK
    Server: Werkzeug/2.1.2 Python/3.9.2
    Date: Sun, 22 May 2022 09:51:36 GMT
    Content-Type: application/json
    Content-Length: 30
    Connection: close


If saludation is not the correct one, it will return an error with status code 500:


    curl -X GET http://localhost:5000/srechallenge?saludation=Hello
    {"data":"Customer saludation Hello not found."}

    HTTP/1.1 500 INTERNAL SERVER ERROR
    Server: Werkzeug/2.1.2 Python/3.9.2
    Date: Sun, 22 May 2022 09:51:26 GMT
    Content-Type: application/json
    Content-Length: 48
    Connection: close

Perhaps it should be better to return an error 400 instead.

I did some changes because the task was asking for an individual deployment for each customer.

As the app is not using databases queries, there is not risk for SQL injections attacks.

Probably would be better to have a proper database with customers details and select from the table the right response based in the saludation. So we will have a single app for all customer and we can have a table in a database for all customer details or multiples databases, one for each customer individually.

Unitests for each scenario are ran in the CI pipeline.

## Deploying with helm
I've used helm charts for the deployment in kubernetes.

Just running following command:

    helm install srechallenge-chart srechallenge-helm/ --values srechallenge-helm/values.yaml

    NAME: srechallenge-chart
    LAST DEPLOYED: Mon May 23 03:44:38 2022
    NAMESPACE: default
    STATUS: deployed
    REVISION: 1
    NOTES:
    1. Get the application URL by running these commands:
        NOTE: It may take a few minutes for the LoadBalancer IP to be available.
            You can watch the status of by running 'kubectl get --namespace default svc -w srechallenge-chart'
    export SERVICE_IP=$(kubectl get svc --namespace default srechallenge-chart --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}")
    echo http://$SERVICE_IP:5000

I've used minikube for testing in local. As the service type is LoadBalancer, I'd to run minikube tunnel to enable my localhost as external IP:

    kubectl get service
    NAME                 TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
    kubernetes           ClusterIP      10.96.0.1        <none>        443/TCP          53m
    srechallenge-chart   LoadBalancer   10.101.164.151   <pending>     5000:32201/TCP   4m50s


    minikube tunnel
    ✅  Tunnel successfully started

    📌  NOTE: Please do not close this terminal as this process must stay alive for the tunnel to be accessible ...

    🏃  Starting tunnel for service srechallenge-chart.


    kubectl get service
    NAME                 TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
    kubernetes           ClusterIP      10.96.0.1        <none>        443/TCP          55m
    srechallenge-chart   LoadBalancer   10.101.164.151   127.0.0.1     5000:32201/TCP   7m31s


    curl -X GET http://localhost:5000/srechallenge?saludation=Hi
    {"data":"Hi there!"}


Of course in a production environment we will use cert-manager, an ingress controller (I like nginx) and configure let's encrypt as issuer. Example configuration:

    ## Nginx Ingress
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
    annotations:
        kubernetes.io/ingress.class: nginx
        cert-manager.io/cluster-issuer: "letsencrypt-{{ .Values.environment }}"
    name: app
    namespace: {{ .Values.namespace }}
    spec:
    tls:
        - hosts:
        - {{ .Values.fqdn }}
        secretName: srechallenge-certificate-{{ .Values.environment }}
    rules:
        - host: {{ .Values.fqdn }}
        http:
            paths:
            - path: /
            pathType: Prefix
            backend:
                service:
                name: web
                port:
                    number: {{ .Values.app }}
                    
More details:
- [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/deploy/)
- [How to Install Kubernetes Cert-Manager and Configure Let’s Encrypt](https://www.howtogeek.com/devops/how-to-install-kubernetes-cert-manager-and-configure-lets-encrypt/)
