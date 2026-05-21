# Repository Policy

**Entity ID:** `devops:Repository`  
**Entity Type:** Entity  
**Version:** 1.0.0  
**Last Updated:** 2026-05-20

## Overview

This policy defines the governance rules, constraints, and best practices for Repository entities within the DevOps ecosystem. Repositories are the foundation of version control, containing source code, configurations, and documentation with strict governance and security controls.

## Description

Represents a source code repository with branching strategy and governance rules. Repositories serve as the single source of truth for application code, infrastructure configurations, and documentation, with comprehensive security and compliance controls.

## Identity

**Identity Key:** `repoId: UUID`  
**Human Reference:** `repoName`

Each repository must have a unique UUID identifier and a human-readable name that clearly identifies the project or application.

## Attributes

### Core Attributes

| Attribute | Type | Description | Required |
|-----------|------|-------------|----------|
| `repoId` | string (UUID) | Unique identifier for the repository | ✅ Yes |
| `repoName` | string | Human-readable repository name | ✅ Yes |
| `repoUrl` | string (URL) | Full URL to the repository | ✅ Yes |
| `defaultBranch` | string | Main branch name (e.g., main, master) | ✅ Yes |
| `branchingStrategy` | enum | Git branching workflow model | ✅ Yes |
| `visibility` | enum | Repository access level | ✅ Yes |
| `hasProtectedBranches` | boolean | Branch protection enabled | ✅ Yes |
| `requirePullRequest` | boolean | PRs required for merges | ✅ Yes |
| `requireCodeReview` | boolean | Code review mandatory | ✅ Yes |
| `minReviewerCount` | integer | Minimum number of reviewers | ✅ Yes |
| `requireSignedCommits` | boolean | Commit signing required | ✅ Yes |
| `hasSecretsScanning` | boolean | Secrets scanning enabled | ✅ Yes |
| `hasDependencyScanning` | boolean | Dependency scanning enabled | ✅ Yes |
| `language` | string | Primary programming language | ✅ Yes |
| `platform` | enum | Git hosting platform | ✅ Yes |

### Branching Strategies

| Strategy | Description | Use Case | Complexity |
|----------|-------------|----------|------------|
| **GITFLOW** | Feature, develop, release, hotfix branches | Large teams, scheduled releases | High |
| **TRUNK_BASED** | Single main branch, short-lived feature branches | Small teams, continuous deployment | Low |
| **FEATURE_BRANCH** | Feature branches merged to main | Medium teams, feature-based development | Medium |
| **RELEASE_BRANCH** | Release branches for version management | Products with multiple versions | Medium |

### Visibility Levels

- **PUBLIC** - Accessible to everyone on the internet
- **PRIVATE** - Accessible only to authorized users
- **INTERNAL** - Accessible to all organization members

### Supported Platforms

- **GITHUB** - GitHub.com or GitHub Enterprise
- **GITLAB** - GitLab.com or self-hosted GitLab
- **BITBUCKET** - Bitbucket Cloud or Bitbucket Server
- **AZURE_REPOS** - Azure DevOps Repositories

## Invariants (Policy Rules)

### 1. Unique Repository Identifier
**Rule:** `repoId must be unique`

**Enforcement:**
- System must validate uniqueness across all repositories
- Duplicate repository IDs must be rejected
- Use UUID v4 for guaranteed uniqueness

**Rationale:** Ensures each repository can be uniquely identified and referenced across the DevOps ecosystem.

### 2. Non-Empty Repository Name
**Rule:** `repoName cannot be empty`

**Enforcement:**
- Repository name must contain at least 3 characters
- Name must match pattern: `^[a-zA-Z0-9-_]+$`
- No spaces or special characters except hyphen and underscore
- Name must be unique within the organization

**Rationale:** Clear, consistent naming is essential for repository discovery and management.

### 3. Protected Default Branch
**Rule:** `defaultBranch must be protected`

**Enforcement:**
- Default branch (main/master) must have branch protection enabled
- Direct commits to default branch must be blocked
- Force pushes to default branch must be disabled
- Branch deletion must be prevented

**Rationale:** Protects the main codebase from accidental or unauthorized changes.

### 4. Pull Request Requirement
**Rule:** `requirePullRequest must be true for main and release branches`

**Enforcement:**
- All changes to main branch must go through pull requests
- All changes to release branches must go through pull requests
- Direct commits are prohibited
- Bypass requires administrator approval

**Rationale:** Ensures all code changes are reviewed and tested before merging.

