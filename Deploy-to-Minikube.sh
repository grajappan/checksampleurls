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