from typing import Literal

from pydantic import BaseModel, Field


class LoanApplication(BaseModel):
    Age: int | None = Field(default=None, ge=18, le=100)
    Income: int | None = Field(default=None, ge=0)
    LoanAmount: int | None = Field(default=None, ge=0)
    CreditScore: int | None = Field(default=None, ge=300, le=850)
    MonthsEmployed: int | None = Field(default=None, ge=0)
    NumCreditLines: int | None = Field(default=None, ge=0)
    InterestRate: float | None = Field(default=None, ge=0, le=100)
    LoanTerm: int | None = Field(default=None, ge=1)
    DTIRatio: float | None = Field(default=None, ge=0, le=1)

    Education: Literal["High School", "Bachelor's", "Master's", "PhD"] | None = None
    EmploymentType: Literal["Unemployed", "Part-time", "Self-employed", "Full-time"] | None = None
    MaritalStatus: Literal["Single", "Married", "Divorced"] | None = None
    HasMortgage: Literal["Yes", "No"] | None = None
    HasDependents: Literal["Yes", "No"] | None = None
    LoanPurpose: Literal["Auto", "Business", "Education", "Home", "Other"] | None = None
    HasCoSigner: Literal["Yes", "No"] | None = None


class PredictionResponse(BaseModel):
    prediction: int
    prediction_label: str
    default_probability: float
    risk_category: str