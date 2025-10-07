# AI for Smarter Primary Health Care in Africa

This repository contains a lightweight, end-to-end prototype that demonstrates how artificial intelligence and data analytics can strengthen Primary Health Care (PHC) systems across African countries. The project combines open data framing, predictive analytics, and decision-support tooling ideas into an integrated package suitable for hackathon delivery.

## Solution Overview

The solution focuses on four complementary capabilities:

1. **Comprehensive PHC Data Landscape** – Harmonises facility readiness, service utilisation, and disease incidence indicators to reveal underserved populations and infrastructure gaps.
2. **Predictive Insights & Diagnostic Support** – Applies statistical forecasting to anticipate patient surges and stock-out risks while surfacing early warning signals for common PHC conditions.
3. **Decision-Support Prototype** – Generates actionable recommendations for staffing, drug inventory, and referral routing that can be embedded into low-bandwidth dashboards or messaging platforms.
4. **Scalability & Impact Plan** – Outlines how the toolset can be localised and scaled across diverse African contexts with multilingual support and offline-first delivery modes.

## Repository Structure

```
├── data/
│   ├── phc_facility_status.csv        # Sample facility readiness and utilisation indicators
│   └── disease_incidence.csv          # Monthly primary-care case trends by region
├── src/
│   └── phc_analysis.py                # Core analytics pipeline and recommendation engine
├── reports/
│   ├── generated_insights.json        # Auto-generated insight bundle (created at runtime)
│   └── solution_overview.md           # Narrative on vision, adoption strategy, and impact pathways
└── README.md
```

## Getting Started

1. (Optional) create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Run the analytics pipeline to generate summary insights and recommendations:
   ```bash
   python src/phc_analysis.py --export reports/generated_insights.json
   ```

The script prints country- and region-level insights to the console and optionally exports them as machine-readable JSON for dashboards or messaging bots. The current implementation relies only on the Python standard library to stay lightweight for low-resource deployments.

## Data Inputs

The repository ships with illustrative sample datasets constructed from publicly available statistics such as the World Bank World Development Indicators, WHO Service Availability and Readiness Assessments, and national DHIS2 portals. Replace these placeholders with live feeds or API connectors during implementation.

- `phc_facility_status.csv` includes staffing ratios, patient throughput, stock-out rates, and functionality scores for facilities across Nigeria, Kenya, Uganda, and South Africa.
- `disease_incidence.csv` tracks monthly cases for malaria, respiratory infections, and maternal health complications to support surge prediction.

## Extending the Prototype

- **Data enrichment**: Connect to open APIs (DHIS2, OpenHIE, World Bank, WHO) or local HMIS exports to refresh datasets automatically.
- **Advanced modelling**: Swap the statistical forecasts with gradient boosting, Bayesian structural time-series, or neural sequence models to capture seasonality and intervention effects.
- **User interfaces**: Integrate with Streamlit, Power BI, RapidPro chatbots, or USSD/SMS gateways for low-bandwidth decision-support experiences.
- **Localisation**: Package recommendations in local languages, incorporate offline caches, and align triage rules with national clinical guidelines.

## License

This project is released under the MIT License. Feel free to adapt and extend it for hackathon or production deployments.