### 5. Minimum Reviewer Count
**Rule:** `minReviewerCount must be at least 1`

**Enforcement:**
- Production repositories: minimum 2 reviewers
- Non-production repositories: minimum 1 reviewer
- Reviewers must be different from the author
- Reviewers must have appropriate permissions

**Rationale:** Ensures code quality through peer review and knowledge sharing.

### 6. Secrets Scanning Mandatory
**Rule:** `hasSecretsScanning must be true`

**Enforcement:**
- Secrets scanning must be enabled for all repositories
- Scanning must run on every commit
- Detected secrets must block commits
- False positives must be explicitly marked

**Rationale:** Prevents accidental exposure of sensitive credentials and API keys.

### 7. No Secrets in Repository
**Rule:** `secrets must never be committed to repository`

**Enforcement:**
- Pre-commit hooks to detect secrets
- Automated scanning on every push
- Immediate alerts for detected secrets
- Mandatory secret rotation if exposed

**Rationale:** Protects sensitive information and prevents security breaches.

## Relationships

### Related Entities

1. **devops:Pipeline**
   - **Relationship:** Repository triggers Pipelines
   - **Cardinality:** 1:N (One repository can have many pipelines)
   - **Constraint:** Repository must exist before pipeline creation

2. **devops:Application**
   - **Relationship:** Repository contains Application code
   - **Cardinality:** 1:1 or 1:N (One repo per app or monorepo)
   - **Constraint:** Application must reference valid repository

3. **devops:Team**
   - **Relationship:** Team owns Repository
   - **Cardinality:** N:1 (Many repositories owned by one team)
   - **Constraint:** Repository must have at least one owning team

## Best Practices

### 1. Repository Naming Convention
```
<organization>-<product>-<component>-<type>

Examples:
- acme-ecommerce-api-service
- acme-ecommerce-web-frontend
- acme-platform-infrastructure-terraform
- acme-shared-library-utils
```

### 2. Branch Naming Convention

**Feature Branches:**
```
feature/<ticket-id>-<short-description>
Example: feature/JIRA-1234-user-authentication
```

**Bugfix Branches:**
```
bugfix/<ticket-id>-<short-description>
Example: bugfix/JIRA-5678-login-error
```

**Hotfix Branches:**
```
hotfix/<version>-<short-description>
Example: hotfix/v1.2.3-security-patch
```

**Release Branches:**
```
release/<version>
Example: release/v2.0.0
```

### 3. Branch Protection Rules

**Main/Master Branch:**
- ✅ Require pull request reviews (minimum 2)
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Require signed commits
- ✅ Include administrators in restrictions
- ✅ Restrict who can push
- ✅ Restrict force pushes
- ✅ Restrict deletions

**Release Branches:**
- ✅ Require pull request reviews (minimum 1)
- ✅ Require status checks to pass
- ✅ Require signed commits
- ✅ Restrict force pushes
- ✅ Restrict deletions

**Development Branch:**
- ✅ Require pull request reviews (minimum 1)
- ✅ Require status checks to pass
- ⚠️ Allow force pushes (with caution)

### 4. Commit Message Convention

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test additions or changes
- `chore`: Build process or auxiliary tool changes

**Example:**
```
feat(auth): add OAuth2 authentication

Implement OAuth2 authentication flow with support for
Google and GitHub providers.

Closes #123
```

### 5. README Requirements

Every repository must include:
- ✅ Project description and purpose
- ✅ Prerequisites and dependencies
- ✅ Installation instructions
- ✅ Usage examples
- ✅ Configuration guide
- ✅ Contributing guidelines
- ✅ License information
- ✅ Contact information

### 6. Security Configuration

**Required Files:**
- `.gitignore` - Exclude sensitive files
- `SECURITY.md` - Security policy and reporting
- `CODEOWNERS` - Code ownership and review assignments
- `.github/dependabot.yml` - Dependency updates (GitHub)

**Scanning Configuration:**
- Enable secrets scanning
- Enable dependency scanning
- Enable code scanning (SAST)
- Configure security alerts
- Set up automated security updates

## Compliance Requirements

### Production Repositories

**Mandatory Settings:**
- ✅ `visibility` = PRIVATE
- ✅ `hasProtectedBranches` = true
- ✅ `requirePullRequest` = true
- ✅ `requireCodeReview` = true
- ✅ `minReviewerCount` >= 2
- ✅ `requireSignedCommits` = true
- ✅ `hasSecretsScanning` = true
- ✅ `hasDependencyScanning` = true

