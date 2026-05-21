# Knowledge Asset Policy

**Entity ID:** `knowledge:KnowledgeAsset`  
**Entity Type:** KnowledgeAsset  
**Version:** 1.0.0  
**Last Updated:** 2026-05-20

## Overview

This policy defines the governance rules, constraints, and best practices for Knowledge Asset entities within the DevOps ecosystem. Knowledge Assets represent organizational knowledge extracted from operations, incidents, and best practices.

## Description

Represents organizational knowledge extracted from DevOps entities and operations. Knowledge Assets capture best practices, lessons learned, troubleshooting guides, runbooks, and architecture decisions to enable knowledge reuse and organizational learning.

## Identity

**Identity Key:** `assetId: UUID`  
**Human Reference:** `assetName`

Each knowledge asset must have a unique UUID identifier and a descriptive name that clearly indicates its content and purpose.

## Attributes

### Core Attributes

| Attribute | Type | Description | Required |
|-----------|------|-------------|----------|
| `assetId` | string (UUID) | Unique identifier | ✅ Yes |
| `assetName` | string | Descriptive asset name | ✅ Yes |
| `assetType` | enum | Type of knowledge | ✅ Yes |
| `category` | enum | Knowledge category | ✅ Yes |
| `content` | string | Knowledge content | ✅ Yes |
| `sourceEntity` | string | Source entity ID | ✅ Yes |
| `sourceEntityType` | string | Type of source | ✅ Yes |
| `extractedAt` | datetime | Extraction timestamp | ✅ Yes |
| `confidence` | float (0-1) | Confidence score | ✅ Yes |
| `applicability` | array<string> | Where applicable | ✅ Yes |
| `tags` | array<string> | Categorization tags | ✅ Yes |
| `relatedAssets` | array<string> | Related asset IDs | ❌ No |
| `usageCount` | integer | Times used | ✅ Yes |
| `rating` | float (0-5) | User rating | ❌ No |
| `status` | enum | Asset status | ✅ Yes |

### Asset Types

| Type | Description | Use Case |
|------|-------------|----------|
| **BEST_PRACTICE** | Proven approaches | "Always run security scans before production" |
| **LESSON_LEARNED** | Knowledge from incidents | "Database migrations need 2x estimated time" |
| **TROUBLESHOOTING_GUIDE** | Problem resolution | "How to resolve pipeline timeout issues" |
| **RUNBOOK** | Operational procedures | "Production deployment runbook" |
| **ARCHITECTURE_DECISION** | Design decisions | "Why we chose Kubernetes over ECS" |
| **PATTERN** | Reusable patterns | "Blue-green deployment pattern" |
| **ANTI_PATTERN** | Patterns to avoid | "Don't deploy on Friday afternoons" |

### Categories

- **PIPELINE** - Pipeline-related knowledge
- **DEPLOYMENT** - Deployment knowledge
- **SECURITY** - Security knowledge
- **PERFORMANCE** - Performance optimization
- **RELIABILITY** - Reliability improvements
- **COST_OPTIMIZATION** - Cost reduction

### Status Values

- **DRAFT** - Initial creation, not reviewed
- **REVIEWED** - Reviewed by experts
- **APPROVED** - Approved for use
- **DEPRECATED** - Outdated, not recommended

## Invariants (Policy Rules)

### 1. Unique Asset Identifier
**Rule:** `assetId must be unique`

**Enforcement:**
- System must validate uniqueness across all knowledge assets
- Duplicate asset IDs must be rejected
- Use UUID v4 for guaranteed uniqueness

**Rationale:** Ensures each knowledge asset can be uniquely identified and referenced.

### 2. Non-Empty Asset Name
**Rule:** `assetName cannot be empty`

**Enforcement:**
- Asset name must contain at least 10 characters
- Name must be descriptive and meaningful
- Name should indicate content type and topic

**Rationale:** Clear names enable knowledge discovery and reuse.

### 3. Valid Asset Type
**Rule:** `assetType must be valid`

**Enforcement:**
- Must be one of the defined asset types
- Invalid types must be rejected
- Type determines validation rules and usage

**Rationale:** Asset type defines how knowledge is used and validated.

### 4. Valid Confidence Score
**Rule:** `confidence must be between 0 and 1`

**Enforcement:**
- Confidence score must be 0.0 to 1.0
- Automated extraction: 0.5-0.8
- Expert-created: 0.8-1.0
- Unvalidated: < 0.5

**Rationale:** Confidence indicates reliability and trustworthiness of knowledge.

