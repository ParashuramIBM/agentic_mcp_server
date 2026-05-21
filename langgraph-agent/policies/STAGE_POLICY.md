# Stage Policy

**Entity ID:** `devops:Stage`  
**Entity Type:** Entity  
**Version:** 1.0.0  
**Last Updated:** 2026-05-20

## Overview

This policy defines the governance rules, constraints, and best practices for Stage entities within CI/CD pipelines. Stages represent discrete phases of the software delivery process such as build, test, scan, and deploy.

## Description

Represents a stage within a CI/CD pipeline such as build, test, scan, deploy. Stages are the building blocks of pipelines, each performing specific tasks in a defined order to ensure quality and security throughout the delivery process.

## Identity

**Identity Key:** `stageId: UUID`  
**Human Reference:** `stageName`

Each stage must have a unique UUID identifier and a human-readable name that clearly describes its purpose within the pipeline.

## Attributes

### Core Attributes

| Attribute | Type | Description | Required |
|-----------|------|-------------|----------|
| `stageId` | string (UUID) | Unique identifier for the stage | ✅ Yes |
| `stageName` | string | Human-readable stage name | ✅ Yes |
| `stageType` | enum | Type of stage operation | ✅ Yes |
| `order` | integer | Execution order within pipeline | ✅ Yes |
| `isParallel` | boolean | Can run in parallel with other stages | ✅ Yes |
| `isMandatory` | boolean | Must execute successfully | ✅ Yes |
| `allowFailure` | boolean | Pipeline continues if stage fails | ✅ Yes |
| `timeoutMinutes` | integer | Maximum execution time | ✅ Yes |
| `retryCount` | integer | Number of retry attempts on failure | ✅ Yes |
| `runCondition` | string | Conditional expression for execution | ❌ No |
| `environment` | string | Target environment for stage | ❌ No |

### Stage Types

| Type | Description | Typical Duration | Mandatory |
|------|-------------|------------------|-----------|
| **BUILD** | Compile source code and create binaries | 5-15 min | ✅ Yes |
| **UNIT_TEST** | Run unit tests | 2-10 min | ✅ Yes |
| **INTEGRATION_TEST** | Run integration tests | 5-20 min | ✅ Yes |
| **SECURITY_SCAN** | Perform security vulnerability scanning | 3-15 min | ✅ Yes (Prod) |
| **CODE_QUALITY** | Analyze code quality and standards | 2-10 min | ⚠️ Recommended |
| **ARTIFACT_PUBLISH** | Publish build artifacts to registry | 1-5 min | ✅ Yes |
| **DEPLOY** | Deploy application to environment | 3-15 min | ✅ Yes |
| **SMOKE_TEST** | Run post-deployment smoke tests | 2-5 min | ✅ Yes (Prod) |
| **APPROVAL** | Manual approval gate | N/A | ✅ Yes (Prod) |
| **ROLLBACK** | Rollback to previous version | 2-10 min | ⚠️ On Failure |
| **NOTIFY** | Send notifications | < 1 min | ❌ No |

## Invariants (Policy Rules)

### 1. Unique Stage Identifier
**Rule:** `stageId must be unique`

**Enforcement:**
- System must validate uniqueness across all pipelines
- Duplicate stage IDs must be rejected
- Use UUID v4 for guaranteed uniqueness

**Rationale:** Ensures each stage can be uniquely tracked and referenced across the entire DevOps ecosystem.

### 2. Non-Empty Stage Name
**Rule:** `stageName cannot be empty`

**Enforcement:**
- Stage name must contain at least 3 characters
- Name must match pattern: `^[a-zA-Z0-9-_ ]+$`
- Whitespace-only names are invalid
- Recommended format: `<type>-<description>` (e.g., "build-api-service")

**Rationale:** Clear stage names are essential for pipeline visualization and troubleshooting.

### 3. Positive Order Value
**Rule:** `order must be positive integer`

**Enforcement:**
- Order must be >= 1
- Order values should be sequential (1, 2, 3, ...)
- Gaps in order sequence are allowed for future insertions
- Parallel stages can share the same order value

**Rationale:** Defines the execution sequence and dependencies between stages.

### 4. Valid Stage Type
**Rule:** `stageType must be valid`

**Enforcement:**
- Must be one of the defined stage types
- Invalid stage types must be rejected at creation
- Stage type determines available operations and tools
- Cannot be changed after stage creation

