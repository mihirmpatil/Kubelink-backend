kubectl config set-cluster bora-catalog --insecure-skip-tls-verify=true --server=http://catalog.kubelink.borathon.photon-infra.com:80
kubectl config set-credentials adminuser --username admin --password admin
kubectl config set-context bora-catalog --cluster bora-catalog --user adminuser
kubectl config use-context bora-catalog
