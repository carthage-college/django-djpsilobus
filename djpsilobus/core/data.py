# -*- coding: utf-8 -*-

DIVISIONS = {
    'ACPR': 'All College Programs',
    'ARHU': 'Arts and Humanities',
    'NSSS': 'Natural and Social Science',
    'PRST': 'Professional Studies',
}
DEPARTMENTS = {
    'ACC': '8cc10fa7-35b6-48b5-8855-e913980bc384',   # Accounting
    'ART': 'b405e986-37f6-42cc-98de-8a3ee616491c',   # Art
    'ARH': '50eee7a8-0a1b-425f-89c1-63b0d2ff7d7b',   # Art History
    'ASN': 'a522e68e-9c37-443c-ac17-eeb1a36653fd',   # Asian Studies Program
    '_ASN': 'a522e68e-9c37-443c-ac17-eeb1a36653fd',  # Asian Studies Program
    'ATH': 'c2b83624-122c-42b6-92eb-cf876c95ca7f',   # Athletic Training
    '_ATH': 'c2b83624-122c-42b6-92eb-cf876c95ca7f',  # Athletic Training
    'BIO': '3b62cbb5-a0b7-4d55-a0ae-f48b480b8eca',   # Biology
    'BUS': '3b00e318-8be7-4f1a-8a82-bc3e923ed682',   # Business Administration
    'CHM': '918a6978-26a4-4b27-b717-4f146b2da173',   # Chemistry
    'CHN': 'f2701464-3fcd-4110-8efb-70932bae8104',   # Chinese
    'CLS': 'fe40404d-7dc9-4199-8b65-ec3d96dcd8e6',   # Classics
    'CDM': '069a94b7-1d14-458a-8167-34e9e8219a09',   # Comms Digital Media
    'CSC': '50b4d81f-8546-4188-993d-2ff580b65c3a',   # Computer Science
    'CONF': 'Conference',                            # Conference
    'ADUL': 'Continuing Studies',                    # Continuing Studies
    'CRJ': 'd9d0f474-c5b3-44cd-a61b-98e8b4bb909b',   # Criminal Justice Program
    '_CRJ': 'd9d0f474-c5b3-44cd-a61b-98e8b4bb909b',  # Criminal Justice Program
    'DIS': 'Discovery Program',                      # Discovery Program
    '_DIS': 'Discovery Program',                     # Discovery Program
    'DNC': 'b8fc6ec1-3269-4ab2-bf36-dcdf8f1d6b1c',   # Dance
    'ECN': 'f17a0469-7407-4871-8e42-88095fe666d8',   # Economics
    'EDU': '17b90ea0-efaa-4eac-b37c-0bb30e4a5267',   # Education
    'EDUC': '17b90ea0-efaa-4eac-b37c-0bb30e4a5267',  # Education
    'ENG': '26028861-1bbd-4508-b87b-e2644db6c5ff',   # English
    'ENRC': 'Enrichment',                            # Enrichment
    'ENV': 'b49790d1-a0e3-4fe2-86da-6a525ab84207',   # Environmental Science
    '_ENV': 'b49790d1-a0e3-4fe2-86da-6a525ab84207',  # Environmental Science
    'EXS': '17c0b1cb-3a61-42a3-a80c-7e4dfe61d44b',   # Exercise & Sport Science
    'AHS': '17c0b1cb-3a61-42a3-a80c-7e4dfe61d44b',   # Allied Health Science (major in EXS department)
    'FAC': 'Finance and Accounting',                 # Sub-Community
    'FAR': 'b405e986-37f6-42cc-98de-8a3ee616491c',   # Fine Arts
    'FIN': 'dbb13442-673d-46b3-8d41-5ac2684607a8',   # Finance
    'FRN': 'e377322f-7764-480b-bb60-1a4433334ee6',   # French
    'GNR': 'b5efeda1-42be-4445-a012-b017d6f01cf7',   # General
    '_GNR': 'b5efeda1-42be-4445-a012-b017d6f01cf7',  # General
    'GEO': '6a88c727-8955-4872-aa26-82667c115878',   # Geo and Earth Science
    'GRM': '5c2fbfeb-328c-46d4-be6e-a95d970239f4',   # German
    'GBL': 'a97cfedb-8ab6-4f9c-aabb-1a1672cb51ac',   # Global Heritage Program
    '_GBL': 'a97cfedb-8ab6-4f9c-aabb-1a1672cb51ac',  # Global Heritage Program
    'GRK': 'd9601907-466d-4a58-9be2-c4d2d49184eb',   # Greek
    'GFW': 'a1cc2e00-12d9-47f4-9c31-88374e94a050',   # Great Ideas Program
    '_GFW': 'a1cc2e00-12d9-47f4-9c31-88374e94a050',  # Great Ideas Program
    'HIS': '21b3c2fc-1588-4051-82e1-614cb17589ba',   # History
    'HON': 'a61dfb67-a8ec-4e4e-b7b7-f694ede5dec7',   # Honors Program
    '_HON': 'a61dfb67-a8ec-4e4e-b7b7-f694ede5dec7',  # Honors Program
    'IPE': '6f0f5e5b-555b-40c3-9d62-01dbf1e5084a',   # Internat Political Econ
    '_IPE': '6f0f5e5b-555b-40c3-9d62-01dbf1e5084a',  # Internat Political Econ
    'JPN': '29b88efe-832c-4436-b987-29de099ca154',   # Japanese
    'LTN': '00bd264c-2ecc-467e-98b6-dcb02e9f3642',   # Latin
    'MGT': 'c75726ee-14c7-420b-bed5-10a43e28cd5c',   # Management
    'MKT': '0f7b06c2-d33f-48e2-8134-f0bae00fa22a',   # Marketing
    'MMK': 'Management and Marketing',               # Sub-Community
    'MTH': 'a3f8696c-46a6-46b6-b20a-2a59feec7fde',   # Mathematics
    'MLA': '82291575-11f4-4942-9a88-2740e627d6e7',   # Modern Languages
    'MUS': '05c999b6-5c68-48fe-9d86-c57b32c1b4e9',   # Music
    'NAT': 'b5efeda1-42be-4445-a012-b017d6f01cf7',   # General
    'NEU': 'aec2533e-233c-4105-bc58-0b4f651d1db1',   # Neuroscience Program
    '_NEU': 'aec2533e-233c-4105-bc58-0b4f651d1db1',  # Neuroscience Program
    'NSG': '03ffb510-6249-447c-8301-dfd3c47b43ca',   # Nursing
    'NUR': '03ffb510-6249-447c-8301-dfd3c47b43ca',   # Nursing
    'PHL': 'd82b9819-13a0-4336-b9ef-2155004e334b',   # Philosophy
    'PEH': '51486552-ecdf-47ba-aceb-d5797048e63f',   # Physical Education/Health
    '_PEH': '51486552-ecdf-47ba-aceb-d5797048e63f',  # Physical Education/Health
    'PARA': 'Paralegal Program',                     # Paralegal
    'PHY': 'f9187381-7681-42e4-b6fe-787a4a421942',   # Physics/Astronomy
    'POL': '9c67a056-2d6e-4d4e-9401-28c712070646',   # Political Science
    'PYC': '0cf20934-7eef-484e-ba99-9a9697688e00',   # Psychological Science
    'REL': '2fa71e84-901f-488e-8cc5-ef5b3ac0ad59',   # Religion
    'ESN': 'Science Works Program',                  # Science Works
    '_ESN': 'Science Works Program',                 # Science Works
    'SSC': '5bc1aa3d-3e90-40d4-9297-64262acf2dd7',   # Social Science Program
    '_SSC': '5bc1aa3d-3e90-40d4-9297-64262acf2dd7',  # Social Science Program
    'SWK': 'ce018c9c-a31b-4482-9d51-c9f23f064b21',   # Social Work
    'SOC': '4535df0e-f074-4dd0-81d9-d9e8825446b4',   # Sociology
    'SPN': 'fa5f7801-1847-4765-ba23-39ab59133777',   # Spanish
    'THR': 'b8fc6ec1-3269-4ab2-bf36-dcdf8f1d6b1c',   # Theatre
    'COR': '88cc91a4-8004-4513-8446-7b12ee1becde',   # Western Heritage Program
    'WHE': '88cc91a4-8004-4513-8446-7b12ee1becde',   # Western Heritage Program
    '_WHE': '88cc91a4-8004-4513-8446-7b12ee1becde',  # Western Heritage Program
    'WMG': 'd0492ec0-13ab-417e-9605-a2ded69200cc',   # Women and Gender Studies
    '_WMG': 'd0492ec0-13ab-417e-9605-a2ded69200cc',  # Women and Gender Studies
}

