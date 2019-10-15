## Dash in IBM Cloud Kubernetes (K8s)

This docuemnt describes the necessary tools/steps to deploy a dash app into kubernetes. 
First we describe the procedure for a single worker (free) deployment in IBM cluoud and
with a flask web server (not production ready). 

The next steps would be to:
1. Use a proper web server for production such as uWSGI (in conjunction with nginx for higher 
throughput [nginx doesn't understand python and can't talk to flask]).
2. Use a Kubernetes cluster with master and workers. This actually changes the way it is 
deployed and exposed in any cloud. 

### The Dash App (```app.py```). 
The first thing to build is the dash app. It is built completely in python and uses the 
microframework flask to serve the application. 
We can pull the data using APIs from here and keep it in memory or we can build another 
microservice to handle the data requests. 
The basic structure of a Dash app has two parts: Layout and Callbacks:
- The Layouts can be interpreted as the front end of the application 
- The Callbacks can be interpreted as the backend or dynamic part which resolves any part 
of the front end that is listening to changes.

The complete guide of Dash can be found at https://dash.plot.ly/ and a gallery of demos apps
can be found at https://dash-gallery.plotly.host/Portal/

#### Run Locally 
You can serve and run the dash app running the app file from terminal. A Flask server is handling things in the background by default the app will listen only 
to the local host at port 8050.

### The conteinerization of the app using Docker. 
The first thing is to have the docker Deamon running in the machine and listening 
to the docker server. 
Then we need to build our image. Since we only need python base and a couple of 
libraries such as dash and pandas, we can use the python:latest image from the docker
hub registry (Docker will automatically look for the image first locally then in the docker hub).
Define the Dockerfile, copy the requirements (using pipfreeze if using virtual environment) or just write the requirements.txt with all the libraries needed. 
Once we have the docker file defined, we can create the image using ```docker build -t <hubusername>/project:tag .``` 
Since the docker file uses the python (with ubuntu) image, you can first pull it using ```docker pull python:latest``` or docker will pull it automatically in the building process.
Now we have to push the image to the registry (we are using docker hub registry) with ```docker push <imagename>``` a login might be necessary. 

#### Test the app in docker.
We can test the app in the container using docker daemon locally.
To do so, we need to run the image as a container with ```docker run -p 8050:8050 <imagename:tag>```. The flask server should be serving to host 0.0.0.0 (any host) 
instead of only the localhost. Once the app goes into the container the routing is handled to docker which is not the localhost anymore. 
Once the container is running we can visit it at localhost:8050. 

### Deploying to K8s. 
The correct configuration of the cluster depends on the requirements of your app and the cloud provider. 
For this example we are using the free K8s instance of IBM Cloud which is free and hs 2 CPUs and 8GB memory.

[Useful tutorial for Kubernetes](https://kubernetes.io/docs/tutorials/kubernetes-basics/deploy-app/deploy-interactive/).

#### IBM Cloud single instance K8.
_You will need to authenticate to the ibmcloud (ibmcloud login --sso) and link the kubectl aplication to the ibmcloud kubernetes service (ibmcloud ks)._

The deployment is a high level concept that manages ReplicaSets and provides declarative updates to Pods along with other processes; the Deployment is the main concept used in kubernetes to deploy apps. 

>Running multiple replicas of a pod will not guarantee high availability but it cannot be achieved without it. For obvious reasons, you should never have all the replicas of a pod on the same node.

There is no evident advantage on running replicas for our pod in our cloud instance since we only have one worker. 

You can create a deployment using a configuration file in yaml where we specify the number of replicas and the image you want to run in the container. You can also create the deployment using the command line of kubernetes _*kubectl*_. 

```kubectl create deployment test-dash-deployment --image=registry.hub.docker.com/<username>/<imagename:tag>```

Finally we need to expose the deployment using ```kubectl expose deployment/test-dash-deployment --type=NodePort --port=8050 --name=test-dash-service --target-port=8050```

We are using NodePort type of service to access the application direcly using the worker and not though a load balancer which all the cloud providers have but not for this special case of free single instance K8s.

>NodePort: Exposes the Service on each Node’s IP at a static port (the NodePort). A ClusterIP Service, to which the NodePort Service routes, is automatically created. You’ll be able to contact the NodePort Service, from outside the cluster, by requesting <NodeIP>:<NodePort>.

>LoadBalancer: Exposes the Service externally using a cloud provider’s load balancer. NodePort and ClusterIP Services, to which the external load balancer routes, are automatically created.

More information of the service at https://kubernetes.io/docs/concepts/services-networking/service/

It is important that the target-port is the port at which our application is listening for traffic.

#### Figure out the public ip. 
IBM cloud uses a specific public ip for each worker and assigns a random port for the service we just created. 
To figure out the port of the service we need to ```kubectl describe service test-dash-service``` and it is listed at NodePort.
To figure out the public ip of the worker we need to type ```ibmcloud ks cluster ls``` to list the clusters running in our workspace, copy the id of our cluster and type ```ibmcloud ks worker ls --cluster <clusterid>``` which will list the public ip of our only worker. 

[You can visit the app here.](http://184.172.250.9:32471/) 




