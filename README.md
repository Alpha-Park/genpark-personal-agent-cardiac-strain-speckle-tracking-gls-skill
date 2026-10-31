# genpark-personal-agent-cardiac-strain-speckle-tracking-gls-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

Echocardiography 2D speckle-tracking Global Longitudinal Strain (GLS) myocardial deformation index and subclinical LV dysfunction sentinel.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `assess_cardiac_gls_strain`
- **Category**: `personal_agent`

### Method Documentation
Assess myocardial deformation using 2D speckle-tracking echocardiography Global Longitudinal Strain (GLS).
GLS measures longitudinal myocardial shortening from base to apex. Normal physiological values are typically more negative than -18.0% (e.g. -20% is normal, -14% is impaired).
Calculates 17-segment polar map average, apex-to-base gradient, and subclinical cardiotoxicity / HFpEF risk categorization.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "assess_cardiac_gls_strain",
    "arguments": {
    "segmental_strains_percent": [
        -21.0,
        -20.5,
        -19.8,
        -20.2,
        -21.4,
        -20.0,
        -19.5,
        -20.1,
        -19.0,
        -19.8,
        -20.5,
        -20.2,
        -22.0,
        -23.1,
        -22.5,
        -21.8,
        -22.4
    ],
    "lvef_percent": 62.0,
    "baseline_gls_percent": -21.5
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