# each name maps to a value that should be used as the Department code
# e.g. FRN (French) is an MLA (Modern Languages) Department
DEPARTMENT_EXCEPTIONS = {
    'AHS': 'EXS',
    'ESN': '_ESN',
    'EDUC': 'EDU',
    'MGT': 'MMK',
    'ARH': 'ART',
    'JPN': 'MLA',
    'FRN': 'MLA',
    'GRM': 'MLA',
    'SPN': 'MLA',
    'CHN': 'MLA',
    'MKT': 'MMK',
    'GRK': 'CLS',
    'LTN': 'CLS',
    'IPE': '_IPE',
    'ACC': 'FAC',
    'FIN': 'FAC',
    'SSC': '_SSC',
    'ASN': '_ASN',
    'NEU': '_NEU',
    'NSG': 'NUR',
    'DIS': '_DIS',
    'GFW': '_GFW',
    'WHE': '_WHE',
    'WMG': '_WMG',
    'PEH': '_PEH',
    'GBL': '_GBL',
    'CRJ': '_CRJ',
    'ATH': '_ATH',
    'COR': '_WHE',
    'GNR': '_GNR',
    'DNC': 'THR',
    'ENV': '_ENV',
    'FAR': 'ART',
    'NAT': '_GNR',
}
# metadata for creating a new item in a collection
ITEM_METADATA = {
    'metadata': [
        {
            'key': 'dc.contributor.author',
            'value': '',
        },
        {
            'key': 'dc.description',
            'language': 'en_US',
            'value': '',
        },
        {
            'key': 'dc.title',
            'language': 'en_US',
            'value': '',
        },
        {
            'key': 'dc.title.alternative',
            'language': 'en_US',
            'value': '',
        },
        {
            'key': 'dc.subject',
            'language': 'en_US',
            'value': '',
        },
        {
            'key': 'dc.subject',
            'language': 'en_US',
            'value': '',
        },
    ],
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
    'Status',
]
