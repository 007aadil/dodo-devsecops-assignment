# Ledger API - DevSecOps Security Hardening

## Overview

This project implements security hardening for the Ledger API as part of the DevSecOps assignment.

## Security Improvements

### 1. Secrets Management
- Removed hardcoded secrets
- Stored secrets in Kubernetes Secret
- Used secretKeyRef in Deployment

### 2. SSRF Protection
- Allowed HTTPS only
- Blocked localhost
- Blocked private IP ranges
- Validated resolved IP addresses

### 3. Sensitive Data Protection
- Masked card PAN
- Only last 4 digits are visible

### 4. Container Security
- Runs as non-root user
- Read-only root filesystem
- Dropped Linux capabilities
- Disabled privilege escalation

### 5. Kubernetes Hardening
- Liveness Probe
- Readiness Probe
- Resource requests
- Resource limits

### 6. Network Security
- Added NetworkPolicy
- Only allows approved traffic

### 7. CI/CD Security
- Bandit SAST
- Trivy container scan
- GitHub Actions pipeline

## Build

```bash
docker build -t ledger-api:starter ./app
