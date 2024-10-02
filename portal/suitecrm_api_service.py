from suitepy.suitecrm import SuiteCRM
from suitepy.suitecrm_cached import SuiteCRMCached

class SuiteCRMManager:
    _suitecrm_instance = None
    _suitecrmcached_instance = None

    @classmethod
    def get_suitecrm_instance(cls):
        if cls._suitecrm_instance is None:
            cls._suitecrm_instance = SuiteCRM()
        return cls._suitecrm_instance

    @classmethod
    def get_suitecrmcached_instance(cls):
        if cls._suitecrmcached_instance is None:
            suitecrm_instance = cls.get_suitecrm_instance()
            cls._suitecrmcached_instance = SuiteCRMCached(suitecrm_instance.__dict__)
        return cls._suitecrmcached_instance
