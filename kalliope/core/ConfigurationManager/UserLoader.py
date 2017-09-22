import os
from six import with_metaclass
import six
from kalliope.core.Models import Singleton
from kalliope.core.Utils import Utils
from .YAMLLoader import YAMLLoader
from kalliope.core.Models.User import User
from kalliope.core.ConfigurationManager.SettingLoader import SettingLoader

class UserNotFound(Exception):
    pass

class UserKeyForgot(Exception):
    pass

DEFAULT_PATH = "users/"

class UserLoader(with_metaclass(Singleton, object)):

    def __init__(self, path=None):
        path = path or DEFAULT_PATH
        self.path = Utils.get_real_file_path(path, True)
        self.users = self.loadUsers()


    def __createDefaultUser(self):
        users = list()
        settings = SettingLoader().settings
        default_user_dict = dict()
        default_user_dict["name"] = "default_user"
        default_user_dict["pmdl"] = settings.triggers[0].name
        default_user_dict["neurons_parameters"] = list()
        default_user_dict["tts"] = dict()
        default_user_dict["tts"]["name"]        = settings.ttss[0].name
        default_user_dict["tts"]["parameters"]  = settings.ttss[0].parameters
        user = User(default_user_dict)
        users.append(user)
        return users


    def loadUsers(self):
        users = list()
        for file in os.listdir(self.path):
            if file.endswith('.yml'):
                user = self.createUserFromYaml( os.path.join(self.path,file) )
                users.append(user)
        return users


    def createUserFromYaml(self, file):
        user_data = YAMLLoader.get_config(file)
        must_exists = ["security_level", "name"]
        for item in must_exists:
            if item not in user_data:
                raise UserKeyForgot("The key %s for user is compulsory in file %s" % (item, file))
        return User(user_data)


    def list(self):
        return self.users


    def getUser(self, index):
        return self.users[index]
