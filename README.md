# 🚀 ELT Birdbase

Projeto com a ingestão de dados do projeto birdbase

## 📚 Documentação

Wiki projeto: {Link}

## 🛠️ Setup

### 🐍 Python

```sh
# MacOS
brew install python@3.12
```

### 🎛️ Venv


#### 🐧 Linux e MacOS
```sh
python3.12 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## 🔥 Execução (Flask)

Autenticação Google Cloud:
```sh
gcloud auth application-default login
```

Para executar a aplicação em modo desenvolvimento, utilize:

```sh
export FLASK_APP=main.py && export FLASK_ENV=development && export FLASK_DEBUG=1 && python3 main.py
```

Caso queira simular produção, utilize:

```sh
export FLASK_APP=main.py && export FLASK_ENV=prod && python3 main.py
```

Estas mesmas variáveis de ambiente podem ser configuradas launch.json do VSCode.

### Exemplos

```sh
curl --location --request POST 'http://127.0.0.1:5000/birds/names'
```

## 🚀 CI/CD

A esteira CI/CD usa **GitHub Actions + Terraform + GCP** com um ambiente único.

### Secrets necessários (GitHub Actions)

Configure os secrets abaixo no repositório:

- `GCP_PROJECT_ID`
- `GCP_SERVICE_ACCOUNT`
- `GCP_WORKLOAD_IDENTITY_PROVIDER`
- `TF_STATE_BUCKET`
- `GCP_REGION`

### Fluxo

1. Pull Request → valida Python + Terraform.
2. Push em `main` → build + deploy.

Consulte `infra/README.md` para detalhes de Terraform/WIF.
