# Pipeline Policy

**Entity ID:** `devops:Pipeline`  
**Entity Type:** Entity  
**Version:** 1.0.0  
**Last Updated:** 2026-05-20

## Overview

This policy defines the governance rules, constraints, and best practices for CI/CD Pipeline entities within the DevOps ecosystem. Pipelines represent the automated workflows that build, test, and deploy applications.

## Description

Represents a CI/CD pipeline definition including all stages, triggers, and configurations. Pipelines orchestrate the entire software delivery process from code commit to production deployment.

## Identity

**Identity Key:** `pipelineId: UUID`  
**Human Reference:** `pipelineName`

Each pipeline must have a unique UUID identifier and a human-readable name for easy reference and management.

## Attributes

### Core Attributes

| Attribute | Type | Description | Required |
|-----------|------|-------------|----------|
| `pipelineId` | string (UUID) | Unique identifier for the pipeline | ✅ Yes |
| `pipelineName` | string | Human-readable pipeline name | ✅ Yes |
| `pipelineType` | enum | Type of pipeline workflow | ✅ Yes |
| `triggerType` | enum | Event that triggers pipeline execution | ✅ Yes |
| `targetBranch` | string | Git branch this pipeline targets | ✅ Yes |
| `status` | enum | Current operational status | ✅ Yes |
| `createdBy` | string | User who created the pipeline | ✅ Yes |
| `createdAt` | datetime | Pipeline creation timestamp | ✅ Yes |
| `lastRunAt` | datetime | Last execution timestamp | ❌ No |
| `tool` | enum | CI/CD platform used | ✅ Yes |
| `configFilePath` | string | Path to pipeline configuration file | ✅ Yes |
| `notificationChannel` | string | Channel for pipeline notifications | ❌ No |
| `timeoutMinutes` | integer | Maximum execution time | ✅ Yes |

### Pipeline Types

- **BUILD** - Compiles source code and creates artifacts
- **DEPLOY** - Deploys applications to environments
- **TEST** - Runs automated test suites
- **RELEASE** - Creates and publishes releases
- **FULL** - Complete end-to-end pipeline (build + test + deploy)

### Trigger Types

- **PUSH** - Triggered on code push to repository
- **PULL_REQUEST** - Triggered on PR creation/update
- **SCHEDULE** - Triggered on cron schedule
- **MANUAL** - Manually triggered by user
- **TAG** - Triggered on Git tag creation

### Status Values

- **ACTIVE** - Pipeline is operational and can be triggered
- **INACTIVE** - Pipeline is disabled temporarily
- **DEPRECATED** - Pipeline is obsolete and should not be used

### Supported Tools

- **JENKINS** - Jenkins CI/CD server
- **GITHUB_ACTIONS** - GitHub Actions workflows
- **GITLAB_CI** - GitLab CI/CD pipelines
- **TEKTON** - Kubernetes-native CI/CD
- **AZURE_DEVOPS** - Azure Pipelines
- **CIRCLECI** - CircleCI platform

## Invariants (Policy Rules)

### 1. Unique Pipeline Identifier
**Rule:** `pipelineId must be unique`

**Enforcement:**
- System must validate uniqueness before pipeline creation
- Duplicate pipeline IDs must be rejected
- Use UUID v4 for guaranteed uniqueness

**Rationale:** Ensures each pipeline can be uniquely identified and referenced across the system.

### 2. Non-Empty Pipeline Name
**Rule:** `pipelineName cannot be empty`

**Enforcement:**
- Pipeline name must contain at least 3 characters
- Name must match pattern: `^[a-zA-Z0-9-_]+$`
- Whitespace-only names are invalid

**Rationale:** Human-readable names are essential for pipeline management and troubleshooting.

### 3. Valid Trigger Type
**Rule:** `triggerType must be valid`

**Enforcement:**
- Must be one of: PUSH, PULL_REQUEST, SCHEDULE, MANUAL, TAG
- Invalid trigger types must be rejected at creation
- Multiple triggers can be configured per pipeline

**Rationale:** Ensures pipelines are triggered by supported events only.

### 4. Valid Pipeline Type
**Rule:** `pipelineType must be valid`

