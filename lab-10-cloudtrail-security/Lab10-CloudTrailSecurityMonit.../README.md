# Lab 10 - CloudTrail Security Monitoring

## Overview
Built a security monitoring pipeline using AWS CloudTrail, CloudWatch, and SNS to detect and alert on suspicious API activity in real time.

## Architecture
```mermaid
graph TD
    A[AWS API Calls] --> B[CloudTrail]
    B --> C[S3 Bucket - Log Archive]
    B --> D[CloudWatch Log Group]
    D --> E[Metric Filter - DeleteTrail Events]
    E --> F[CloudWatch Alarm]
    F --> G[SNS Topic]
    G --> H[Email Alert]
```

## Resources Created
- **CloudTrail** - Multi-region trail with global service events
- **S3 Bucket** - Encrypted log archive
- **CloudWatch Log Group** - Real-time log streaming
- **Metric Filter** - Detects `DeleteTrail` API calls
- **CloudWatch Alarm** - Triggers on suspicious activity
- **SNS Topic** - Security alert notifications
- **IAM Role** - Least-privilege CloudTrail logging

## Key Concepts
- Security monitoring and threat detection
- CloudWatch metric filters for API event detection
- SNS alerting pipeline
- Infrastructure as Code via CloudFormation

## Deployment
```bash
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name lab10-cloudtrail-monitoring \
  --capabilities CAPABILITY_NAMED_IAM
```
## Screenshots

### CloudFormation Stack - CREATE_COMPLETE
![CloudFormation](screenshots/lab10cloudformation.png)

### CloudTrail - SecurityTrail Active
![CloudTrail](screenshots/lab10cloudtrail.png)

### CloudWatch Alarm
![CloudWatch Alarm](screenshots/lab10cloudwatch.png)

### SNS Topic
![SNS Topic](screenshots/lab10SNS.png)

### S3 Bucket
![S3 Bucket](screenshots/lab10securitytrail.png)