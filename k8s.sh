echo "=======Building the cclookup image from the Dockerfile======="
docker build -t grajappan4401/checksampleurls:latest .
echo "=======Login to Docker registry to push the image to dockerhub========"
docker login registry.hub.docker.com 
if [ $? -eq 1 ]; then
    echo "Docker login failed. Retry again"
    exit 1
fi
echo "=======Pushing the image to my docker hub public repo grajappan4401/cclookup======="
docker push grajappan4401/checksampleurls:latest
echo "=======Installing Minikube======="
#brew install minikube
echo "=======Starting the minikube cluster====="
minikube start --vm-driver=virtualbox
echo "=======Install kubectl in local machine======"
#brew install kubectl
echo "=======Set kubeconfig context to minikube====="
kubectl config set-context minikube
echo "=======Deploying the CheckURL Service API========"
kubectl create -f checkurls_service.yaml
echo "=======Install Prometheus============"
minikubeip=`minikube ip`
sed -i'.original' "s/minikubeip/$minikubeip/g" prometheus-config.yml
kubectl create namespace monitoring
kubectl apply -f prometheus-config.yml
kubectl apply -f prom-graf.yaml
echo "========Waiting for a minute and a half the POD to comeup====="
sleep 90
echo "======Testing the CheckURLService API======="
curl -s $minikubeip:31080/
curl -s $minikubeip:31080/
curl -s $minikubeip:31080/
curl $minikubeip:31080/metrics


