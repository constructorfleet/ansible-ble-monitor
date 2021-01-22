# ansible-ble-monitor
Ansible role to set up and install Monitor.sh - Distributed BTLE Device Tracking on a Raspberry Pi (i.e. Zero W)

## Requirements
1. Access to an MQTT broker
2. A provisioned device with BT modem

## Variables

**monitor_version**: Git commit, tag or branch of Monitor to install, default `master`.  
**mqtt_host**: IP or FQDN of the MQTT broker.  
**mqtt_port**: The MQTT port to connect to, default `1883`.  
**mqtt_username**: The username to connect to the MQTT broker, default `blemonitor`.  
**mqtt_version**: The MQTT protocol version, valid values: 3.1 3.11 or 4, default `3.11`.  
**ble_monitor_mqtt_topic_base**: The base MQTT topic to publish and subscribe to, default `monitor`.  
**ble_monitor_identifier**: The identifier of the monitor instance, default `blemonitor1`.  
**arrival_max_scans**: Maximum number of scans to trigger an arrival event, default `1`.  
**departure_max_scans**: Maximum number of scans to trigger a departure event, default `2`.  
**beacon_expiration_seconds**: The number of seconds before considering a beacon expired, default `240`.  
**minimum_scan_interval**: Minimum number of seconds between scans, default `50`.  
**name_request_interval**: The number of seconds between name request commands, lower can increase responsiveness but can also clog up the scanner, default `3`.  
**anonymous_expiration_seconds**: The number of seconds before considering an unknown device expired, default `75`.  
**rssi_delta_report_trigger**: The change in RSSI that triggers a report published to MQTT, default `-20`.  
**rssi_threshold**: The minimum RSSI before considering the device away, default `-75`.  
**hci_device**: The name of the device to use for scanning, default `hci0`.  
**cooperative_scan_confidence_threshold**: The level of confidence before triggering a scan to other monitors, default `60`.  
**confidence_reporting_threshold**: The leve lof confidence before assuming the device is leaving, default `59`.  
**minimum_departure_scan_interval**: The minimum number of seconds between departure scans, default `30`.  
**minimum_arrival_scan_interval**: The minimum number of seconds between arrival scans, default `15`.  
**observed_advertisement_interval**: The minimum number of seconds used to estimate advertisement intervals reported to MQTT, default `50`  
**pass_pdu_values**: List of PDU types to process, default:  

```yaml
pass_pdu_values:
  - ADV_IND
  - ADV_SCAN_IND
  - ADV_NONCONN_IND
  - SCAN_RSP
```

**pass_regex**: Regular expression that, when matched, triggers processing, default `.*`  
**pass_manufacturers**: List of regular expressions to match device manufacturers to process, default:  
```yaml
pass_manufacturers:
  - '.*'
```

**ignore_regex**: Regular expression that, when matched, ignores the device, default `None`.  
**ignore_manufacturers**: List of regular expressions that, when matched, ignores the device, default `None`.   
**report_scan_messages**: Whether to report all scan message to MQTT, including scan timing, default  `False`.    
**reporting_mode**: Whether to report the `alias` or the `mac` to MQTT, default `alias`.  
**report_device_tracker**: Whether to send an MQTT message with Home-Assistant Device Tracker properties, default `False`.  
**device_tracker_state_when_present**: When reporting a device tracker that is detected, set the state to this string, default `home`.  
**device_tracker_state_when_absent**: When reporting a device tracker that is not detected, set the state to this string, default `not_home`.  

### Service Options
service_options:
  scan_repeatedly: true
  scan_for_beacons: true
  report_all_results: true
  on_trigger:
    scan_known_devices: true
    scan_arrivals: true
    scan_depart: true
    relay_arrive_depart: true

## Example playbook

```ansible
---
- name: Deploy Monitor.sh
  hosts: ble-monitors
  remote_user: root
  gather_facts: yes

  tasks:
    - import_role:
        name: ble-monitor
```

