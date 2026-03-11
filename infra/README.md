# Terraform – Infra CI/CD (GCP)

Esta pasta contém a infraestrutura para rodar a API no Cloud Run com **ambiente único** e autenticação via **Workload Identity Federation (WIF)**.

## 📦 O que é criado

- APIs GCP necessárias (Run, Artifact Registry, IAM, Cloud Build)
- Artifact Registry (Docker)
- Cloud Run (v2)
- Service Account de runtime
- Service Account para o GitHub Actions
- Workload Identity Pool/Provider para GitHub Actions

## ✅ Pré‑requisitos

- Terraform >= 1.5
- Conta GCP com permissões de admin para criar IAM/Cloud Run/Artifact Registry
- Bucket GCS para state remoto

## 🔐 Variáveis do ambiente

Edite o arquivo `infra/envs/main.tfvars` e preencha `project_id` e ajustes de nomes se necessário.

## 🧱 Backend remoto (GCS)

O backend está definido como **GCS**. No `terraform init`, passe o bucket:

```sh
terraform init -backend-config="bucket=<SEU_BUCKET>" -backend-config="prefix=elt-birdbase/main"
```

## ▶️ Execução local

```sh
cd infra
terraform init -backend-config="bucket=<SEU_BUCKET>" -backend-config="prefix=elt-birdbase/main"
terraform plan -var-file=envs/main.tfvars
terraform apply -var-file=envs/main.tfvars
```

## 🔗 Outputs úteis

- `cloud_run_url`
- `deployer_service_account`
- `wif_provider`
