### VR360 Project - Real Time Analytics

## Virtual Environment

python3 -m venv real_cv
source real_cv/bin/activate  # (Linux/Mac)
# or
real_cv\Scripts\activate     # (Windows)

# bash
pip install --upgrade pip
pip install -r requirements.txt
## Run Application Locally
# bash
cd app
streamlit run main.py

Access the web dashboard in your browser at http://localhost:8501/

# Deployment
# Docker
To build and run with Docker:

# bash
docker build -t real_cv_project .
docker run -p 8501:8501 real_cv_project
# Kubernetes
To deploy on a Kubernetes cluster (like AWS EKS/Minikube):

# bash
kubectl apply -f deployment/k8s/deployment.yaml
# AWS Deployment
You can run on EC2 or EKS. For EC2:

Launch EC2 instance and install Docker.

Clone your repo, build, and run the Docker image as above.

Use S3 for storing models or datasets.

For full MLOps and production scaling, deploy with Kubernetes on AWS EKS, and utilize AWS S3 for persistent storage.

# MLOps & CI-CD
# GitHub Actions Workflow
Create a workflow file at .github/workflows/deploy.yml:

text
name: CI/CD Pipeline

on:
  push:
    branches: [ "main" ]
  pull_request:

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: your-ecr-repo-name
  ECS_SERVICE: your-ecs-service-name
  ECS_CLUSTER: your-ecs-cluster-name
  CONTAINER_NAME: real-cv-app

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        pytest tests/

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}

    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v2

    - name: Build, tag, and push image to ECR
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        IMAGE_TAG: ${{ github.sha }}
      run: |
        docker build -t $ECR_REGISTRY/${{ env.ECR_REPOSITORY }}:$IMAGE_TAG .
        docker push $ECR_REGISTRY/${{ env.ECR_REPOSITORY }}:$IMAGE_TAG

    - name: Deploy to ECS
      uses: aws-actions/amazon-ecs-update-task-definition@v4
      with:
        task-definition: your-ecs-taskdef.json
        service: ${{ env.ECS_SERVICE }}
        cluster: ${{ env.ECS_CLUSTER }}
        image: ${{ steps.login-ecr.outputs.registry }}/${{ env.ECR_REPOSITORY }}:${{ github.sha }}
This workflow will automatically:

Run unit tests

Build and push your Docker image to AWS ECR

Trigger a deployment to your ECS/EKS or EC2-based service

Other deployment options: You can adapt this pipeline to trigger an EC2 update via CodeDeploy or SSM, or to perform a rolling update on your EKS cluster13.

Adding Secrets
Go to your GitHub repository → Settings → Secrets and variables → Actions:

Add AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY with necessary IAM permissions for ECR/ECS or EC2.

You can add other secrets as needed (e.g., DOCKERHUB_USERNAME, etc.)

Testing
Run unit tests before each commit or in CI:

bash
pytest tests/