**Rationale:** Stage type defines the operations, tools, and validation rules applicable to the stage.

### 5. Mandatory Stage Execution
**Rule:** `isMandatory stages cannot be skipped`

**Enforcement:**
- Mandatory stages must execute in all pipeline runs
- Cannot be disabled or bypassed
- Failure of mandatory stage fails the entire pipeline
- Override requires explicit approval from authorized personnel

**Rationale:** Ensures critical quality and security gates are always enforced.

### 6. Security Before Production Deploy
**Rule:** `SECURITY_SCAN must run before DEPLOY in production pipelines`

**Enforcement:**
- SECURITY_SCAN stage order must be < DEPLOY stage order
- Production pipelines without SECURITY_SCAN are rejected
- SECURITY_SCAN must complete successfully before DEPLOY
- Bypass requires security team approval

**Rationale:** Prevents deployment of vulnerable code to production environments.

### 7. Production Approval Gate
**Rule:** `APPROVAL stage required before production deployment`

**Enforcement:**
- Production DEPLOY stages must be preceded by APPROVAL stage
- APPROVAL stage must have isMandatory = true
- Approval must be granted by authorized approvers
- Automated approvals are prohibited for production

**Rationale:** Ensures human oversight for production deployments to prevent unauthorized or risky changes.

## Relationships

### Related Entities

1. **devops:Pipeline**
   - **Relationship:** Stage belongs to Pipeline
   - **Cardinality:** N:1 (Many stages belong to one pipeline)
   - **Constraint:** Stage cannot exist without a parent pipeline

2. **devops:Guardrail**
   - **Relationship:** Stage is governed by Guardrails
   - **Cardinality:** N:M (Many stages can have many guardrails)
   - **Constraint:** SECURITY_SCAN and DEPLOY stages must have guardrails

3. **devops:SecurityScan**
   - **Relationship:** SECURITY_SCAN stage produces SecurityScan results
   - **Cardinality:** 1:N (One stage produces many scan results)
   - **Constraint:** SECURITY_SCAN stages must produce scan results

## Best Practices

### 1. Stage Naming Convention
```
<type>-<component>-<environment>
Examples:
- build-api-service
- test-integration-suite
- scan-security-sast
- deploy-production-blue
- approve-production-release
```

### 2. Stage Ordering Strategy

**Sequential Stages (Typical Order):**
```
1. BUILD
2. UNIT_TEST
3. CODE_QUALITY
4. SECURITY_SCAN
5. ARTIFACT_PUBLISH
6. DEPLOY (Dev)
7. INTEGRATION_TEST
8. APPROVAL (for Prod)
9. DEPLOY (Prod)
10. SMOKE_TEST
11. NOTIFY
```

**Parallel Stages (Same Order):**
```
Order 3:
- UNIT_TEST (parallel)
- CODE_QUALITY (parallel)
- SECURITY_SCAN (parallel)
```

### 3. Timeout Configuration

| Stage Type | Recommended Timeout | Maximum Timeout |
|------------|---------------------|-----------------|
| BUILD | 15 minutes | 30 minutes |
| UNIT_TEST | 10 minutes | 20 minutes |
| INTEGRATION_TEST | 20 minutes | 40 minutes |
| SECURITY_SCAN | 15 minutes | 30 minutes |
| CODE_QUALITY | 10 minutes | 20 minutes |
| ARTIFACT_PUBLISH | 5 minutes | 10 minutes |
| DEPLOY | 15 minutes | 30 minutes |
| SMOKE_TEST | 5 minutes | 10 minutes |
| APPROVAL | No timeout | N/A |
| ROLLBACK | 10 minutes | 20 minutes |
| NOTIFY | 2 minutes | 5 minutes |

### 4. Retry Strategy

| Stage Type | Recommended Retries | Retry Delay |
|------------|---------------------|-------------|
| BUILD | 1 | 30 seconds |
| UNIT_TEST | 2 | 10 seconds |
| INTEGRATION_TEST | 1 | 30 seconds |
| SECURITY_SCAN | 2 | 60 seconds |
| CODE_QUALITY | 1 | 30 seconds |
| ARTIFACT_PUBLISH | 3 | 30 seconds |
| DEPLOY | 0 | N/A |
| SMOKE_TEST | 2 | 30 seconds |
| APPROVAL | 0 | N/A |
| ROLLBACK | 1 | 10 seconds |
| NOTIFY | 3 | 10 seconds |

