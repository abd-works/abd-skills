# {SolutionName} — Deployment Architecture Elements

> **Diagram:** `deployment-architecture.drawio` · C4 Deployment
> **Last updated:** YYYY-MM-DD

---

## Environments

*Use when: a distinct deployment target exists (Production, Staging, Development). One entry per environment shown in the diagram.*

### {Environment Name} (Deployment Environment)
{Where it runs and the availability or purpose expectation.}

### {Environment Name} (Deployment Environment) *(if applicable)*
{Where it runs and the availability or purpose expectation.}

---

## Deployment Nodes

*Use when: an infrastructure element hosts containers or other nodes — region, VPC, AZ, cluster, managed service, VM. One entry per box or nested boundary in the diagram.*

### {Name} (Deployment Node)
{Provider / technology and what it hosts.}

### {Name} (Deployment Node)
{Provider / technology and what it hosts.}

### {Name} (Deployment Node) *(if applicable)*
{Provider / technology and what it hosts.}

---

## Infrastructure Nodes

*Use when: a supporting network element appears in the diagram — load balancer, CDN, DNS, WAF, API gateway. One entry per node.*

### {Name} (Infrastructure Node)
{Type and traffic role.}

### {Name} (Infrastructure Node) *(if applicable)*
{Type and traffic role.}

---

## Container Instances

*Use when: a running application, service, or database appears in the diagram. One entry per distinct process.*

### {Name} (Container Instance)
{What runs, replica count, and scaling behaviour.}

### {Name} (Container Instance) *(if applicable)*
{What runs, replica count, and scaling behaviour.}

---

## Relationships

*Use when: an arrow appears in the diagram. One entry per arrow; state protocol and whether the path is public or private.*

### {Source} → {Target}: {Protocol} (Relationship)
{What flows and across which network boundary.}

### {Source} → {Target}: {Protocol} (Relationship)
{What flows and across which network boundary.}

---

## Legend

| Visual | Meaning |
|---|---|
| Outer rounded box | Deployment environment |
| Inner rounded box | Deployment node |
| Solid box | Container instance |
| Diamond / cylinder | Infrastructure node |
| Solid arrow | Runtime connection; label shows protocol |
| Dashed arrow | Async / event-driven connection |

---

## Example

*Remove this section before committing.*

```markdown
## Environments

### Production (Deployment Environment)
AWS us-east-1; multi-AZ at the data tier, 99.9% availability target.

### Staging (Deployment Environment)
Single-AZ mirror of production at reduced instance sizes; used for pre-release testing.

## Deployment Nodes

### AWS us-east-1 (Deployment Node)
Primary AWS region hosting all production workloads.

### Production VPC (Deployment Node)
Isolates production resources; public subnets for the ALB, private subnets for app and
data tiers.

### AWS RDS PostgreSQL 15 Multi-AZ (Deployment Node)
Managed relational database; primary in us-east-1a, synchronous standby in us-east-1b.

### AWS ElastiCache Redis 7 (Deployment Node)
Single-node managed cache; cache miss on failure is the accepted degradation.

## Infrastructure Nodes

### AWS ALB (Infrastructure Node)
Application Load Balancer; terminates HTTPS and routes traffic to ECS target groups.

### AWS CloudFront (Infrastructure Node)
CDN caching static SPA assets globally; forwards /api/* to the ALB.

## Container Instances

### Orders API (Container Instance)
Node.js/Fastify; 2 ECS Fargate tasks, auto-scales to 10 on CPU above 70%.

### Admin API (Container Instance)
Node.js/Fastify; 1 ECS Fargate task, not publicly routable.

## Relationships

### Customer → CloudFront: HTTPS (Relationship)
Browser requests static assets from the edge; API calls forwarded to the ALB.

### CloudFront → ALB: HTTPS (Relationship)
CloudFront forwards /api/* to the ALB within the AWS network.

### ALB → Orders API: HTTP (Relationship)
Decrypted requests forwarded to ECS containers on port 3000 in the private subnet.

### Orders API → RDS: TCP 5432 (Relationship)
API tasks connect to the RDS primary over the Postgres wire protocol in the private subnet.
```
