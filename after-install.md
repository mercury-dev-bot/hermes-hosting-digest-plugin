# Installed

`hosting-digest` is installed.

Enable it if you did not pass `--enable` during install:

```bash
hermes plugins enable hosting-digest
hermes gateway restart
```

Then run it from chat:

```text
/hosting-digest
```

The plugin expects the digest script at `$HERMES_HOME/scripts/vultr_cost_digest.py`
unless `HOSTING_DIGEST_SCRIPT` is set.
