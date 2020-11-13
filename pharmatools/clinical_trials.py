"""
functions to interact with the ClinicalTrials.gov API
"""

import requests
from pharmatools.helpers import get_disease_term

BASE_URL = "https://clinicaltrials.gov/api/query/field_values/"


def get_trial_data(drug, disease, date):
    """
    gets information on a drug/disease combination from
    ClinicalTrials.gov API
    """
    params = drug, get_disease_term(disease), date

    n_trials, status = get_trials_total_and_status(*params)
    organizers = get_trials_organizers(*params)
    phases = get_trials_phases(*params)

    trial_data = {
        "n_trials": n_trials,
        "status": status,
        "organizers": organizers,
        "phases": phases,
    }

    return trial_data


def get_ct_response(drug, disease, date, field):
    """
    basic function to query the ClinicalTrials.gov API
    """
    params = {
        "expr": f"({drug}) AND ({disease})",
        "fmt": "json",
        "sfpd_e": date,  # latest date of first post on clinicaltrials.gov, format dd/mm/yyyy
        "field": field,  # OrgClass,Phase
    }

    response = requests.get(BASE_URL, params=params).json()

    return response


def get_trials_total_and_status(drug, disease, date):
    """
    returns the total number of trials and dictionary of the status of trials
    """

    response = get_ct_response(drug, disease, date, "OverallStatus")
    n_studies = response["FieldValuesResponse"]["NStudiesFound"]
    field_values = response["FieldValuesResponse"]["FieldValues"]
    status = {
        "Not yet recruiting": 0,
        "Recruiting": 0,
        "Enrolling by invitation": 0,
        "Active, not recruiting": 0,
        "Suspended": 0,
        "Terminated": 0,
        "Completed": 0,
        "Withdrawn": 0,
        "Unknown status": 0,
    }

    # fill status dictionary
    for value in field_values:
        if value["FieldValue"] == "Not yet recruiting":
            status["Not yet recruiting"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "Recruiting":
            status["Recruiting"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "Enrolling by invitation":
            status["Enrolling by invitation"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "Active, not recruiting":
            status["Active, not recruiting"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "Suspended":
            status["Suspended"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "Terminated":
            status["Terminated"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "Completed":
            status["Completed"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "Withdrawn":
            status["Withdrawn"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "Unknown status":
            status["Unknown status"] = value["NStudiesFoundWithValue"]

    return n_studies, status


def get_trials_organizers(drug, disease, date):
    """
    returns a dictionary with the organizers of trials
    """

    response = get_ct_response(drug, disease, date, "OrgClass")
    field_values = response["FieldValuesResponse"]["FieldValues"]

    organizers = {
        "FED": 0,
        "INDIV": 0,
        "INDUSTRY": 0,
        "NETWORK": 0,
        "NIH": 0,
        "OTHER": 0,
        "OTHER_GOV": 0,
    }

    # fill status dictionary
    for value in field_values:
        if value["FieldValue"] == "FED":
            organizers["FED"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "INDIV":
            organizers["INDIV"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "INDUSTRY":
            organizers["INDUSTRY"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "NETWORK":
            organizers["NETWORK"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "NIH":
            organizers["NIH"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "OTHER":
            organizers["OTHER"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "OTHER_GOV":
            organizers["OTHER_GOV"] = value["NStudiesFoundWithValue"]

    return organizers


def get_trials_phases(drug, disease, date):
    """
    returns a dictionary of trials phases
    """

    response = get_ct_response(drug, disease, date, "Phase")
    field_values = response["FieldValuesResponse"]["FieldValues"]

    phases = {
        "Early Phase 1": 0,
        "Not Applicable": 0,
        "Phase 1": 0,
        "Phase 2": 0,
        "Phase 3": 0,
        "Phase 4": 0,
    }

    # fill status dictionary
    for value in field_values:
        if value["FieldValue"] == "Early Phase 1":
            phases["Early Phase 1"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "Not Applicable":
            phases["Not Applicable"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "Phase 1":
            phases["Phase 1"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "Phase 2":
            phases["Phase 2"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "Phase 3":
            phases["Phase 3"] = value["NStudiesFoundWithValue"]
        if value["FieldValue"] == "Phase 4":
            phases["Phase 4"] = value["NStudiesFoundWithValue"]

    return phases
