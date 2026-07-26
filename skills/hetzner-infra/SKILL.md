---
name: hetzner-infra
description: Provision and manage Hetzner Cloud VPS servers with OpenTofu. Use when the user asks to create/provision/manage a VPS or server on Hetzner, or to work with hetzner-infra terraform.
---

# Hetzner Infra

Manage Hetzner **Cloud** servers (hcloud API) declaratively via OpenTofu. Dedicated/Robot API is out of scope.

## Prereqs (check first, fail fast)
- `~/.local/bin/tofu version` works (installed v1.12.4; otherwise install from opentofu releases)
- `HCLOUD_TOKEN` is set in the environment: `test -n "$HCLOUD_TOKEN"`. If missing, ask Jimmy to create one: Hetzner Cloud console → project → Security → API Tokens (read+write). He exports it himself.
- SSH keypair exists (`ls ~/.ssh/id_ed25519.pub`); generate with `ssh-keygen -t ed25519` if not.

## Hard rules (never break)
1. The API token is NEVER written to any file in a repo. Env var only — the hcloud provider reads `HCLOUD_TOKEN` automatically.
2. `.gitignore` must cover `*.tfstate*`, `.terraform/`, `*.auto.tfvars`, `tfplan`, `crash.log` BEFORE any `git init`/commit.
3. Never run `tofu apply` without showing Jimmy the plan first. Never run `tofu destroy` (or anything replacing a resource) without explicit confirmation for that specific action.
4. No Hetzner Robot (dedicated) API — Cloud only.

## Pricing — NEVER quote from memory
Hetzner prices change (2025-2026 saw big increases). Before telling Jimmy any price, fetch it live:

```bash
curl -fsS -H "Authorization: Bearer $(cat ~/.config/hetzner-infra/token)" \
  https://api.hetzner.cloud/v1/pricing | python3 -c "
import json,sys
for st in json.load(sys.stdin)['pricing']['server_types']:
    for p in st['prices']:
        if p['location']=='fsn1': print(st['name'], p['price_hourly']['gross'], p['price_monthly']['gross'])
"
```

Reference snapshot (gross €, fsn1, fetched 2026-07-19 — verify before quoting):
- cx22 6.59/mo — NOTE: listed in pricing but NOT orderable ("server type not found" on create); deprecated
- cpx11 7.19 · cx23 7.79 · cax11 8.39 · cx33 10.79 · cx32 11.99 · cpx21 13.19 · cax21 14.99
- cpx12 16.19 · cx43 22.19 · cpx31 24.59 · cpx22 27.59 · cx42 29.39 · cax31 29.99
- ccx* = dedicated vCPU, 60.59 and up
- cx* = shared x86 · cax* = shared ARM · cpx* = shared AMD (deprecated naming, still orderable)

## Working example
A known-good config lives at `/home/vincerhodes/dev/hetzner-infra/terraform/` (main.tf, variables.tf, outputs.tf). Copy it as the starting point for a new project rather than writing from scratch.

## Workflow — new project
1. Create `<project>/terraform/` and copy the example files in.
2. Adjust `variables.tf` defaults if asked (`cx23` x86 is the reliable cheap default — `cax11` ARM has been sold out EU-wide; locations: `fsn1`, `nbg1`, `hel1`, `ash`, `hil`). If apply fails with `resource_unavailable`, that type is out of stock in that location — switch type/location and retry.
3. Recommend tightening `allowed_ssh_cidrs` to Jimmy's current IP (`curl -s ifconfig.me` + `/32`).
4. `tofu init && tofu validate`.
5. `tofu plan -out=tfplan`, show the plan summary, get confirmation, then `tofu apply tfplan`.
6. Output the IPv4; verify SSH with `ssh -o BatchMode=yes root@<ip> true`.

## Workflow — existing project
1. Look for existing `terraform/*.tf` and respect its structure; edit minimally.
2. Same plan → confirm → apply cycle. After apply, `tofu plan` should show no drift — mention it if it doesn't.

## Common operations
- Add a server: copy the `hcloud_server` resource with a new name; attach existing ssh_key/firewall by reference.
- Resize: change `server_type`, then plan/apply (requires shutdown; hcloud handles it — warn about downtime).
- List what's live: `tofu show` or `tofu output`.
- Costs: flag it if a plan adds resources — Hetzner bills hourly until destroyed.
