## ADDED Requirements

### Requirement: Task completion update requires commit evidence

Coding agent MUST update OpenSpec tasks checkboxes to complete only after commit gates are satisfied and a commit hash for the same logical change is produced.

#### Scenario: Mark task complete after commit

- **WHEN** coding agent completes a task group for a single OpenSpec change
- **AND** required verification succeeds
- **AND** a commit for that logical change is created
- **THEN** coding agent updates corresponding tasks from open to complete
- **AND** completion report includes the commit hash and verification commands

#### Scenario: Prevent premature task completion

- **WHEN** required verification is missing or failed, or commit creation is blocked
- **THEN** coding agent MUST NOT mark related tasks as complete
- **AND** coding agent reports blocked status with failure conditions and required next action

### Requirement: Mixed dirty tree handling before completion declaration

Coding agent MUST isolate commit scope before declaring completion, and MUST stop for user decision when safe isolation is not possible.

#### Scenario: Commit with isolated scope in dirty tree

- **WHEN** unrelated working tree changes exist
- **AND** target change files can be isolated with explicit staging
- **THEN** coding agent creates commit only from isolated files
- **AND** report includes isolated file list and rationale

#### Scenario: Stop when isolation is unsafe

- **WHEN** unrelated changes cannot be safely separated without risky operations
- **THEN** coding agent stops before task completion update
- **AND** coding agent asks user how to proceed
