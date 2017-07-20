kubectl config set-cluster borathon-kube --insecure-skip-tls-verify=true --server=https://app.kubelink.borathon.photon-infra.com:6443
kubectl config set-credentials adminuser --username admin --password admin
kubectl config set-context borathon-context --cluster borathon-kube --user adminuser
kubectl config use-context borathon-context
