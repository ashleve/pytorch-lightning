import os
from time import sleep

import pytest
from integrations_app_examples.public import _PATH_EXAMPLES

from lightning_app.testing.testing import run_app_in_cloud, wait_for


@pytest.mark.cloud
def test_template_react_ui_example_cloud() -> None:
    """This test ensures streamlit works in the cloud by clicking a button and checking the logs."""
    with run_app_in_cloud(os.path.join(_PATH_EXAMPLES, "app_template_react_ui")) as (
        _,
        view_page,
        fetch_logs,
        _,
    ):

        def click_button(*_, **__):
            button = view_page.frame_locator("iframe").locator('button:has-text("Start Printing")')
            button.wait_for(timeout=3 * 1000)
            if button.all_text_contents() == ["Start Printing"]:
                button.click()
                return True

        wait_for(view_page, click_button)

        has_logs = False
        while not has_logs:
            for log in fetch_logs():
                if "0: Hello World!" in log:
                    has_logs = True
            sleep(1)
