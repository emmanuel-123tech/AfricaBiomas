# PHC Intelligence Suite – Solution Overview

## 1. PHC Data Landscape

The prototype unifies three data pillars to uncover the current state of Primary Health Care (PHC):

| Pillar | Description | Sample Fields | Primary Sources |
| --- | --- | --- | --- |
| Facility Readiness | Infrastructure, staffing, essential services | staff_count, functionality_score, electricity_reliability | WHO SARA, Service Availability & Readiness surveys, National Health Facility Master Lists |
| Utilisation & Workload | Patient volumes, referral flows, waiting times | daily_visits, visits_per_staff | DHIS2 routine service statistics, SmartCare, OpenMRS |
| Population Health & Disease Burden | Morbidity trends for priority PHC conditions | malaria_cases, respiratory_cases, maternal_complications | DHIS2 disease surveillance, IDSR, World Bank, GHO |

**Underserved clusters** are flagged when facilities show fewer than 12 health workers per 10,000 people, functionality below 0.6, or unreliable utilities. This highlights rural states in Nigeria (Kaduna, Kano), coastal counties in Kenya (Kilifi), and northern Uganda (Gulu) as priority investment zones.

## 2. Predictive Insights & Diagnostic Support

A lightweight analytics layer applies linear-trend forecasts to monthly disease incidence. Alerts are generated when next-month projections deviate by ±20 cases, supporting proactive triage and supply-chain triggers. Extending the pipeline with gradient boosting or prophet-style models would capture seasonality and rainfall effects that drive malaria and respiratory peaks.

Diagnostic support can plug into standard Integrated Management of Childhood Illness (IMCI) and WHO PEN protocols by matching presenting symptoms with facility capacity. A rules-based knowledge base triages patients to community health workers, PHC clinics, or district hospitals, ensuring early detection of severe malaria, pneumonia, or obstetric emergencies.

## 3. Integrated Decision-Support Prototype

The Python toolkit outputs four data products:

1. **Country dashboard feed** – aggregated readiness and utilisation metrics, consumable by Power BI, Superset, or Kobo dashboards.
2. **Priority facility watchlist** – top underperforming facilities with staffing, functionality, and commodity gaps.
3. **Surge forecast stream** – near-term predictions for malaria, respiratory, and maternal complications to pre-position supplies.
4. **Actionable recommendations** – staffing redeployment counts, stock-out escalation flags, and referral activation prompts.

These outputs can be surfaced through:

- **Low-bandwidth dashboards** with offline caching (e.g., Streamlit + sqlite or Power Apps).
- **Chat-based assistants** integrated into WhatsApp, RapidPro, or USSD channels for facility managers to query in natural language.
- **Automated SMS alerts** to district health officers for surge warnings or urgent stock replenishment tasks.

## 4. Visualisation & Policy Engagement

The dashboard narrative emphasises:

- Underserved facility clusters overlayed on population density and poverty maps.
- Wait-time and workload heatmaps to guide staffing reallocations.
- Disease surge projections with uncertainty bands and recommended actions.
- KPI scorecards for the Africa Health Strategy 2016–2030 (coverage, equity, quality) to inform budget planning.

Insights are exportable as JSON, CSV, or directly into BI connectors, enabling rapid briefing packs for Ministries of Health, donor partners, and civil society monitors.

## 5. Scalability & Impact Roadmap

| Phase | Activities | Impact Metrics |
| --- | --- | --- |
| Pilot (3–6 months) | Deploy in two districts per country; integrate with DHIS2 and facility master list; train district health teams | % facilities submitting weekly data; reduction in stock-out incidents; time-to-escalate critical cases |
| National Rollout (6–18 months) | Automate ETL pipelines; expand to multilingual chatbot; embed triage rules with national guidelines | Patient-to-provider ratio improvements; decrease in avoidable referrals; forecast accuracy |
| Regional Expansion (18–36 months) | Onboard additional countries via AU/CDC networks; standardise data schema; build federated analytics | Cross-border outbreak detection time; alignment with UHC tracer indicators |

**Sustainability enablers** include open-source licensing, modular API architecture, and localisation partnerships with digital health implementers (e.g., PATH, Medic, Ona). Impact can be tracked through improved facility functionality scores, reduced patient waiting times, and higher commodity availability, directly advancing Universal Health Coverage and the Africa Health Strategy 2016–2030.
