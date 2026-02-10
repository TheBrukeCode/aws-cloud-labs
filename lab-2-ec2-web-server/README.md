## EC2 + Apache Web Server Lab
### Overview

This lab demonstrates deploying a basic web server using Amazon EC2, configuring secure network access with Security Groups, and validating public connectivity by serving a static web page through Apache.
The goal of this lab is to understand foundational compute concepts in AWS, including instance lifecycle management, network exposure, and bootstrapping software using EC2 user data.

## Architecture Highlights
EC2 instance launched in a public subnet
Public IPv4 address used to access the web server
Security Group configured with:
HTTP (port 80) open to the internet
SSH (port 22) restricted to a trusted IP
Apache web server installed automatically at launch
Static HTML page served directly from the EC2 instance
This architecture represents the simplest compute-based web hosting model in AWS and serves as a baseline for more advanced designs (ALB, ASG, CloudFront).

## AWS Services Used
Amazon EC2
Virtual server hosting the web application
Amazon VPC
Provides networking and IP addressing
Security Groups
Acts as a stateful firewall controlling inbound access

## Implementation Details
EC2 Instance Deployment
Instance launched using the Free Tier–eligible instance type
Key pair configured for secure SSH access
Instance placed in a subnet with a route to an Internet Gateway
User Data Bootstrapping
Apache installed automatically during instance launch
Web server configured without manual SSH setup
Ensures consistent, repeatable instance initialization

## Network Security
Security Group rules explicitly defined:
Inbound HTTP traffic allowed on port 80
SSH access limited to a specific source IP
No direct modification of NACLs required
Demonstrates AWS best practice of using Security Groups for instance-level control
### Screenshots

### Live EC2 Instance
![EC2 Running](lab-2-ec2-web-server/screenshots/ec2-instance-live.png)

### Inbound Security Rules
![Security Group](lab-2-ec2-web-server/screenshots/security-inboundrules.png)

### Apache Service Running
![Apache Status](lab-2-ec2-web-server/screenshots/terminal-running.png)

### Website Live in Browser
![Site Live](lab-2-ec2-web-server/screenshots/ec2-livesite.png)
