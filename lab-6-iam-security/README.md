# Lab 6: IAM Security Hardening

## What This Lab Does
Deploys a security-hardened AWS environment using IAM least-privilege principles and audit logging.

## Architecture
```mermaid
graph TD
    A[Developer] -->|Assumes Role| B[IAM Role: lab-6-ec2-role]
    B -->|Attached via| C[EC2 Instance Profile]
    C -->|Scoped Access Only| D[S3 App Bucket]
    B -->|Least Privilege Policy| E[s3:GetObject / s3:PutObject / s3:ListBucket]
    F[CloudTrail] -->|Logs All API Calls| G[S3 CloudTrail Logs Bucket]
    H[Any AWS API Call] -->|Captured by| F
```
## Resources Created
| Resource | Purpose |
|---|---|
| IAM Role | Least-privilege access for EC2 |
| EC2 Instance Profile | Attaches IAM role to EC2 |
| S3 App Bucket | Scoped data storage |
| S3 Logs Bucket | CloudTrail audit logs |
| CloudTrail Trail | Logs all AWS API calls |

## Key Security Concepts
- **Least Privilege** - EC2 role only has s3:GetObject, s3:PutObject, s3:ListBucket
- **Audit Logging** - CloudTrail records every API call made in the account
- **IaC Security** - All IAM resources defined in CloudFormation for auditability

## Deployment
```bash
aws cloudformation deploy \
  --template-file lab-6-iam-security.yaml \
  --stack-name lab-6-iam-security \
  --capabilities CAPABILITY_NAMED_IAM
```