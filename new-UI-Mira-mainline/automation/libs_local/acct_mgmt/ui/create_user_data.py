"""
Create user data template
"""
from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils

rand = RandomGenUtils.random_string_of_chars(7)


class CreateUserData:
    email = f"some+{rand}@mail.com"
    password = "Placeholder1!"
    first_name = f"{rand} firstname"
    last_name = f"{rand} lastname"
    business_name = rand
    description = f"{rand} description"
    street_address = f"{rand} street"
    street_address2 = f"{rand}2 street"
    city_name = f"{rand.capitalize()} city"
    state_or_province = "ca"
    postal_code = RandomGenUtils.random_string_of_chars(5, lowercase=False,
                                                        uppercase=False, digits=True)
    country = "United States"
    language = "English"
    time_zone = "Pacific Time"
    phone_number = "111-111-1111"


class CheckEligibilityData:
    nmservice = 'YES'
    device = 'Network as a Service'
    country = 'American Samoa'
    location = 'Single Geo'
    network_count = RandomGenUtils.random_string_of_chars(
        2, lowercase=False, uppercase=False, digits=True)
    mail_id = f"some+{rand}@gmail.com"


class UserPreferencesData:
    """
    Userpreference default options
    """
    language: str = 'English'
    timeout: str = '5'
