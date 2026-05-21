# Environment Policy

**Entity ID:** `devops:Environment`  
**Entity Type:** Entity  
**Version:** 1.0.0  
**Last Updated:** 2026-05-20

## Overview

This policy defines the governance rules, constraints, and best practices for Environment entities within the DevOps ecosystem. Environments represent deployment targets with specific configurations, security controls, and operational requirements.

## Description

Represents a deployment environment such as dev, staging, or production. Environments are isolated runtime contexts where applications are deployed, tested, and operated with appropriate security, monitoring, and compliance controls.

## Identity

**Identity Key:** `environmentId: UUID`  
**Human Reference:** `environmentName`

Each environment must have a unique UUID identifier and a human-readable name that clearly identifies its purpose and type.

## Attributes

### Core Attributes

| Attribute | Type | Description | Required |
|-----------|------|-------------|----------|
| `environmentId` | string (UUID) | Unique identifier for the environment | ✅ Yes |
| `environmentName` | string | Human-readable environment name | ✅ Yes |
| `environmentType` | enum | Type of environment | ✅ Yes |
| `cloudProvider` | enum | Cloud or infrastructure provider | ✅ Yes |
| `region` | string | Geographic region or data center | ✅ Yes |
| `isProduction` | boolean | Production environment flag | ✅ Yes |
| `requiresApproval` | boolean | Deployment approval required | ✅ Yes |
| `approvalGroup` | string | Group authorized to approve | ❌ No |
| `autoDeployEnabled` | boolean | Automatic deployment enabled | ✅ Yes |
| `rollbackEnabled` | boolean | Rollback capability enabled | ✅ Yes |
| `monitoringEnabled` | boolean | Monitoring and observability enabled | ✅ Yes |
| `alertingEnabled` | boolean | Alerting and notifications enabled | ✅ Yes |
| `maintenanceWindowStart` | time | Maintenance window start time | ❌ No |
| `maintenanceWindowEnd` | time | Maintenance window end time | ❌ No |
| `complianceLevel` | enum | Compliance certification level | ✅ Yes |

### Environment Types

| Type | Description | Use Case | Stability |
|------|-------------|----------|-----------|
| **DEV** | Development environment | Active development, frequent changes | Low |
| **SIT** | System Integration Testing | Integration testing | Medium |
| **UAT** | User Acceptance Testing | Business user testing | Medium |
| **STAGING** | Pre-production staging | Production-like testing | High |
| **PRODUCTION** | Live production | Customer-facing services | Critical |
| **DR** | Disaster Recovery | Backup production site | Critical |

### Cloud Providers

| Provider | Description | Regions |
|----------|-------------|---------|
| **AWS** | Amazon Web Services | us-east-1, us-west-2, eu-west-1, ap-southeast-1, etc. |
| **AZURE** | Microsoft Azure | eastus, westus2, westeurope, southeastasia, etc. |
| **GCP** | Google Cloud Platform | us-central1, us-east1, europe-west1, asia-southeast1, etc. |
| **IBM_CLOUD** | IBM Cloud | us-south, us-east, eu-gb, eu-de, jp-tok, etc. |
| **ON_PREMISE** | On-premises data center | Custom data center locations |
| **HYBRID** | Hybrid cloud | Mix of cloud and on-premises |

### Compliance Levels

- **SOC2** - Service Organization Control 2
- **PCI_DSS** - Payment Card Industry Data Security Standard
- **HIPAA** - Health Insurance Portability and Accountability Act
- **ISO27001** - Information Security Management
- **NONE** - No specific compliance requirements

## Invariants (Policy Rules)

### 1. Unique Environment Identifier
**Rule:** `environmentId must be unique`

**Enforcement:**
- System must validate uniqueness across all environments
- Duplicate environment IDs must be rejected
- Use UUID v4 for guaranteed uniqueness

**Rationale:** Ensures each environment can be uniquely identified and referenced across the DevOps ecosystem.

### 2. Non-Empty Environment Name
**Rule:** `environmentName cannot be empty`

**Enforcement:**
- Environment name must contain at least 3 characters
- Name must match pattern: `^[a-zA-Z0-9-_]+$`
- No spaces or special characters except hyphen and underscore
- Name must be unique within the organization

**Rationale:** Clear, consistent naming is essential for environment identification and management.

### 3. Production Approval Requirement
**Rule:** `isProduction environments require requiresApproval = true`

