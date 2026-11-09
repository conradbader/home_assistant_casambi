# Casambi for Home Assistant

A custom integration that connects [Casambi](https://casambi.com/) lights to [Home Assistant](https://www.home-assistant.io/) through the Casambi Cloud API.

This is a maintained fork of [hellqvio86/home_assistant_casambi](https://github.com/hellqvio86/home_assistant_casambi), which was archived after Casambi stopped issuing API keys to end users. The fork keeps the integration working on current Home Assistant releases.

## Is this the right integration for you?

**You need an existing Casambi API key.** Casambi no longer issues new ones, so this integration is mainly useful if you already have a key, for example from the [Homebridge plugin](https://github.com/awahlig/homebridge-casambi).

Without a key, look at [casambi-bt-hass](https://github.com/lkempf/casambi-bt-hass), which talks to the lights over Bluetooth.

## What is different from the original

- Works on Home Assistant 2026.11 (tested version)
- Logs in with the network password only, so no account password is needed
- The setup form reports rejected credentials instead of accepting them
- Adds a **Leuchtrichtung** slider for lights with up/down control
- Fixes the rejected color modes and several setup and reconnect errors

## Features

Lights are discovered automatically. Changes arrive by websocket, and the integration also polls the Casambi cloud once a minute.

| Entity | Purpose |
| --- | --- |
| Light | On/off, brightness, color temperature, RGB and RGBW, depending on the fixture |
| Number `Leuchtrichtung` | Up/down light direction: 100 % is fully up, 0 % is fully down |
| Binary sensor `Status` | Whether the fixture is online |

### Setting the direction in automations

Use the slider entity with `number.set_value`:

```yaml
action: number.set_value
target:
  entity_id: number.kitchen_light_leuchtrichtung
data:
  value: 100
```

The older `casambi.light_turn_on` service still works. It sets brightness and `distribution` together, and counts the other way: `0` is fully up and `255` is fully down.

### Not supported

| OEM | Fixture model | Limitation |
| --- | --- | --- |
| OLIGO | GRACE PL HA TW | Fixtures with two dimmers are not supported |
| OLIGO | CURVED | Both dimmers (up and down light) are controlled together by one light entity |

## Requirements

- Home Assistant 2026.11 or newer
- A Casambi API key
- A Casambi network with an [active gateway](https://support.casambi.com/support/solutions/articles/12000017046-how-to-enable-a-gateway-for-a-network-), which is usually a phone or tablet running the Casambi app
- A GitHub account connected to the Home Assistant Marketplace

## Installation

1. Go to **Settings > Marketplace > Add from link**.
2. Enter `conradbader/home_assistant_casambi` and select **Add**. If asked for the type, choose **Integration**.
3. Open the repository and install it.
4. Restart Home Assistant and reload the browser page.
5. Go to **Settings > Devices & services > Add integration > Casambi**.
6. Enter the API key, the email and the network password. If you use the Homebridge plugin in network login mode, these are the same values.

### Updating

Open the integration in **Settings > Marketplace**, install the update and restart Home Assistant.

## Troubleshooting

To get detailed logs, add this to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.casambi: debug
    aiocasambi: debug
```

> [!WARNING]
> With debug logging on, the `aiocasambi` library writes the API key and network password to the log. Turn it off again afterwards, and remove those values before sharing a log.

## Related projects

- [aiocasambi](https://github.com/hellqvio86/aiocasambi): the library this integration uses
- [homebridge-casambi](https://github.com/awahlig/homebridge-casambi): Homebridge plugin for Casambi
- [casambi-bt-hass](https://github.com/lkempf/casambi-bt-hass): Home Assistant integration using Bluetooth

## Credits and license

Originally written by Olof Hellqvist. Licensed under the MIT License, see [LICENSE](LICENSE).

This integration is neither affiliated with nor endorsed by Casambi.
