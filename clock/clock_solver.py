"""
Module for calculating the angle between clock hands.

This module provides functionality to determine the smallest angle
between the hour and minute hands of an analog clock, taking into
account precise time down to seconds.
"""

import json
import logging #info|error|warning
import os
from typing import List, Dict, Union

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def calculate_clock_angle(hours: int, minutes: int, seconds: int = 0) -> float:
    """
    Calculates the smallest angle between the hour and minute hands.

    The calculation accounts for the progressive movement of the hour hand
    based on minutes and seconds.

    Args:
        hours (int): The hour value (0-23).
        minutes (int): The minute value (0-59).
        seconds (int, optional): The second value (0-59). Defaults to 0.

    Returns:
        float: The absolute smallest angle between hands (0-180 degrees).

    Raises:
        ValueError: If inputs are outside valid ranges.
    """ 
    if not (0 <= hours <= 23):
        raise ValueError(f"Hours must be between 0 and 23, got {hours}")
    if not (0 <= minutes <= 59):
        raise ValueError(f"Minutes must be between 0 and 59, got {minutes}")
    if not (0 <= seconds <= 59):
        raise ValueError(f"Seconds must be between 0 and 59, got {seconds}")

    adjusted_hours = hours % 12 

    hour_angle = (adjusted_hours * 30) + (minutes * 0.5) + (seconds * (0.5 / 60))
    minute_angle = (minutes * 6) + (seconds * 0.1)

    # Різниця: зовн кут та внутрішній 
    diff = abs(hour_angle - minute_angle)

    final_angle = min(diff, 360 - diff)
    
    return round(final_angle, 4)


def run_tests_from_file(filepath: str) -> None:\

    """
    Loads test cases from a JSON file and runs them.
    """
    if not os.path.exists(filepath):
        logging.error(f"Файл не знайдено: {filepath}")
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f: #context manager
            test_cases = json.load(f) #List of Dicts
    except json.JSONDecodeError:
        logging.error(f"Помилка читання JSON: {filepath}")
        return

    passed = 0
    print(f"{'Time (H:M:S)':<15} | {'Expected':<10} | {'Actual':<10} | {'Status'}")
    print("-" * 55)

    for case in test_cases:
        h = case.get('hours')
        m = case.get('minutes')
        s = case.get('seconds', 0) 
        expected = case.get('expected_angle')
        
        try:
            actual = calculate_clock_angle(h, m, s)
            
            is_correct = abs(actual - expected) < 0.01
            
            status = "PASS" if is_correct else "FAIL"
            if is_correct:
                passed += 1
            
            time_str = f"{h:02}:{m:02}:{s:02}"
            print(f"{time_str:<15} | {expected:<10} | {actual:<10} | {status}")
            
        except ValueError as e:
            print(f"{h}:{m}:{s} | Error: {e}")

    print("-" * 55)
    logging.info(f"Test Run Complete: {passed}/{len(test_cases)} passed.")

if __name__ == "__main__":
    run_tests_from_file("clock_test_data.json")