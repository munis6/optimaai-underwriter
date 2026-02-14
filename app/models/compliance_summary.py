from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class RuleSummary(BaseModel):
    ruleId: str
    description: str
    passed: bool
    category: str | None = None
    severity: str | None = None
    impact: str | None = None
    narrative: str | None = None
    fieldsChecked: list | None = None
    valuesObserved: dict | None = None
    reason: str | None = None
    checkType: str | None = None


class ComplianceSummary(BaseModel):
    state: str
    stateFullName: str
    overallComplianceStatus: str
    complianceSummary: str
    rulesChecked: List[RuleSummary]
    version: str = "1.0"

    # Optional but useful for PDF/UI
    underwritingSummary: Optional[Dict[str, Any]] = None
    aiInsightsSummary: Optional[Dict[str, Any]] = None
