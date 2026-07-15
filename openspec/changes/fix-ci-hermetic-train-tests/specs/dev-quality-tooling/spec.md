## ADDED Requirements

### Requirement: Code-quality PR workflow must not require privileged changed-files integrations
The PR code-quality workflow MUST determine changed files using repository git metadata available after checkout, and MUST NOT depend on third-party integrations that can fail with repository permission errors.

#### Scenario: Run code-quality on a pull request with standard GitHub Actions token
- **WHEN** the PR code-quality workflow runs with the default repository token
- **THEN** it resolves modified files from local git history after checkout
- **AND** the workflow does not fail with `Resource not accessible by integration` while collecting changed files