### 5. Failure Handling

**Critical Stages (allowFailure = false):**
- BUILD
- SECURITY_SCAN (production)
- DEPLOY
- APPROVAL

**Non-Critical Stages (allowFailure = true):**
- CODE_QUALITY (non-production)
- NOTIFY
- SMOKE_TEST (non-production)

### 6. Parallel Execution

**Safe for Parallel Execution:**
- UNIT_TEST + CODE_QUALITY
- SECURITY_SCAN + CODE_QUALITY
- Multiple DEPLOY stages to different environments

**Must Run Sequentially:**
- BUILD → ARTIFACT_PUBLISH
- SECURITY_SCAN → DEPLOY (production)
- APPROVAL → DEPLOY (production)
- DEPLOY → SMOKE_TEST

## Compliance Requirements

### Production Pipeline Stages

**Mandatory Stages:**
- ✅ BUILD
- ✅ UNIT_TEST
- ✅ SECURITY_SCAN
- ✅ ARTIFACT_PUBLISH
- ✅ APPROVAL
- ✅ DEPLOY
- ✅ SMOKE_TEST

**Stage Configuration:**
- ✅ All mandatory stages must have isMandatory = true
- ✅ SECURITY_SCAN must have allowFailure = false
- ✅ APPROVAL must be manual (no automation)
- ✅ DEPLOY must have rollback capability
- ✅ All stages must have appropriate timeouts

### Non-Production Pipeline Stages

**Mandatory Stages:**
- ✅ BUILD
- ✅ UNIT_TEST
- ✅ ARTIFACT_PUBLISH
- ✅ DEPLOY

**Optional Stages:**
- ⚠️ SECURITY_SCAN (recommended)
- ⚠️ CODE_QUALITY (recommended)
- ⚠️ INTEGRATION_TEST (recommended)
- ❌ APPROVAL (not required)

## Validation Rules

### Pre-Creation Validation
```yaml
validations:
  - check: stageId uniqueness
    action: reject if duplicate
  
  - check: stageName format
    action: reject if invalid pattern
  
  - check: order value
    action: reject if not positive integer
  
  - check: stageType validity
    action: reject if not in allowed types
  
  - check: timeout range
    action: reject if outside 1-120 minutes
  
  - check: production pipeline requirements
    action: reject if missing mandatory stages
```

### Runtime Validation
```yaml
validations:
  - check: stage execution order
    action: fail if order violated
  
  - check: mandatory stage completion
    action: fail pipeline if mandatory stage fails
  
  - check: security scan before deploy
    action: block deploy if scan not completed
  
  - check: approval before production deploy
    action: block deploy if not approved
  
  - check: timeout exceeded
    action: terminate stage execution
```

## Examples

### Example 1: Build Stage
```json
{
  "stageId": "880e8400-e29b-41d4-a716-446655440000",
  "stageName": "build-api-service",
  "stageType": "BUILD",
  "order": 1,
  "isParallel": false,
  "isMandatory": true,
  "allowFailure": false,
  "timeoutMinutes": 15,
  "retryCount": 1,
  "runCondition": "branch == 'main' || branch == 'develop'",
  "environment": null
}
```

### Example 2: Security Scan Stage (Production)
```json
{
  "stageId": "990e8400-e29b-41d4-a716-446655440001",
  "stageName": "scan-security-sast",
  "stageType": "SECURITY_SCAN",
  "order": 4,
  "isParallel": false,
  "isMandatory": true,
  "allowFailure": false,
  "timeoutMinutes": 15,
  "retryCount": 2,
  "runCondition": "environment == 'production'",
  "environment": "production"
}
```

### Example 3: Parallel Test Stages
```json
[
  {
    "stageId": "aa0e8400-e29b-41d4-a716-446655440002",
    "stageName": "test-unit-suite",
    "stageType": "UNIT_TEST",
    "order": 2,
    "isParallel": true,
    "isMandatory": true,
    "allowFailure": false,
    "timeoutMinutes": 10,
    "retryCount": 2,
    "runCondition": null,
    "environment": null
  },
  {
    "stageId": "bb0e8400-e29b-41d4-a716-446655440003",
    "stageName": "quality-code-analysis",
    "stageType": "CODE_QUALITY",
    "order": 2,
    "isParallel": true,
    "isMandatory": false,
    "allowFailure": true,
    "timeoutMinutes": 10,
    "retryCount": 1,
    "runCondition": null,
    "environment": null
  }
]
```

