def form_select_format(l):
    # insert a blank at the beginning
    l.insert(0,"")
    # format for form.select option is [{'value':"var1"},{'value':"var2"}...]
    return [{'value': k} for k in l]

# resources 
def format():
    return ["Data Dictionary", "CSV", "ASCII", "STATA", "SQL", "PDF", "SAS", "XML", "word doc", 
           "excel", "TXT", "TAB", "JSON"] #+other
def storage_location():
    return ["Research Server", "SQLServer", "Postgres", "MS Access", "Z Drive", "SES",
            "RightNow"] #+other
def sensitivity_level():
    a = ["Public", "Low", "Medium", "High"]
    return form_select_format(a)
def file_sizes():
    a = ["<500 MB","501-1,000 MB","1001-10,000 MB",">10,000 MB"]
    return form_select_format(a)
def update_size():
    return file_sizes()
def approximate_total_size():
    return file_sizes()
def resource_type():
    a = ["Canonical","Extract","Documentation","Data Dictionary","Other"]
    return form_select_format(a)

# datasets
def legal_authority_for_collection():
    return ["Market Monitoring", "Supervision", "Enforcement", "Consumer Response"]
def privacy_pia_title():
    return ["CFPB Business Intelligence Tool",
            "Certain Supervision, Enforcement, and Fair Lending Data used for Market Research",
            "Civil Penalty Fund PIA",
            "Compliance Analysis Toolkit (CAT) PIA",
            "Consumer Education PIA ",
            "Consumer Experience Research PIA ",
            "Consumer Response PIA",
            "Consumerfinance.gov PIA",
            "Directory Database System PIA",
            "Extranet PIA",
            "Freedom of Information Act/Privacy Act System",
            "HUD Counselor Tool PIA",
            "Industry, Expert, and Community Input and Engagement PIA",
            "Litigation and Investigation Support Toolset (LIST) PIA",
            "Market Analysis of Administrative Data Under Research Authorities PIA",
            "Market Research in the Field PIA ",
            "Matters Management System (MMS) PIA",
            "MMS October 2012 update",
            "Nationwide Mortgage Licensing System & Registry PIA",
            "Republication of the Home Mortgage Disclosure Act Public Use Dataset",
            "Scheduling and Examination System (SES) PIA",
            "SES November 2012 update",
            "N/A",]
def privacy_sorn_number():
    return ["CFPB.001 - Freedom of Information Act/Privacy Act System",
            "CFPB.002 - Depository Institution Supervision Database",
            "CFPB.003 - Non-Depository Institution Supervision Database",
            "CFPB.004 - Enforcement Database",
            "CFPB.005 - Consumer Response Database",
            "CFPB.006 - Social Networks and Citizen Engagement",
            "CFPB.007 - Directory Database",
            "CFPB.008 - Transit Subsidy",
            "CFPB.009 - Employee Administrative Records",
            "CFPB.010 - Ombudsman System",
            "CFPB.011 - Correspondence Tracking Database",
            "CFPB.012 - Interstate Land Sales Registration Files (ILS)",
            "CFPB.013 - External Contact Database",
            "CFPB.014 - Direct Registration and User Management System (DRUMS)",
            "CFPB.015 - Ethics Program Records",
            "CFPB.016 - CFPB Advisory Boards and Committees",
            "CFPB.017 - Small Business Review Panels and Cost of Credit Consultations",
            "CFPB.018 - CFPB Litigation Files",
            "CFPB.019 - Nationwide Mortgage Licensing System & Registry (NMLS)",
            "CFPB.020 - Site Badge and Visitor Management System",
            "CFPB.021 - Consumer Education and Engagement Records",
            "CFPB.022 - Market and Consumer Research Records",
            "CFPB.023 - Prize Competitions Program Records",
            "CFPB.024 - Judicial and Administrative Filings Collection",
            "CFPB.025 - Civil Penalty Fund and Bureau-Administered Redress Program Records",
            "CFPB.026 - Biographies",
            "Government-wide",
            "N/A",]
def relevant_governing_documents():
    return ["Contract", "MOU", "NDA", "Interagency Agreement", "Other"] 
def content_spatial():
    return [""]
def frequency_standards():
#http://dublincore.org/groups/collections/frequency/
    a=["Triennial", "Biennial","Annual",
       "Semiannual","Three times a year","Quarterly","Bimonthly","Monthly", 
       "Semimonthly","Biweekly","Three times a month","Weekly",
       "Semiweekly","Three times a week","Daily",
       "Continuous","Irregular",]
    # want shorter options first
    a.reverse() 
    return form_select_format(a)
def content_periodicity():
    return frequency_standards()
def update_frequency():
    return frequency_standards()
def acquisition_method():
    return ["commercial purchase", "custom purchase", "public download", 
            "received from government agency", "received from third party", 
            "complaint database", "direct collection", "supervision examination", 
            "enforcement investigation", "mandatory collection through order",]
def pra_exclusion():
    return ["5 C.F.R. 1320.3(h)(1)",
            "5 C.F.R. 1320.3(h)(2)",
            "5 C.F.R. 1320.3(h)(3)",
            "5 C.F.R. 1320.3(h)(4)",
            "5 C.F.R. 1320.3(h)(5)",
            "5 C.F.R. 1320.3(h)(6)",
            "5 C.F.R. 1320.3(h)(7)",
            "5 C.F.R. 1320.3(h)(8)",
            "5 C.F.R. 1320.3(h)(9)",
            "5 C.F.R. 1320.3(h)(10)",
            "N/A",]
def privacy_pia_notes():
    return ["PIA Published", "No PIA - No PII", "No PIA - Only Employee PII", 
            "No PIA - All PII Aggregated"]
def transfer_method():
    a=["Website", "SFTP", "FTP", "Physical Media", "Email", "Connect Direct", "Other"]
    return form_select_format(a)