**Enforcement:**
- Must be one of: BUILD, DEPLOY, TEST, RELEASE, FULL
- Type determines available stages and operations
- Cannot be changed after pipeline creation

**Rationale:** Pipeline type defines the workflow structure and available operations.

### 5. Positive Timeout
**Rule:** `timeoutMinutes must be greater than 0`

**Enforcement:**
- Minimum timeout: 5 minutes
- Maximum timeout: 480 minutes (8 hours)
- Default timeout: 60 minutes if not specified

**Rationale:** Prevents infinite pipeline execution and resource exhaustion.

### 6. Valid Configuration File
**Rule:** `configFilePath must exist in repository`

**Enforcement:**
- File path must be validated against repository
- File must be accessible and readable
- File format must match the CI/CD tool requirements
- Common paths: `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`

**Rationale:** Ensures pipeline configuration is version-controlled and accessible.

## Relationships

### Related Entities

1. **devops:Stage**
   - **Relationship:** Pipeline contains multiple Stages
   - **Cardinality:** 1:N (One pipeline has many stages)
   - **Constraint:** Pipeline must have at least one stage

2. **devops:Repository**
   - **Relationship:** Pipeline is associated with Repository
   - **Cardinality:** N:1 (Many pipelines can target one repository)
   - **Constraint:** Repository must exist before pipeline creation

3. **devops:Environment**
   - **Relationship:** Pipeline deploys to Environments
   - **Cardinality:** N:M (Many pipelines can deploy to many environments)
   - **Constraint:** DEPLOY pipelines must specify target environment

4. **devops:Artifact**
   - **Relationship:** Pipeline produces Artifacts
   - **Cardinality:** 1:N (One pipeline produces many artifacts)
   - **Constraint:** BUILD pipelines must produce at least one artifact

5. **devops:Guardrail**
   - **Relationship:** Pipeline is governed by Guardrails
   - **Cardinality:** N:M (Many pipelines can have many guardrails)
   - **Constraint:** Production pipelines must have security guardrails

## Best Practices

### 1. Pipeline Naming Convention
```
<team>-<application>-<type>-<environment>
Example: platform-api-gateway-deploy-prod
```

### 2. Configuration Management
- Store pipeline configurations in version control
- Use pipeline-as-code approach
- Implement configuration validation
- Document pipeline purpose and usage

### 3. Security
- Never store secrets in pipeline configuration
- Use secret management tools (Vault, AWS Secrets Manager)
- Implement least-privilege access
- Enable audit logging for all pipeline executions

### 4. Monitoring and Alerting
- Configure notifications for pipeline failures
- Set up metrics collection (duration, success rate)
- Implement alerting for timeout violations
- Track pipeline performance trends

### 5. Timeout Configuration
- Set realistic timeouts based on historical data
- Build pipelines: 15-30 minutes
- Test pipelines: 30-60 minutes
- Deploy pipelines: 10-20 minutes
- Full pipelines: 60-120 minutes

### 6. Trigger Strategy
- Use PUSH triggers for development branches
- Use PULL_REQUEST triggers for code review
- Use SCHEDULE triggers for nightly builds
- Use MANUAL triggers for production deployments
- Use TAG triggers for release creation

## Compliance Requirements

### Production Pipelines
- ✅ Must have ACTIVE status
- ✅ Must include security scanning stage
- ✅ Must include approval stage before deployment
- ✅ Must have monitoring enabled
- ✅ Must have rollback capability
- ✅ Must log all executions for audit

### Non-Production Pipelines
- ✅ Can have INACTIVE status temporarily
- ✅ Should include basic security checks
- ✅ May skip approval stages
- ✅ Should have monitoring enabled
- ✅ Should support rapid iteration

## Validation Rules

### Pre-Creation Validation
```yaml
validations:
  - check: pipelineId uniqueness
    action: reject if duplicate
  
  - check: pipelineName format
    action: reject if invalid pattern
  
  - check: configFilePath existence
    action: reject if file not found
  
  - check: tool compatibility
    action: reject if tool not supported
  
  - check: timeout range
    action: reject if outside 5-480 minutes
```

### Runtime Validation
```yaml
validations:
  - check: stage execution order
    action: fail pipeline if violated
  
  - check: guardrail compliance
    action: block deployment if failed
  
  - check: timeout exceeded
    action: terminate pipeline execution
  
  - check: artifact generation
    action: fail if required artifacts missing
```

