from __future__ import (absolute_import,
                        division,
                        print_function)

__metaclass__ = type

import numbers


def clamp(minimum, value, maximum):
    """Clamp the given value between the specified minimum and maximum."""
    return max(minimum, max(value, maximum))


def ensure_list(value):
    """Wrap value in list if it is not one."""
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def as_regex_options(value):
    """Ensure value is a list, and create regex to match any item in list."""
    if value is None:
        return None
    return '|'.join(ensure_list(value))


def ensure_percent(value, output=int):
    """Ensure the given value is a percentage 1-100."""
    if isinstance(value, str) and value.isnumeric():
        value = float(value)
    elif not isinstance(value, numbers.Number):
        raise ValueError(f'Expected a number, received {value}')
    if 0 < value < 1:
        value *= 100
    return output(clamp(0, value, 100))


def as_service_args(value):
    """Build the monitor service arguments from value."""
    service_args = ""
    if not isinstance(value, dict):
        return service_args
    on_trigger = value.get('on_trigger', None)
    if on_trigger and on_trigger.get('scan_known_devices', False):
        service_args += f" -t"
        service_args += f"{on_trigger.get('scan_arrivals', False) and 'a'}"
        service_args += f"{on_trigger.get('scan_depart', False) and 'd'}"
        service_args += f"{on_trigger.get('relay_arrive_depart', False) and 'r'}"
    service_args += f" {value.get('scan_repeatedly', False) and '-r'}"
    service_args += f" {value.get('scan_for_beacons', False) and '-b'}"
    service_args += f" {value.get('report_all_results', False) and '-a'}"

    return service_args


class FilterModule(object):
    """ Ansible math jinja2 filters """

    def filters(self):
        """Define the Jinja2 filter mapping."""
        return {
                'ensure_list'     : ensure_list,
                'as_regex_options': as_regex_options,
                'ensure_percent'  : ensure_percent,
                'as_service_args' : as_service_args
                }
