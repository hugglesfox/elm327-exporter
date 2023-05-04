def test_ignition_off(emulator, client):
    # Change scenario to engine off
    emulator.set_sorted_obd_msg("engineoff")

    resp = client.get("/metrics")
    assert "rpm" not in resp.text

    # Change scenario to car and ensure that the server reconnects
    emulator.set_sorted_obd_msg("car")

    resp = client.get("/metrics")
    assert "rpm" in resp.text