### 5. Valid Status
**Rule:** `status must be valid`

**Enforcement:**
- Must be one of: DRAFT, REVIEWED, APPROVED, DEPRECATED
- Status transitions must follow workflow
- APPROVED assets require expert review
- DEPRECATED assets cannot be used

**Rationale:** Status workflow ensures knowledge quality and relevance.

## Relationships

### Related Entities

1. **devops:Pipeline**
   - **Relationship:** Knowledge extracted from Pipeline
   - **Cardinality:** N:1 (Many assets from one pipeline)

2. **devops:Stage**
   - **Relationship:** Knowledge extracted from Stage
   - **Cardinality:** N:1 (Many assets from one stage)

3. **devops:Repository**
   - **Relationship:** Knowledge extracted from Repository
   - **Cardinality:** N:1 (Many assets from one repository)

4. **devops:Environment**
   - **Relationship:** Knowledge extracted from Environment
   - **Cardinality:** N:1 (Many assets from one environment)

5. **analytics:Pattern**
   - **Relationship:** Knowledge derived from Pattern
   - **Cardinality:** N:M (Many-to-many relationship)

6. **analytics:Insight**
   - **Relationship:** Knowledge supports Insight
   - **Cardinality:** N:M (Many-to-many relationship)

## Best Practices

### 1. Knowledge Naming Convention
```
<type>: <topic> - <specific-detail>

Examples:
- "Best Practice: Production Deployment - Security Scanning"
- "Lesson Learned: Database Migration - Time Estimation"
- "Troubleshooting: Pipeline Timeout - Memory Issues"
- "Runbook: Incident Response - Production Outage"
```

### 2. Content Structure

**Best Practice Format:**
```markdown
## Context
[When and where this applies]

## Practice
[What to do]

## Rationale
[Why this works]

## Example
[Concrete example]

## References
[Related resources]
```

**Lesson Learned Format:**
```markdown
## Incident Summary
[What happened]

## Root Cause
[Why it happened]

## Resolution
[How it was fixed]

## Prevention
[How to prevent recurrence]

## Related Incidents
[Similar past incidents]
```

**Troubleshooting Guide Format:**
```markdown
## Problem Description
[Symptoms and indicators]

## Diagnosis Steps
[How to identify the issue]

## Resolution Steps
[Step-by-step fix]

## Verification
[How to confirm resolution]

## Prevention
[How to avoid in future]
```

### 3. Confidence Scoring

| Source | Confidence Range | Validation |
|--------|------------------|------------|
| Automated extraction | 0.5 - 0.7 | Requires review |
| Expert-created | 0.8 - 0.9 | Peer reviewed |
| Validated in production | 0.9 - 1.0 | Proven effective |
| Unvalidated | 0.0 - 0.5 | Not recommended |

### 4. Applicability Tagging

**Environment Tags:**
- `PRODUCTION`, `STAGING`, `UAT`, `DEV`

**Technology Tags:**
- `KUBERNETES`, `DOCKER`, `AWS`, `AZURE`, `GCP`

**Domain Tags:**
- `MICROSERVICES`, `MONOLITH`, `SERVERLESS`

**Team Tags:**
- `BACKEND`, `FRONTEND`, `DEVOPS`, `SRE`

### 5. Knowledge Lifecycle

```
DRAFT → REVIEWED → APPROVED → [IN_USE] → DEPRECATED
  ↓         ↓          ↓                      ↓
[Edit]  [Revise]  [Update]              [Archive]
```

**Lifecycle Rules:**
- DRAFT: Can be edited freely
- REVIEWED: Requires approval for changes
- APPROVED: Requires change request for updates
- DEPRECATED: Read-only, archived after 90 days

## Compliance Requirements

### Knowledge Quality Standards

**Mandatory for APPROVED Status:**
- ✅ Content must be clear and actionable
- ✅ Must include concrete examples
- ✅ Must reference source entities
- ✅ Must have confidence score ≥ 0.8
- ✅ Must be reviewed by domain expert
- ✅ Must have appropriate tags

**Recommended:**
- ⚠️ Include diagrams or screenshots
- ⚠️ Link to related documentation
- ⚠️ Provide success metrics
- ⚠️ Include contact information

### Review Requirements

**BEST_PRACTICE:**
- Minimum 2 expert reviews
- Validation in at least 3 use cases
- Documented success metrics

**LESSON_LEARNED:**
- Incident post-mortem completed
- Root cause analysis documented
- Prevention measures identified

