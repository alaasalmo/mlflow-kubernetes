
# <p width=600 align="center"><b>Introduction into MLflow and Kubernetes</b></p>

MLflow is a key tool in MLOps (Machine Learning Operations) used by data scientists to streamline the machine learning lifecycle. This post will explain how to build MLflow within a Docker container, deploy the container on Minikube, and explore the benefits of integrating MLflow with Docker and Kubernetes (Minikube).

Docker has become increasingly popular in AI development, particularly in machine learning, due to its ability to create reproducible environments, manage dependencies, and facilitate efficient model deployment. Additionally, when combined with Kubernetes/Minikube, Docker enhances resource sharing and scalability. Optimizing resource usage, infrastructure choices, and deployment strategies can significantly reduce costs in AI workloads using Docker and Kubernetes.

Before diving into the MLflow application, it is essential to define two key terms and their relationship: MLflow and MLOps.

MLflow is an open-source platform developed by Databricks for managing machine learning workflows.
MLOps (Machine Learning Operations) provides guidelines for managing the full lifecycle of machine learning models, ensuring seamless deployment and maintenance.
MLflow is widely used by data scientists and MLOps teams to track model versions, compare different deployment iterations, and manage the machine learning lifecycle efficiently. Our goal in this article is to build MLflow on a container-based platform (Docker) and deploy it in a Kubernetes/Minikube environment for better container orchestration and MLflow management. Minikube is chosen for its ease of implementation and ability to run on a single node.

By leveraging MLflow in an MLOps workflow, data scientists can efficiently track, deploy, and manage machine learning models, making it a powerful tool for AI-driven applications.

#### I.	The diagram for our implementation

<p align="center">
<img align="center" src="img\mlflow-diagam-general.jpg" wodth=90%>
<br>Figure-1
</p>

Figure 1 provides an overview of how MLflow integrates with Docker and Minikube for efficient machine learning workflow management. The first step in this process is building the MLflow Docker container.

Docker is an open-source platform that functions similarly to a virtual machine but is more lightweight, as it contains fewer OS commands and services. The primary goal is to package the MLflow application within a Docker container and expose its functionality through API services. However, while Docker can run individual containers, it requires an orchestration platform to manage multiple containers efficiently.

Kubernetes is a widely used open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications. In this article, our objective is to deploy MLflow as a service, which can be utilized by individual users or groups. Kubernetes enables the creation of multiple independent services, allowing each to scale up or down as needed, providing greater flexibility and resource efficiency.

Minikube, a lightweight version of Kubernetes, is ideal for development and testing purposes. It is easy to install and can run on a local machine, making it a convenient option for deploying MLflow in a controlled environment.

#### II.	MLflow expected diagram (Infrastructure)

<p align="center">
<img align="center" src="img\mlflow-daigram-details.jpg" wodth=90%>
<br>Figure-2
</p>

Figure 2 illustrates the overall MLflow infrastructure, highlighting its key components and connectivity options. This infrastructure remains consistent whether deployed on-premises or within a Kubernetes/Minikube environment.

MLflow provides multiple ways for users to interact with its service, including Jupyter Notebook, IDE tools, and the command line. Regardless of the method, all interactions rely on the MLflow API service.

Within a Kubernetes/Minikube environment, an Ingress controller is required to route incoming requests to the MLflow tracking service. The tracking service utilizes SQLite to store the MLruns database and includes a local artifact repository.

MLruns Database Structure
The MLruns database contains essential metadata related to machine learning experiments, including:

✅ Experiments – Metadata about each experiment.

✅ Run ID – A unique identifier assigned to each run.

✅ Parameters – Input parameters used for model training (e.g., hyperparameters like learning rate).

✅ Metrics – Performance metrics logged during the run (e.g., accuracy, loss).

✅ Tags – Labels providing additional context for each run.
Artifact Storage and Model Information

Artifacts Location – Stores experiment artifacts, such as model files, plots, and other generated outputs, within the filesystem.
Models – Contains information about models logged during runs, including model signatures and input schemas.
Other Metadata – Tracks additional details, such as run start and end times, execution status (e.g., completed, failed), and other auxiliary data.
By leveraging this structured approach, MLflow efficiently tracks and manages machine learning workflows across different deployment environments.

#### III.	MLflow interfaces

<p align="center">
<img align="center" src="img\mlflow-general-diagram.jpg">
<br>Figure-3
</p>

Figure 3 illustrates the three types of interfaces available in MLflow for connecting to the core MLflow system running on Minikube.

MLflow provides three primary interfaces:

✅ Coding Interface – Users can interact with MLflow through Jupyter Notebook, Visual Studio Code, or any Python-based application.

✅ Web Interface – The web UI allows users to manage experiments, track runs, organize artifacts, review logs, and handle model versioning.

✅ MLflow CLI – The command-line interface (CLI) enables users to execute commands and connect to the MLflow server via its API.

Each interface offers flexibility in managing and monitoring machine learning workflows, catering to different user preferences and development environments.

#### IV.	Implementation steps of building MLflow with Minkkube

##### A. Build MlFlow on docker
###### - Introduction to Docker Containers
Docker is a software platform that enables the creation and deployment of applications within lightweight, portable containers. A container is a minimal virtualized environment that includes only the essential services needed to run an application, unlike traditional virtual machines (VMs), which replicate an entire operating system.

Unlike VMs, Docker containers share some services with the host system, making them more efficient, faster, and smaller in size. Their lightweight nature allows for better resource utilization, scalability, and rapid deployment based on application requirements.

###### - Build MFlow in Minikube
When creating a Docker container, we need to define a Dockerfile, which contains the necessary scripts for setting up the container environment. These scripts can be divided into three main sections:

