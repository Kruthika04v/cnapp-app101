pipeline {
    agent any

    environment {
        IMAGE_NAME = "cnappacr2026.azurecr.io/notes-app"
        RESOURCE_GROUP = "Cnapp-RG"
        AKS_CLUSTER = "myAKS-cluster"
        ACR_NAME = "cnappacr2026"
        TENANT_ID = "981439d1-88ac-4c7c-bd5d-d5df66bc0f4c"
    }

    stages {

        stage('Azure Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'azure-sp-creds',
                    usernameVariable: 'AZURE_CLIENT_ID',
                    passwordVariable: 'AZURE_CLIENT_SECRET'
                )]) {
                    sh '''
                    az login --service-principal \
                        --username $AZURE_CLIENT_ID \
                        --password $AZURE_CLIENT_SECRET \
                        --tenant $TENANT_ID

                    az account set --subscription "Kruthika's-Subscription"
                    '''
                }
            }
        }

        stage('Login to ACR') {
            steps {
                sh 'az acr login --name $ACR_NAME'
            }
        }

        stage('Build & Push Image (FIXED)') {
            steps {
                sh '''
                docker buildx build \
                    --platform linux/amd64 \
                    -t $IMAGE_NAME:${BUILD_NUMBER} \
                    -t $IMAGE_NAME:latest \
                    --push .
                '''
            }
        }

        stage('Deploy to AKS') {
            steps {
                sh '''
                az aks get-credentials \
                    --resource-group $RESOURCE_GROUP \
                    --name $AKS_CLUSTER \
                    --overwrite-existing

                kubectl get nodes

                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml

                kubectl set image deployment/notes-app \
                    notes-app=$IMAGE_NAME:${BUILD_NUMBER}

                kubectl rollout status deployment/notes-app
                '''
            }
        }
    }
}
