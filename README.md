# AWS CloudFormation VPC Lab

This project provisions a basic AWS VPC infrastructure using CloudFormation.

## Architecture

Resources created:

- VPC (10.0.0.0/16)
- Public Subnet
- Internet Gateway
- VPC Gateway Attachment

## Deployment

Deploy using AWS CLI:

```bash
aws cloudformation deploy \
--template-file template.yaml \
--stack-name lab-4-vpc-networkingaws cloudformation delete-stack \
--stack-name lab-4-vpc-networking


Tools Used
AWS CloudFormation
AWS CLI
YAML
Infrastructure as Code
