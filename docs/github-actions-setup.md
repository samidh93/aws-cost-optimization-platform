# GitHub Actions Configuration Guide

## 🔐 Required GitHub Secrets

To enable GitHub Actions to build and push container images to ECR, you need to add these secrets to your GitHub repository:

### **1. AWS Access Key ID**
- **Secret Name**: `AWS_ACCESS_KEY_ID`
- **Value**: Your AWS access key ID
- **How to get**: AWS Console → IAM → Users → cost-optimization-user → Security credentials

### **2. AWS Secret Access Key**
- **Secret Name**: `AWS_SECRET_ACCESS_KEY`
- **Value**: Your AWS secret access key
- **How to get**: AWS Console → IAM → Users → cost-optimization-user → Security credentials

## 📋 How to Add Secrets to GitHub

### **Method 1: GitHub Web Interface**
1. Go to your GitHub repository
2. Click **Settings** tab
3. Click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Add each secret:
   - Name: `AWS_ACCESS_KEY_ID`
   - Value: `AKIA...` (your access key)
6. Click **Add secret**
7. Repeat for `AWS_SECRET_ACCESS_KEY`

### **Method 2: GitHub CLI**
```bash
# Install GitHub CLI if not installed
brew install gh

# Login to GitHub
gh auth login

# Add secrets
gh secret set AWS_ACCESS_KEY_ID --body "YOUR_ACCESS_KEY_ID"
gh secret set AWS_SECRET_ACCESS_KEY --body "YOUR_SECRET_ACCESS_KEY"
```

## 🚀 How to Trigger the Workflow

### **Automatic Triggers**
- **Push to main branch**: Builds and pushes images
- **Push to develop branch**: Builds and pushes images
- **Pull requests**: Builds images (doesn't push)

### **Manual Trigger**
1. Go to **Actions** tab in GitHub
2. Select **Build and Push Container Images**
3. Click **Run workflow**
4. Select branch and click **Run workflow**

## 📊 Monitoring the Workflow

### **View Progress**
1. Go to **Actions** tab in GitHub
2. Click on the latest workflow run
3. Click on **build-and-push** job
4. View logs for each step

### **Success Indicators**
- ✅ All steps show green checkmarks
- Images appear in ECR repositories
- No error messages in logs

## 🔧 Troubleshooting

### **Common Issues**

**1. AWS Credentials Error**
```
Error: The security token included in the request is invalid
```
**Solution**: Check that AWS secrets are correct and user has ECR permissions

**2. ECR Repository Not Found**
```
Error: repository does not exist
```
**Solution**: Ensure ECR repositories are created first (run `app-ecr-only.py`)

**3. Docker Build Fails**
```
Error: failed to build image
```
**Solution**: Check Dockerfile syntax and dependencies

### **Debug Steps**
1. Check GitHub Actions logs
2. Verify AWS credentials
3. Ensure ECR repositories exist
4. Test Docker builds locally

## 💰 Cost Considerations

### **GitHub Actions**
- **Free tier**: 2,000 minutes/month
- **Our workflow**: ~5-10 minutes per run
- **Estimated usage**: 20-40 runs/month = FREE

### **ECR Storage**
- **Free tier**: 500 MB/month
- **Our images**: ~350 MB total
- **Cost**: $0.00 (under free tier)

## 🎯 Next Steps After Setup

1. **Add secrets** to GitHub repository
2. **Push code** to trigger workflow
3. **Monitor build** progress in Actions tab
4. **Verify images** in ECR console
5. **Deploy to EKS** (next phase)

## 📝 Quick Commands

```bash
# Check if secrets are set
gh secret list

# View workflow runs
gh run list

# View specific run logs
gh run view <run-id>

# Trigger manual run
gh workflow run "Build and Push Container Images"
```
