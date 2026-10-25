# Azure App Service and Container Apps Deployment Guide for Tara PrivacyOS

This repository is **100% cloud-ready** for direct deployment on Microsoft Azure.

---

## 🚀 Option 1: Azure App Service (Linux Web App - Recommended)

### Step 1: Login to Azure CLI
```bash
az login
```

### Step 2: Create Resource Group and App Service Plan
```bash
az group create --name TaraPrivacyOS-RG --location eastus
az appservice plan create --name TaraPrivacyOS-Plan --resource-group TaraPrivacyOS-RG --sku B1 --is-linux
```

### Step 3: Create the Web App with Python 3.11 Runtime
```bash
az webapp create \
  --resource-group TaraPrivacyOS-RG \
  --plan TaraPrivacyOS-Plan \
  --name tara-privacyos-app \
  --runtime "PYTHON:3.11" \
  --startup-file "python run.py"
```

### Step 4: Configure App Settings & Environment Variables
Run this command or configure them via **Azure Portal > Configuration > Application Settings**:
```bash
az webapp config appsettings set --resource-group TaraPrivacyOS-RG --name tara-privacyos-app --settings \
  PORT=8000 \
  ENV=production \
  AZURE_OPENAI_ENDPOINT="https://tara-infotech-storytellingupdated.services.ai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-02-15-preview" \
  AZURE_OPENAI_API_KEY="YOUR_AZURE_OPENAI_KEY" \
  AZURE_OPENAI_DEPLOYMENT="gpt-4o-mini" \
  AZURE_OPENAI_API_VERSION="2024-02-15-preview"
```

### Step 5: Deploy Code via ZIP or Git
```bash
# Deploy with az webapp up or zip deploy
az webapp up --resource-group TaraPrivacyOS-RG --name tara-privacyos-app
```

---

## 🐳 Option 2: Docker Container (Azure App Service for Containers or Azure Container Apps)

### Build and Push to Azure Container Registry (ACR)
```bash
# 1. Login to ACR
az acr login --name <your-acr-name>

# 2. Build and Tag
docker build -t <your-acr-name>.azurecr.io/tara-privacyos:v1 .

# 3. Push Image
docker push <your-acr-name>.azurecr.io/tara-privacyos:v1

# 4. Deploy to Container App
az containerapp up \
  --name tara-privacyos \
  --resource-group TaraPrivacyOS-RG \
  --image <your-acr-name>.azurecr.io/tara-privacyos:v1 \
  --target-port 8000 \
  --ingress external
```

---

## 🩺 Verifying Health & Endpoints Post-Deployment

- **Health check**: `https://<your-app-name>.azurewebsites.net/api/health`
- **Azure OpenAI Connection Status**: `https://<your-app-name>.azurewebsites.net/api/azure-status`
- **Swagger Documentation**: `https://<your-app-name>.azurewebsites.net/docs`
- **Web UI & Login**: `https://<your-app-name>.azurewebsites.net/login`
