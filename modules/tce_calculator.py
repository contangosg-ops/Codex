def sea_consumption(inputs: dict, condition: str) -> float:
    condition_key = f"{condition} Sea Consumption mt/day"
    if condition_key in inputs:
        return float(inputs[condition_key])
    return float(inputs.get("Sea Consumption mt/day", 0))


def calculate_tce(inputs: dict) -> dict:
    cargo_quantity = float(inputs["Cargo Quantity mt"])
    freight_rate = float(inputs["Freight Rate USD/mt"])
    commission_pct = float(inputs["Commission %"])

    ballast_distance = float(inputs["Ballast Distance nm"])
    laden_distance = float(inputs["Laden Distance nm"])
    ballast_speed = float(inputs["Ballast Speed kn"])
    laden_speed = float(inputs["Laden Speed kn"])
    sea_margin_pct = float(inputs.get("Sea Margin %", 0))

    laden_sea_consumption = sea_consumption(inputs, "Laden")
    ballast_sea_consumption = sea_consumption(inputs, "Ballast")
    port_consumption = float(inputs["Port Consumption mt/day"])
    bunker_price = float(inputs["Bunker Price USD/mt"])

    load_port_days = float(inputs["Load Port Days"])
    discharge_port_days = float(inputs["Discharge Port Days"])
    waiting_days = float(inputs["Waiting Days"])

    load_port_cost = float(inputs.get("Load Port Cost USD", 0))
    discharge_port_cost = float(inputs.get("Discharge Port Cost USD", 0))
    port_cost = float(inputs.get("Port Cost USD", load_port_cost + discharge_port_cost))
    if "Port Cost USD" not in inputs:
        port_cost = load_port_cost + discharge_port_cost
    canal_cost = float(inputs["Canal Cost USD"])
    other_cost = float(inputs["Other Cost USD"])

    gross_freight = cargo_quantity * freight_rate
    commission = gross_freight * commission_pct / 100
    net_freight = gross_freight * (1 - commission_pct / 100)

    ballast_days_base = ballast_distance / ballast_speed / 24 if ballast_speed else 0
    laden_days_base = laden_distance / laden_speed / 24 if laden_speed else 0
    sea_margin_factor = 1 + sea_margin_pct / 100
    ballast_days = ballast_days_base * sea_margin_factor
    laden_days = laden_days_base * sea_margin_factor
    port_days = load_port_days + discharge_port_days + waiting_days
    total_voyage_days = ballast_days + laden_days + port_days

    ballast_sea_bunker_cost = ballast_days * ballast_sea_consumption * bunker_price
    laden_sea_bunker_cost = laden_days * laden_sea_consumption * bunker_price
    sea_bunker_cost = ballast_sea_bunker_cost + laden_sea_bunker_cost
    port_bunker_cost = port_days * port_consumption * bunker_price
    bunker_cost = sea_bunker_cost + port_bunker_cost

    total_voyage_cost = bunker_cost + port_cost + canal_cost + other_cost
    net_voyage_profit = net_freight - total_voyage_cost
    tce = net_voyage_profit / total_voyage_days if total_voyage_days else 0

    return {
        **inputs,
        "Gross Freight USD": gross_freight,
        "Commission USD": commission,
        "Net Freight USD": net_freight,
        "Sea Margin %": sea_margin_pct,
        "Ballast Days Base": ballast_days_base,
        "Laden Days Base": laden_days_base,
        "Ballast Days": ballast_days,
        "Laden Days": laden_days,
        "Port Days": port_days,
        "Total Voyage Days": total_voyage_days,
        "Ballast Sea Bunker Cost USD": ballast_sea_bunker_cost,
        "Laden Sea Bunker Cost USD": laden_sea_bunker_cost,
        "Sea Bunker Cost USD": sea_bunker_cost,
        "Port Bunker Cost USD": port_bunker_cost,
        "Bunker Cost USD": bunker_cost,
        "Load Port Cost USD": load_port_cost,
        "Discharge Port Cost USD": discharge_port_cost,
        "Port Cost USD": port_cost,
        "Canal Cost USD": canal_cost,
        "Other Cost USD": other_cost,
        "Total Voyage Cost USD": total_voyage_cost,
        "Net Voyage Profit USD": net_voyage_profit,
        "TCE USD/day": tce,
    }
