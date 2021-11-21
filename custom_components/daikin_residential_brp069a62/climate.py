"""Support for the Daikin BRP069A62."""
import logging
_LOGGER = logging.getLogger(__name__)

import voluptuous as vol

from homeassistant.components.climate import PLATFORM_SCHEMA, ClimateEntity
from homeassistant.components.climate.const import (
    ATTR_HVAC_MODE,
    HVAC_MODE_OFF,
    HVAC_MODE_HEAT,
    HVAC_MODE_COOL,
    HVAC_MODE_AUTO,
    SUPPORT_TARGET_TEMPERATURE,
)
from homeassistant.const import ATTR_TEMPERATURE, CONF_HOST, CONF_NAME, TEMP_CELSIUS
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN as DAIKIN_DOMAIN,
    DAIKIN_DEVICES,
    ATTR_TARGET_TEMPERATURE,
    ATTR_HVAC_MODE_COOL,
    ATTR_HVAC_MODE_HEAT,
    ATTR_HVAC_MODE_AUTO,
    ATTR_HVAC_MODE_OFF,
    ATTR_HVAC_MODE_SET,
)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_HOST): cv.string, vol.Optional(CONF_NAME): cv.string}
)

HA_HVAC_TO_DAIKIN = {
    HVAC_MODE_COOL: ATTR_HVAC_MODE_COOL,
    HVAC_MODE_HEAT: ATTR_HVAC_MODE_HEAT,
    HVAC_MODE_AUTO: ATTR_HVAC_MODE_AUTO,
    HVAC_MODE_OFF: ATTR_HVAC_MODE_OFF,
}

HA_ATTR_TO_DAIKIN = {
    ATTR_HVAC_MODE: ATTR_HVAC_MODE_SET,
    ATTR_TARGET_TEMPERATURE: ATTR_TARGET_TEMPERATURE,
}

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Old way of setting up the Daikin HVAC platform.

    Can only be called when a user accidentally mentions the platform in their
    config. But even in that case it would have been ignored.
    """


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Daikin climate entities."""
    for dev_id, device in hass.data[DAIKIN_DOMAIN][DAIKIN_DEVICES].items():
        _LOGGER.debug("Daikin Climate Add: {}".format(device))
        async_add_entities([DaikinClimate(device)], update_before_add=True)


class DaikinClimate(ClimateEntity):
    """Representation of a Daikin Heat Pump."""

    def __init__(self, device):
        """Initialize the climate device."""
        self._device = device
        self._list = {
            ATTR_HVAC_MODE: list(HA_HVAC_TO_DAIKIN),
        }
        self._supported_features = SUPPORT_TARGET_TEMPERATURE


    async def _set(self, settings):
        """Set device settings using API."""
        values = {}
        for attr in [ATTR_TEMPERATURE, ATTR_HVAC_MODE]:
            value = settings.get(attr)
            if value is None:
                continue
            daikin_attr = HA_ATTR_TO_DAIKIN.get(attr)
            if daikin_attr is not None:
                if attr == ATTR_HVAC_MODE:
                    values[daikin_attr] = HA_HVAC_TO_DAIKIN[value]
                elif value in self._list[attr]:
                    values[daikin_attr] = value.lower()
                else:
                    _LOGGER.error("Invalid value %s for %s", attr, value)
            # temperature
            elif attr == ATTR_TEMPERATURE:
                try:
                    values[HA_ATTR_TO_DAIKIN[ATTR_TARGET_TEMPERATURE]] = str(int(value))
                except ValueError:
                    _LOGGER.error("Invalid temperature %s", value)
        if values:
            await self._device.set(values)

    @property
    def available(self):
        """Return the availability of the underlying device."""
        return self._device.available

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return self._supported_features

    @property
    def name(self):
        """Return the name of the thermostat, if any."""
        return self._device.name

    @property
    def unique_id(self):
        """Return a unique ID."""
        devID = self._device.getId()
        return f"{devID}"

    @property
    def temperature_unit(self):
        """Return the unit of measurement which this thermostat uses."""
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._device.leavingWater_temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._device.target_temperature

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        stepVal = self._device.target_temperature_step
        return stepVal

    @property
    def min_temp(self):
        """Return the supported step of target temperature."""
        stepVal = self._device.target_temperature_minValue
        return stepVal

    @property
    def max_temp(self):
        """Return the supported step of target temperature."""
        stepVal = self._device.target_temperature_maxValue
        return stepVal

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        # The service climate.set_temperature can set the hvac_mode too, see
        # https://www.home-assistant.io/integrations/climate/#service-climateset_temperature
        # se we first set the hvac_mode, if provided, then the temperature.

        await self._device.async_set_temperature(kwargs[ATTR_TEMPERATURE])

    async def async_update(self):
        """Retrieve latest state."""
        await self._device.api.async_update()

    @property
    def hvac_mode(self):
        """Return current operation ie. heat, cool, idle."""
        mode = self._device.hvac_mode
        return mode

    @property
    def hvac_modes(self):
        """Return the list of available operation modes."""
        return self._device.hvac_modes

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        hvac_mode = HA_HVAC_TO_DAIKIN[hvac_mode]
        await self._device.async_set_hvac_mode(hvac_mode)

    @property
    def device_info(self):
        """Return a device description for device registry."""
        return self._device.device_info()
