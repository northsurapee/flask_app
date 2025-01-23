import os
import uuid

import pandas as pd


def excel_diff_check(expected_file, expected_sheet, actual_file, actual_sheet, STORAGE_FOLDER):
    # Define the output directory and file name
    output_file_id = str(uuid.uuid4())
    output_file_name = f"{output_file_id}_result.xlsx"
    output_file_path = os.path.join(STORAGE_FOLDER, output_file_name)

    # Ensure the output directory exists
    os.makedirs(STORAGE_FOLDER, exist_ok=True)

    # Create a new output file from scratch, replacing if it exists
    with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
        # Load expected and actual sheets
        expected_df = pd.read_excel(expected_file, sheet_name=expected_sheet)
        actual_df = pd.read_excel(actual_file, sheet_name=actual_sheet)

        expected_df.to_excel(writer, sheet_name='expected', index=False)
        actual_df.to_excel(writer, sheet_name='actual', index=False)

        # Compare aspects
        summary_data = []

        # Number of columns
        expected_columns = len(expected_df.columns)
        actual_columns = len(actual_df.columns)
        column_result = "Pass" if expected_columns == actual_columns else "Fail"
        column_reason = "" if column_result == "Pass" else "Mismatch in number of columns"
        summary_data.append(["Number of columns", expected_columns, actual_columns, column_result, column_reason])

        # Number of rows
        expected_rows = len(expected_df)
        actual_rows = len(actual_df)
        row_result = "Pass" if expected_rows == actual_rows else "Fail"
        row_reason = "" if row_result == "Pass" else "Mismatch in number of rows"
        summary_data.append(["Number of rows", expected_rows, actual_rows, row_result, row_reason])

        # Number of cells
        expected_cells = expected_df.size
        actual_cells = actual_df.size
        cell_result = "Pass" if expected_cells == actual_cells else "Fail"
        cell_reason = "" if cell_result == "Pass" else "Mismatch in number of cells"
        summary_data.append(["Number of cells", expected_cells, actual_cells, cell_result, cell_reason])

        # Matching cells
        match_count = 0
        diff_count = 0
        diff_cells = []

        for col in set(expected_df.columns).intersection(set(actual_df.columns)):
            expected_col_data = expected_df[col].fillna('')
            actual_col_data = actual_df[col].fillna('')

            for i, (expected_value, actual_value) in enumerate(zip(expected_col_data, actual_col_data), start=1):
                if expected_value == actual_value:
                    match_count += 1
                else:
                    diff_count += 1
                    diff_cells.append(f"Column '{col}' Row {i}")

        total_cells = min(expected_cells, actual_cells)
        matching_result = "Pass" if diff_count == 0 else "Fail"
        matching_reason = (
            "" if diff_count == 0 else
            f"Mismatched cells: {', '.join(diff_cells[:5])}..." if len(diff_cells) > 5 else
            f"Mismatched cells: {', '.join(diff_cells)}"
        )
        summary_data.append(["Matching cells", total_cells, match_count, matching_result, matching_reason])

        # Create a summary DataFrame
        summary_df = pd.DataFrame(summary_data, columns=['Aspect', 'Expect', 'Actual', 'Result', 'Reason'])

        # Save the summary sheet to the output file
        summary_df.to_excel(writer, sheet_name='summary', index=False)

    # Return the path to the result file
    return output_file_path


