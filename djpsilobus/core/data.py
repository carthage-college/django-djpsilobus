# Divisions
DIVISIONS = {
    "ACPR":"All College Programs",
    "ARHU":"Arts and Humanities",
    "NSSS":"Natural and Social Science",
    "PRST":"Professional Studies"
}
# Departments
DEPARTMENTS = {
    "ACC":"229", #Accounting
    "ART":"209", #Art
    "ARH":"210", #Art History
    "ASN":"212", #Asian Studies Program
    "_ASN":"212", #Asian Studies Program
    "ATH":"215", #Athletic Training
    "_ATH":"215", #Athletic Training
    "BIO":"214", #Biology
    "BUS":"216", #Business Administration
    "CHM":"217", #Chemistry
    "CHN":"208", #Chinese
    "CLS":"226", #Classics
    "CDM":"219", #Communication Digital Media
    "CSC":"204", #Computer Science
    "CONF":"Conference",
    "ADUL":"Continuing Studies",
    "CRJ":"220", #Criminal Justice Program
    "_CRJ":"220", #Criminal Justice Program
    "DIS":"Discovery Program",
    "_DIS":"Discovery Program",
    "ECN":"221", #Economics
    "EDU":"222", #Education
    "ENG":"223", #English
    "ENRC":"Enrichment",
    "ENV":"224", #Environmental Science
    "_ENV":"224", #Environmental Science
    "EXS":"225", #Exercise and Sport Science
    "FIN":"230", #Finance
    "FAC":"Finance and Accounting", # Sub-Community
    "FRN":"205", # French
    "GNR":"261",
    "_GNR":"261",
    "GEO":"231", #Geography and Earth Science
    "GRM":"232", #German
    "GBL":"233", #Global Heritage Program
    "_GBL":"233", #Global Heritage Program
    "GRK":"227", #Greek
    "GFW":"234", #Great Ideas Program
    "_GFW":"234", #Great Ideas Program
    "HIS":"235", #History
    "HON":"236", #Honors Program
    "_HON":"236", #Honors Program
    "IPE":"237", #International Political Economy
    "_IPE":"237", #International Political Economy
    "JPN":"206", # Japanese
    "LTN":"228", #Latin
    "MGT":"239", #Management
    "MKT":"238", #Marketing
    "MMK":"Management and Marketing", # Sub-Community
    "MTH":"202", #Mathematics
    "MLA":"207", #Modern Languages
    "MUS":"240", #Music
    "NEU":"241", #Neuroscience Program
    "_NEU":"241", #Neuroscience Program
    "NSG":"242", #Nursing
    "NUR":"242", #Nursing
    "PEH":"243", #Physical Education/Health Program
    "_PEH":"243", #Physical Education/Health Program
    "PARA":"Paralegal Program",
    "PHL":"244", #Philosophy
    "PHY":"203", #Physics/Astronomy
    "POL":"245", #Political Science
    "PYC":"246", #Psychological Science
    "REL":"247", #Religion
    "ESN":"Science Works Program",
    "_ESN":"Science Works Program",
    "SSC":"248", #Social Science Program
    "_SSC":"248", #Social Science Program
    "SWK":"249", #Social Work
    "SOC":"250", #Sociology
    "SPN":"201", # Spanish
    "THR":"251", #Theatre
    "COR":"252", #Western Heritage Program
    "WHE":"252", #Western Heritage Program
    "_WHE":"252", #Western Heritage Program
    "WMG":"253", #Women and Gender Studies
    "_WMG":"253" #Women and Gender Studies
}
# each name maps to a value that should be used as the Department code
# e.g. FRN (French) is an MLA (Modern Languages) Department
DEPARTMENT_EXCEPTIONS = {
    'ESN':'_ESN','MGT':'MMK','ARH':'ART','JPN':'MLA','FRN':'MLA','GRM':'MLA',
    'SPN':'MLA','CHN':'MLA','MKT':'MMK','GRK':'CLS','LTN':'CLS','IPE':'_IPE',
    'ACC':'FAC','FIN':'FAC','SSC':'_SSC','ASN':'_ASN','NEU':'_NEU','NSG':'NUR',
    'DIS':'_DIS','GFW':'_GFW','WHE':'_WHE','WMG':'_WMG','PEH':'_PEH',
    'GBL':'_GBL','CRJ':'_CRJ','ATH':'_ATH','COR':'_WHE','GNR':'_GNR',
    'DNC','THR'
}
# metadata for creating a new item in a collection
ITEM_METADATA = {
    "metadata":[
        {
            "key": "dc.contributor.author",
            "value": ""
        },
        {
            "key": "dc.description",
            "language": "en_US",
            "value": ""
        },
        {
            "key": "dc.title",
            "language": "en_US",
            "value": ""
        },
        {
            "key": "dc.title.alternative",
            "language": "en_US",
            "value": ""
        },
        {
            "key": "dc.subject",
            "language": "en_US",
            "value": ""
        },
        {
            "key": "dc.subject",
            "language": "en_US",
            "value": ""
        }
    ]
}

HEADERS = [
    'Course Number',
    'Catelog Year',
    'Year',
    'Session',
    'Section',
    'Sub-Session',
    'Course Title',
    'Section Title',
    'Faculty ID',
    'Faculty First name',
    'Faculty Lastname',
    'Faculty Full Name',
    'Needs Syllabus',
    'Status'
]
