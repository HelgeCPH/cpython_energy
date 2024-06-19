import asyncio
import httpx
import json
import requests
import sys
from datetime import datetime
from pathlib import Path
from otii_tcp_client import otii_connection, otii as otii_application
from otii_tcp_client.arc import Channel


SERVER_URL = "http://10.0.0.4:5000"
CLIENT_1_URL = "http://10.0.0.3:5001/trigger"
CLIENT_2_URL = "http://10.0.0.2:5001/trigger"
CLIENT_3_URL = "http://10.0.0.5:5001/trigger"


def create_otii_app(host="127.0.0.1", port=1905):
    # Connect to the Otii 3 application
    connection = otii_connection.OtiiConnection(host, port)
    connect_response = connection.connect_to_server(try_for_seconds=10)
    if connect_response["type"] == "error":
        raise Exception(
            f'Exit! Error code: {connect_response["errorcode"]}, '
            f'Description: {connect_response["payload"]["message"]}'
        )
    otii_app = otii_application.Otii(connection)

    return otii_app


def configure_multimeter(otii_app):
    # Based on the example from
    # https://github.com/qoitech/otii-tcp-client-python/blob/master/examples/basic_measurement.py
    devices = otii_app.get_devices()
    if len(devices) == 0:
        raise Exception("No Arc or Ace connected!")
    device = devices[0]

    # Enable the main current, voltage, and power channels

    device.enable_channel(Channel.MAIN_CURRENT)
    device.enable_channel(Channel.MAIN_VOLTAGE)
    device.enable_channel(Channel.MAIN_POWER)

    device.set_channel_samplerate(Channel.MAIN_CURRENT, 10000)
    device.set_channel_samplerate(Channel.MAIN_VOLTAGE, 10000)
    device.set_channel_samplerate(Channel.MAIN_POWER, 10000)

    # Get the active project
    project = otii_app.get_active_project()

    return project, device


def collect_data(otii_project, device):
    # Get statistics for the recording
    recording = otii_project.get_last_recording()
    df = recording.get_dataframe(device, (Channel.MAIN_CURRENT, Channel.MAIN_VOLTAGE, Channel.MAIN_POWER))
    return df, recording.name

def generate_output(otii_project, device):
    # Get statistics for the recording
    recording = otii_project.get_last_recording()
    minimum, maximum, avg, energy = recording.get_complete_channel_statistics(device, Channel.MAIN_CURRENT)
    print(f"{Channel.MAIN_CURRENT.name}: {minimum}, {maximum}, {avg}, {energy}", flush=True)

    for channel in (Channel.MAIN_VOLTAGE, Channel.MAIN_POWER):
        minimum, maximum, avg = recording.get_complete_channel_statistics(device, channel)
        print(f"{channel.name}: {minimum}, {maximum}, {avg}", flush=True)


# def generate_output(device, recording, statistics):
#     # Print the statistics
#     info = recording.get_channel_info(device.id, "mc")
#     print(f'From:        {info["from"]} s', flush=True)
#     print(f'To:          {info["to"]} s', flush=True)
#     print(f'Offset:      {info["offset"]} s', flush=True)
#     print(f'Sample rate: {info["sample_rate"]}', flush=True)

#     print(f'Min:         {statistics["min"]:.5} A', flush=True)
#     print(f'Max:         {statistics["max"]:.5} A', flush=True)
#     print(f'Average:     {statistics["average"]:.5} A', flush=True)
#     print(f'Energy:      {statistics["energy"] / 3600:.5} Wh', flush=True)


async def get_async(url):
    print(f"Starting scenario on {url}...", flush=True)
    timeout = httpx.Timeout(10.0, read=None)
    async with httpx.AsyncClient() as client:
        return await client.get(url, timeout=timeout)


async def main(scenario_no, otii_project, device, out_path):
    # reset server db
    print("Clearing DB on remote server...", flush=True)
    r = requests.get(f"{SERVER_URL}/cleardb")

    if r.ok:
        # start three clients
        print("Starting scenario on three clients...", flush=True)
        start_time = datetime.now()
        client_urls = [CLIENT_1_URL, CLIENT_2_URL, CLIENT_3_URL]

        otii_project.start_recording()

        results = await asyncio.gather(*map(get_async, client_urls))
        print(results, flush=True)

        otii_project.stop_recording()

        t_delta = datetime.now() - start_time
        print(f"Scenario took {t_delta}", flush=True)
        print("Done with scenario...", flush=True)

        df, recording_name = collect_data(otii_project, device)
        df.to_csv(Path(out_path, f"{recording_name}.csv"))
        generate_output(otii_project, device)


if __name__ == "__main__":
    # Store it to "../data/out/minitwit3x"
    out_path = Path(sys.argv[1])
    otii_project, device = configure_multimeter(create_otii_app())
    # project, device = None, None
    for idx in range(10):
        # Run the scenario 10 times
        asyncio.run(main(idx, otii_project, device, out_path))

    # otii_project.save_as(str(Path(out_path, "otii3_proj")))
