# Hermes Hosting Digest Plugin

Standalone Hermes plugin that registers `/hosting-digest` for on-demand hosting
cost digest reports.

The command runs the same Python script used by Tyler's scheduled Vultr cost
cron, defaulting to:

```text
$HERMES_HOME/scripts/vultr_cost_digest.py
```

If `HERMES_HOME` is unset, it falls back to `~/.hermes/scripts/vultr_cost_digest.py`.
Set `HOSTING_DIGEST_SCRIPT` to point at a different script.

## Install

```bash
hermes plugins install mercury-dev-bot/hermes-hosting-digest-plugin --enable
hermes gateway restart
```

## Use

From any Hermes CLI or gateway session after restart:

```text
/hosting-digest
```

Help:

```text
/hosting-digest help
```

## Local validation

```bash
python3 -m pytest -q
```
