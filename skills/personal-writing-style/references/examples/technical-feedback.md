# Example: technical feedback

Fictional example. The code review observation below is invented to illustrate
how to separate an observation, a risk and verification still needed.

---

## Make dependency versions explicit when replaying a saved job

The job record stores the selected test version, but the dependency resolver uses
the latest available helper. A saved job can therefore resolve a different helper
after the shared library changes.

This is a reproducibility risk, not evidence that an existing job has failed.

I suggest recording the complete resolved dependency set when the job starts and
using that set for replay. If an exact dependency is unavailable, the replay should
stop with a clear message rather than silently substitute a newer version.

To verify the change, save a job with one helper version, publish a newer version
in a test environment, and replay the saved job. Confirm that it still uses the
original helper and that the run record shows which version was executed.