**Mandatory Files:**
- ✅ README.md
- ✅ LICENSE
- ✅ SECURITY.md
- ✅ CODEOWNERS
- ✅ .gitignore

**Mandatory Workflows:**
- ✅ CI/CD pipeline
- ✅ Security scanning
- ✅ Code quality checks
- ✅ Automated testing

### Non-Production Repositories

**Mandatory Settings:**
- ✅ `hasProtectedBranches` = true
- ✅ `requirePullRequest` = true
- ✅ `requireCodeReview` = true
- ✅ `minReviewerCount` >= 1
- ✅ `hasSecretsScanning` = true

**Recommended Settings:**
- ⚠️ `requireSignedCommits` = true
- ⚠️ `hasDependencyScanning` = true

## Validation Rules

### Pre-Creation Validation
```yaml
validations:
  - check: repoId uniqueness
    action: reject if duplicate
  
  - check: repoName format
    action: reject if invalid pattern
  
  - check: repoUrl validity
    action: reject if invalid URL
  
  - check: platform support
    action: reject if platform not supported
  
  - check: visibility level
    action: reject if invalid visibility
  
  - check: branching strategy
    action: reject if invalid strategy
```

### Post-Creation Validation
```yaml
validations:
  - check: branch protection enabled
    action: alert if not enabled within 24 hours
  
  - check: secrets scanning enabled
    action: block commits if not enabled
  
  - check: required files present
    action: alert if missing
  
  - check: CODEOWNERS configured
    action: alert if not configured
  
  - check: CI/CD pipeline configured
    action: alert if not configured within 48 hours
```

### Runtime Validation
```yaml
validations:
  - check: secrets in commits
    action: block commit and alert security team
  
  - check: large files
    action: block if file > 100MB
  
  - check: binary files
    action: alert if binary file committed
  
  - check: commit signature
    action: block if signature required but missing
```

## Examples

### Example 1: Production Microservice Repository
```json
{
  "repoId": "ee0e8400-e29b-41d4-a716-446655440000",
  "repoName": "acme-ecommerce-api-service",
  "repoUrl": "https://github.com/acme/ecommerce-api-service",
  "defaultBranch": "main",
  "branchingStrategy": "TRUNK_BASED",
  "visibility": "PRIVATE",
  "hasProtectedBranches": true,
  "requirePullRequest": true,
  "requireCodeReview": true,
  "minReviewerCount": 2,
  "requireSignedCommits": true,
  "hasSecretsScanning": true,
  "hasDependencyScanning": true,
  "language": "Python",
  "platform": "GITHUB"
}
```

### Example 2: Infrastructure Repository
```json
{
  "repoId": "ff0e8400-e29b-41d4-a716-446655440001",
  "repoName": "acme-platform-infrastructure-terraform",
  "repoUrl": "https://gitlab.com/acme/platform-infrastructure",
  "defaultBranch": "main",
  "branchingStrategy": "FEATURE_BRANCH",
  "visibility": "PRIVATE",
  "hasProtectedBranches": true,
  "requirePullRequest": true,
  "requireCodeReview": true,
  "minReviewerCount": 2,
  "requireSignedCommits": true,
  "hasSecretsScanning": true,
  "hasDependencyScanning": true,
  "language": "HCL",
  "platform": "GITLAB"
}
```

### Example 3: Open Source Library
```json
{
  "repoId": "110e8400-e29b-41d4-a716-446655440002",
  "repoName": "acme-shared-library-utils",
  "repoUrl": "https://github.com/acme/shared-utils",
  "defaultBranch": "main",
  "branchingStrategy": "GITFLOW",
  "visibility": "PUBLIC",
  "hasProtectedBranches": true,
  "requirePullRequest": true,
  "requireCodeReview": true,
  "minReviewerCount": 1,
  "requireSignedCommits": false,
  "hasSecretsScanning": true,
  "hasDependencyScanning": true,
  "language": "JavaScript",
  "platform": "GITHUB"
}
```

### Example 4: Documentation Repository
```json
{
  "repoId": "220e8400-e29b-41d4-a716-446655440003",
  "repoName": "acme-platform-documentation",
  "repoUrl": "https://github.com/acme/platform-docs",
  "defaultBranch": "main",
  "branchingStrategy": "TRUNK_BASED",
  "visibility": "INTERNAL",
  "hasProtectedBranches": true,
  "requirePullRequest": true,
  "requireCodeReview": true,
  "minReviewerCount": 1,
  "requireSignedCommits": false,
  "hasSecretsScanning": true,
  "hasDependencyScanning": false,
  "language": "Markdown",
  "platform": "GITHUB"
}
```

