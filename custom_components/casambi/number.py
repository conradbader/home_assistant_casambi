"""
Number implementation for Casambi, used for the up/down light direction
"""

import logging

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant

from .casambi.CasambiEntity import CasambiEntity
from .const import DOMAIN, CONF_CONTROLLER

_LOGGER = logging.getLogger(__name__)


class CasambiDistributionNumber(NumberEntity, CasambiEntity):
    """Slider for the split between a light's upward and downward output."""

    _attr_icon = "mdi:arrow-up-down"
    _attr_mode = NumberMode.SLIDER
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(self, unit, controller, hass):
        """Initialize the slider."""
        CasambiEntity.__init__(self, unit, controller, hass, "Leuchtrichtung")

    @property
    def native_value(self) -> int:
        """Return the current direction in percent."""
        return round(self.unit.distribution * 100)

    async def async_set_native_value(self, value: float) -> None:
        """Set the direction in percent."""
        await self.unit.set_unit_distribution(distribution=round(value / 100, 2))
        self.schedule_state_update()

    def update_state(self):
        """Update the state after the controller polled the network."""
        self.schedule_state_update()

    def process_update(self, data):
        """Update the state after a websocket message."""
        self.schedule_state_update()


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities
):
    """Add a direction slider for every light that supports it."""
    controller = hass.data[DOMAIN][CONF_CONTROLLER]

    async_add_entities(
        CasambiDistributionNumber(unit, controller, hass)
        for unit in controller.aiocasambi_controller.get_units()
        if unit.is_light() and unit.supports_distribution()
    )

    return True
