"""
functions to get data from the PubMed API
"""

import os
import json
import xml.etree.ElementTree as ET
from math import ceil
import requests
from Bio import Entrez
from pharmatools.helpers import get_disease_term


def get_pubmed_data(drug, disease, date):
    """
    combination of helper functions to get titles and abstracts
    from PubMed
    """

    ids = get_pubmed_ids(drug, disease, date)
    if ids is None:
        return None
    return get_abstracts(ids), len(ids)


def get_pubmed_ids(drug, disease, date):
    """
    gets IDs of articles on a drug/disease combination from
    PubMed API
    """
    # setting user parameters for PubMed API
    Entrez.api_key = os.getenv("PUBMED_API_KEY")
    Entrez.email = os.getenv("PUBMED_EMAIL")

    disease = get_disease_term(disease)
    date_str = date.strftime("%Y/%m/%d")

    search_term = f'({drug}) AND ({disease}) \
                  AND (("1900/01/01"[Date - Publication] : "{date_str}"[Date - Publication]))'

    handle = Entrez.esearch(
        db="pubmed", retmax=100_000, term=search_term, sort="relevance", retmode="json"
    )
    result = json.load(handle)
    handle.close()

    try:
        ids = result["esearchresult"]["idlist"]
    except KeyError:
        print("esearchresult not found")
        return None
    return ids


def get_abstracts(ids):
    """
    gets abstracts in form of one text element for all
    IDs in a list
    """
    # setting user parameters for PubMed API
    Entrez.api_key = os.getenv("PUBMED_API_KEY")
    Entrez.email = os.getenv("PUBMED_EMAIL")

    handle = Entrez.efetch(db="pubmed", id=ids, rettype="abstract", retmode="text")
    result = handle.read()
    return result


def split_into_batches(ids):
    """
    divides a list of IDs into batches of max size 200
    as this is the max of IDs the PubMed abstracts API
    can handle at a time
    """

    # split task to max size of 200
    list_size = len(ids)
    batches = []

    if list_size > 200:
        n_batches = ceil(list_size / 200)

        for batch in range(n_batches):
            batches.append(ids[batch + (batch * 200) : 200 + (batch * 200)])
    else:
        batches.append(ids)

    return batches


def get_titles_abstracts(ids):
    """
    returns the titles and abstracts of all IDs
    from PubMed
    """

    batches = split_into_batches(ids)

    titles = []
    abstracts = []

    for batch in batches:
        batch_titles, batch_abstracts = get_titles_abstracts_batch(batch)
        titles = titles + batch_titles
        abstracts = abstracts + batch_abstracts

    return titles, abstracts


def get_titles_abstracts_batch(batch):
    """
    IF POSSIBLE USE FUNCTIONS ABOVE AS THEY USE
    THE ENTREZ PACKAGE
    gets titles and abstracts from PubMed given
    one batch of IDs of max size 200
    EMAIL needs to be set as an environment variable
    """

    user_email = os.getenv("PUBMED_EMAIL")

    # make API call to get article data
    params = {"db": "pubmed", "id": batch, "email": user_email, "rettype": "xml"}
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    response = requests.get(base_url + "efetch.fcgi", params=params)

    # handle result in form of XML
    root = ET.fromstring(response.content)

    batch_titles = []
    for title in root.iter("ArticleTitle"):
        title_content = ""
        try:
            title_content += title.text
        except TypeError:
            print("no title")
        batch_titles.append(title_content)

    batch_abstracts = []
    for abstract in root.iter("Abstract"):
        abstract_content = ""
        for abstract_pg in abstract.findall("AbstractText"):
            try:
                abstract_content += abstract_pg.text
            except TypeError:
                print("no abstract")
        batch_abstracts.append(abstract_content)

    return batch_titles, batch_abstracts
