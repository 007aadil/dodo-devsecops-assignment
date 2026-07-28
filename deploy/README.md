# Ledger API DevSecOps Assignment

## Overview

This project demonstrates DevSecOps best practices for a Flask application.

## Security Improvements

- Masked PAN in transaction responses
- SSRF protection
- Secrets moved to Kubernetes Secret
- Non-root container
- Readiness probe
- Liveness probe
- Resource limits
- NetworkPolicy
- ServiceAccount
- RBAC
- GitHub Actions CI/CD
- Bandit SAST
- Trivy container scanning

## Docker

Build

```bash
docker build -t ledger-api:starter app
