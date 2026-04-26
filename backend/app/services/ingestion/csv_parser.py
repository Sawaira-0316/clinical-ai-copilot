"""
backend/app/services/ingestion/csv_parser.py
Flexible file parser supporting CSV, Excel, PDF, and TXT formats.
"""

import csv
import io
from typing import Any, Optional


# ── Helpers ───────────────────────────────────────────────────────────────────

def clean_value(value: Any) -> Optional[str]:
    if value is None:
        return None
    value = str(value).strip()
    if value == "" or value.lower() in {"nan", "null", "none", "n/a", "na", "-"}:
        return None
    return value


def parse_int(value: Any) -> Optional[int]:
    val = clean_value(value)
    if val is None:
        return None
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return None


def is_row_empty(row: dict) -> bool:
    return all(clean_value(v) is None for v in row.values())


def normalize_gender(value: Any) -> Optional[str]:
    val = clean_value(value)
    if not val:
        return None
    mapping = {
        "m": "Male", "male": "Male",
        "f": "Female", "female": "Female",
        "other": "Other",
    }
    return mapping.get(val.lower(), val)


NAME_COLS = {"name", "patient_name", "full_name", "firstname", "first_name", "patientname"}
AGE_COLS = {"age", "patient_age", "age_years", "years"}
GENDER_COLS = {"gender", "sex", "patient_gender", "patient_sex"}
ID_COLS = {"subject_id", "patient_id", "id", "hadm_id", "row_id", "patientid"}


def find_col(headers: list, candidates: set) -> Optional[str]:
    for h in headers:
        if h.lower().strip() in candidates:
            return h
    return None


def build_patient_from_row(row: dict, headers: list, line_num: int) -> dict:
    """Build a patient dict from a row using smart column detection."""
    name_col = find_col(headers, NAME_COLS)
    age_col = find_col(headers, AGE_COLS)
    gender_col = find_col(headers, GENDER_COLS)
    id_col = find_col(headers, ID_COLS)

    if name_col:
        name = clean_value(row.get(name_col))
    elif id_col:
        name = f"Patient-{clean_value(row.get(id_col, str(line_num)))}"
    else:
        name = f"Patient-{line_num}"

    age = parse_int(row.get(age_col)) if age_col else None
    gender = normalize_gender(row.get(gender_col)) if gender_col else None

    return {
        "name": name or f"Patient-{line_num}",
        "age": age,
        "gender": gender,
    }


# ── CSV Parser ────────────────────────────────────────────────────────────────

def parse_csv(content: bytes) -> tuple[list[dict], list[str]]:
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = content.decode("latin-1")

    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None:
        raise ValueError("CSV file has no headers.")

    headers = list(reader.fieldnames)
    patients = []
    errors = []

    for line_num, row in enumerate(reader, start=2):
        row = {k.strip(): v for k, v in row.items()}
        if is_row_empty(row):
            continue
        patients.append(build_patient_from_row(row, headers, line_num))

    return patients, errors


# ── Excel Parser ──────────────────────────────────────────────────────────────

def parse_excel(content: bytes) -> tuple[list[dict], list[str]]:
    try:
        import openpyxl
    except ImportError:
        raise ValueError("openpyxl not installed. Run: pip install openpyxl")

    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    ws = wb.active

    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        raise ValueError("Excel file is empty.")

    headers = [str(h).strip() if h is not None else f"col_{i}" for i, h in enumerate(rows[0])]
    patients = []
    errors = []

    for line_num, row in enumerate(rows[1:], start=2):
        row_dict = {headers[i]: row[i] for i in range(min(len(headers), len(row)))}
        if is_row_empty(row_dict):
            continue
        patients.append(build_patient_from_row(row_dict, headers, line_num))

    wb.close()
    return patients, errors


# ── PDF Parser ────────────────────────────────────────────────────────────────

def parse_pdf(content: bytes) -> tuple[list[dict], list[str]]:
    try:
        import pdfplumber
    except ImportError:
        raise ValueError("pdfplumber not installed. Run: pip install pdfplumber")

    patients = []
    errors = []

    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            # Try to extract tables first
            tables = page.extract_tables()
            for table in tables:
                if not table or len(table) < 2:
                    continue
                headers = [str(h).strip() if h else f"col_{i}" for i, h in enumerate(table[0])]
                for line_num, row in enumerate(table[1:], start=2):
                    row_dict = {headers[i]: row[i] for i in range(min(len(headers), len(row)))}
                    if is_row_empty(row_dict):
                        continue
                    patients.append(build_patient_from_row(row_dict, headers, line_num))

            # If no tables found, extract text and try to parse
            if not tables:
                text = page.extract_text()
                if text:
                    lines = [l.strip() for l in text.split("\n") if l.strip()]
                    for i, line in enumerate(lines):
                        parts = line.split()
                        if len(parts) >= 2:
                            patients.append({
                                "name": f"Patient-Page{page_num}-{i+1}",
                                "age": None,
                                "gender": None,
                            })

    if not patients:
        raise ValueError("No patient data found in PDF.")

    return patients, errors


# ── TXT Parser ────────────────────────────────────────────────────────────────

def parse_txt(content: bytes) -> tuple[list[dict], list[str]]:
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = content.decode("latin-1")

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if not lines:
        raise ValueError("Text file is empty.")

    # Try CSV-style parsing first
    try:
        reader = csv.DictReader(io.StringIO(text))
        if reader.fieldnames and len(reader.fieldnames) > 1:
            return parse_csv(content)
    except Exception:
        pass

    # Fall back to line-by-line parsing
    patients = []
    errors = []
    for i, line in enumerate(lines, start=1):
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 1 and parts[0]:
            patient = {"name": parts[0], "age": None, "gender": None}
            if len(parts) >= 2:
                patient["age"] = parse_int(parts[1])
            if len(parts) >= 3:
                patient["gender"] = normalize_gender(parts[2])
            patients.append(patient)

    if not patients:
        raise ValueError("No valid data found in text file.")

    return patients, errors


# ── Main Parser Class ─────────────────────────────────────────────────────────

class CSVParser:
    """
    Universal file parser supporting CSV, Excel, PDF, and TXT.
    Auto-detects format and parses patient data.
    """

    @staticmethod
    def parse_patients_csv(content: bytes, filename: str = "upload.csv") -> tuple[list[dict], list[str]]:
        """
        Parse patient data from any supported file format.
        Auto-detects format from filename extension.
        """
        ext = filename.lower().split(".")[-1] if "." in filename else "csv"

        if ext in ("xlsx", "xls"):
            patients, errors = parse_excel(content)
        elif ext == "pdf":
            patients, errors = parse_pdf(content)
        elif ext == "txt":
            patients, errors = parse_txt(content)
        else:
            # Default to CSV
            patients, errors = parse_csv(content)

        if not patients:
            raise ValueError(f"No valid patient rows found in {ext.upper()} file.")

        return patients, errors