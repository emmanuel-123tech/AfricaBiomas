"""Analytics toolkit for strengthening Primary Health Care (PHC) delivery in Africa.

This module ingests facility readiness indicators and disease incidence trends to
produce:

* Coverage and service quality gaps
* Near-term forecasts of patient surges and stock-out risk
* Actionable recommendations for staffing, commodities, and referral routing

The script can be executed directly to print insights to the console or export
machine-readable JSON for dashboard or chatbot integration.
"""
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


FACILITY_FILE = Path("data/phc_facility_status.csv")
DISEASE_FILE = Path("data/disease_incidence.csv")


@dataclass
class ForecastResult:
    """Represents near-term forecasts for a specific region."""

    country: str
    region: str
    indicator: str
    current_value: float
    forecast_value: float
    delta: float

    def as_dict(self) -> Dict[str, float | str]:
        return {
            "country": self.country,
            "region": self.region,
            "indicator": self.indicator,
            "current_value": round(self.current_value, 2),
            "forecast_value": round(self.forecast_value, 2),
            "delta": round(self.delta, 2),
        }


def load_facility_data(path: Path = FACILITY_FILE) -> List[Dict[str, object]]:
    """Load facility readiness data into a list of dictionaries."""

    facilities: List[Dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            facilities.append(
                {
                    "country": row["country"],
                    "region": row["region"],
                    "facility_id": row["facility_id"],
                    "facility_type": row["facility_type"],
                    "catchment_population": float(row["catchment_population"]),
                    "staff_count": float(row["staff_count"]),
                    "daily_visits": float(row["daily_visits"]),
                    "stockout_rate": float(row["stockout_rate"]),
                    "functionality_score": float(row["functionality_score"]),
                    "electricity_reliability": float(row["electricity_reliability"]),
                    "water_access": bool(int(row["water_access"])),
                }
            )
    return facilities


def load_disease_data(path: Path = DISEASE_FILE) -> List[Dict[str, object]]:
    """Load disease incidence data."""

    disease_rows: List[Dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            disease_rows.append(
                {
                    "country": row["country"],
                    "region": row["region"],
                    "month": row["month"],
                    "malaria_cases": float(row["malaria_cases"]),
                    "respiratory_cases": float(row["respiratory_cases"]),
                    "maternal_complications": float(row["maternal_complications"]),
                }
            )
    return disease_rows


def compute_facility_gaps(facilities: List[Dict[str, object]]) -> List[Dict[str, object]]:
    """Derive staffing and service quality indicators per facility."""

    enriched: List[Dict[str, object]] = []
    for facility in facilities:
        record = dict(facility)
        pop = facility["catchment_population"] or 1
        staff = facility["staff_count"]
        record["staff_per_10k"] = (staff / pop) * 10000
        record["visits_per_staff"] = (facility["daily_visits"] / staff) if staff else 0.0
        record["undercapacity"] = (
            record["staff_per_10k"] < 12
            or record["functionality_score"] < 0.6
            or not record["water_access"]
            or record["electricity_reliability"] < 0.6
        )
        enriched.append(record)
    return enriched


def aggregate_country_landscape(facilities: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    """Summarise key coverage gaps by country."""

    summary: Dict[str, Dict[str, float]] = {}
    counts: Dict[str, int] = {}

    for facility in facilities:
        country = facility["country"]
        counts[country] = counts.get(country, 0) + 1
        bucket = summary.setdefault(
            country,
            {
                "staff_per_10k": 0.0,
                "functionality": 0.0,
                "stockout": 0.0,
                "undercapacity": 0.0,
            },
        )
        bucket["staff_per_10k"] += facility["staff_per_10k"]
        bucket["functionality"] += facility["functionality_score"]
        bucket["stockout"] += facility["stockout_rate"]
        bucket["undercapacity"] += 1.0 if facility["undercapacity"] else 0.0

    results: List[Dict[str, object]] = []
    for country, metrics in summary.items():
        total = counts[country]
        results.append(
            {
                "country": country,
                "facilities": total,
                "avg_staff_per_10k": metrics["staff_per_10k"] / total if total else 0.0,
                "avg_functionality": metrics["functionality"] / total if total else 0.0,
                "stockout_rate": metrics["stockout"] / total if total else 0.0,
                "undercapacity_rate": round((metrics["undercapacity"] / total) if total else 0.0, 2),
            }
        )
    return results


def _linear_forecast(values: Sequence[float]) -> float:
    """Forecast the next value using a simple linear trend."""

    n = len(values)
    if n == 0:
        return 0.0
    if n == 1:
        return float(values[0])
    if all(val == values[0] for val in values):
        return float(values[0])

    x_values = list(range(n))
    mean_x = sum(x_values) / n
    mean_y = sum(values) / n

    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, values))
    denominator = sum((x - mean_x) ** 2 for x in x_values)
    slope = numerator / denominator if denominator else 0.0
    intercept = mean_y - slope * mean_x
    return slope * n + intercept


def forecast_disease_trends(disease_rows: List[Dict[str, object]]) -> List[ForecastResult]:
    """Forecast near-term patient volumes for each region and condition."""

    grouped: Dict[Tuple[str, str], List[Dict[str, object]]] = {}
    for row in disease_rows:
        key = (row["country"], row["region"])
        grouped.setdefault(key, []).append(row)

    forecasts: List[ForecastResult] = []
    for (country, region), rows in grouped.items():
        sorted_rows = sorted(rows, key=lambda item: item["month"])
        latest = sorted_rows[-1]
        for indicator in ("malaria_cases", "respiratory_cases", "maternal_complications"):
            history = [float(item[indicator]) for item in sorted_rows]
            forecast_value = _linear_forecast(history)
            current_value = float(latest[indicator])
            forecasts.append(
                ForecastResult(
                    country=country,
                    region=region,
                    indicator=indicator,
                    current_value=current_value,
                    forecast_value=forecast_value,
                    delta=forecast_value - current_value,
                )
            )
    return forecasts


def recommend_resources(facilities: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    """Generate staffing and commodity recommendations per facility."""

    recommendations: List[Dict[str, object]] = []
    for facility in facilities:
        pop = facility["catchment_population"]
        current_staff = facility["staff_count"]
        target_staff = (18 * pop) / 10000
        required_staff = max(0, round(target_staff - current_staff))
        urgent_stock = facility["stockout_rate"] > 0.4
        referral_needed = (
            facility["functionality_score"] < 0.5 and facility["daily_visits"] > 120
        )
        recommendations.append(
            {
                "country": facility["country"],
                "region": facility["region"],
                "facility_id": facility["facility_id"],
                "facility_type": facility["facility_type"],
                "staff_count": current_staff,
                "required_staff": required_staff,
                "urgent_stock_replenishment": urgent_stock,
                "refer_patients": referral_needed,
            }
        )
    return recommendations


def compile_insights() -> Dict[str, object]:
    """Generate a consolidated package of insights for downstream use."""

    facilities = compute_facility_gaps(load_facility_data())
    disease_rows = load_disease_data()

    country_view = aggregate_country_landscape(facilities)
    forecasts = forecast_disease_trends(disease_rows)
    recommendations = recommend_resources(facilities)

    underserved = [facility for facility in facilities if facility["undercapacity"]]
    underserved = sorted(underserved, key=lambda row: (row["country"], row["staff_per_10k"]))[:10]

    underserved_records = [
        {
            "country": row["country"],
            "region": row["region"],
            "facility_id": row["facility_id"],
            "staff_per_10k": row["staff_per_10k"],
            "functionality_score": row["functionality_score"],
            "stockout_rate": row["stockout_rate"],
        }
        for row in underserved
    ]

    return {
        "country_summary": country_view,
        "underserved_facilities": underserved_records,
        "forecasts": [forecast.as_dict() for forecast in forecasts],
        "recommendations": recommendations,
    }


def print_insights(insights: Dict[str, object]) -> None:
    """Render insights in a human-readable format."""

    print("=== Country Landscape ===")
    for country in insights["country_summary"]:
        print(
            f"{country['country']}: {country['facilities']} facilities | "
            f"Avg staff/10k={country['avg_staff_per_10k']:.1f} | "
            f"Functionality={country['avg_functionality']:.2f} | "
            f"Stock-outs={country['stockout_rate']:.2f} | "
            f"Undercapacity rate={country['undercapacity_rate']:.2f}"
        )

    print("\n=== Priority Facilities ===")
    if not insights["underserved_facilities"]:
        print("All facilities meet minimum standards.")
    else:
        for facility in insights["underserved_facilities"]:
            print(
                f"{facility['country']} - {facility['region']} - {facility['facility_id']}: "
                f"staff/10k={facility['staff_per_10k']:.1f}, "
                f"functionality={facility['functionality_score']:.2f}, "
                f"stock-out={facility['stockout_rate']:.2f}"
            )

    print("\n=== Forecast Alerts ===")
    for forecast in insights["forecasts"]:
        if abs(forecast["delta"]) < 20:
            continue
        direction = "increase" if forecast["delta"] > 0 else "decrease"
        print(
            f"{forecast['country']} - {forecast['region']} ({forecast['indicator']}): "
            f"{direction} of {abs(forecast['delta']):.1f} expected next month"
        )

    print("\n=== Resource Recommendations ===")
    for rec in insights["recommendations"]:
        actions: List[str] = []
        if rec["required_staff"] > 0:
            actions.append(f"hire/deploy {int(rec['required_staff'])} staff")
        if rec["urgent_stock_replenishment"]:
            actions.append("expedite essential medicines")
        if rec["refer_patients"]:
            actions.append("activate referral support")

        if actions:
            print(f"{rec['country']} - {rec['facility_id']}: " + ", ".join(actions))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate PHC insights and recommendations.")
    parser.add_argument(
        "--export",
        type=Path,
        help="Optional path to export insights as JSON",
    )

    args = parser.parse_args()

    insights = compile_insights()
    print_insights(insights)

    if args.export:
        args.export.parent.mkdir(parents=True, exist_ok=True)
        with args.export.open("w", encoding="utf-8") as handle:
            json.dump(insights, handle, indent=2)
        print(f"\nInsights exported to {args.export}")


if __name__ == "__main__":
    main()
