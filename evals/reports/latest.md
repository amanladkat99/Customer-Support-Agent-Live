# Nightly Eval Report

- Generated: 2026-11-10T13:04:51.353510+00:00
- Status: failed
- Cases: 14 total / 14 evaluated / 0 skipped

## Aggregate Metrics

- Faithfulness: 0.4753
- Answer relevancy: 0.7520
- Context precision: 1.0000
- DeepEval expected-tools pass rate: 1.0000
- DeepEval no-PII pass rate: 1.0000
- DeepEval no-promises pass rate: 1.0000
- DeepEval length-bound pass rate: 1.0000

## Thresholds

- Faithfulness >= 0.64
- Answer relevancy >= 0.7
- Context precision >= 0.6
- Deterministic DeepEval assertions: 100% pass

## Case Highlights

- `atm_pin_safety_guidance`: ragas={'faithfulness': 0.4444, 'answer_relevancy': 0.8276, 'context_precision': 1.0} deepeval={expected_tools=True, no_pii_leak=True, no_forbidden_promises=True, length_bound=True}
- `plan_atm_issue_priority`: ragas={'faithfulness': 0.4545, 'answer_relevancy': 0.6336, 'context_precision': 1.0} deepeval={expected_tools=True, no_pii_leak=True, no_forbidden_promises=True, length_bound=True}
- `plan_min_balance_priority`: ragas={'faithfulness': 0.1667, 'answer_relevancy': 0.6502, 'context_precision': 1.0} deepeval={expected_tools=True, no_pii_leak=True, no_forbidden_promises=True, length_bound=True}
- `low_risk_kyc_frequency`: ragas={'faithfulness': 0.25, 'answer_relevancy': 0.921, 'context_precision': 1.0} deepeval={expected_tools=True, no_pii_leak=True, no_forbidden_promises=True, length_bound=True}
- `email_update_timing`: ragas={'faithfulness': 0.6667, 'answer_relevancy': 0.698, 'context_precision': 1.0} deepeval={expected_tools=True, no_pii_leak=True, no_forbidden_promises=True, length_bound=True}
- `plan_kyc_update_priority`: ragas={'faithfulness': 0.5, 'answer_relevancy': 0.4161, 'context_precision': 1.0} deepeval={expected_tools=True, no_pii_leak=True, no_forbidden_promises=True, length_bound=True}
- `atm_cash_debited_reversal`: ragas={'faithfulness': 0.5556, 'answer_relevancy': 0.8219, 'context_precision': 1.0} deepeval={expected_tools=True, no_pii_leak=True, no_forbidden_promises=True, length_bound=True}
- `atm_standard_limit`: ragas={'faithfulness': 0.2, 'answer_relevancy': 0.8759, 'context_precision': 1.0} deepeval={expected_tools=True, no_pii_leak=True, no_forbidden_promises=True, length_bound=True}
- `dmat_not_available`: ragas={'faithfulness': 0.25, 'answer_relevancy': 0.7664, 'context_precision': 1.0} deepeval={expected_tools=True, no_pii_leak=True, no_forbidden_promises=True, length_bound=True}
- `closure_within_14_days`: ragas={'faithfulness': 0.3333, 'answer_relevancy': 0.7133, 'context_precision': 1.0} deepeval={expected_tools=True, no_pii_leak=True, no_forbidden_promises=True, length_bound=True}

## Notes

- Cases below per-case thresholds: atm_pin_safety_guidance, plan_atm_issue_priority, plan_min_balance_priority, low_risk_kyc_frequency, email_update_timing, plan_kyc_update_priority, atm_cash_debited_reversal, atm_standard_limit, dmat_not_available, closure_within_14_days, atm_wrong_pin_manual_reset, non_maintenance_fee
