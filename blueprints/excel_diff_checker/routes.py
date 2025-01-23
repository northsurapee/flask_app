import os
import uuid
import time

import pandas as pd

from . import excel_diff_checker_bp
from flask import render_template, request, send_file

from .logic import excel_diff_check

STORAGE_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'temp_files')

# File expiration time (in seconds)
FILE_EXPIRATION_TIME = 300


@excel_diff_checker_bp.route('/')
def index():
    return render_template('index.html')


@excel_diff_checker_bp.route('/upload', methods=['POST'])
def upload_files():
    # Ensure both files are uploaded
    expected_file = request.files['expected_file']
    actual_file = request.files['actual_file']

    # Generate unique identifiers for the files
    expected_file_id = str(uuid.uuid4())
    actual_file_id = str(uuid.uuid4())

    # Save the files
    expected_file_path = os.path.join(STORAGE_FOLDER, f"{expected_file_id}_{expected_file.name}.xlsx")
    actual_file_path = os.path.join(STORAGE_FOLDER, f"{actual_file_id}_{actual_file.name}.xlsx")

    expected_file.save(expected_file_path)
    actual_file.save(actual_file_path)

    # Get sheet names for both files
    expected_file_sheets = pd.ExcelFile(expected_file_path).sheet_names
    actual_file_sheets = pd.ExcelFile(actual_file_path).sheet_names

    # Run cleanup to remove expired files after upload
    cleanup_expired_files()

    return render_template(
        'select_sheet.html',
        expected_file_sheets=expected_file_sheets,
        actual_file_sheets=actual_file_sheets,
        expected_file_name=expected_file.filename,
        actual_file_name=actual_file.filename,
        expected_file_path=expected_file_path,
        actual_file_path=actual_file_path,
    )


@excel_diff_checker_bp.route('/process', methods=['POST'])
def process_files():
    # Retrieve filenames and selected sheets
    expected_file_path = request.form['expected_file_path']
    actual_file_path = request.form['actual_file_path']
    expect_sheet = request.form['expect_sheet']
    actual_sheet = request.form['actual_sheet']

    # Process both selected sheets
    process_file = excel_diff_check(expected_file_path,
                                    expect_sheet,
                                    actual_file_path,
                                    actual_sheet,
                                    STORAGE_FOLDER
                                    )

    return send_file(process_file, as_attachment=True)


def cleanup_expired_files():
    current_time = time.time()

    # List all files in the storage folder
    for file_name in os.listdir(STORAGE_FOLDER):
        file_path = os.path.join(STORAGE_FOLDER, file_name)

        # Get the file's last modified time
        file_modified_time = os.path.getmtime(file_path)

        # Check if the file has expired (older than the defined expiration time)
        if current_time - file_modified_time > FILE_EXPIRATION_TIME:
            try:
                os.remove(file_path)  # Delete expired file
                print(f"Removed expired file: {file_name}")
            except Exception as e:
                print(f"Error removing file {file_name}: {str(e)}")