**Enforcement:**
- Production environments must have requiresApproval = true
- Approval cannot be disabled for production
- Bypass requires executive approval
- Audit trail must be maintained

**Rationale:** Ensures human oversight for production deployments to prevent unauthorized or risky changes.

### 4. Production Monitoring Requirement
**Rule:** `isProduction environments must have monitoringEnabled = true`

**Enforcement:**
- Production environments must have monitoring enabled
- Monitoring cannot be disabled
- Monitoring must cover all critical metrics
- Alerts must be configured

**Rationale:** Ensures production issues are detected and resolved quickly.

### 5. Production Alerting Requirement
**Rule:** `isProduction environments must have alertingEnabled = true`

**Enforcement:**
- Production environments must have alerting enabled
- Alerting cannot be disabled
- Alert channels must be configured
- On-call rotation must be defined

**Rationale:** Ensures production incidents trigger immediate notifications to responsible teams.

### 6. Production Auto-Deploy Restriction
**Rule:** `autoDeployEnabled must be false for PRODUCTION`

**Enforcement:**
- Production environments cannot have auto-deploy enabled
- All production deployments must be manual or approval-gated
- Override requires security team approval
- Audit trail must be maintained

**Rationale:** Prevents unintended or untested changes from reaching production automatically.

### 7. Disaster Recovery Requirement
**Rule:** `DR environment must exist if environmentType = PRODUCTION`

**Enforcement:**
- Every production environment must have a corresponding DR environment
- DR environment must be in a different region
- DR environment must be regularly tested
- Failover procedures must be documented

**Rationale:** Ensures business continuity and disaster recovery capabilities.

### 8. Compliance Level Requirement
**Rule:** `complianceLevel must match organizational policy`

**Enforcement:**
- Compliance level must be specified for all environments
- Production environments must have appropriate compliance level
- Compliance controls must be implemented
- Regular compliance audits must be conducted

**Rationale:** Ensures regulatory and organizational compliance requirements are met.

## Relationships

### Related Entities

1. **devops:Infrastructure**
   - **Relationship:** Environment runs on Infrastructure
   - **Cardinality:** 1:N (One environment has many infrastructure components)
   - **Constraint:** Infrastructure must exist before environment creation

2. **devops:Pipeline**
   - **Relationship:** Pipeline deploys to Environment
   - **Cardinality:** N:M (Many pipelines can deploy to many environments)
   - **Constraint:** Pipeline must specify target environment

3. **devops:Deployment**
   - **Relationship:** Environment receives Deployments
   - **Cardinality:** 1:N (One environment has many deployments)
   - **Constraint:** Deployment must target valid environment

4. **devops:Guardrail**
   - **Relationship:** Environment is governed by Guardrails
   - **Cardinality:** N:M (Many environments can have many guardrails)
   - **Constraint:** Production environments must have security guardrails

## Best Practices

### 1. Environment Naming Convention
```
<application>-<type>-<region>

Examples:
- ecommerce-api-prod-us-east
- ecommerce-api-staging-us-west
- ecommerce-api-dev-local
- platform-services-uat-eu-west
```

### 2. Environment Hierarchy

**Promotion Path:**
```
DEV → SIT → UAT → STAGING → PRODUCTION
```

**Characteristics by Environment:**

| Environment | Auto-Deploy | Approval | Monitoring | Alerting | Rollback |
|-------------|-------------|----------|------------|----------|----------|
| DEV | ✅ Yes | ❌ No | ⚠️ Basic | ❌ No | ⚠️ Optional |
| SIT | ✅ Yes | ❌ No | ⚠️ Basic | ❌ No | ✅ Yes |
| UAT | ⚠️ Optional | ⚠️ Optional | ✅ Yes | ⚠️ Optional | ✅ Yes |
| STAGING | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| PRODUCTION | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| DR | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |

### 3. Region Selection

**Primary Considerations:**
- **Latency:** Choose regions close to users
- **Compliance:** Select regions meeting regulatory requirements
- **Cost:** Consider pricing differences between regions
- **Availability:** Use regions with high availability SLAs
- **Disaster Recovery:** DR region should be geographically separate

**Recommended Configurations:**

**US-Based Application:**
- Primary: us-east-1 (AWS) or eastus (Azure)
- DR: us-west-2 (AWS) or westus2 (Azure)

