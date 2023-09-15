import os
import datetime
import string
import random
import urllib3
import logging

log = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# TODO: Refactor: remove "AOP_Random_Utils" and its methods after replacing their calls (in tests and other lib-modules)
# by corresponding methods from "RandomGenUtils" class below (GLCP-36232)
class AOP_Random_Utils:
    """
    Helper functions for AOP libs
    """

    def __init__(self):
        pass

    def generate_random_alphanumeric_string(self, length_of_random_string=7):
        """

        :rtype: string
        :type length_of_random_string: int
        """
        # using random.choices()
        # generating random strings
        random_string_suffix = ''.join(random.choices(string.ascii_uppercase +
                                                      string.digits, k=length_of_random_string))
        # print result
        # print("\nThe generated random string : {}\n".format(random_string_suffix))
        return random_string_suffix

    def generate_random_numeric_string(self, length_of_random_string=5):
        """
        Generates a random string of digits of the specified length.
        :param length_of_random_string: number of digits to generate in string
        :return: a string of randomly generated digits
        """
        return ''.join(random.choices(string.digits, k=length_of_random_string))

    def generate_random_MAC_address(self, mac_prefix="00:00:00"):
        """

        :return: random MAC address starting with 24 bit mac_prefix specified
        :rtype: string
        """
        # Randomize the NIC bits for MAC
        local_mac_random = mac_prefix + ":%02x:%02x:%02x" % (
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return local_mac_random.upper()


class RandomGenUtils:
    """Helper methods for generating random data."""

    @staticmethod
    def random_string_of_chars(length=7, lowercase=True, uppercase=False, digits=False):
        """Generate text string with specified length and set of ascii-characters.

        Args:
            length: int - length of string to be generated
            lowercase: bool - include lowercase into source of characters for generated string
            uppercase: bool - include uppercase into source of characters for generated string
            digits: bool - include digits into source of characters for generated string

        Returns:
            str - string of randomly generated characters with requested length and set of characters
        """

        if not any([lowercase, uppercase, digits]):
            raise ValueError("At least one set of characters should be selected: lowercase, uppercase or digits")
        charset = ""
        if lowercase:
            charset += string.ascii_lowercase
        if uppercase:
            charset += string.ascii_uppercase
        if digits:
            charset += string.digits
        return "".join(random.choices(charset, k=length))

    @staticmethod
    def generate_random_MAC_address(mac_prefix="00:00:00"):
        """Generate random MAC-address starting with specified prefix.

        Args:
            mac_prefix: str - starting prefix of resulted MAC-address

        Returns:
            str - generated MAC-address as text
        """

        # Randomize the NIC bits for MAC
        local_mac_random = mac_prefix + ":%02X:%02X:%02X" % (
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return local_mac_random