### Example 4: Production Approval Stage
```json
{
  "stageId": "cc0e8400-e29b-41d4-a716-446655440004",
  "stageName": "approve-production-release",
  "stageType": "APPROVAL",
  "order": 8,
  "isParallel": false,
  "isMandatory": true,
  "allowFailure": false,
  "timeoutMinutes": null,
  "retryCount": 0,
  "runCondition": "environment == 'production'",
  "environment": "production"
}
```

### Example 5: Deploy Stage with Rollback
```json
{
  "stageId": "dd0e8400-e29b-41d4-a716-446655440005",
  "stageName": "deploy-production-blue",
  "stageType": "DEPLOY",
  "order": 9,
  "isParallel": false,
  "isMandatory": true,
  "allowFailure": false,
  "timeoutMinutes": 15,
  "retryCount": 0,
  "runCondition": "approved == true",
  "environment": "production"
}
```

## Conditional Execution

### Run Condition Syntax
```javascript
// Branch-based conditions
branch == 'main'
branch startsWith 'release/'
branch matches '^feature/.*$'

// Environment-based conditions
environment == 'production'
environment in ['staging', 'production']

// Event-based conditions
trigger == 'PUSH'
trigger == 'TAG'

// Approval-based conditions
approved == true
approver in ['devops-team', 'security-team']

// Combined conditions
branch == 'main' && environment == 'production'
trigger == 'TAG' || manual == true
```

## Audit and Compliance

### Audit Trail Requirements
- Log all stage executions with start/end timestamps
- Record all stage failures with error details
- Track all retry attempts
- Log all approval decisions with approver identity
- Maintain execution logs for 90 days minimum

### Compliance Checks
- Daily validation of mandatory stage execution
- Weekly review of stage failure rates
- Monthly audit of production stage configurations
- Quarterly security scan compliance review
- Continuous monitoring of timeout violations

## Troubleshooting

### Common Issues

**Issue 1: Stage Timeout**
- **Symptom:** Stage exceeds configured timeout
- **Solution:** Increase timeout or optimize stage operations
- **Prevention:** Monitor average execution time and set appropriate timeouts

**Issue 2: Mandatory Stage Failure**
- **Symptom:** Pipeline fails due to mandatory stage failure
- **Solution:** Fix the underlying issue causing stage failure
- **Prevention:** Implement proper error handling and retry logic

**Issue 3: Security Scan Blocking Deploy**
- **Symptom:** Deploy stage blocked due to security scan failure
- **Solution:** Fix security vulnerabilities or request security team approval
- **Prevention:** Run security scans earlier in development cycle

**Issue 4: Parallel Stage Conflicts**
- **Symptom:** Parallel stages interfere with each other
- **Solution:** Ensure stages are truly independent or run sequentially
- **Prevention:** Carefully design stage dependencies

## Metrics and KPIs

### Stage Performance Metrics
- **Success Rate:** Percentage of successful stage executions
- **Average Duration:** Mean execution time per stage type
- **Failure Rate:** Percentage of failed stage executions
- **Retry Rate:** Percentage of stages requiring retries
- **Timeout Rate:** Percentage of stages exceeding timeout

### Target KPIs by Stage Type

| Stage Type | Success Rate | Avg Duration | Timeout Rate |
|------------|--------------|--------------|--------------|
| BUILD | > 98% | < 15 min | < 1% |
| UNIT_TEST | > 95% | < 10 min | < 2% |
| INTEGRATION_TEST | > 90% | < 20 min | < 3% |
| SECURITY_SCAN | > 95% | < 15 min | < 2% |
| DEPLOY | > 99% | < 15 min | < 0.5% |

## References

- [Pipeline Policy](./PIPELINE_POLICY.md)
- [CI/CD Stage Best Practices](https://example.org/stage-best-practices)
- [Security Scanning Guidelines](https://example.org/security-scanning)
- [DevOps Ontology Specification](../devops-cicd-infrastructure-ontology.jsonld)

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-05-20 | DevOps Team | Initial policy creation |

---

**Policy Owner:** DevOps Platform Team  
**Review Cycle:** Quarterly  
**Next Review:** 2026-08-20