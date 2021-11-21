"""Daikin Residential base appliance, represent a Daikin device."""

import logging
_LOGGER = logging.getLogger(__name__)

from homeassistant.components.climate.const import (
    HVAC_MODE_OFF,
    HVAC_MODE_HEAT,
    HVAC_MODE_COOL,
    HVAC_MODE_AUTO,
)

from homeassistant.components.water_heater import (
    STATE_PERFORMANCE,
    STATE_HEAT_PUMP,
    STATE_OFF,
)

from .device import DaikinResidentialDevice

from .const import(
    ATTR_INSIDE_TEMPERATURE,
    ATTR_OUTSIDE_TEMPERATURE,
    ATTR_LW_TEMPERATURE,
    ATTR_TARGET_TEMPERATURE,
    ATTR_DHW_TEMPERATURE,
    ATTR_DHW_TARGET_TEMPERATURE,
    ATTR_DHW_STATE_OFF,
    ATTR_DHW_STATE_HEAT_PUMP,
    ATTR_DHW_STATE_PERFOMANCE,
    ATTR_DHW_TARGET_TEMPERATURE,
    ATTR_OPERATION_MODE,
    ATTR_CLIMATE_ON_OFF,
    ATTR_DHW_TANK_ON_OFF,
    ATTR_DHW_POWERFUL,
    ATTR_HVAC_MODE_COOL,
    ATTR_HVAC_MODE_HEAT,
    ATTR_HVAC_MODE_AUTO,
    ATTR_HVAC_MODE_OFF,
    ATTR_STATE_ON,
    ATTR_STATE_OFF,
    SWITCH_CLIMATE_ONOFF,
    SWITCH_DHW_TANK_ONOFF,
    SWITCH_POWERFUL_ONOFF,
    DAIKIN_CMD_SETS,
    MP_GATEWAY,
    KEY_MAC,
    KEY_IP,
)

HA_SWITCH_TO_DAIKIN = {
    SWITCH_CLIMATE_ONOFF: ATTR_CLIMATE_ON_OFF,
    SWITCH_DHW_TANK_ONOFF: ATTR_DHW_TANK_ON_OFF,
    SWITCH_POWERFUL_ONOFF: ATTR_DHW_POWERFUL,
}

DAIKIN_HVAC_TO_HA = {
    ATTR_HVAC_MODE_COOL: HVAC_MODE_COOL,
    ATTR_HVAC_MODE_HEAT: HVAC_MODE_HEAT,
    ATTR_HVAC_MODE_AUTO: HVAC_MODE_AUTO,
    ATTR_HVAC_MODE_OFF: HVAC_MODE_OFF,
}

DAIKIN_DHW_TO_HA = {
    ATTR_DHW_STATE_PERFOMANCE: STATE_PERFORMANCE,
    ATTR_DHW_STATE_HEAT_PUMP: STATE_HEAT_PUMP,
    ATTR_DHW_STATE_OFF: STATE_OFF,
}


