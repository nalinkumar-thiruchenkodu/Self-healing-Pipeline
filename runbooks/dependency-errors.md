# Runbook: dependency install fails

Symptom: `ERROR: No matching distribution found for <package>==<version>`.

Cause: the pinned version does not exist (typo) or was removed.

Fix: pip prints "from versions: ..." in the log. Choose the closest valid
version, keep it pinned (`package==x.y.z`), and re-run the build.
Do not unpin or switch to `>=`.
