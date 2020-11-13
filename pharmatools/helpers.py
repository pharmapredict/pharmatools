def get_disease_term(disease):
    """
    replaces commas by OR to create a search term
    """
    return disease.replace(", ", " OR ")
