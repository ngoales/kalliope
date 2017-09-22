from kalliope.core.Utils.Utils import Utils

class UserKeyDoesNotExists(Exception):
    pass


class User(object):


    def __init__(self, dico):
        self.dict = dico
        self.identities = self.__initIdentities()


    def __initIdentities(self):
        """
        Get the synapse, using its synapse name, from the synapse list
        :return: All know identities of user
        :rtype: Dict
        """
        identities = list()
        identities.append(Utils.encode_text_utf8(self.get("name").lower()))
        if "akas" in self.dict :
            for aka in self.get("akas"):
                identities.append(Utils.encode_text_utf8(aka.lower()))
        return identities


    def get(self, key):
        """
        Get value of key
        :param key: the key to get
        :type key: str
        """
        if key not in self.dict:
            raise UserKeyDoesNotExists("User key %s not exists in user model" % key)
        return self.dict[key]