**TROUBLESHOOTING_GUIDE:**
- Tested resolution steps
- Multiple scenarios covered
- Verification steps included

**RUNBOOK:**
- Step-by-step procedures
- Rollback procedures included
- Emergency contacts listed

## Validation Rules

### Pre-Creation Validation
```yaml
validations:
  - check: assetId uniqueness
    action: reject if duplicate
  
  - check: assetName length
    action: reject if < 10 characters
  
  - check: assetType validity
    action: reject if invalid
  
  - check: confidence range
    action: reject if outside 0-1
  
  - check: content not empty
    action: reject if empty
  
  - check: sourceEntity exists
    action: reject if invalid reference
```

### Post-Creation Validation
```yaml
validations:
  - check: expert review
    action: alert if not reviewed within 7 days
  
  - check: usage tracking
    action: alert if not used within 30 days
  
  - check: rating collection
    action: prompt users for rating after use
  
  - check: relevance check
    action: review if not used in 90 days
```

### Status Transition Validation
```yaml
transitions:
  DRAFT → REVIEWED:
    - requires: content completeness check
    - requires: expert assignment
  
  REVIEWED → APPROVED:
    - requires: expert approval
    - requires: confidence ≥ 0.8
    - requires: applicability defined
  
  APPROVED → DEPRECATED:
    - requires: deprecation reason
    - requires: replacement asset (if applicable)
```

## Examples

### Example 1: Best Practice
```json
{
  "assetId": "ka-001",
  "assetName": "Best Practice: Production Deployment - Security Scanning",
  "assetType": "BEST_PRACTICE",
  "category": "SECURITY",
  "content": "## Context\nAll production deployments\n\n## Practice\nAlways run SAST and DAST security scans before deploying to production. Block deployment if critical vulnerabilities are found.\n\n## Rationale\nPrevents deployment of vulnerable code, reduces security incidents by 85%.\n\n## Example\n```yaml\nstages:\n  - security_scan\n  - deploy_production\n```",
  "sourceEntity": "pipeline-prod-001",
  "sourceEntityType": "Pipeline",
  "extractedAt": "2026-05-20T10:00:00Z",
  "confidence": 0.95,
  "applicability": ["PRODUCTION", "STAGING"],
  "tags": ["security", "deployment", "scanning", "production"],
  "relatedAssets": ["ka-002", "ka-015"],
  "usageCount": 45,
  "rating": 4.8,
  "status": "APPROVED"
}
```

### Example 2: Lesson Learned
```json
{
  "assetId": "ka-002",
  "assetName": "Lesson Learned: Database Migration - Time Estimation",
  "assetType": "LESSON_LEARNED",
  "category": "DEPLOYMENT",
  "content": "## Incident Summary\nDatabase migration took 4 hours instead of estimated 2 hours, causing extended downtime.\n\n## Root Cause\nUnderestimated data volume and index rebuild time.\n\n## Resolution\nCompleted migration in maintenance window, communicated delay to stakeholders.\n\n## Prevention\n- Always multiply estimated time by 2x for database migrations\n- Test migrations on production-sized datasets\n- Have rollback plan ready\n- Schedule longer maintenance windows",
  "sourceEntity": "deployment-db-mig-001",
  "sourceEntityType": "Deployment",
  "extractedAt": "2026-05-15T14:30:00Z",
  "confidence": 0.92,
  "applicability": ["PRODUCTION", "STAGING"],
  "tags": ["database", "migration", "estimation", "downtime"],
  "relatedAssets": ["ka-003"],
  "usageCount": 12,
  "rating": 4.5,
  "status": "APPROVED"
}
```

### Example 3: Troubleshooting Guide
```json
{
  "assetId": "ka-003",
  "assetName": "Troubleshooting: Pipeline Timeout - Memory Issues",
  "assetType": "TROUBLESHOOTING_GUIDE",
  "category": "PIPELINE",
  "content": "## Problem Description\nPipeline times out during build stage with OOM errors.\n\n## Diagnosis Steps\n1. Check build logs for 'OutOfMemoryError'\n2. Review memory allocation in pipeline config\n3. Check for memory leaks in build scripts\n\n## Resolution Steps\n1. Increase memory allocation: `memory: 4GB → 8GB`\n2. Add memory monitoring\n3. Optimize build scripts\n4. Enable incremental builds\n\n## Verification\n- Pipeline completes successfully\n- Memory usage stays below 80%\n- Build time within acceptable range",
  "sourceEntity": "pipeline-build-001",
  "sourceEntityType": "Pipeline",
  "extractedAt": "2026-05-18T09:15:00Z",
  "confidence": 0.88,
  "applicability": ["ALL"],
  "tags": ["pipeline", "timeout", "memory", "troubleshooting"],
  "relatedAssets": ["ka-004", "ka-005"],
  "usageCount": 23,
  "rating": 4.7,
  "status": "APPROVED"
}
```

