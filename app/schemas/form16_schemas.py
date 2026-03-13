from pydantic import BaseModel


class SalaryDetails(BaseModel):
    gross_salary: float
    standard_deduction: float
    income_from_salary: float
    net_tax_payable: float
    income_from_other_source: float
    relief_89: float
    total_tds: float


class Form16Data(BaseModel):
    employer_name: str
    employer_pan: str
    employer_tan: str
    employee_pan: str
    salary_details: SalaryDetails


class Form16Response(BaseModel):
    status: str
    data: Form16Data