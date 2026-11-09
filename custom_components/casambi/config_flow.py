"""
Config flow for Casambi integration
"""

import asyncio
import logging
from typing import Any, Dict, Optional

import aiohttp
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries, core
from homeassistant.const import (
    CONF_EMAIL,
    CONF_API_KEY,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)
import voluptuous as vol

from aiocasambi.helper import Helper
from aiocasambi.errors import AiocasambiException

from .const import (
    DOMAIN,
    CONF_NETWORK_PASSWORD,
)

_LOGGER = logging.getLogger(__name__)

_PASSWORD_SELECTOR = TextSelector(TextSelectorConfig(type=TextSelectorType.PASSWORD))


class InvalidAuth(Exception):
    """Casambi rejected the API key, email or network password."""


class CannotConnect(Exception):
    """The Casambi cloud could not be reached."""


async def validate_network_login(
    email: str, api_key: str, network_password: str, hass: core.HomeAssistant
) -> None:
    """Log in to the Casambi network, raising if that is not possible."""
    session = async_get_clientsession(hass)
    helper = Helper(email=email, api_key=api_key, websession=session)

    try:
        valid = await helper.test_network_password(password=network_password)
    except (AiocasambiException, aiohttp.ClientError, asyncio.TimeoutError) as err:
        raise CannotConnect from err

    if not valid:
        raise InvalidAuth


class CasambiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow using the network login, like the Homebridge plugin."""

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            try:
                await validate_network_login(
                    user_input[CONF_EMAIL],
                    user_input[CONF_API_KEY],
                    user_input[CONF_NETWORK_PASSWORD],
                    self.hass,
                )
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except CannotConnect:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title="Casambi", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): cv.string,
                    vol.Required(CONF_EMAIL): cv.string,
                    vol.Required(CONF_NETWORK_PASSWORD): _PASSWORD_SELECTOR,
                }
            ),
            errors=errors,
        )
