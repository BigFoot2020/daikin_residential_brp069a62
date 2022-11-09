# HA integration for BRP069A62 LAN Adapter

Home Assistant custom component for integration of Daikin Altherma Hydronic Heat Pumps with BRP069A62 LAN Adapter via Daikin Cloud. BRP069A62 firmware has to be updated to work with Daikin Residential Contoller app (connected to Daikin Cloud). Daikin BRP069A61 (with Smart Grid) should also work. 

This work is based on from Speleolontra "daikin_residential_altherma" repository (https://github.com/speleolontra/daikin_residential_altherma) and modified to support Daikin Altherma R Heat Pump with BRP069A62 LAN Adapter in weatherDependent mode. Original HA Integration was cloned from Rospogrigio's work "https://github.com/rospogrigio/daikin_residential".

# WARNING
This is a first experimental release, tested only on my Daikin Altherma R with BRP069A62.

# Installation using HACS:

Open "HACS" section then "Integrations" and click on three points menu at top right. Click on "Custom reporitories" and add repository "https://github.com/bigfoot2020/daikin_residential_brp069a62" with category "Integration".
This will copy the "daikin_residential_brp069a62" folder into "custom_components" folder of Home Assistant.
Make sure to restart Home Assistant, then go to "Using config flow" chapter.

# Manual Installation

Copy the "daikin_residential_brp069a62" folder and all of its contents into your Home Assistant's "custom_components" folder. This is often located inside of your "/config" folder. If you are running Hass.io, use SAMBA to copy the folder over. If you are running Home Assistant Supervised, the "custom_components" folder might be located at "/usr/share/hassio/homeassistant". It is possible that your "custom_components" folder does not exist. If that is the case, create the folder in the proper location, and then copy the "daikin_residential_brp069a62" folder and all of its contents inside the newly created "custom_components" folder.

# Using config flow

Start by going to Configuration -> Integrations and pressing the "+ ADD INTEGRATION" button to create a new Integration, then select "Daikin Residential Controller for BRP069A62" in the drop-down menu.

Follow the instructions, you just have to type the email and password used in the Daikin Residential Controller app. After pressing the "Submit" button, the integration will be added, and the Daikin devices connected to your cloud account will be created.

# YAML config files (not tested)

Just add the following lines to your configuration.yaml file specifying the email and password used in the Daikin Residential App, and the Daikin devices connected to your cloud account will be created.

daikin_residential_altherma:
  email: [your_email]
  password: [your_pwd]


# Thanks to:

This code is based on @Speleolontra's and @Rospogrigio's work that in turn is based on @Apollon77 's work, in finding a way to retrieve the token set, and to send the HTTP commands over the cloud. This integration would not exist without their hard work, my part was to adapt code to work with Altherma R/BRP069A62 controlled by Daikin Residential Controller app.

# Next steps

- Evaluate combining this integration with @Speleolontra and @Rospogrigio to work with different Daikin Air Conditioning and Heat Pump devices.
- Move API/Base/device to separate Python library as recommended by HA development.
- Water heater target temperature step in HA is 0.5, device supports 1. 
- Insert other read only/info parametera/sensors
- other ideas?
