import json
from datetime import datetime


def iso_to_millis(iso_timestamp):
    """
    Convert ISO 8601 timestamp to milliseconds.
    Example: 2021-04-05T10:15:30Z -> 1617617730000
    """
    dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
    return int(dt.timestamp() * 1000)


def unify_data():
    """
    Combine two telemetry formats into one unified format.
    """
    with open("data-1.json") as f:
        data_1 = json.load(f)

    with open("data-2.json") as f:
        data_2 = json.load(f)

    unified = []

    # data-1 already has timestamps in milliseconds
    for item in data_1:
        unified.append(item)

    # data-2 timestamps are ISO, convert them
    for item in data_2:
        unified.append({
            "deviceId": item["deviceId"],
            "timestamp": iso_to_millis(item["timestamp"]),
            "temperature": item["temperature"]
        })

    return unified


def main():
    result = unify_data()

    with open("data-result.json") as f:
        expected = json.load(f)

    # Order-independent comparison
    assert sorted(result, key=lambda x: (x["deviceId"], x["timestamp"])) == \
           sorted(expected, key=lambda x: (x["deviceId"], x["timestamp"]))

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
