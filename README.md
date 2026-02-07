# AWS Cloud Labs
Hands-on AWS labs demonstrating cloud architecture, security, and scalability concepts. 

This repository contains hands-on AWS labs I’ve completed to build real-world cloud architecture skills.

## Labs

### 1. CloudFront + Private S3 Static Website
- Hosted a static website using Amazon S3
- Secured the bucket with Origin Access Control (OAC)
- Served content globally via CloudFront
- Resolved 403/404 errors caused by incorrect S3 endpoints and cache behavior

**AWS Services Used**
- Amazon S3
- Amazon CloudFront
- IAM
- AWS WAF (optional testing)

**Key Concepts**
- Private S3 access
- Origin Access Control (OAC)
- Cache invalidation
- HTTP vs HTTPS origin behavior

---

## Screenshots

### CloudFront – General Settings
![CloudFront General](screenshots/cloudfront-general.png)

### CloudFront – Origins (Private S3 with OAC)
![CloudFront Origins](screenshots/cloudfront-origins-s3-oac.png)

### CloudFront – Behaviors
![CloudFront Behaviors](screenshots/cloudfront-behaviors.png)

### CloudFront – Security
![CloudFront Security](screenshots/cloudfront-security.png)

### S3 Bucket Policy (OAC)
![S3 Bucket Permissions](screenshots/s3-bucket-permissions-oac.png)

### Site Live via CloudFront
![Site Working](screenshots/site-working-browser.png)

## EC2 + Apache Web Server Lab
### Overview

Launched an EC2 instance (Free Tier)
Connected securely via SSH using key pairs
Installed and configured Apache (httpd)
Exposed HTTP (port 80) publicly
Restricted SSH (port 22) to my IP only
Verified the site from a browser

![EC2 Running](ec2-instance-live.png)
![Security Group](security-inboundrules.png)
![Apache Status](terminal-running.png)
![Site Live](ec2-livesite.png)