### Example 4: Runbook
```json
{
  "assetId": "ka-004",
  "assetName": "Runbook: Incident Response - Production Outage",
  "assetType": "RUNBOOK",
  "category": "RELIABILITY",
  "content": "## Incident Detection\n1. Monitor alerts trigger\n2. Verify outage scope\n3. Assess impact\n\n## Immediate Response\n1. Page on-call engineer\n2. Create incident ticket\n3. Start incident bridge\n4. Notify stakeholders\n\n## Investigation\n1. Check recent deployments\n2. Review error logs\n3. Analyze metrics\n4. Identify root cause\n\n## Resolution\n1. Implement fix or rollback\n2. Verify service restoration\n3. Monitor for stability\n\n## Post-Incident\n1. Conduct post-mortem\n2. Document lessons learned\n3. Implement preventive measures\n\n## Contacts\n- On-call: +1-555-0100\n- Incident Commander: +1-555-0101\n- Engineering Manager: +1-555-0102",
  "sourceEntity": "team-sre-001",
  "sourceEntityType": "Team",
  "extractedAt": "2026-05-10T08:00:00Z",
  "confidence": 0.98,
  "applicability": ["PRODUCTION"],
  "tags": ["incident", "outage", "runbook", "sre"],
  "relatedAssets": ["ka-005", "ka-006"],
  "usageCount": 8,
  "rating": 5.0,
  "status": "APPROVED"
}
```

## Knowledge Discovery

### Search and Retrieval

**Search Criteria:**
- Full-text search in content
- Filter by asset type
- Filter by category
- Filter by tags
- Filter by confidence score
- Filter by status
- Sort by rating
- Sort by usage count

**Recommendation Engine:**
```python
def recommend_knowledge(context):
    # Find relevant assets based on:
    - Current entity type
    - Current operation
    - Historical usage patterns
    - Similar incidents
    - User role and team
    
    # Rank by:
    - Relevance score
    - Confidence score
    - User rating
    - Usage frequency
```

### Knowledge Reuse

**Automatic Suggestions:**
- During pipeline creation: Suggest relevant best practices
- During incident response: Suggest troubleshooting guides
- During deployment: Suggest relevant runbooks
- During code review: Suggest architecture decisions

**Usage Tracking:**
- Track when knowledge is accessed
- Track when knowledge is applied
- Track success/failure outcomes
- Collect user feedback

## Metrics and KPIs

### Knowledge Asset Metrics

**Quantity Metrics:**
- Total knowledge assets
- Assets by type
- Assets by category
- Assets by status

**Quality Metrics:**
- Average confidence score
- Average user rating
- Approval rate
- Deprecation rate

**Usage Metrics:**
- Total usage count
- Usage by asset type
- Usage by team
- Reuse rate

**Impact Metrics:**
- Incidents prevented
- Time saved
- Cost savings
- Quality improvements

### Target KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Knowledge Coverage | > 80% | % of entities with knowledge |
| Average Confidence | > 0.85 | Mean confidence score |
| Average Rating | > 4.0 | Mean user rating |
| Usage Rate | > 60% | % of assets used monthly |
| Approval Rate | > 90% | % reaching APPROVED status |
| Time to Approval | < 7 days | Days from DRAFT to APPROVED |

## Audit and Compliance

### Audit Trail Requirements
- Log all knowledge asset creation
- Track all modifications
- Record all status changes
- Monitor all usage
- Maintain version history

### Compliance Checks
- Weekly quality review
- Monthly usage analysis
- Quarterly relevance review
- Annual comprehensive audit

## References

- [Ontology Knowledge Management Guide](../ONTOLOGY_KNOWLEDGE_MANAGEMENT_GUIDE.md)
- [Extended Ontology](../devops-cicd-infrastructure-ontology-extended.jsonld)
- [Pattern Policy](./PATTERN_POLICY.md)
- [Insight Policy](./INSIGHT_POLICY.md)

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-05-20 | DevOps Team | Initial policy creation |

---

**Policy Owner:** Knowledge Management Team  
**Review Cycle:** Quarterly  
**Next Review:** 2026-08-20