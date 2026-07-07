from io import BytesIO

import pandas as pd
from openpyxl.styles import Font, PatternFill


def build_excel_workbook(scenarios: pd.DataFrame) -> bytes:
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        scenarios.to_excel(writer, sheet_name="Scenarios", index=False)
        workbook = writer.book
        worksheet = writer.sheets["Scenarios"]

        money_columns = {
            "Freight Rate USD/mt",
            "Gross Freight USD",
            "Commission USD",
            "Net Freight USD",
            "HSFO Price USD/mt",
            "VLSFO Price USD/mt",
            "Bunker Price USD/mt",
            "Ballast Sea Bunker Cost USD",
            "Laden Sea Bunker Cost USD",
            "Sea Bunker Cost USD",
            "Port Bunker Cost USD",
            "Bunker Cost USD",
            "Load Port Cost USD",
            "Discharge Port Cost USD",
            "Port Cost USD",
            "Canal Cost USD",
            "Other Cost USD",
            "Total Voyage Cost USD",
            "Net Voyage Profit USD",
            "TCE USD/day",
        }
        day_columns = {
            "Ballast Days Base",
            "Laden Days Base",
            "Ballast Days",
            "Laden Days",
            "Port Days",
            "Load Port Days",
            "Discharge Port Days",
            "Waiting Days",
            "Total Voyage Days",
        }

        header_fill = PatternFill(fill_type="solid", fgColor="1F4E5F")
        header_font = Font(bold=True, color="FFFFFF")

        for cell in worksheet[1]:
            cell.font = header_font
            cell.fill = header_fill

        for column_cells in worksheet.columns:
            header = column_cells[0].value
            max_length = max(len(str(cell.value)) if cell.value is not None else 0 for cell in column_cells)
            worksheet.column_dimensions[column_cells[0].column_letter].width = min(max(max_length + 2, 12), 28)

            if header in money_columns:
                for cell in column_cells[1:]:
                    cell.number_format = '$#,##0.00'
            elif header in day_columns:
                for cell in column_cells[1:]:
                    cell.number_format = '0.00'

        worksheet.freeze_panes = "A2"

    output.seek(0)
    return output.getvalue()
