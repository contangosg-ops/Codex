import pandas as pd
import streamlit as st

from modules.excel_exporter import build_excel_workbook
from modules.tce_calculator import calculate_tce


APP_TITLE = "Capesize C5 TCE Calculator"

VESSEL_SPEC = {
    "Vessel Type": "Baltic BCI 182 Type",
    "Scrubber": "Non-scrubber fitted",
    "DWT mt": 182000,
    "SSW Draft m": 18.2,
    "Max Age yrs": 10,
    "LOA m": 292,
    "Beam m": 45,
    "TPC": 123,
    "Grain cbm": 199500,
    "Cargo Quantity mt": 160000,
    "Diesel at Sea": "No diesel at sea",
}

DEFAULT_SCRUBBER_STATUS = "Non-scrubber fitted"
FUEL_PRICE_DEFAULTS = {
    "HSFO": 500.0,
    "VLSFO": 620.0,
}

SPEED_CONSUMPTION = {
    14: {"Laden Sea Consumption mt/day": 52.0, "Ballast Sea Consumption mt/day": 44.0},
    13: {"Laden Sea Consumption mt/day": 44.0, "Ballast Sea Consumption mt/day": 36.0},
    12: {"Laden Sea Consumption mt/day": 36.0, "Ballast Sea Consumption mt/day": 29.0},
    11: {"Laden Sea Consumption mt/day": 29.0, "Ballast Sea Consumption mt/day": 23.0},
}

ROUTE_SPEC = {
    "Route Name": "C5 Qingdao-Dampier-Qingdao Round Voyage",
    "Ballast Leg": "Qingdao to Dampier",
    "Laden Leg": "Dampier to Qingdao",
    "Ballast Distance nm": 3532.0,
    "Laden Distance nm": 3532.0,
    "Sea Margin %": 5.0,
    "Load Rate mt/day": 80000.0,
    "Discharge Rate mt/day": 30000.0,
    "Waiting Days": 0.0,
    "Load Port Cost USD": 140000.0,
    "Discharge Port Cost USD": 120000.0,
    "Canal Cost USD": 0.0,
    "Port Consumption mt/day": 5.0,
}


def number_input(label: str, value: float, step: float, min_value: float = 0.0) -> float:
    return float(st.number_input(label, min_value=min_value, value=float(value), step=float(step)))


def format_money(value: float) -> str:
    return f"${value:,.0f}"


def format_number(value: float, decimals: int = 2) -> str:
    return f"{value:,.{decimals}f}"


def scrubber_status(vessel_spec: dict) -> str:
    return vessel_spec.get("Scrubber") or DEFAULT_SCRUBBER_STATUS


def fuel_type_for_scrubber(status: str) -> str:
    normalized = status.strip().lower()
    if normalized.startswith("scrubber fitted"):
        return "HSFO"
    return "VLSFO"


def apply_speed_profile(inputs: dict, ballast_speed: int, laden_speed: int) -> dict:
    ballast_consumption = SPEED_CONSUMPTION[ballast_speed]
    laden_consumption = SPEED_CONSUMPTION[laden_speed]
    return {
        **inputs,
        "Optimization Mode": "Max TCE by Ballast/Laden Speed",
        "Ballast Speed kn": float(ballast_speed),
        "Laden Speed kn": float(laden_speed),
        "Laden Sea Consumption mt/day": laden_consumption["Laden Sea Consumption mt/day"],
        "Ballast Sea Consumption mt/day": ballast_consumption["Ballast Sea Consumption mt/day"],
    }


def optimize_speed(inputs: dict) -> tuple[dict, pd.DataFrame]:
    results = []
    for ballast_speed in SPEED_CONSUMPTION:
        for laden_speed in SPEED_CONSUMPTION:
            result = calculate_tce(apply_speed_profile(inputs, ballast_speed, laden_speed))
            result["Ballast Speed Case kn"] = ballast_speed
            result["Laden Speed Case kn"] = laden_speed
            result["Speed Combination"] = f"B{ballast_speed} / L{laden_speed}"
            results.append(result)

    best_result = max(results, key=lambda item: item["TCE USD/day"])
    comparison = pd.DataFrame(results)
    return best_result, comparison


