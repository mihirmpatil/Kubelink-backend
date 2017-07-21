kubectl config set-cluster bora-catalog --insecure-skip-tls-verify=true --server=http://catalog-catalog-apiserver.catalog.svc.cluster.local:80
kubectl config set-credentials adminuser --username admin --password admin
kubectl config set-context bora-catalog --cluster bora-catalog --user adminuser

