kubectl config set-cluster borathon-kube --insecure-skip-tls-verify=true --server=https://kubernetes.default.svc.cluster.local:443
kubectl config set-credentials adminuser --username admin --password admin
kubectl config set-context borathon-context --cluster borathon-kube --user adminuser
kubectl config use-context borathon-context