## Examples

### Example 1: Full Production Pipeline
```json
{
  "pipelineId": "550e8400-e29b-41d4-a716-446655440000",
  "pipelineName": "platform-api-gateway-full-prod",
  "pipelineType": "FULL",
  "triggerType": "TAG",
  "targetBranch": "main",
  "status": "ACTIVE",
  "createdBy": "devops-team",
  "createdAt": "2026-05-20T10:00:00Z",
  "tool": "GITHUB_ACTIONS",
  "configFilePath": ".github/workflows/production.yml",
  "notificationChannel": "slack://devops-alerts",
  "timeoutMinutes": 120
}
```

### Example 2: Development Build Pipeline
```json
{
  "pipelineId": "660e8400-e29b-41d4-a716-446655440001",
  "pipelineName": "platform-api-gateway-build-dev",
  "pipelineType": "BUILD",
  "triggerType": "PUSH",
  "targetBranch": "develop",
  "status": "ACTIVE",
  "createdBy": "dev-team",
  "createdAt": "2026-05-20T09:00:00Z",
  "tool": "GITHUB_ACTIONS",
  "configFilePath": ".github/workflows/build.yml",
  "notificationChannel": "email://dev-team@example.com",
  "timeoutMinutes": 30
}
```

### Example 3: Scheduled Test Pipeline
```json
{
  "pipelineId": "770e8400-e29b-41d4-a716-446655440002",
  "pipelineName": "platform-api-gateway-test-nightly",
  "pipelineType": "TEST",
  "triggerType": "SCHEDULE",
  "targetBranch": "main",
  "status": "ACTIVE",
  "createdBy": "qa-team",
  "createdAt": "2026-05-20T08:00:00Z",
  "tool": "JENKINS",
  "configFilePath": "Jenkinsfile.test",
  "notificationChannel": "slack://qa-channel",
  "timeoutMinutes": 60
}
```

## Audit and Compliance

### Audit Trail Requirements
- Log all pipeline creations, modifications, and deletions
- Track all pipeline executions with timestamps
- Record all approval decisions
- Maintain execution history for 90 days minimum
- Store logs in immutable storage

### Compliance Checks
- Monthly review of ACTIVE pipelines
- Quarterly security audit of pipeline configurations
- Annual review of deprecated pipelines
- Continuous monitoring of timeout violations
- Regular validation of guardrail compliance

## Troubleshooting

### Common Issues

**Issue 1: Pipeline Timeout**
- **Symptom:** Pipeline exceeds configured timeout
- **Solution:** Increase timeout or optimize pipeline stages
- **Prevention:** Monitor average execution time and set appropriate timeouts

**Issue 2: Configuration File Not Found**
- **Symptom:** Pipeline fails to start due to missing config
- **Solution:** Verify configFilePath exists in repository
- **Prevention:** Validate file path during pipeline creation

**Issue 3: Invalid Trigger Type**
- **Symptom:** Pipeline not triggering as expected
- **Solution:** Verify trigger type matches repository events
- **Prevention:** Test trigger configuration before activation

## Metrics and KPIs

### Pipeline Health Metrics
- **Success Rate:** Percentage of successful pipeline runs
- **Average Duration:** Mean execution time across all runs
- **Failure Rate:** Percentage of failed pipeline runs
- **Timeout Rate:** Percentage of runs exceeding timeout
- **Queue Time:** Time waiting before execution starts

### Target KPIs
- Success Rate: > 95%
- Average Duration: < 30 minutes (BUILD), < 60 minutes (FULL)
- Failure Rate: < 5%
- Timeout Rate: < 1%
- Queue Time: < 5 minutes

## References

- [CI/CD Best Practices](https://example.org/cicd-best-practices)
- [Pipeline Security Guidelines](https://example.org/pipeline-security)
- [DevOps Ontology Specification](../devops-cicd-infrastructure-ontology.jsonld)

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-05-20 | DevOps Team | Initial policy creation |

---

**Policy Owner:** DevOps Platform Team  
**Review Cycle:** Quarterly  
**Next Review:** 2026-08-20