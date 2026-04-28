pipeline {
    agent any

    environment {
        IMAGE_NAME = "cnappacr2026.azurecr.io/notes-app"
        RESOURCE_GROUP = "Cnapp-RG"
        AKS_CLUSTER = "myAKS-cluster"
        ACR_NAME = "cnappacr2026"
        TENANT_ID = "981439d1-88ac-4c7c-bd5d-d5df66bc0f4c"
        IMAGE_TAG = "${BUILD_NUMBER}"
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

        stage('ACR Login') {
            steps {
                sh '''
                az acr login --name $ACR_NAME
                '''
            }
        }

        stage('Build Docker Image (AMD64 FIX)') {
            steps {
                sh '''
                echo "Building image for linux/amd64..."

                docker build \
                    --platform linux/amd64 \
                    -t $IMAGE_NAME:$IMAGE_TAG .

                docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest
                '''
            }
        }

        stage('Push Image to ACR') {
            steps {
                sh '''
                echo "Pushing images to ACR..."

                docker push $IMAGE_NAME:$IMAGE_TAG
                docker push $IMAGE_NAME:latest
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

                echo "Applying Kubernetes manifests..."
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml

                echo "Updating deployment image..."
                kubectl set image deployment/notes-app \
                    notes-app=$IMAGE_NAME:$IMAGE_TAG

                echo "Waiting for rollout..."
                kubectl rollout status deployment/notes-app --timeout=180s

                echo "Checking running pods..."
                kubectl get pods

                echo "Checking service (for browser access)..."
                kubectl get svc
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Deployment SUCCESS - Check AKS Service External IP"
        }
        failure {
            echo "❌ Pipeline FAILED - check logs"
        }
    }
}