🤗 <b>Root-Level Configuration</b> – This section sets up environment variables and executes commands with root privileges.

🤗 <b>User Configuration & MLflow Installation</b> – The user is switched from root to a non-root user for security reasons. In this stage, MLflow is installed using Python’s pip package manager.

🤗 <b>Entry Point & Execution Commands</b> – This section defines the entry point and includes RUN commands to initialize the container.

In our Dockerfile example, we begin with root privileges and later switch to a non-root base, ensuring compatibility with Kubernetes and Persistent Volume Claims (PVCs) for storage management. PVC is a Kubernetes feature that allows containers to request and manage persistent storage efficiently.

to build the docker image file, you will need the following files:
<a href="doocker/runmlflow.sh">runmlflow.sh</a> file
<a href="doocker/requirements.txt">requirements.txt</a> file
<a href="doocker/Dockerfile">Dockerfile</a> file
Or you can generate the file (the file it's already but if you want to generate it):


```
cat >>meta.yaml<< EOF
artifact_location: file:////mflow/mlruns/449779801724405851
creation_time: 1724463060230
experiment_id: '449779801724405851'
last_update_time: 1724463060230
lifecycle_stage: active
name: Anomaly Detection
EOF
```
<a href="doocker/meta.yaml">meta.yaml</a> file 
</br>

✅ If you want the image, you can pass the docker build and get the image from https://hub.docker.com/repository/docker/alaasalmo/mlflow

Build docker image

```
"docker login --username XXXXXXX --password XXXXXXX"
"docker build -f Dockerfile -t mlflow:1.0.0 ."
"docker tag mlflow:0.1.0 alaasalmo/mlflow:1.0.0"
"docker push alaasalmo/mlflow:0.1.0"
```

##### B. Using MLFlow docker with Minikube

We need to start the cube and check the Minikube on one node. After you start the minkube, you can go to the node that run the minikube. The minukube runs on one node

Start minikube
```
minikube start --driver=hyperv -v=11
kubectl get node
```

✅ <b>Build the folder in minikube</b>
We need to create the path of folder to use it in PVC
```
minikube ssh
sudo su -
mkdir /mnt/data
echo 'Hello from Kubernetes storage' > /mnt/data/index.html
chmod 777 /mnt/data
exit
exit
```
✅ <b>Build PV and PVC</b>
We need to build PV (Persistent Volume) and PVC (Persistent Volume Claim) to use them 

<a href="storage/pv.yaml">pv.yaml</a> file
```
kubectl apply -f pv.yaml
```
<a href="storage/pvc.yaml">pvc.yaml</a> file
```
kubectl apply -f pvc.yaml
```

✅ <b>Deploy the pod</b>
<a href="minikube/deployment.yaml">deployment.yaml</a> file

```
kubectl apply -f deployment.yaml
```

✅ <b>Create service</b>

To Create service, you need first to enable the ingress

```
minikube addons enable ingress
```
Crate the mlflow service for port 5050

```
kubectl expose deployment mlflow-srvc --type=NodePort --port=5050
```
or we can deploy the file for service (mlflow-srvc)

<a href="minikube/mlflow-srvc.yaml">mlflow-srvc.yaml</a> file

Get the URL

```
minikube service list
minikube service mlflow-srvc –url
Output:
http://172.25.183.169:31434
```
Note: Use the URL above in the browser

Go to the web and check the mlflow

<p align="center">
<img align="center" src="img\main-page.jpg" wodth=90%>
</p>

##### C. Build the model with MLflow

In this example, we will build and compare two machine learning models using MLflow. The implementation can be done in a Jupyter Notebook or any Python IDE, such as Visual Studio Code.

We will use the Credit Card Fraud Detection dataset from Kaggle to train our models.

For this dataset, we will implement and evaluate two models: Logistic Regression and XGBoost.

After running the model in Python, we can view it in MLflow. However, to access the artifact files, we need to manually transfer them to the appropriate folder.

In our setup, we use PVC (Persistent Volume Claim) as distributed storage. To streamline this process, one solution is to configure Amazon S3 as the artifact storage. This allows MLflow to save artifacts directly to S3 and retrieve them seamlessly when needed.

In our next post, we will explore an alternative solution using a Jupyter Notebook pod to directly access the distributed storage.


The example python for buildig machine learning code 

<a href="machinelearning/logisticregressionandXGBoost.py">logisticregressionandXGBoost.py</a> file

After we run the model, we go to the mlflow page and check:

1- Experiments (Top menue)

<p align="center">
<img align="center" src="img\main-page2.jpg" wodth=90%>
</p>

2- Register Model (Top menu)

<p align="center">
<img align="center" src="img\main-page3.jpg" wodth=90%>
</p>

When we run the command</br> 
mlflow.sklearn.log_model(xg, "xgboost model", registered_model_name="XGBoostModel")</br>
mlflow.sklearn.log_model(lr, "LogisticRegression model", registered_model_name="LogisticRegressionModel")</br>

According the two examples above Where is the model saved and artifacts in our model?

✅ <b>MLflow Tracking Database (Model Registry)</b>
Since you specified registered_model_name="XGBoostModel", the model is stored in the MLflow Model Registry, which is typically connected to a database backend (like PostgreSQL or MySQL, depending on your MLflow setup).
You can access it via MLflow UI or through MLflow’s API.

✅ <b>Artifact Store (if configured)</b>
If your MLflow is connected to an artifact store (like AWS S3, Google Cloud Storage, or a local file system), the model will be stored there. 
In our model after run the model locally we have to transfer we can use the command to poin t to the local mlflow.set_tracking_uri("file:/your/local/mlflow/artifacts").   
The exact storage location depends on your MLflow configuration.

✅