def render_vessel_spec() -> None:
    st.subheader("Fixed Baltic Vessel Description")

    route_cols = st.columns(3)
    route_cols[0].metric("Route Basis", ROUTE_SPEC["Route Name"])
    route_cols[1].metric("Ballast Leg", ROUTE_SPEC["Ballast Leg"])
    route_cols[2].metric("Laden Leg", ROUTE_SPEC["Laden Leg"])

    spec_cols = st.columns(5)
    spec_cols[0].metric("Vessel Type", VESSEL_SPEC["Vessel Type"])
    spec_cols[1].metric("DWT", f"{VESSEL_SPEC['DWT mt']:,.0f} mt")
    spec_cols[2].metric("Draft", f"{VESSEL_SPEC['SSW Draft m']:.1f} m SSW")
    spec_cols[3].metric("LOA / Beam", f"{VESSEL_SPEC['LOA m']} m / {VESSEL_SPEC['Beam m']} m")
    status = scrubber_status(VESSEL_SPEC)
    spec_cols[4].metric("Scrubber", status)

    detail_cols = st.columns(5)
    detail_cols[0].metric("Max Age", f"{VESSEL_SPEC['Max Age yrs']} yrs")
    detail_cols[1].metric("TPC", f"{VESSEL_SPEC['TPC']}")
    detail_cols[2].metric("Grain", f"{VESSEL_SPEC['Grain cbm']:,.0f} cbm")
    detail_cols[3].metric("Cargo Basis", f"{VESSEL_SPEC['Cargo Quantity mt']:,.0f} mt")
    detail_cols[4].metric("At Sea", VESSEL_SPEC["Diesel at Sea"])

    with st.expander("Speed & Consumption Table"):
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Speed kn": speed,
                        "Laden MFO mt/day": values["Laden Sea Consumption mt/day"],
                        "Ballast MFO mt/day": values["Ballast Sea Consumption mt/day"],
                        "Diesel at Sea": "0",
                    }
                    for speed, values in SPEED_CONSUMPTION.items()
                ]
            ),
            use_container_width=True,
            hide_index=True,
        )

    with st.expander("C5 Round Voyage Basis"):
        st.dataframe(
            pd.DataFrame(
                [
                    {"Item": "Round Voyage", "Value": ROUTE_SPEC["Route Name"]},
                    {"Item": "Ballast Leg", "Value": ROUTE_SPEC["Ballast Leg"]},
                    {"Item": "Laden Leg", "Value": ROUTE_SPEC["Laden Leg"]},
                    {"Item": "Default Ballast Distance nm", "Value": f"{ROUTE_SPEC['Ballast Distance nm']:,.0f}"},
                    {"Item": "Default Laden Distance nm", "Value": f"{ROUTE_SPEC['Laden Distance nm']:,.0f}"},
                    {"Item": "Default Sea Margin %", "Value": f"{ROUTE_SPEC['Sea Margin %']:.1f}"},
                    {"Item": "Default Load Rate mt/day", "Value": f"{ROUTE_SPEC['Load Rate mt/day']:,.0f}"},
                    {"Item": "Default Discharge Rate mt/day", "Value": f"{ROUTE_SPEC['Discharge Rate mt/day']:,.0f}"},
                    {"Item": "Default Dampier Load Port Cost USD", "Value": f"{ROUTE_SPEC['Load Port Cost USD']:,.0f}"},
                    {"Item": "Default Qingdao Discharge Port Cost USD", "Value": f"{ROUTE_SPEC['Discharge Port Cost USD']:,.0f}"},
                ]
            ),
            use_container_width=True,
            hide_index=True,
        )


