from backend.export.excel.workbook import CustomWorkbook

workbook = CustomWorkbook('sheet_config_gziz1.json')
workbook.add_sheets()
workbook.set_sheets_properties()
workbook.fill_sheets()
workbook.create_excel()
