def get_clinic(_inst):
    _dict = {
        'CHUM'  : clinic_CHUM(),
        'CHUS'  : clinic_CHUS(),
        'HGJ'   : clinic_HGJ(),
        'HMR'   : clinic_HMR()
    }

    return _dict.get(_inst)

class clinic_CHUM:
    size = 65

    prefix = '/HN-CHUM-{:03d}'

    dictionary = ['08-27-1885-TomoTherapy Patient Disease',
                  '08-27-1885-ORL C-18582',
                  '08-27-1885-ORL C- ET C-22679',
                  '08-27-1885-AMYGDALE G TOMO C- PROTOCOLE T-09882',
                  '08-27-1885-ORL TOMO C-  TEP-34366',
                  '08-27-1885-ORL IMRT PROT TEP C-05034',
                  '08-27-1885-RESCAN ORL IMRT C--89742']

    outlier = [54, 58, 64]

class clinic_CHUS:
    size = 102

    prefix = '/HN-CHUS-{:03d}'

    regexROI = '08-27-1885-[0-9]*$'
    regexCT  = '1.000000-RTstructCTsim-CTPET-CT-[0-9]*$'

    dictionary = ['08-27-1885-TEP cancerologique',
                  '08-27-1885-ORL-52158',
                  '08-27-1885-OROPHARYNX-81994',
                  '08-27-1885-RT Planning',
                  '08-27-1885-R-ONCO POSITION DE TX FDG TE-',
                  '08-27-1885-Imagerie de planification en radio-oncologie PACS',
                  '08-27-1885-ADENOMEGALIE CERVICALE FDG T-',
                  '08-27-1885-CARCINOME EPIDERMOIDE FDG TE-',
                  '08-27-1885-recherche de metastase fdg t-',
                  '08-27-1885-CA AMYGDALE FDG TEP POSITION-',
                  '08-27-1885-CA AMYGDALE FDG TEP EN POS D-',
                  '08-27-1885-CA LANGUE FDG TEP POSITION T-69772']

    outlier = [9, 26, 31, 37, 40, 43, 44, 46, 52, 54, 57, 58, 68, 72, 79, 81, 89, 90, 98, 101, 102]

class clinic_HGJ:
    size = 92

    prefix = '/HN-HGJ-{:03d}'

    dictionary = ['08-27-1885-L',
                  '08-27-1885-NASOPHARYNX',
                  '08-27-1885-R',
                  '08-27-1885-O',
                  '08-27-1885-H',
                  '08-27-1885-SUPRAGLOTTI',
                  '08-27-1885-CA',
                  '08-27-1885-NASO',
                  '08-27-1885-ENT',
                  '08-27-1885-B',
                  '08-27-1885-TONSIL']

    outlier = [68]

class clinic_HMR:
    size = 41

    prefix = '/HN-HMR-{:03d}'

    dictionary = ['08-27-1885-OROPHARYNX',
                  '08-27-1885-NASOPHARYNX',
                  '08-27-1885-HYPOPHARYNX',
                  '08-27-1885-PHARYNX',
                  '08-27-1885-LARYNX',
                  '08-27-1885-NASOCOU',
                  '08-27-1885-IRM',
                  '08-27-1885-TEP-TETE-COU-18456',
                  '08-27-1885-TEP-TETE COU-48016',
                  '08-27-1885-TEP-TETE-COU-00079',
                  '08-27-1885-TEP TETE ET COU-83970',
                  '08-27-1885-TEP TETE ET COU-95648',
                  '08-27-1885-TEP- TETE COU-33718',
                  '08-27-1885-TEP PANC. SPHERE ORL-04734',
                  '08-27-1885-TEP PANC. SPHERE ORL-24008',
                  '08-27-1885-TEP PANC. SPHERE ORL-75645',
                  '08-27-1885-ACQUISITIONS SUPPLMEN-81475',
                  '08-27-1885-TEP PANC. SPHERE ORL-62304',
                  '08-27-1885-TEP PANC. SPHERE ORL-04821',
                  '08-27-1885-TEP avec synchronistio-26227',
                  '08-27-1885-TEP avec synchronistio-39491',
                  '08-27-1885-TEP PANC. SPHERE ORL-01161',
                  '08-27-1885-ACQUISITIONS SUPPLMEN-76823',
                  '08-27-1885-TEP PANC. SPHERE ORL-19101',
                  '08-27-1885-TEP PANC.  POUMONPLEVRE-50138',
                  '08-27-1885-BASE',
                  '08-27-1885-TEP PANC. OESOPHAGE',
                  '08-27-1885-SPHRE ORL',
                  '08-27-1885-PALAIS MOUCOU BILAT',
                  '08-27-1885-RT Planning',
                  '08-27-1885-ORL',
                  '08-27-1885-AMYGDALE',
                  '08-27-1885-COU']

    outlier = [12]



