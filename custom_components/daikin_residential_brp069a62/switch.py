"""Support for Daikin BRP069A61 switches."""
from homeassistant.helpers.entity import ToggleEntity

from .daikin_base import Appliance

from .const import (
    DOMAIN as DAIKIN_DOMAIN,
    DAIKIN_DEVICES,
    DAIKIN_SWITCHES,
    DAIKIN_SWITCHES_ICONS,
    ATTR_STATE_OFF,
    ATTR_STATE_ON,
    MP_CLIMATE,
    MP_DHW_TANK,
    SWITCH_CLIMATE_ONOFF,
)

import logging
_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Old way of setting up the platform.

    Can only be called when a user accidentally mentions the platform in their
    config. But even in that case it would have been ignored.
    """


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Daikin switches."""
    for dev_id, device in hass.data[DAIKIN_DOMAIN][DAIKIN_DEVICES].items():
        switches = DAIKIN_SWITCHES
        for switch in switches:
            if device.support_switch(switch):
                _LOGGER.debug("Daikin Switch Adding: %s", switch)
                async_add_entities([DaikinSwitch(device, switch)])
            

class DaikinSwitch(ToggleEntity):
    """Representation of a switch."""

    def __init__(self, device: Appliance, switch_id: str):
        """Initialize the zone."""
        self._device = device
        self._switch_id = switch_id
        if switch_id in DAIKIN_SWITCHES:
            if switch_id == SWITCH_CLIMATE_ONOFF:
                subname = device.managementPoints[MP_CLIMATE]["name"]["value"]
            else:
                subname = device.managementPoints[MP_DHW_TANK]["name"]["value"]
            self._name = "{} {} {}".format(self._device.name,subname,switch_id)
        else:
            self._name = f"{device.name} {switch_id}"

    @property
    def available(self):
        """Return the availability of the underlying device."""
        return self._device.available

    @property
    def unique_id(self):
        """Return a unique ID."""
        devID = self._device.getId()
        return f"{devID}-{self._switch_id}"

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return DAIKIN_SWITCHES_ICONS[self._switch_id]
 
    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return the state of the switch."""
        return self._device.get_switch_state(self._switch_id) == ATTR_STATE_ON

    @property
    def device_info(self):
        """Return a device description for device registry."""
        return self._device.device_info()

    async def async_update(self):
        """Retrieve latest state."""
        await self._device.api.async_update()

    async def async_turn_on(self, **kwargs):
        """Turn the zone on."""
        await self._device.set_switch_state(self._switch_id, ATTR_STATE_ON)

    async def async_turn_off(self, **kwargs):
        """Turn the zone off."""
        await self._device.set_switch_state(self._switch_id, ATTR_STATE_OFF)
