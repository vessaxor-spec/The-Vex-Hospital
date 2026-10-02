# Repository Department

## Examines

- repository integrity and tracked object structure;
- branch and worktree assumptions;
- dependency and nested-repository consistency;
- generated versus source artifacts;
- executable/buildable state;
- configuration and file-layout drift;
- repository hygiene that directly affects operation.

## Preferred evidence

Repository metadata, tracked-file inspection, build/compile checks, dependency metadata, and reproducible repository commands.

## Questions

- Can a clean checkout reproduce the expected state?
- Are tracked metadata and repository structure consistent?
- Is a required artifact generated locally but absent from source control?
- Are runtime artifacts being mistaken for source?
- Does a repository defect block diagnosis or execution?

## Avoid

An untidy working tree is not automatically a clinical defect. Show operational impact.