class Appliance(DaikinResidentialDevice):  # pylint: disable=too-many-public-methods
    """Daikin main appliance class."""

    @staticmethod
    def translate_mac(value):
        """Return translated MAC address."""
        return ":".join(value[i : i + 2] for i in range(0, len(value), 2))

    def __init__(self, jsonData, apiInstance):
        """Init the pydaikin appliance, representing one Daikin device."""
        super().__init__(jsonData, apiInstance)

    async def init(self):
        """Init status."""
        # Re-defined in all sub-classes
        raise NotImplementedError

    def getCommandSet(self, param):
        _LOGGER.debug("Daikin Base getCommandSet param = %s",param)
        cmd_set = DAIKIN_CMD_SETS[param].copy()
        if "%operationMode%" in cmd_set[2]:
            operation_mode = self.getValue(ATTR_OPERATION_MODE)
            cmd_set[2] = cmd_set[2].replace("%operationMode%", operation_mode)
        _LOGGER.debug("Daikin Base getCommandSet result = %s",str(cmd_set))
        return cmd_set

    def getData(self, param):
        """Get the current data of a data object."""
        cmd_set = self.getCommandSet(param)
        v = self.get_data(cmd_set[0], cmd_set[1], cmd_set[2])
        _LOGGER.debug("Daikin Base getData result = %s", v)
        return v

    def getValue(self, param):
        """Get the current value of a data object."""
        data = self.getData(param)
        if data is None:
            return None
        return data["value"]

    def getValidValues(self, param):
        """Get the valid values of a data object."""
        data = self.getData(param)
        if data is None:
            return None
        return data["values"]

    async def setValue(self, param, value):
        """Set the current value of a data object."""
        cmd_set = self.getCommandSet(param)
        return await self.set_data(cmd_set[0], cmd_set[1], cmd_set[2], value)

    @property
    def mac(self):
        """Return device's MAC address."""
        return self.get_value(MP_GATEWAY, KEY_MAC)

    @property
    def ip(self):
        """Return device's IP address."""
        return self.get_value(MP_GATEWAY, KEY_IP)

    @property
    def support_dhw_temperature(self):
        """Return True if the device supports outsite temperature measurement."""
        return self.getData(ATTR_DHW_TEMPERATURE) is not None

    @property
    def dhw_temperature(self):
        """Return current outside temperature."""
        return float(self.getValue(ATTR_DHW_TEMPERATURE))

    @property
    def support_dhw_target_temperature(self):
        """Return True if the device supports outsite temperature measurement."""
        return self.getData(ATTR_DHW_TARGET_TEMPERATURE) is not None

    @property
    def dhw_target_temperature(self):
        """Return current outside temperature."""
        return float(self.getValue(ATTR_DHW_TARGET_TEMPERATURE))

    @property
    def support_outside_temperature(self):
        """Return True if the device supports outsite temperature measurement."""
        return self.getData(ATTR_OUTSIDE_TEMPERATURE) is not None

    @property
    def outside_temperature(self):
        """Return current outside temperature."""
        return float(self.getValue(ATTR_OUTSIDE_TEMPERATURE))

    @property
    def support_inside_temperature(self):
        """Return True if the device supports outsite temperature measurement."""
        return self.getData(ATTR_INSIDE_TEMPERATURE) is not None

    @property
    def inside_temperature(self):
        """Return current inside temperature."""
        return float(self.getValue(ATTR_INSIDE_TEMPERATURE))

    @property
    def support_lw_temperature(self):
        """Return True if the device supports outsite temperature measurement."""
        return self.getData(ATTR_LW_TEMPERATURE) is not None

    @property
    def leavingWater_temperature(self):
        """Return current inside temperature."""
        return float(self.getValue(ATTR_LW_TEMPERATURE))

    def support_switch(self, switch_id):
        """Return True if the device supports switch."""
        _LOGGER.debug("Daikin Base Support Switch: {}".format(switch_id))
        switch_id = HA_SWITCH_TO_DAIKIN[switch_id]
        switch = self.getData(switch_id)
        _LOGGER.debug("Daikin Base Support Switch result: {}".format(switch))
        return self.getData(switch_id) is not None

    def get_switch_state(self, switch_id):
        """Return switch state."""
        switch_id = HA_SWITCH_TO_DAIKIN[switch_id]
        if self.getData(switch_id) is None:
            return False
        status = self.getValue(switch_id)
        _LOGGER.debug("Daikin Base Get Switch State {}: {}".format(switch_id,status))
        return self.getValue(switch_id)

    async def set_switch_state(self, switch_id, status):
        """Set the switch state."""
        switch_id = HA_SWITCH_TO_DAIKIN[switch_id]
        if self.getData(switch_id) is None:
            return False
        return await self.setValue(switch_id, status)

    async def set(self, settings):
        """Set settings on Daikin device."""
        raise NotImplementedError

    @property
    def target_temperature(self):
        """Return current target temperature."""
        return float(self.getValue(ATTR_TARGET_TEMPERATURE))

    @property
    def target_temperature_step(self):
        """Return current target temperature."""
        return float(self.getData(ATTR_TARGET_TEMPERATURE)["stepValue"])

    @property
    def target_temperature_minValue(self):
        """Return current target temperature."""
        return float(self.getData(ATTR_TARGET_TEMPERATURE)["minValue"])

    @property
    def target_temperature_maxValue(self):
        """Return current target temperature."""
        return float(self.getData(ATTR_TARGET_TEMPERATURE)["maxValue"])

    @property
    def dhw_target_temperature_step(self):
        """Return current target temperature."""
        return float(self.getData(ATTR_DHW_TARGET_TEMPERATURE)["stepValue"])

    @property
    def dhw_target_temperature_minValue(self):
        """Return current target temperature."""
        return float(self.getData(ATTR_DHW_TARGET_TEMPERATURE)["minValue"])

    @property
    def dhw_target_temperature_maxValue(self):
        """Return current target temperature."""
        return float(self.getData(ATTR_DHW_TARGET_TEMPERATURE)["maxValue"])

    @property
    def hvac_mode(self):
        """Return current HVAC mode."""
        mode = ATTR_HVAC_MODE_OFF
        if self.getValue(ATTR_CLIMATE_ON_OFF) != ATTR_STATE_OFF:
            mode = self.getValue(ATTR_OPERATION_MODE)
        return DAIKIN_HVAC_TO_HA.get(mode)

    @property
    def hvac_modes(self):
        """Return the list of available HVAC modes."""
        modes = [HVAC_MODE_OFF]
        for mode in self.getValidValues(ATTR_OPERATION_MODE):
            modes.append(DAIKIN_HVAC_TO_HA[mode])
        return modes

    async def async_set_temperature(self, value):
        """Set new target temperature."""
        _LOGGER.debug("Daikin Base Set ATTR_TARGET_TEMPERATURE: %s", value)
        operationMode = self.getValue(ATTR_OPERATION_MODE)
        if operationMode not in [ATTR_HVAC_MODE_AUTO, ATTR_HVAC_MODE_COOL, ATTR_HVAC_MODE_HEAT]:
            return None
        return await self.setValue(ATTR_TARGET_TEMPERATURE, int(value))

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new HVAC mode."""
        _LOGGER.debug("Daikin Base Set HVAC mode: %s", hvac_mode)
        if hvac_mode == ATTR_HVAC_MODE_OFF:
            return await self.setValue(ATTR_CLIMATE_ON_OFF, hvac_mode)
        if hvac_mode not in [ATTR_HVAC_MODE_AUTO, ATTR_HVAC_MODE_COOL, ATTR_HVAC_MODE_HEAT]:
            _LOGGER.warning("Daikin Base Set invalid HVAC mode: %s", hvac_mode)
            return None
        if self.getValue(ATTR_CLIMATE_ON_OFF) != ATTR_STATE_OFF:
            await self.setValue(ATTR_CLIMATE_ON_OFF, ATTR_STATE_ON)
        return await self.setValue(ATTR_OPERATION_MODE, hvac_mode)

    @property
    def dhw_state(self):
        """Return current HVAC mode."""
        state = ATTR_DHW_STATE_OFF
        if self.getValue(ATTR_DHW_TANK_ON_OFF) != ATTR_STATE_OFF:
            if self.getValue(ATTR_DHW_POWERFUL) == ATTR_STATE_ON:
                state = ATTR_DHW_STATE_PERFOMANCE
            else:
                state = ATTR_DHW_STATE_HEAT_PUMP
        return DAIKIN_DHW_TO_HA.get(state)

    @property
    def dhw_states(self):
        """Return the list of available HVAC modes."""
        states = [STATE_OFF, STATE_HEAT_PUMP, STATE_PERFORMANCE]
        return states

    async def async_set_dhw_temperature(self, value):
        """Set new target temperature."""
        _LOGGER.debug("Daikin Base Set ATTR_DHW TARGET_TEMPERATURE: %s", value)
        if self.getValue(ATTR_DHW_TANK_ON_OFF) != ATTR_STATE_ON:
            return None
        return await self.setValue(ATTR_DHW_TARGET_TEMPERATURE, int(value))

    async def async_set_dhw_stat(self, dhw_state):
        """Set new DHW state."""
        _LOGGER.debug("Daikin Base Set DHW state: %s", dhw_state)
        if dhw_state == STATE_OFF:
            return await self.setValue(ATTR_DHW_TANK_ON_OFF, ATTR_STATE_OFF)
        if dhw_state == STATE_PERFORMANCE:
            if self.getValue(ATTR_DHW_TANK_ON_OFF) != ATTR_STATE_ON:
                await self.setValue(ATTR_DHW_TANK_ON_OFF, ATTR_STATE_ON)
            return await self.setValue(ATTR_DHW_POWERFUL, ATTR_STATE_ON)
        if dhw_state == STATE_HEAT_PUMP:
            if self.getValue(ATTR_DHW_TANK_ON_OFF) != ATTR_STATE_ON:
                return await self.setValue(ATTR_DHW_TANK_ON_OFF, ATTR_STATE_ON)
            await self.setValue(ATTR_DHW_POWERFUL, ATTR_STATE_OFF)
        _LOGGER.warning("Daikin Base Set invalid DHW state: %s", dhw_state)
        return None

