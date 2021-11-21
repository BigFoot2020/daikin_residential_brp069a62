"""Support for Daikin AC sensors."""
from homeassistant.const import (
    CONF_DEVICE_CLASS,
    CONF_ICON,
    CONF_NAME,
    CONF_TYPE,
    CONF_UNIT_OF_MEASUREMENT,
)
from homeassistant.helpers.entity import Entity

from .daikin_base import Appliance

from .const import (
    DOMAIN as DAIKIN_DOMAIN,
    DAIKIN_DEVICES,
    ATTR_INSIDE_TEMPERATURE,
    ATTR_OUTSIDE_TEMPERATURE,
    ATTR_LW_TEMPERATURE,
    ATTR_DHW_TEMPERATURE,
    ATTR_DHW_TARGET_TEMPERATURE,
    SENSOR_TYPE_TEMPERATURE,
    SENSOR_TYPES,
)

import logging
_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, async_add_entities):
    """Old way of setting up the Daikin sensors.

    Can only be called when a user accidentally mentions the platform in their
    config. But even in that case it would have been ignored.
    """


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Daikin sensors based on config_entry."""
    sensors = []

    for dev_id, device in hass.data[DAIKIN_DOMAIN][DAIKIN_DEVICES].items():
        if device.support_inside_temperature:
            sensor = DaikinSensor.factory(device, ATTR_INSIDE_TEMPERATURE)
            sensors.append(sensor)

        if device.support_outside_temperature:
            sensor = DaikinSensor.factory(device, ATTR_OUTSIDE_TEMPERATURE)
            sensors.append(sensor)

        if device.support_lw_temperature:
            sensor = DaikinSensor.factory(device, ATTR_LW_TEMPERATURE)
            sensors.append(sensor)

        if device.support_dhw_temperature:
            sensor = DaikinSensor.factory(device, ATTR_DHW_TEMPERATURE)
            sensors.append(sensor)

        if device.support_dhw_target_temperature:
            sensor = DaikinSensor.factory(device, ATTR_DHW_TARGET_TEMPERATURE)
            sensors.append(sensor)

    async_add_entities(sensors)


class DaikinSensor(Entity):
    """Representation of a Sensor."""

    @staticmethod
    def factory(device: Appliance, monitored_state: str):
        """Initialize any DaikinSensor."""
        cls = {
            SENSOR_TYPE_TEMPERATURE: DaikinClimateSensor,
        }[SENSOR_TYPES[monitored_state][CONF_TYPE]]
        return cls(device, monitored_state)

    def __init__(self, device: Appliance, monitored_state: str) -> None:
        """Initialize the sensor."""
        self._device = device
        self._sensor = SENSOR_TYPES[monitored_state]
        self._name = f"{device.name} {self._sensor[CONF_NAME]}"
        self._device_attribute = monitored_state

    @property
    def available(self):
        """Return the availability of the underlying device."""
        return self._device.available

    @property
    def unique_id(self):
        """Return a unique ID."""
        devID = self._device.getId()
        return f"{devID}_{self._device_attribute}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        raise NotImplementedError

    @property
    def device_class(self):
        """Return the class of this device."""
        return self._sensor.get(CONF_DEVICE_CLASS)

    @property
    def icon(self):
        """Return the icon of this device."""
        return self._sensor.get(CONF_ICON)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        uom = self._sensor[CONF_UNIT_OF_MEASUREMENT]
        return uom

    async def async_update(self):
        """Retrieve latest state."""
        await self._device.api.async_update()

    @property
    def device_info(self):
        """Return a device description for device registry."""
        return self._device.device_info()


class DaikinClimateSensor(DaikinSensor):
    """Representation of a Climate Sensor."""

    @property
    def state(self):
        """Return the internal state of the sensor."""
        if self._device_attribute == ATTR_INSIDE_TEMPERATURE:
            return self._device.inside_temperature
        
        if self._device_attribute == ATTR_OUTSIDE_TEMPERATURE:
            return self._device.outside_temperature
        
        if self._device_attribute == ATTR_LW_TEMPERATURE:
            return self._device.leavingWater_temperature
        
        if self._device_attribute == ATTR_DHW_TEMPERATURE:
            return self._device.dhw_temperature

        if self._device_attribute == ATTR_DHW_TARGET_TEMPERATURE:
            return self._device.dhw_target_temperature

        return None
