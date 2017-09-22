
from kalliope.core.ConfigurationManager.UserLoader import UserLoader
from kalliope.core.Utils.Utils import Utils
from kalliope.core.ConfigurationManager.SettingLoader import SettingLoader

class NoContextUser(Exception):
    pass

class UserContext :
    current_user = None

    @classmethod
    def getUser(cls):
        return cls.current_user


    @classmethod
    def setUser(cls, user):
        cls.current_user = user


    @classmethod
    def getUserByIdentity(cls, identity):
        user = None
        for u in UserLoader().list():
            if identity.lower() in u.identities:
                user = u
                break
        return user


    @classmethod
    def getNeuronParameter(cls, neuron_name, user=None):
        user = user or cls.current_user
        if user is None:
            return None

        user_parameters = user.get('neurons_parameters')
        neuron_name = neuron_name.lower()
        if neuron_name not in user_parameters:
            return None

        return user_parameters[neuron_name]



    @classmethod
    def getTTS(cls):
        if cls.getUser() is None:
            cls.setUser( UserLoader().getUser(0) )
            Utils.print_danger("Ne pas passer en admin quand pas d'utilisateur")
        return cls.current_user.get('tts')

    @classmethod
    def getSecurityLevel(cls):
        return cls.current_user.get('security_level')

    @classmethod
    def isGranted(cls, synapse):
        settings = SettingLoader().settings
        policy = settings.security_policy

        # if pass_all continu immediatly
        if( policy == "pass_all"):
            return True

        can_execute = False
        if synapse.security_level < 0 or cls.getSecurityLevel() >= synapse.security_level:
            can_execute = True

        return can_execute