**Europe-Based Application:**
- Primary: eu-west-1 (AWS) or westeurope (Azure)
- DR: eu-central-1 (AWS) or northeurope (Azure)

**Global Application:**
- Primary: us-east-1, eu-west-1, ap-southeast-1
- DR: us-west-2, eu-central-1, ap-northeast-1

### 4. Maintenance Windows

**Production Environments:**
- Schedule during low-traffic periods
- Typical windows: 2 AM - 6 AM local time
- Communicate to users in advance
- Have rollback plan ready

**Non-Production Environments:**
- More flexible scheduling
- Can be during business hours
- Minimal communication required

### 5. Monitoring Configuration

**Essential Metrics:**
- **Infrastructure:** CPU, memory, disk, network
- **Application:** Response time, error rate, throughput
- **Business:** Transaction volume, user activity
- **Security:** Failed logins, suspicious activity

**Monitoring Tools:**
- Prometheus + Grafana
- Datadog
- New Relic
- AWS CloudWatch
- Azure Monitor
- Google Cloud Monitoring

### 6. Alerting Configuration

**Alert Severity Levels:**

| Severity | Response Time | Escalation | Examples |
|----------|---------------|------------|----------|
| **Critical** | Immediate | Page on-call | Service down, data loss |
| **High** | 15 minutes | Notify team | High error rate, performance degradation |
| **Medium** | 1 hour | Email team | Elevated latency, minor issues |
| **Low** | 4 hours | Log only | Warnings, informational |

**Alert Channels:**
- PagerDuty / Opsgenie for critical alerts
- Slack / Teams for high/medium alerts
- Email for low priority alerts
- SMS for production critical alerts

## Compliance Requirements

### Production Environments

**Mandatory Settings:**
- ✅ `isProduction` = true
- ✅ `requiresApproval` = true
- ✅ `autoDeployEnabled` = false
- ✅ `rollbackEnabled` = true
- ✅ `monitoringEnabled` = true
- ✅ `alertingEnabled` = true
- ✅ `complianceLevel` = appropriate level (not NONE)

**Mandatory Controls:**
- ✅ Network isolation and security groups
- ✅ Encryption at rest and in transit
- ✅ Access logging and audit trails
- ✅ Backup and disaster recovery
- ✅ Incident response procedures
- ✅ Change management process

**Mandatory Documentation:**
- ✅ Architecture diagrams
- ✅ Runbooks and procedures
- ✅ Disaster recovery plan
- ✅ Security controls documentation
- ✅ Compliance certifications

### Non-Production Environments

**Mandatory Settings:**
- ✅ `monitoringEnabled` = true (recommended)
- ✅ `rollbackEnabled` = true (recommended)

**Recommended Settings:**
- ⚠️ `requiresApproval` = true (for UAT/STAGING)
- ⚠️ `alertingEnabled` = true (for STAGING)
- ⚠️ `complianceLevel` = matching production (for STAGING)

## Validation Rules

### Pre-Creation Validation
```yaml
validations:
  - check: environmentId uniqueness
    action: reject if duplicate
  
  - check: environmentName format
    action: reject if invalid pattern
  
  - check: environmentType validity
    action: reject if invalid type
  
  - check: cloudProvider support
    action: reject if provider not supported
  
  - check: region validity
    action: reject if region not valid for provider
  
  - check: production requirements
    action: reject if production rules violated
```

### Post-Creation Validation
```yaml
validations:
  - check: monitoring configured
    action: alert if not configured within 24 hours
  
  - check: alerting configured
    action: alert if not configured within 24 hours
  
  - check: DR environment exists
    action: alert if production without DR
  
  - check: compliance controls
    action: alert if controls not implemented
  
  - check: backup configured
    action: alert if not configured within 48 hours
```

### Runtime Validation
```yaml
validations:
  - check: deployment approval
    action: block deployment if approval required but not granted
  
  - check: maintenance window
    action: block deployment outside maintenance window
  
  - check: monitoring health
    action: alert if monitoring not reporting
  
  - check: compliance drift
    action: alert if configuration drifts from policy
```

## Examples

