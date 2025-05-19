# Pentra
**Platform for End-to-End Threat Route Analysis**

Pentra is a security analytics platform that reconstructs attacker movement across systems using log-based sessionization, policy mismatch detection, and threat technique mapping.

---

## 🔍 What does Pentra do?

- **Reconstructs attack sessions** from raw security logs
- **Detects policy misconfigurations** through snapshot analysis
- **Maps events** to MITRE ATT&CK or Kill Chain models
- **Outputs explainable reports** for analyst review

---

## 🧠 Architecture Overview

- **Parser Layer**: Normalizes logs into 1st and 2nd pass schemas
- **Evaluators**:
  - `evaluate_event_type`: behavioral scoring
  - `evaluate_policy`: snapshot policy evaluator
  - `evaluate_role`: entrypoint/pivot/expansion classification
- **TTP Mapper**: Converts evaluated findings into mapped TTPs
- **Reporter**: Outputs JSON/HTML reports (PDF later)

---

## 📄 Sample Files

You can explore:
- [`docs/architecture.md`](docs/architecture.md)
- [`schemas/event_type_definitions_sample.yaml`](schemas/event_type_definitions_sample.yaml)

---

## 🚀 Roadmap

- [x] Architectural design completed
- [x] Core YAML schema defined (sample only)
- [ ] Full MVP parser and evaluators
- [ ] TTP simulation engine (planned)

---

## 📘 License

This repository shares conceptual files only.  
Core logic remains private in internal development repositories.

MIT License — see `LICENSE`
