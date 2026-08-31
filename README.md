# End-to-End Kubernetes DevSecOps Pipeline on AWS

> A production-grade CI/CD pipeline that containerizes an application, scans it for vulnerabilities, and continuously deploys it to a Kubernetes cluster on AWS (EKS) — with infrastructure provisioned as code, GitOps-driven delivery, and full observability.

![AWS](https://img.shields.io/badge/AWS-EKS-FF9900?logo=amazonaws&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-1.31-326CE5?logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?logo=terraform&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![ArgoCD](https://img.shields.io/badge/ArgoCD-GitOps-EF7B4D?logo=argo&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?logo=githubactions&logoColor=white)

---

## Overview

This project implements the complete journey of an application from source code to a live, monitored production deployment — the same workflow used by real engineering teams. It demonstrates hands-on skills across cloud infrastructure, containerization, CI/CD automation, security, Kubernetes orchestration, GitOps, and observability.

A deliberately simple Python (Flask) application serves as the payload; the focus is the **platform and automation built around it**.

## Architecture

```
   Developer
      │  git push
      ▼
┌─────────────────────────────────────────────────────────────┐
│  GitHub Actions (CI)                                         │
│   run tests → Trivy security scan → build image → push ECR  │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
  Amazon ECR  ──────────────┐
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Amazon EKS (Kubernetes)                                    │
│   Argo CD (GitOps) syncs manifests from Git → Deployment    │
│   → Pods behind a LoadBalancer Service                      │
│                                                             │
│   Prometheus + Grafana  →  metrics & dashboards             │
└─────────────────────────────────────────────────────────────┘

  Infrastructure (VPC, IAM, EKS) provisioned with Terraform.
```

## Tech Stack

| Layer | Technology |
|---|---|
| Application | Python (Flask) |
| Containerization | Docker |
| Image Registry | Amazon ECR |
| CI/CD | GitHub Actions |
| Security Scanning | Trivy |
| Infrastructure as Code | Terraform |
| Orchestration | Amazon EKS (Kubernetes 1.31) |
| GitOps / Continuous Delivery | Argo CD |
| Monitoring & Observability | Prometheus + Grafana |
| Cluster Provisioning | eksctl |

## Key Features

- **Infrastructure as Code** — the entire AWS environment (VPC, subnets, IAM roles, EKS cluster) is defined in Terraform and reproducible from a single command.
- **Automated CI/CD** — every push to `main` triggers automated testing, security scanning, image build, and publication to Amazon ECR.
- **DevSecOps** — Trivy scans each image for CRITICAL/HIGH vulnerabilities inside the pipeline, shifting security left.
- **GitOps delivery** — Argo CD continuously reconciles the cluster to match the desired state declared in Git; deployments happen by committing, not by manual `kubectl`.
- **Observability** — Prometheus collects cluster and application metrics; Grafana visualizes them in live dashboards.
- **Self-healing & scalable** — Kubernetes runs multiple replicas behind a load balancer, restarts failed pods, and scales across worker nodes.

## Results & Optimizations

Measured, reproducible improvements from this project:

| Metric | Result | How It Was Measured |
| --- | --- | --- |
| Image size | 287 MB → 48 MB (83% smaller) | Multi-stage Docker build + non-root user |
| Image vulnerabilities | 421 → 19 HIGH/CRITICAL (95% fewer) | Trivy scan after rebasing to slim base |
| CI/CD pipeline speed | 57 seconds end-to-end | GitHub Actions: test → scan → build → push |
| Self-healing | ~10 seconds pod recovery | Deleted a pod; timed reschedule to Ready |
| Zero-downtime deploy | 300/300 requests (100%) | Continuous load during a live rolling update |
| Infra provisioning | ~18 minutes from code | eksctl provisioned VPC, IAM, cluster, nodes |

## Screenshots

### CI/CD Pipeline — automated test, scan, build & push
![CI/CD Pipeline](docs/screenshots/CICD-Pipeline.png)

### Kubernetes — application pods running on the cluster
![Kubernetes pods](docs/screenshots/kubernetes-pod.png)

### Argo CD — GitOps continuous delivery
![Argo CD dashboard](docs/screenshots/argocd-1.jpeg)
![Argo CD application detail](docs/screenshots/argocd-2.jpeg)

### Grafana — live cluster monitoring
![Grafana dashboard](docs/screenshots/grafana-1.png)
![Grafana metrics](docs/screenshots/grafana-2.png)

## Repository Structure

```
.
├── app.py                     # Flask application
├── test_app.py                # Unit tests (run in CI)
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container image definition
├── .github/workflows/         # GitHub Actions CI/CD pipeline
│   └── deploy.yml
├── terraform/                 # Infrastructure as Code (VPC, IAM, EKS)
│   ├── main.tf
│   └── outputs.tf
├── k8s/                       # Kubernetes manifests (Deployment + Service)
│   └── k8s-deployment.yaml
├── argocd/                    # Argo CD Application (GitOps config)
│   └── application.yaml
└── docs/screenshots/          # Project screenshots
```

## How It Works

1. **Code & containerize** — the app is packaged into a Docker image defined by the `Dockerfile`.
2. **CI pipeline** — on every push, GitHub Actions runs tests, scans the image with Trivy, builds it, and pushes it to Amazon ECR.
3. **Provision infrastructure** — Terraform stands up the VPC, IAM roles, and an EKS cluster on AWS.
4. **GitOps deploy** — Argo CD watches this repository and automatically deploys the Kubernetes manifests to the cluster.
5. **Serve & scale** — the app runs as multiple pods behind an AWS load balancer, reachable on the public internet.
6. **Monitor** — Prometheus scrapes metrics and Grafana presents live dashboards of cluster and application health.

## Running It Yourself

<details>
<summary>Prerequisites</summary>

- AWS account + AWS CLI configured
- Docker, kubectl, eksctl, Terraform, Helm installed
</details>

```bash
# 1. Provision the EKS cluster
eksctl create cluster --name cloud-devops-eks --region ap-south-1 \
  --version 1.31 --node-type t3.small --nodes 2 --managed

# 2. Deploy the app via Argo CD (GitOps)
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl apply -f argocd/application.yaml

# 3. Install monitoring
helm install monitoring prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace
```

## Engineering Notes

Provisioning EKS worker nodes surfaced a real-world node-registration challenge. I diagnosed it methodically — checking node health, service quotas, cluster endpoint access, and Kubernetes version compatibility — and made the pragmatic engineering decision to provision the working cluster with `eksctl` while retaining the Terraform infrastructure code. This mirrors real production troubleshooting: isolate the failure, weigh trade-offs, and keep the delivery moving.

---

## Author

**Arjun Dharun Raj R**
Aspiring Cloud / DevOps Engineer

*If you found this project interesting, feel free to star the repo.*
