import pdfplumber
import re



def extract_form16_data(filepath):
    text = extract_text(filepath)
    # print(text)
    certificate_no = extract_certificate_no(text)
    assessment_year = extract_assessment_year(text)
    period = extract_employment_period(text)

    print("Certificate No:", certificate_no)
    print("Assessment Year:", assessment_year)
    print("Employment Period:", period)

    employer_name = find(
        r"([A-Z\s]+PRIVATE LIMITED)",
        text
    )

    pan_block = re.search(
        r"PAN of the Deductor\s+TAN of the Deductor.*?\n([A-Z0-9]{10})\s+([A-Z0-9]{10})\s+([A-Z0-9]{10})",
        text
    )

    employer_pan = None
    employer_tan = None
    employee_pan = None


    if pan_block:
        employer_pan = pan_block.group(1)
        employer_tan = pan_block.group(2)
        employee_pan = pan_block.group(3)

    return {

        "employer_name": employer_name,
        "employer_pan": employer_pan,
        "employer_tan": employer_tan,
        "employee_pan": employee_pan,
        "salary_details": extract_salary_fields(text)
    }

def extract_certificate_no(text):
    m = re.search(r"Certificate (?:No\.|Number:)\s*([A-Z0-9]+)", text)
    return m.group(1) if m else None


def extract_assessment_year(text):
    m = re.search(r"Assessment Year\s*[:]*\s*(\d{4}-\d{2})", text)
    return m.group(1) if m else None


def extract_employment_period(text):
    m = re.search(
        r"Assessment Year\s*\d{4}-\d{2}\s+(\d{2}-[A-Za-z]{3}-\d{4})\s+(\d{2}-[A-Za-z]{3}-\d{4})",
        text
    )

    if m:
        return {
            "from": m.group(1),
            "to": m.group(2)
        }

    return {
        "from": None,
        "to": None
    }

def extract_net_tax(text):

    m = re.search(
        r"Net tax payable.*?\)\s*([\d\.]+)",
        text
    )

    if not m:
        return None

    return float(m.group(1))

def extract_salary_fields(text):

    def num(pattern):
        m = re.search(pattern, text)
        return float(m.group(1)) if m else 0

    gross_salary = num(
        r"Salary as per provisions contained in section 17\(1\)\s+([\d\.]+)"
    )

    net_tax_payable = extract_net_tax(text)

    balance = gross_salary - net_tax_payable

    standard_deduction = num(
        r"Standard deduction under section 16\(ia\)\s+([\d\.]+)"
    )

    income_from_salary = balance - standard_deduction

    other_source_income = num(
        r"Income under the head Other Sources offered for TDS\s+([\d\.]+)"
    )

    

    relief_89 = num(
        r"Relief under section 89.*?([\d\.]+)"
    )

    total_tds = num(
        r"Total \(Rs\.\)\s+[\d\.]+\s+([\d\.]+)\s+([\d\.]+)"
    )

    return {
        "gross_salary": gross_salary,
        "standard_deduction": standard_deduction,
        "income_from_salary": income_from_salary,
        "net_tax_payable": net_tax_payable,
        "income_from_other_source": other_source_income,
        "relief_89": relief_89,
        "total_tds": total_tds
    }


def find(pattern, text):

    m = re.search(pattern, text, re.DOTALL)

    if not m:
        return None

    return m.group(1).strip()

def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text



