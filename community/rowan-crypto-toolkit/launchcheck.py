"""LaunchCheck: offline lint for user-supplied Solana launch configuration claims."""
import argparse
import json

def inspect(config):
    if not isinstance(config, dict):
        raise ValueError("expected JSON object")
    findings = []
    def add(code, severity, description):
        findings.append({"code": code, "severity": severity, "message": description})
    supply = config.get("supply")
    if isinstance(supply, bool) or not isinstance(supply, (int, float)) or not 0 < supply <= 1e18:
        add("INVALID_SUPPLY", "error", "Supply must be positive, <= 1e18")
    decimals = config.get("decimals")
    if type(decimals) is not int or not 0 <= decimals <= 9:
        add("INVALID_DECIMALS", "error", "Starter policy supports decimals 0..9")
    for key in ("mint_authority", "freeze_authority"):
        val = config.get(key)
        if val not in ("revoked", "retained"):
            add("AUTHORITY_UNCLEAR", "error", key + " must be revoked or retained")
        elif val == "retained":
            add("AUTHORITY_RETAINED", "warning", key + " is retained; secure and disclose")
    allocations = config.get("allocations")
    if not isinstance(allocations, list) or not allocations:
        add("ALLOCATIONS_MISSING", "error", "Provide named percentage allocations")
    else:
        total = 0
        for item in allocations:
            if (not isinstance(item, dict) or not isinstance(item.get("name"), str)
                or not item["name"].strip() or isinstance(item.get("percent"), bool)
                or not isinstance(item.get("percent"), (int,float))
                or not 0 <= item["percent"] <= 100):
                add("ALLOCATION_INVALID", "error", "Each allocation needs a name and 0..100 percent")
            else:
                total += item["percent"]
        if abs(total - 100) > 0.000001:
            add("ALLOCATION_SUM", "error", "Allocations do not add to 100%")
    if not config.get("public_disclosures_url"):
        add("DISCLOSURES_MISSING", "warning", "Provide public disclosures")
    if config.get("network") == "mainnet-beta" and not config.get("devnet_tested"):
        add("DEVNET_TEST_MISSING", "warning", "Test on devnet first")
    return {"ok": not any(f["severity"] == "error" for f in findings), "issues": findings,
            "scope": "User-supplied config lint only; no blockchain verification or security audit"}

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("json_config")
    args = p.parse_args()
    with open(args.json_config, encoding="utf8") as f:
        print(json.dumps(inspect(json.load(f)), indent=2))
