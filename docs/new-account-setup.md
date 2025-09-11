# New AWS Account Setup Guide

This guide will help you set up a new AWS account specifically for this cost optimization platform project.

## 🆕 Creating a New AWS Account

### **Step 1: Account Creation**
1. **Go to AWS Sign-up**: https://aws.amazon.com/
2. **Click "Create an AWS Account"**
3. **Enter account details**:
   - Email address (use a different email than your existing account)
   - Password
   - AWS account name (e.g., "Cost-Optimization-Demo")

### **Step 2: Contact Information**
1. **Account type**: Personal
2. **Full name**: Your name
3. **Phone number**: Your phone number
4. **Country/Region**: Select your country
5. **Address**: Your address

### **Step 3: Payment Information**
1. **Credit/Debit card**: Required even for free tier
2. **Billing address**: Same as contact address
3. **Identity verification**: Complete phone verification

### **Step 4: Support Plan**
1. **Choose "Basic Support"** (Free)
2. **Skip** paid support plans

### **Step 5: Account Verification**
1. **Wait for account activation** (usually immediate)
2. **Check email** for confirmation
3. **Sign in** to AWS Console

## 🔑 Setting Up Access Keys

### **Step 1: Create IAM User**
1. **Go to IAM Console**: https://console.aws.amazon.com/iam/
2. **Click "Users"** → "Create user"
3. **User name**: `cost-optimization-user`
4. **Access type**: Programmatic access
5. **Attach policies**: `AdministratorAccess` (for demo purposes)
6. **Create user**

### **Step 2: Download Credentials**
1. **Download CSV file** with access keys
2. **Keep this file secure** - you won't see it again!

### **Step 3: Configure AWS CLI**
```bash
aws configure
# Enter your access key ID
# Enter your secret access key
# Region: us-east-1
# Output format: json
```

## 🌍 Region Selection

**Recommended regions for free tier:**
- **us-east-1** (N. Virginia) - Best for free tier
- **us-west-2** (Oregon) - Good alternative
- **eu-west-1** (Ireland) - For EU users
- **ap-southeast-1** (Singapore) - For Asia users

**Set your region:**
```bash
aws configure set region us-east-1
```

## ✅ Verification Steps

### **Step 1: Verify Account Setup**
```bash
./scripts/verify-new-account.py
```

This will check:
- ✅ AWS credentials are working
- ✅ Account has no charges (new account)
- ✅ All required services are available
- ✅ Region is properly configured

### **Step 2: Check Free Tier Status**
1. **Go to AWS Billing Console**: https://console.aws.amazon.com/billing/
2. **Click "Free Tier"** in the left sidebar
3. **Verify you see "12 months remaining"**
4. **Check available services**:
   - EC2: 750 hours/month
   - S3: 5GB storage
   - Lambda: 1M requests/month
   - RDS: 750 hours/month

## 🚀 Next Steps

Once your new account is verified:

1. **Run setup**:
   ```bash
   ./scripts/setup.sh
   ```

2. **Deploy the platform**:
   ```bash
   ./scripts/deploy.sh
   ```

3. **Access the platform**:
   ```bash
   ./scripts/get-urls.sh
   ```

4. **Always cleanup when done**:
   ```bash
   ./scripts/cleanup.sh
   ```

## ⚠️ Important Reminders

### **Free Tier Limits to Remember:**
- **EC2**: Only use t2.micro instances
- **EKS**: Free cluster management, pay for worker nodes
- **Lambda**: 1M requests/month
- **S3**: 5GB storage
- **RDS**: Only db.t2.micro instances
- **CloudWatch**: 10 custom metrics

### **Cost Monitoring:**
- **Set up billing alerts** in AWS Console
- **Monitor costs daily** during development
- **Always run cleanup scripts** after testing
- **Check AWS Billing Dashboard** regularly

### **Security Best Practices:**
- **Never commit access keys** to git
- **Use IAM roles** when possible
- **Enable MFA** on your root account
- **Rotate access keys** regularly

## 🆘 Troubleshooting

### **Common Issues:**

1. **"Access Denied" errors**:
   - Wait 5-10 minutes for permissions to propagate
   - Check IAM user has correct policies

2. **"Region not available"**:
   - Some services take time to be available in new accounts
   - Try a different region

3. **"Cost Explorer not available"**:
   - Normal for new accounts
   - May take 24-48 hours to be available

4. **"EKS not available"**:
   - EKS may not be available in all regions for new accounts
   - Try us-east-1 or us-west-2

### **Getting Help:**
- **AWS Documentation**: https://docs.aws.amazon.com/
- **AWS Support**: Basic support is free
- **AWS Forums**: https://forums.aws.amazon.com/

## 📞 Support

If you encounter issues:
1. **Check this guide** first
2. **Run verification scripts**
3. **Check AWS Console** for error messages
4. **Contact AWS Support** if needed

Remember: This is a demonstration project - always prioritize cost management and cleanup!
