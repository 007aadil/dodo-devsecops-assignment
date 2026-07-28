# Ledger API – DevSecOps Security Hardening

## Overview

This project implements security hardening for a containerized Flask-based Ledger API running on Kubernetes. The objective is to improve the application's security posture by applying container hardening, Kubernetes security best practices, CI/CD security scanning, and secure secret management.

---

# Project Structure

```text
.
├── LICENSE
├── README.md
├── app
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── deploy
│   ├── README.md
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── ingress.yaml
│   ├── networkpolicy.yaml
│   ├── rbac.yaml
│   ├── sealedsecret.yaml
│   └── serviceaccount.yaml
└── policies
    ├── require-nonroot.yaml
    └── test-pod.yaml
```

---

# Security Improvements

## Container Security

* Uses a lightweight Python Alpine base image.
* Runs the application as a non-root user (UID 1000).
* Uses a fixed working directory.
* Applies least-privilege container permissions.
* Uses Kubernetes readiness and liveness probes.

---

## Kubernetes Security

Implemented the following Kubernetes security controls:

* Deployment
* Service
* ConfigMap
* ServiceAccount
* RBAC (Role & RoleBinding)
* NetworkPolicy
* Ingress
* Sealed Secrets
* Kyverno Admission Policy

---

## Secret Management

Plaintext credentials have been removed from Kubernetes manifests.

Secrets are managed using **Bitnami Sealed Secrets**, allowing encrypted secrets to be safely stored in Git while the Sealed Secrets Controller decrypts them inside the Kubernetes cluster.

Protected values include:

* STRIPE_API_KEY
* DB_PASSWORD

---

## Configuration Management

Application configuration is managed using a Kubernetes ConfigMap.

Example values include:

* Application environment
* Log level

---

# Network Security

A Kubernetes NetworkPolicy restricts ingress traffic to the Ledger API pods.

Only approved workloads can communicate with the application on port **8080**.

---

# RBAC

A dedicated ServiceAccount is used instead of the default account.

The application receives only the minimum Kubernetes permissions required through:

* Role
* RoleBinding

This follows the Principle of Least Privilege.

---

# Admission Policy (Kyverno)

Kyverno is configured to enforce container security.

Policy implemented:

* Containers must run as non-root.

Validation was verified by attempting to deploy a non-compliant pod, which was correctly rejected.

---

# CI/CD Pipeline

GitHub Actions automates the security pipeline.

Pipeline stages:

1. Checkout Repository
2. Install Dependencies
3. Bandit Static Application Security Testing (SAST)
4. Docker Image Build
5. Trivy Container Image Vulnerability Scan
6. Build & Push Image to GitHub Container Registry (GHCR)

---

# Security Scanning

## Bandit

Static analysis is performed on the Python application source code.

Checks include:

* Insecure coding practices
* Common Python security issues

---

## Trivy

Container images are scanned for:

* Critical vulnerabilities
* High vulnerabilities
* OS package vulnerabilities
* Python package vulnerabilities

---

# Deployment

Apply all Kubernetes resources:

```bash
kubectl apply -f deploy/
```

Apply Kyverno policy:

```bash
kubectl apply -f policies/require-nonroot.yaml
```

---

# Verification

Verify application deployment:

```bash
kubectl get all -n payments
```

Verify ConfigMap:

```bash
kubectl get configmap -n payments
```

Verify ServiceAccount:

```bash
kubectl get sa -n payments
```

Verify RBAC:

```bash
kubectl get role,rolebinding -n payments
```

Verify NetworkPolicy:

```bash
kubectl get networkpolicy -n payments
```

Verify Ingress:

```bash
kubectl get ingress -n payments
```

Verify Sealed Secret:

```bash
kubectl get sealedsecrets -n payments
```

Verify Kyverno Policy:

```bash
kubectl get clusterpolicy
```

---

# API Endpoints

Health Check

```text
GET /health
```

Transactions

```text
GET /transactions
```

---

# Technologies Used

* Python 3.12
* Flask
* Docker
* Kubernetes
* GitHub Actions
* Bandit
* Trivy
* Kyverno
* Bitnami Sealed Secrets

---

# Security Features Summary

* Non-root Docker container
* Minimal Alpine base image
* Kubernetes ConfigMap
* Encrypted secrets using Sealed Secrets
* ServiceAccount
* RBAC
* NetworkPolicy
* Ingress
* Kyverno admission control
* Bandit SAST
* Trivy image scanning
* GitHub Actions CI/CD

---

# Result

The Ledger API has been successfully hardened using container security best practices, Kubernetes security controls, policy enforcement, secure secret management, and automated DevSecOps security scanning, resulting in a significantly improved security posture suitable for deployment in a Kubernetes environment.

