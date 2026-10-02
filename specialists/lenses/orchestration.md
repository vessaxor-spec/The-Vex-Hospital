# Orchestration Department

## Examines

- routing and delegation;
- task ownership;
- context handoff;
- sub-agent boundaries;
- duplicate work;
- loops, dead ends, and termination;
- aggregation and conflict resolution;
- fallback behavior.

## Preferred evidence

Route traces, delegation contracts, worker results, handoff payloads, termination conditions, and cross-agent state.

## Questions

- Which component owned the decision?
- Was the delegated task bounded and complete?
- Did the worker receive enough context without unnecessary contamination?
- Was worker output independently checked where required?
- Can two agents believe the other owns the same responsibility?
- What ends the loop?

## Avoid

Adding another agent is not a treatment for unclear responsibility.
