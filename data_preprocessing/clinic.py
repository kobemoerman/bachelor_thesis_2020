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
    regex  = '^\d*.000000-RTstructCTsim-CTPET-CT-\d*$'

    outlier = [54, 58, 64]

class clinic_CHUS:
    size = 102

    prefix = '/HN-CHUS-{:03d}'
    regex  = 'Pinnacle (ROI|POI)-\d*$'

    outlier = [90]

class clinic_HGJ:
    size = 92

    prefix = '/HN-HGJ-{:03d}'
    regex  = '^\d*.000000-RTstructCTsim-CTPET-CT-\d*$'

    outlier = []

class clinic_HMR:
    size = 41

    prefix = '/HN-HMR-{:03d}'
    regex  = '^\d*.000000-RTstructCTsim-CTPET-CT-\d*$'

    outlier = []

