import os
import pandas as pd

from django.core.management.base import BaseCommand
from apps.common.models import (
    Sheet,
    Tab,
    TabFields,
    TabRow,
    TabCell,
    FieldType
)


def detect_type(series):

    series = series.dropna()

    if series.empty:
        return FieldType.STRING

    if pd.api.types.is_datetime64_any_dtype(series):
        return FieldType.DATE

    if pd.api.types.is_numeric_dtype(series):
        return FieldType.NUMERIC

    return FieldType.STRING


def find_header_row(df):
    max_count = 0
    header_row = 0

    for i in range(min(10, len(df))):
        count = df.iloc[i].count()

        if count > max_count:
            max_count = count
            header_row = i

    return header_row


class Command(BaseCommand):
    help = "Import Excel structure and data dynamically"

    def handle(self, *args, **options):

        file_path = input("Enter Excel file path: ").strip().strip('"').strip("'")

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR("File not found"))
            return

        self.stdout.write(self.style.WARNING("Clearing existing data..."))

        TabCell.objects.all().delete()
        TabRow.objects.all().delete()
        TabFields.objects.all().delete()
        Tab.objects.all().delete()
        Sheet.objects.all().delete()

        file_name = os.path.splitext(os.path.basename(file_path))[0]

        sheet_obj = Sheet.objects.create(name=file_name)

        xls = pd.ExcelFile(file_path)

        for sheet_name in xls.sheet_names:

            self.stdout.write(self.style.SUCCESS(f"\nProcessing tab: {sheet_name}"))

            tab_obj = Tab.objects.create(
                sheet=sheet_obj,
                name=sheet_name
            )

            df = pd.read_excel(xls, sheet_name, header=None)

            header_row = find_header_row(df)

            headers = df.iloc[header_row]

            data = df.iloc[header_row + 1:]

            field_map = {}

            # Create fields
            for col_index, header in headers.items():

                if pd.isna(header):
                    continue

                column_data = data[col_index]

                field_type = detect_type(column_data)

                field = TabFields.objects.create(
                    tab=tab_obj,
                    name=str(header).strip(),
                    type=field_type
                )

                field_map[col_index] = field

                self.stdout.write(f"   Field: {header} ({field_type})")

            # Create rows and cells
            for row_index, row_data in data.iterrows():

                if row_data.isna().all():
                    continue

                row_obj = TabRow.objects.create(
                    tab=tab_obj,
                    row_index=row_index
                )

                for col_index, field in field_map.items():

                    value = row_data[col_index]

                    if pd.isna(value):
                        continue

                    TabCell.objects.create(
                        row=row_obj,
                        field=field,
                        value=str(value)
                    )

        self.stdout.write(self.style.SUCCESS("\nImport completed"))