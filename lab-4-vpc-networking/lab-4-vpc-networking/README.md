# AWS CloudFormation VPC Lab (Lab 4)

This project provisions a complete AWS VPC infrastructure using CloudFormation, including public and private subnets, internet access, and secure S3 connectivity.

---

## Architecture

```
Internet
    │
    ▼
Internet Gateway (lab-4-vpc-igw)
    │
    ▼
┌─────────────────────────────────────┐
│           VPC (lab-4-vpc-vpc)       │
│         CIDR: 10.0.0.0/16           │
│                                     │
│  ┌──────────────┐  ┌─────────────┐  │
│  │ Public Subnet│  │Public Subnet│  │
│  │     AZ-1     │  │    AZ-2     │  │
│  └──────┬───────┘  └──────┬──────┘  │
│         │                 │         │
│    NAT Gateway            │         │
│         │                 │         │
│  ┌──────▼───────┐  ┌──────▼──────┐  │
│  │Private Subnet│  │Private Subnet│ │
│  │     AZ-1     │  │    AZ-2     │  │
│  └──────────────┘  └─────────────┘  │
│                                     │
│  S3 Gateway Endpoint                │
└─────────────────────────────────────┘
```

---

## Resources Created

| Resource | Name | Purpose |
|---|---|---|
| VPC | lab-4-vpc-vpc | Main network container (10.0.0.0/16) |
| Internet Gateway | lab-4-vpc-igw | Enables public internet access |
| Public Subnets (x2) | — | Host public-facing resources |
| Private Subnets (x2) | — | Host backend/internal resources |
| NAT Gateway | lab-4-nat-gw | Allows private subnets to reach internet (outbound only) |
| Elastic IP | — | Static IP assigned to NAT Gateway |
| Route Table (public) | — | Routes public subnet traffic to IGW |
| Route Tables (private x2) | — | Routes private subnet traffic to NAT Gateway |
| S3 VPC Endpoint | vpce-* | Private S3 access without internet routing |

---

## Key Concepts

- **Internet Gateway** — Allows inbound and outbound internet traffic for public subnets
- **NAT Gateway** — Allows private subnet instances to initiate outbound internet connections (e.g. for software updates) while blocking inbound connections from the internet
- **S3 VPC Endpoint** — Enables private subnets to access S3 without traffic leaving AWS's network
- **DNS Hostnames & Resolution** — Enabled on the VPC so EC2 instances receive DNS names

---

## Prerequisites

- AWS CLI installed and configured (`aws configure`)
- IAM permissions for VPC, CloudFormation, and EC2
- An AWS account in `us-east-1` (N. Virginia)

---

## Deployment

### Deploy the stack

```bash
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name lab-4-vpc-networking
```

### View stack resources

```bash
aws cloudformation describe-stack-resources \
  --stack-name lab-4-vpc-networking
```

---

## Cleanup

To avoid ongoing charges (especially from the NAT Gateway and Elastic IP), delete the stack when done:

```bash
aws cloudformation delete-stack \
  --stack-name lab-4-vpc-networking
```

> ⚠️ **Cost warning:** NAT Gateways and unattached Elastic IPs incur hourly charges. Always clean up after lab work.

---

## Tools Used

- AWS CloudFormation
- AWS CLI
- YAML
- Infrastructure as Code (IaC)
