pipeline {
    agent any

    environment {
        ACR_NAME = "cnappacr2026"
        ACR_LOGIN_SERVER = "cnappacr2026.azurecr.io"
        IMAGE_NAME = "notes-app"

        RESOURCE_GROUP = "Cnapp-RG"
        AKS_CLUSTER = "myAKS-cluster"

        TENANT_ID = "981439d1-88ac-4c7c-bd5d-d5df66bc0f4c"
        SUBSCRIPTION = "Kruthika's-Subscription"
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

                    az account set --subscription "$SUBSCRIPTION"
                    '''
                }
            }
        }

        stage('Login to ACR') {
            steps {
                sh '''
                az acr login --name $ACR_NAME
                '''
            }
        }

        stage('Build Docker Image (FIXED AMD64)') {
            steps {
                sh '''
                echo "Building Docker image for AMD64..."

                docker build --platform linux/amd64 \
                    -t $ACR_LOGIN_SERVER/$IMAGE_NAME:${BUILD_NUMBER} .

                docker tag $ACR_LOGIN_SERVER/$IMAGE_NAME:${BUILD_NUMBER} \
                           $ACR_LOGIN_SERVER/$IMAGE_NAME:latest
                '''
            }
        }

        stage('Push Image to ACR') {
            steps {
                sh '''
                echo "Pushing image to ACR..."

                docker push $ACR_LOGIN_SERVER/$IMAGE_NAME:${BUILD_NUMBER}
                docker push $ACR_LOGIN_SERVER/$IMAGE_NAME:latest
                '''
            }
        }

        stage('Deploy to AKS') {
            steps {
                sh '''
                echo "Getting AKS credentials..."

                az aks get-credentials \
                    --resource-group $RESOURCE_GROUP \
                    --name $AKS_CLUSTER \
                    --overwrite-existing

                echo "Checking cluster..."
                kubectl get nodes

                echo "Deploying Kubernetes manifests..."
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml

                echo "Updating image..."
                kubectl set image deployment/notes-app \
                    notes-app=$ACR_LOGIN_SERVER/$IMAGE_NAME:${BUILD_NUMBER}

                '''
            }
        }
    }

    post {
        success {
            echo "✅ SUCCESS: App deployed to AKS"
        }

        failure {
            echo "❌ FAILED: Check logs for issues"
        }
    }
}