## Access Control

### Repository Roles

| Role | Permissions | Use Case |
|------|-------------|----------|
| **Admin** | Full control, settings, delete | Repository owners |
| **Maintainer** | Manage repo, merge PRs | Team leads |
| **Write** | Push code, create branches | Developers |
| **Triage** | Manage issues, PRs | Support team |
| **Read** | View and clone | External collaborators |

### Team-Based Access
```yaml
teams:
  - name: platform-team
    role: Admin
    repositories: ["*-platform-*"]
  
  - name: backend-team
    role: Maintainer
    repositories: ["*-api-*", "*-service-*"]
  
  - name: frontend-team
    role: Maintainer
    repositories: ["*-web-*", "*-mobile-*"]
  
  - name: devops-team
    role: Admin
    repositories: ["*-infrastructure-*", "*-pipeline-*"]
```

## Audit and Compliance

### Audit Trail Requirements
- Log all repository access (read, write, admin)
- Track all branch protection changes
- Record all permission modifications
- Monitor all secrets scanning alerts
- Maintain audit logs for 1 year minimum

### Compliance Checks
- Daily secrets scanning
- Weekly dependency vulnerability scanning
- Monthly access review
- Quarterly security audit
- Annual compliance certification

### Compliance Standards
- **SOC 2** - Access controls, audit logging
- **PCI DSS** - Secrets management, access restrictions
- **HIPAA** - Data protection, audit trails
- **ISO 27001** - Information security management
- **GDPR** - Data privacy, right to deletion

## Troubleshooting

### Common Issues

**Issue 1: Secrets Detected in Commit**
- **Symptom:** Commit blocked due to secrets scanning
- **Solution:** Remove secrets, use environment variables or secret management
- **Prevention:** Configure pre-commit hooks, use .gitignore

**Issue 2: Branch Protection Bypass**
- **Symptom:** Direct commit to protected branch
- **Solution:** Revert commit, enforce branch protection
- **Prevention:** Include administrators in restrictions

**Issue 3: Large File Committed**
- **Symptom:** Repository size growing rapidly
- **Solution:** Use Git LFS for large files, remove from history
- **Prevention:** Configure file size limits, use .gitignore

**Issue 4: Unsigned Commits**
- **Symptom:** Commits without GPG signature
- **Solution:** Configure GPG signing, re-sign commits
- **Prevention:** Require signed commits in branch protection

## Metrics and KPIs

### Repository Health Metrics
- **Commit Frequency:** Commits per day/week
- **Pull Request Velocity:** Time from PR creation to merge
- **Code Review Coverage:** Percentage of PRs reviewed
- **Security Alert Response Time:** Time to resolve security alerts
- **Branch Protection Compliance:** Percentage of protected branches

### Target KPIs
- Commit Frequency: > 5 commits/day (active repos)
- PR Velocity: < 24 hours (non-production), < 48 hours (production)
- Code Review Coverage: 100%
- Security Alert Response: < 24 hours (critical), < 7 days (non-critical)
- Branch Protection Compliance: 100%

## Migration Guide

### Migrating to New Repository

**Pre-Migration Checklist:**
- ✅ Export all code and history
- ✅ Document all branches and tags
- ✅ Export all issues and PRs
- ✅ Backup all CI/CD configurations
- ✅ Document all integrations

**Migration Steps:**
1. Create new repository with proper configuration
2. Import code with full history
3. Recreate branch structure
4. Configure branch protection
5. Set up CI/CD pipelines
6. Enable security scanning
7. Configure access controls
8. Update documentation
9. Notify team members
10. Archive old repository

**Post-Migration Validation:**
- ✅ Verify all branches migrated
- ✅ Verify all tags migrated
- ✅ Test CI/CD pipelines
- ✅ Verify security scanning
- ✅ Validate access controls
- ✅ Update all references

## References

- [Pipeline Policy](./PIPELINE_POLICY.md)
- [Git Best Practices](https://example.org/git-best-practices)
- [Branch Protection Guide](https://example.org/branch-protection)
- [Secrets Management](https://example.org/secrets-management)
- [DevOps Ontology Specification](../devops-cicd-infrastructure-ontology.jsonld)

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-05-20 | DevOps Team | Initial policy creation |

---

**Policy Owner:** DevOps Platform Team  
**Review Cycle:** Quarterly  
**Next Review:** 2026-08-20