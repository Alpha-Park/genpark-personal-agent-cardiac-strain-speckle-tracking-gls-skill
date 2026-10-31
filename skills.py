# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-personal-agent-cardiac-strain-speckle-tracking-gls-skill
Category: personal_agent
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def assess_cardiac_gls_strain(segmental_strains_percent, lvef_percent=60.0, baseline_gls_percent=None):
    if not segmental_strains_percent:
        raise ValueError("segmental_strains_percent list cannot be empty")
    
    n_segments = len(segmental_strains_percent)
    avg_gls = sum(segmental_strains_percent) / n_segments
    
    # Apex to base strain comparison if 17 or 18 segments provided
    # segments usually ordered basal (1-6), mid (7-12), apical (13-17)
    apical_sparing_ratio = 1.0
    if n_segments >= 16:
        basal = sum(segmental_strains_percent[:6]) / 6.0
        mid = sum(segmental_strains_percent[6:12]) / 6.0
        apical = sum(segmental_strains_percent[12:]) / len(segmental_strains_percent[12:])
        denom = (abs(basal) + abs(mid)) if (abs(basal) + abs(mid)) > 0 else 1.0
        apical_sparing_ratio = (2.0 * abs(apical)) / denom
    
    # Categorization based on ASE/EACVI guidelines
    # More negative is better
    if avg_gls <= -18.0:
        status = "NORMAL_MYOCARDIAL_DEFORMATION"
        clinical_interpretation = "Normal left ventricular longitudinal systolic performance."
    elif avg_gls <= -16.0:
        status = "BORDERLINE_GLS_REDUCTION"
        clinical_interpretation = "Mild subclinical myocardial strain reduction. Monitor closely if under cardiotoxic chemotherapy or hypertension."
    elif avg_gls <= -12.0:
        status = "ABNORMAL_SUBCLINICAL_DYSFUNCTION"
        clinical_interpretation = "Significant subclinical left ventricular systolic dysfunction despite preserved LVEF."
    else:
        status = "SEVERE_MYOCARDIAL_IMPAIRMENT"
        clinical_interpretation = "Severe longitudinal mechanical dysfunction indicative of progressive myocardial fibrosis or cardiomyopathy."
        
    cardiotoxicity_relative_drop_pct = 0.0
    cancer_therapy_cardiotoxicity_alert = False
    if baseline_gls_percent is not None and abs(baseline_gls_percent) > 0:
        # Relative reduction = (abs(baseline) - abs(current)) / abs(baseline) * 100
        cardiotoxicity_relative_drop_pct = ((abs(baseline_gls_percent) - abs(avg_gls)) / abs(baseline_gls_percent)) * 100.0
        if cardiotoxicity_relative_drop_pct >= 15.0:
            cancer_therapy_cardiotoxicity_alert = True
            
    cardiac_amyloidosis_suspected = apical_sparing_ratio > 1.3 and avg_gls > -17.0
    
    return {
        "mean_gls_percent": round(avg_gls, 2),
        "segments_evaluated": n_segments,
        "lvef_percent": lvef_percent,
        "apical_sparing_ratio": round(apical_sparing_ratio, 2),
        "cardiac_amyloidosis_apical_sparing_pattern": cardiac_amyloidosis_suspected,
        "status": status,
        "relative_drop_from_baseline_percent": round(cardiotoxicity_relative_drop_pct, 2) if baseline_gls_percent else None,
        "cardiotoxicity_alert": cancer_therapy_cardiotoxicity_alert,
        "clinical_interpretation": clinical_interpretation
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "assess_cardiac_gls_strain",
                        "description": """Assess myocardial deformation using 2D speckle-tracking echocardiography Global Longitudinal Strain (GLS).
GLS measures longitudinal myocardial shortening from base to apex. Normal physiological values are typically more negative than -18.0% (e.g. -20% is normal, -14% is impaired).
Calculates 17-segment polar map average, apex-to-base gradient, and subclinical cardiotoxicity / HFpEF risk categorization.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = assess_cardiac_gls_strain(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'segmental_strains_percent': [-21.0, -20.5, -19.8, -20.2, -21.4, -20.0, -19.5, -20.1, -19.0, -19.8, -20.5, -20.2, -22.0, -23.1, -22.5, -21.8, -22.4], 'lvef_percent': 62.0, 'baseline_gls_percent': -21.5}
        out = assess_cardiac_gls_strain(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