### Example 1: Production Environment (AWS)
```json
{
  "environmentId": "330e8400-e29b-41d4-a716-446655440000",
  "environmentName": "ecommerce-api-prod-us-east",
  "environmentType": "PRODUCTION",
  "cloudProvider": "AWS",
  "region": "us-east-1",
  "isProduction": true,
  "requiresApproval": true,
  "approvalGroup": "production-approvers",
  "autoDeployEnabled": false,
  "rollbackEnabled": true,
  "monitoringEnabled": true,
  "alertingEnabled": true,
  "maintenanceWindowStart": "02:00:00",
  "maintenanceWindowEnd": "06:00:00",
  "complianceLevel": "SOC2"
}
```

### Example 2: Staging Environment (Azure)
```json
{
  "environmentId": "440e8400-e29b-41d4-a716-446655440001",
  "environmentName": "ecommerce-api-staging-us-west",
  "environmentType": "STAGING",
  "cloudProvider": "AZURE",
  "region": "westus2",
  "isProduction": false,
  "requiresApproval": true,
  "approvalGroup": "staging-approvers",
  "autoDeployEnabled": false,
  "rollbackEnabled": true,
  "monitoringEnabled": true,
  "alertingEnabled": true,
  "maintenanceWindowStart": "01:00:00",
  "maintenanceWindowEnd": "05:00:00",
  "complianceLevel": "SOC2"
}
```

### Example 3: Development Environment (GCP)
```json
{
  "environmentId": "550e8400-e29b-41d4-a716-446655440002",
  "environmentName": "ecommerce-api-dev-us-central",
  "environmentType": "DEV",
  "cloudProvider": "GCP",
  "region": "us-central1",
  "isProduction": false,
  "requiresApproval": false,
  "approvalGroup": null,
  "autoDeployEnabled": true,
  "rollbackEnabled": true,
  "monitoringEnabled": true,
  "alertingEnabled": false,
  "maintenanceWindowStart": null,
  "maintenanceWindowEnd": null,
  "complianceLevel": "NONE"
}
```

### Example 4: Disaster Recovery Environment (AWS)
```json
{
  "environmentId": "660e8400-e29b-41d4-a716-446655440003",
  "environmentName": "ecommerce-api-dr-us-west",
  "environmentType": "DR",
  "cloudProvider": "AWS",
  "region": "us-west-2",
  "isProduction": true,
  "requiresApproval": true,
  "approvalGroup": "production-approvers",
  "autoDeployEnabled": false,
  "rollbackEnabled": true,
  "monitoringEnabled": true,
  "alertingEnabled": true,
  "maintenanceWindowStart": "02:00:00",
  "maintenanceWindowEnd": "06:00:00",
  "complianceLevel": "SOC2"
}
```

### Example 5: UAT Environment (IBM Cloud)
```json
{
  "environmentId": "770e8400-e29b-41d4-a716-446655440004",
  "environmentName": "platform-services-uat-eu-gb",
  "environmentType": "UAT",
  "cloudProvider": "IBM_CLOUD",
  "region": "eu-gb",
  "isProduction": false,
  "requiresApproval": true,
  "approvalGroup": "business-users",
  "autoDeployEnabled": false,
  "rollbackEnabled": true,
  "monitoringEnabled": true,
  "alertingEnabled": true,
  "maintenanceWindowStart": "20:00:00",
  "maintenanceWindowEnd": "23:00:00",
  "complianceLevel": "ISO27001"
}
```

## Access Control

### Environment Access Levels

| Role | DEV | SIT | UAT | STAGING | PRODUCTION | DR |
|------|-----|-----|-----|---------|------------|-----|
| **Developer** | Full | Read/Write | Read | Read | Read | No Access |
| **QA Engineer** | Read | Full | Full | Read/Write | Read | No Access |
| **DevOps Engineer** | Full | Full | Full | Full | Read/Write | Read/Write |
| **SRE** | Read | Read | Read | Read/Write | Full | Full |
| **Security Team** | Read | Read | Read | Read | Read | Read |
| **Business User** | No Access | No Access | Read | No Access | No Access | No Access |

### Approval Groups

**Production Approvers:**
- Engineering Manager
- DevOps Lead
- Security Lead
- Product Owner

**Staging Approvers:**
- Team Lead
- Senior Developer
- QA Lead

**UAT Approvers:**
- Product Owner
- Business Analyst
- QA Lead

## Audit and Compliance

### Audit Trail Requirements
- Log all deployments with timestamp and user
- Track all approval decisions
- Record all configuration changes
- Monitor all access attempts
- Maintain audit logs for 1 year minimum (production)

### Compliance Checks
- Daily monitoring health check
- Weekly security scan
- Monthly access review
- Quarterly disaster recovery test
- Annual compliance audit