def build_inputs() -> dict:
    st.subheader("C5 Market Inputs")

    status = scrubber_status(VESSEL_SPEC)
    fuel_type = fuel_type_for_scrubber(status)

    market_cols = st.columns(5)
    with market_cols[0]:
        freight_rate = number_input("C5 Freight Rate USD/mt", 8.50, 0.10)
    with market_cols[1]:
        commission_pct = number_input("Commission %", 5.00, 0.10)
    with market_cols[2]:
        hsfo_price = number_input("HSFO Price USD/mt", FUEL_PRICE_DEFAULTS["HSFO"], 10.0)
    with market_cols[3]:
        vlsfo_price = number_input("VLSFO Price USD/mt", FUEL_PRICE_DEFAULTS["VLSFO"], 10.0)
    with market_cols[4]:
        other_cost = number_input("Other Cost USD", 0.0, 1000.0)
    bunker_price = hsfo_price if fuel_type == "HSFO" else vlsfo_price

    fuel_cols = st.columns(3)
    fuel_cols[0].metric("Scrubber Status", status)
    fuel_cols[1].metric("Fuel Type Used", fuel_type)
    fuel_cols[2].metric("Used Fuel Price", format_money(bunker_price))

    st.subheader("Speed & Voyage Assumptions")

    speed_cols = st.columns(4)
    with speed_cols[0]:
        port_consumption = number_input(
            "Port MFO Consumption mt/day",
            ROUTE_SPEC["Port Consumption mt/day"],
            0.5,
        )

    distance_cols = st.columns(4)
    with distance_cols[0]:
        ballast_distance = number_input(
            "Qingdao to Dampier Ballast Distance nm",
            ROUTE_SPEC["Ballast Distance nm"],
            50.0,
        )
    with distance_cols[1]:
        laden_distance = number_input(
            "Dampier to Qingdao Laden Distance nm",
            ROUTE_SPEC["Laden Distance nm"],
            50.0,
        )
    with distance_cols[2]:
        sea_margin_pct = number_input("Sea Margin %", ROUTE_SPEC["Sea Margin %"], 0.5)
    with distance_cols[3]:
        cargo_quantity = number_input("Cargo Quantity mt", VESSEL_SPEC["Cargo Quantity mt"], 1000.0)

    port_time_cols = st.columns(4)
    with port_time_cols[0]:
        load_rate = number_input("Load Rate mt/day", ROUTE_SPEC["Load Rate mt/day"], 1000.0)
    with port_time_cols[1]:
        discharge_rate = number_input("Discharge Rate mt/day", ROUTE_SPEC["Discharge Rate mt/day"], 1000.0)
    with port_time_cols[2]:
        waiting_days = number_input("Waiting Days", ROUTE_SPEC["Waiting Days"], 0.25)
    with port_time_cols[3]:
        load_port_cost = number_input("Dampier Load Port Cost USD", ROUTE_SPEC["Load Port Cost USD"], 1000.0)

    cargo_cols = st.columns(4)
    with cargo_cols[0]:
        discharge_port_cost = number_input(
            "Qingdao Discharge Port Cost USD",
            ROUTE_SPEC["Discharge Port Cost USD"],
            1000.0,
        )
    with cargo_cols[1]:
        canal_cost = number_input("Canal Cost USD", ROUTE_SPEC["Canal Cost USD"], 1000.0)

    load_port_days = cargo_quantity / load_rate if load_rate else 0
    discharge_port_days = cargo_quantity / discharge_rate if discharge_rate else 0
    port_cost = load_port_cost + discharge_port_cost

    calc_cols = st.columns(4)
    calc_cols[0].metric("Calculated Load Port Days", f"{format_number(load_port_days)} days")
    calc_cols[1].metric("Calculated Discharge Port Days", f"{format_number(discharge_port_days)} days")
    calc_cols[2].metric("Calculated Port Days", f"{format_number(load_port_days + discharge_port_days + waiting_days)} days")
    calc_cols[3].metric("Calculated Port Cost", format_money(port_cost))

    return {
        "Scenario Name": "Capesize C5",
        "Vessel Type": VESSEL_SPEC["Vessel Type"],
        "Route Name": ROUTE_SPEC["Route Name"],
        "Ballast Leg": ROUTE_SPEC["Ballast Leg"],
        "Laden Leg": ROUTE_SPEC["Laden Leg"],
        "Cargo Quantity mt": cargo_quantity,
        "Load Rate mt/day": load_rate,
        "Discharge Rate mt/day": discharge_rate,
        "Freight Rate USD/mt": freight_rate,
        "Commission %": commission_pct,
        "Ballast Distance nm": ballast_distance,
        "Laden Distance nm": laden_distance,
        "Sea Margin %": sea_margin_pct,
        "Port Consumption mt/day": port_consumption,
        "Scrubber Status": status,
        "Fuel Type": fuel_type,
        "HSFO Price USD/mt": hsfo_price,
        "VLSFO Price USD/mt": vlsfo_price,
        "Bunker Price USD/mt": bunker_price,
        "Load Port Days": load_port_days,
        "Discharge Port Days": discharge_port_days,
        "Waiting Days": waiting_days,
        "Load Port Cost USD": load_port_cost,
        "Discharge Port Cost USD": discharge_port_cost,
        "Port Cost USD": port_cost,
        "Canal Cost USD": canal_cost,
        "Other Cost USD": other_cost,
        "Scrubber": status,
        "Diesel at Sea": VESSEL_SPEC["Diesel at Sea"],
    }


