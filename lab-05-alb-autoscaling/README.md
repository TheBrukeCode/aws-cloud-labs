# AWS ALB + Auto Scaling Lab (Lab 5)

This project deploys a highly available web architecture using:

- Application Load Balancer
- Auto Scaling Group
- EC2 instances
- Target Groups
- Public subnets across multiple Availability Zones

## Architecture

Internet  
↓  
Application Load Balancer  
↓  
Target Group  
↓  
Auto Scaling Group  
↓  
EC2 Instances  

---

## Application Load Balancer

![ALB](screenshots/lab5balancer.png)

## Target Group

![Target Group](screenshots/lab5targets.png)

## Auto Scaling Group

![Auto Scaling](screenshots/lab5asg.png)

## EC2 Instances

![EC2](screenshots/lab5instances.png)



## Resources Created

| Resource | Purpose |
|--------|--------|
| Application Load Balancer | Distributes traffic |
| Target Group | Routes requests to EC2 |
| Auto Scaling Group | Maintains instance count |
| EC2 Instances | Serve web traffic |

## Deployment

```bash
aws cloudformation deploy \
--template-file template.yaml \
--stack-name lab-5-alb-autoscaling
