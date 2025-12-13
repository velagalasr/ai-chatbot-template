# Deploying to Azure

This guide covers deploying your chatbot to Azure.

## Option 1: Azure Container Instances (ACI)

Simplest option for quick deployment.

### Prerequisites

- Azure account
- Azure CLI installed and configured
- Docker image built

### Steps

#### 1. Login to Azure

```bash
az login
```

#### 2. Create Resource Group

```bash
az group create --name chatbot-rg --location eastus
```

#### 3. Create Azure Container Registry (ACR)

```bash
az acr create --resource-group chatbot-rg --name chatbotregistry --sku Basic
```

#### 4. Build and Push Image

```bash
# Login to ACR
az acr login --name chatbotregistry

# Build and push
az acr build --registry chatbotregistry --image chatbot:latest -f deployment/azure/Dockerfile .
```

#### 5. Create Container Instance

```bash
az container create \
  --resource-group chatbot-rg \
  --name chatbot-instance \
  --image chatbotregistry.azurecr.io/chatbot:latest \
  --cpu 1 \
  --memory 2 \
  --registry-login-server chatbotregistry.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --dns-name-label chatbot-app \
  --ports 8501 \
  --environment-variables OPENAI_API_KEY=<your-key>
```

#### 6. Access Your Chatbot

```bash
# Get the FQDN
az container show --resource-group chatbot-rg --name chatbot-instance --query ipAddress.fqdn
```

Visit: `http://<fqdn>:8501`

## Option 2: Azure App Service

For production workloads with auto-scaling.

### Steps

#### 1. Create App Service Plan

```bash
az appservice plan create \
  --name chatbot-plan \
  --resource-group chatbot-rg \
  --is-linux \
  --sku B1
```

#### 2. Create Web App

```bash
az webapp create \
  --resource-group chatbot-rg \
  --plan chatbot-plan \
  --name chatbot-webapp \
  --deployment-container-image-name chatbotregistry.azurecr.io/chatbot:latest
```

#### 3. Configure App Settings

```bash
az webapp config appsettings set \
  --resource-group chatbot-rg \
  --name chatbot-webapp \
  --settings OPENAI_API_KEY=<your-key> \
             WEBSITES_PORT=8501
```

#### 4. Enable Container Registry Access

```bash
az webapp config container set \
  --name chatbot-webapp \
  --resource-group chatbot-rg \
  --docker-custom-image-name chatbotregistry.azurecr.io/chatbot:latest \
  --docker-registry-server-url https://chatbotregistry.azurecr.io \
  --docker-registry-server-user <username> \
  --docker-registry-server-password <password>
```

## Option 3: Azure Kubernetes Service (AKS)

For enterprise-scale deployments.

### Steps

#### 1. Create AKS Cluster

```bash
az aks create \
  --resource-group chatbot-rg \
  --name chatbot-cluster \
  --node-count 2 \
  --enable-managed-identity \
  --attach-acr chatbotregistry
```

#### 2. Get Credentials

```bash
az aks get-credentials --resource-group chatbot-rg --name chatbot-cluster
```

#### 3. Deploy to Kubernetes

Create `deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chatbot-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: chatbot
  template:
    metadata:
      labels:
        app: chatbot
    spec:
      containers:
      - name: chatbot
        image: chatbotregistry.azurecr.io/chatbot:latest
        ports:
        - containerPort: 8501
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: chatbot-secrets
              key: openai-key
---
apiVersion: v1
kind: Service
metadata:
  name: chatbot-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8501
  selector:
    app: chatbot
```

Deploy:

```bash
kubectl apply -f deployment.yaml
```

## Security with Azure Key Vault

### Store Secrets in Key Vault

```bash
# Create Key Vault
az keyvault create \
  --name chatbot-keyvault \
  --resource-group chatbot-rg \
  --location eastus

# Add secret
az keyvault secret set \
  --vault-name chatbot-keyvault \
  --name openai-key \
  --value "<your-key>"
```

### Access from Container Instance

```bash
az container create \
  --resource-group chatbot-rg \
  --name chatbot-instance \
  --image chatbotregistry.azurecr.io/chatbot:latest \
  --assign-identity \
  --environment-variables \
    AZURE_KEYVAULT_NAME=chatbot-keyvault
```

## Monitoring with Application Insights

```bash
# Create Application Insights
az monitor app-insights component create \
  --app chatbot-insights \
  --location eastus \
  --resource-group chatbot-rg \
  --application-type web

# Get instrumentation key
az monitor app-insights component show \
  --app chatbot-insights \
  --resource-group chatbot-rg \
  --query instrumentationKey
```

Add to environment variables:
```bash
APPLICATIONINSIGHTS_CONNECTION_STRING=<connection-string>
```

## Cost Management

1. **Use appropriate SKUs** (B1 for dev, S1+ for prod)
2. **Auto-scaling** for App Service
3. **Reserved Instances** for cost savings
4. **Azure Cost Management** for tracking
5. **Stop/deallocate** dev instances when not in use

## Backup and Disaster Recovery

1. **Azure Backup** for persistence
2. **Geo-redundant storage** for data
3. **Multiple regions** for high availability
4. **Azure Front Door** for global distribution