def render_speed_comparison(comparison: pd.DataFrame, best_combination: str) -> None:
    st.subheader("Speed Optimization")
    display_columns = [
        "Speed Combination",
        "Ballast Speed Case kn",
        "Laden Speed Case kn",
        "Laden Sea Consumption mt/day",
        "Ballast Sea Consumption mt/day",
        "Total Voyage Days",
        "Bunker Cost USD",
        "Net Voyage Profit USD",
        "TCE USD/day",
    ]
    display_df = comparison[display_columns].copy()
    display_df["Selected"] = display_df["Speed Combination"].eq(best_combination).map({True: "Yes", False: ""})
    display_df = display_df[
        [
            "Selected",
            "Speed Combination",
            "Ballast Speed Case kn",
            "Laden Speed Case kn",
            "Laden Sea Consumption mt/day",
            "Ballast Sea Consumption mt/day",
            "Total Voyage Days",
            "Bunker Cost USD",
            "Net Voyage Profit USD",
            "TCE USD/day",
        ]
    ]
    st.dataframe(
        display_df.style.format(
            {
                "Laden Sea Consumption mt/day": "{:,.0f}",
                "Ballast Sea Consumption mt/day": "{:,.0f}",
                "Total Voyage Days": "{:,.2f}",
                "Bunker Cost USD": "${:,.0f}",
                "Net Voyage Profit USD": "${:,.0f}",
                "TCE USD/day": "${:,.0f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


def render_used_speed_consumption(result: dict) -> None:
    st.subheader("Used Speed and Consumption")
    used_cols = st.columns(5)
    used_cols[0].metric("Ballast Speed", f"{format_number(result['Ballast Speed kn'], 0)} kn")
    used_cols[1].metric("Ballast MFO", f"{format_number(result['Ballast Sea Consumption mt/day'], 0)} mt/day")
    used_cols[2].metric("Laden Speed", f"{format_number(result['Laden Speed kn'], 0)} kn")
    used_cols[3].metric("Laden MFO", f"{format_number(result['Laden Sea Consumption mt/day'], 0)} mt/day")
    used_cols[4].metric("Optimization", "Best of 16")


def render_results(result: dict) -> None:
    st.subheader("TCE Result")

    tce_cols = st.columns([1.2, 1, 1, 1])
    tce_cols[0].metric("TCE USD/day", format_money(result["TCE USD/day"]))
    tce_cols[1].metric("Net Voyage Profit", format_money(result["Net Voyage Profit USD"]))
    tce_cols[2].metric("Total Voyage Days", f"{format_number(result['Total Voyage Days'])} days")
    tce_cols[3].metric("Bunker Cost", format_money(result["Bunker Cost USD"]))

    st.subheader("Calculation Breakdown")
    breakdown_cols = st.columns(4)
    with breakdown_cols[0]:
        st.markdown("##### Revenue")
        st.metric("Gross Freight", format_money(result["Gross Freight USD"]))
        st.metric("Commission", format_money(result["Commission USD"]))
        st.metric("Net Freight", format_money(result["Net Freight USD"]))

    with breakdown_cols[1]:
        st.markdown("##### Days")
        st.metric("Sea Margin", f"{format_number(result['Sea Margin %'], 1)}%")
        st.metric("Ballast Days", f"{format_number(result['Ballast Days'])} days")
        st.metric("Laden Days", f"{format_number(result['Laden Days'])} days")
        st.metric("Port Days", f"{format_number(result['Port Days'])} days")

    with breakdown_cols[2]:
        st.markdown("##### Consumption")
        st.metric("Laden MFO", f"{format_number(result['Laden Sea Consumption mt/day'], 0)} mt/day")
        st.metric("Ballast MFO", f"{format_number(result['Ballast Sea Consumption mt/day'], 0)} mt/day")
        st.metric("Port MFO", f"{format_number(result['Port Consumption mt/day'], 1)} mt/day")

    with breakdown_cols[3]:
        st.markdown("##### Costs")
        st.metric("Load Port Cost", format_money(result["Load Port Cost USD"]))
        st.metric("Discharge Port Cost", format_money(result["Discharge Port Cost USD"]))
        st.metric("Port Cost", format_money(result["Port Cost USD"]))
        st.metric("Total Voyage Cost", format_money(result["Total Voyage Cost USD"]))


def render_export(result: dict, comparison: pd.DataFrame) -> None:
    result_df = pd.concat([pd.DataFrame([result]), comparison], ignore_index=True)
    excel_bytes = build_excel_workbook(result_df)
    st.download_button(
        "Export C5 TCE Excel",
        data=excel_bytes,
        file_name="capesize_c5_tce.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=False,
    )


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="ship", layout="wide")
    st.title(APP_TITLE)
    st.caption("Capesize C5 TCE calculation using the Baltic non-scrubber BCI 182 Type description.")

    render_vessel_spec()
    used_speed_slot = st.container()
    inputs = build_inputs()
    result, comparison = optimize_speed(inputs)
    with used_speed_slot:
        render_used_speed_consumption(result)
    render_results(result)
    render_speed_comparison(comparison, result["Speed Combination"])
    render_export(result, comparison)


if __name__ == "__main__":
    main()
