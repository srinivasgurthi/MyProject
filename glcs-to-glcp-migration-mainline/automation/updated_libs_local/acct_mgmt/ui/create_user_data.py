"""
Create user data template
"""
from dataclasses import dataclass, field, InitVar

from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils


@dataclass
class CreateUserData:
    rand: InitVar[str] = RandomGenUtils.random_string_of_chars(7)
    email: str = field(init=False, default=f"some+{rand}@mail.com")
    password: str = field(init=False, default="Placeholder1!")
    first_name: str = field(init=False, default=f"{rand} firstname")
    last_name: str = field(init=False, default=f"{rand} lastname")
    business_name: str = field(init=False, default=rand)
    description: str = field(init=False, default=f"{rand} description")
    street_address: str = field(init=False, default=f"{rand} street")
    street_address2: str = field(init=False, default=f"{rand} street2")
    city_name: str = field(init=False, default=f"{rand.capitalize()} city")
    state_or_province: str = field(init=False, default="ca")
    postal_code: str = field(
        init=False,
        default=RandomGenUtils.random_string_of_chars(
            5, lowercase=False, uppercase=False, digits=True
        ),
    )
    country: str = field(init=False, default="United States")
    language: str = field(init=False, default="English")
    time_zone: str = field(init=False, default="Pacific Time")
    phone_number: str = field(init=False, default="111-111-1111")

    def __post_init__(self, rand):
        self.email: str = f"some+{rand}@mail.com"
        self.first_name: str = f"{rand} firstname"
        self.last_name: str = f"{rand} lastname"
        self.business_name: str = rand
        self.description: str = f"{rand} description"
        self.street_address: str = f"{rand} street"
        self.street_address2: str = f"{rand} street2"
        self.city_name: str = f"{rand.capitalize()} city"


@dataclass
class CheckEligibilityData:
    rand: InitVar[str] = RandomGenUtils.random_string_of_chars(7)
    nmservice: str = field(init=False, default="YES")
    device: str = field(init=False, default="Network as a Service")
    country: str = field(init=False, default="American Samoa")
    location: str = field(init=False, default="Single Geo")
    network_count: int = field(
        init=False,
        default=RandomGenUtils.random_string_of_chars(
            2, lowercase=False, uppercase=False, digits=True
        ),
    )
    mail_id: str = field(init=False, default=f"some+{rand}@gmail.com")

    def __post_init__(self, rand):
        self.mail_id = f"some+{rand}@gmail.com"


@dataclass
class UserPreferencesData:
    """
    Userpreference default options
    """

    language: str = "English"
    timeout: str = "5"
