# Demo App: Build, Dockerize & Deploy to Local Kubernetes

This guide shows you how to:

1. Initialize a Go module  
2. Build and tag Docker images  
3. Push to Docker Hub  
4. Install **kind** (Kubernetes in Docker)  
5. Create a local cluster  
6. Deploy your app  
7. Roll out a new version with Blue/Green deployment

---

## Prerequisites

- **Go** installed (1.16+ recommended)  
- **Docker** CLI and daemon running  
- **kubectl** (or alias `k`) installed and configured  
- A Docker Hub account with a repository created  

---

## 1. Initialize the Go Module

Create and initialize a `go.mod` file to track dependencies:

```bash
# From your project root:
go mod init demo
```

> **What this does:**  
> - Creates a `go.mod` file  
> - Sets your module path to `demo`  

---

## 2. Build & Run Locally

Compile and run your Go app to verify it works:

```bash
# Build the binary
go build -o bin/app src/main.go

# Run on port 8080
bin/app
```

Point your browser at `http://localhost:8080` to confirm it’s serving.

---

## 3. Build, Tag & Push Your Docker Image

### 3.1 Log in to Docker Hub

```bash
docker login -u <dockerhub_username>
```

### 3.2 Build the Image

```bash
# Tag in one step (best practice)
docker build -t <dockerhub_username>/<dockerhub_repo>:v1.0.0 .
```

### 3.3 Verify & Tag by Digest (optional)

```bash
# List all images
docker image ls

# (If you have a digest you prefer)
docker tag <image_id> <dockerhub_username>/<dockerhub_repo>:v1.0.0
```

### 3.4 Push to Docker Hub

```bash
docker push <dockerhub_username>/<dockerhub_repo>:v1.0.0

# Confirm it’s there
docker image ls | grep v1.0.0
```

---

## 4. Install kind (Local Kubernetes)

Grab the latest binary for your architecture:

```bash
# For AMD64 / x86_64
curl -Lo kind https://kind.sigs.k8s.io/dl/v0.29.0/kind-linux-amd64
chmod +x kind
sudo mv kind /usr/local/bin/
```

> More info: https://kind.sigs.k8s.io/

---

## 5. Create a Local Kubernetes Cluster

```bash
# Create a cluster named "demo"
kind create cluster --name demo

# Verify nodes and pods
kubectl get nodes
kubectl get pods --all-namespaces -o wide --sort-by='.spec.nodeName'
```

---

## 6. Deploy Your First Version

### 6.1 Create a Namespace

```bash
kubectl create namespace demo
```

### 6.2 Deploy & Expose

```bash
kubectl create deployment demo \
  --image=<dockerhub_username>/<dockerhub_repo>:v1.0.0 \
  -n demo

# Forward port 8080 to localhost
kubectl port-forward deploy/demo 8080:8080 -n demo
```

### 6.3 Verify

```bash
kubectl get deployments -n demo
kubectl logs deploy/demo -n demo
```

---

## 7. Roll Out a New Version (v1.0.1)

### 7.1 Clone & Build

```bash
git clone https://github.com/den-vasyliev/devops-types.git
cp devops-types/html/*svg ./html
rm -rf devops-types

# Build new image
docker build -t <dockerhub_username>/<dockerhub_repo>:v1.0.1 .
```

### 7.2 Test Locally

```bash
docker run -p 8080:8080 <dockerhub_username>/<dockerhub_repo>:v1.0.1
```

### 7.3 Push to Docker Hub

```bash
docker push <dockerhub_username>/<dockerhub_repo>:v1.0.1
```

---

## 8. Blue/Green Deployment

1. **Check current rollout**  
   ```bash
   kubectl get deploy demo -n demo -o wide
   ```
2. **Watch pod updates**  
   ```bash
   kubectl get pods -w -n demo
   ```
3. **Switch to v1.0.1**  
   ```bash
   kubectl set image deployment/demo \
     devops-k8s=<dockerhub_username>/<dockerhub_repo>:v1.0.1 \
     -n demo

   # Re-establish port-forward
   kubectl port-forward deploy/demo 8080:8080 -n demo
   ```
   > Here, `devops-k8s` is the container name in your Deployment spec.

4. **Verify the new rollout**  
   ```bash
   kubectl rollout status deployment/demo -n demo
   kubectl get pods -n demo -o wide
   ```

---

## Next Steps

- Automate builds & deploys with CI/CD (GitHub Actions, GitLab CI, etc.)  
- Add health/readiness probes to your Deployment  
- Expose via a Service & Ingress/controller for real traffic  
- Implement true Blue/Green or Canary with tools like Argo Rollouts