### Compliance Standards by Level

**SOC 2:**
- Access controls and authentication
- Encryption at rest and in transit
- Audit logging and monitoring
- Incident response procedures
- Change management process

**PCI DSS:**
- Network segmentation
- Encryption of cardholder data
- Access control and authentication
- Regular security testing
- Vulnerability management

**HIPAA:**
- PHI data encryption
- Access controls and audit trails
- Breach notification procedures
- Business associate agreements
- Risk assessments

**ISO 27001:**
- Information security management system
- Risk assessment and treatment
- Security controls implementation
- Continuous improvement
- Management review

## Troubleshooting

### Common Issues

**Issue 1: Deployment Blocked by Approval**
- **Symptom:** Deployment fails due to missing approval
- **Solution:** Request approval from authorized approvers
- **Prevention:** Plan deployments in advance, communicate with approvers

**Issue 2: Monitoring Not Reporting**
- **Symptom:** No metrics or alerts from environment
- **Solution:** Check monitoring agent status, verify network connectivity
- **Prevention:** Implement monitoring health checks, set up meta-alerts

**Issue 3: Auto-Deploy Enabled in Production**
- **Symptom:** Policy violation detected
- **Solution:** Disable auto-deploy immediately, investigate how it was enabled
- **Prevention:** Implement policy enforcement, regular compliance audits

**Issue 4: DR Environment Out of Sync**
- **Symptom:** DR environment configuration differs from production
- **Solution:** Sync DR configuration with production
- **Prevention:** Automate DR synchronization, regular DR testing

## Disaster Recovery

### DR Testing Schedule

| Environment Type | Test Frequency | Test Type |
|------------------|----------------|-----------|
| PRODUCTION | Quarterly | Full failover test |
| STAGING | Monthly | Partial failover test |
| UAT | As needed | Configuration validation |

### DR Procedures

**Failover Steps:**
1. Declare disaster and activate DR plan
2. Notify stakeholders and teams
3. Verify DR environment health
4. Update DNS to point to DR
5. Validate application functionality
6. Monitor DR environment closely
7. Document issues and resolutions

**Failback Steps:**
1. Verify primary environment is restored
2. Sync data from DR to primary
3. Test primary environment thoroughly
4. Schedule maintenance window
5. Update DNS to point to primary
6. Monitor primary environment
7. Deactivate DR environment
8. Conduct post-mortem review

## Metrics and KPIs

### Environment Health Metrics
- **Uptime:** Percentage of time environment is available
- **Deployment Frequency:** Number of deployments per week
- **Deployment Success Rate:** Percentage of successful deployments
- **Mean Time to Recovery (MTTR):** Average time to recover from incidents
- **Mean Time Between Failures (MTBF):** Average time between incidents

### Target KPIs by Environment

| Environment | Uptime | MTTR | Deployment Success | Deployment Frequency |
|-------------|--------|------|-------------------|---------------------|
| PRODUCTION | 99.9% | < 1 hour | > 99% | 1-2/week |
| STAGING | 99% | < 2 hours | > 95% | 5-10/week |
| UAT | 95% | < 4 hours | > 90% | 2-5/week |
| DEV | 90% | < 8 hours | > 85% | 10-20/week |

## Cost Optimization

### Cost Management Strategies

**Development Environments:**
- Use smaller instance sizes
- Implement auto-shutdown during off-hours
- Use spot/preemptible instances
- Share resources across teams

**Staging Environments:**
- Right-size instances based on usage
- Implement auto-scaling
- Use reserved instances for predictable workloads
- Regular cost reviews

**Production Environments:**
- Use reserved instances for base capacity
- Implement auto-scaling for peak loads
- Optimize storage and data transfer
- Regular cost optimization reviews

## References

- [Pipeline Policy](./PIPELINE_POLICY.md)
- [Stage Policy](./STAGE_POLICY.md)
- [Cloud Provider Best Practices](https://example.org/cloud-best-practices)
- [Disaster Recovery Planning](https://example.org/dr-planning)
- [Compliance Standards](https://example.org/compliance)
- [DevOps Ontology Specification](../devops-cicd-infrastructure-ontology.jsonld)

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-05-20 | DevOps Team | Initial policy creation |

---

**Policy Owner:** DevOps Platform Team  
**Review Cycle:** Quarterly  
**Next Review:** 2026-08-20