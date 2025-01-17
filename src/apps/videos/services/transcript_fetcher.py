import base64
import re
import typing as t

import requests

ORIGIN = "https://www.youtube.com/youtubei/"
API_VERSION = "v1"
API_KEY = "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
TRANSCRIPT_URL = f"{ORIGIN}{API_VERSION}/get_transcript?key={API_KEY}"


def parse_transcriptions_youtube(data: dict) -> dict:
    """Parse YouTube transcriptions data into cues and text."""
    result_text = ""
    result_cues = []

    if "actions" not in data:
        return {"text": "", "cues": []}
    for action in data["actions"]:
        panel = action.get("updateEngagementPanelAction", None)
        if panel is None:
            continue
        transcript_renderer = panel["content"]["transcriptRenderer"]
        body_content = transcript_renderer["body"]["transcriptBodyRenderer"]
        for cue_g in body_content["cueGroups"]:
            cue_g_content = cue_g["transcriptCueGroupRenderer"]
            cue_g_cues = cue_g_content["cues"]
            for _, cue in enumerate(cue_g_cues):
                cue_content = cue["transcriptCueRenderer"]
                cue_text_data = cue_content["cue"]
                if "simpleText" not in cue_text_data:
                    continue
                text = cue_text_data["simpleText"]
                result_text += text + " "
                result_cues.append(
                    {
                        "text": text,
                        "start_offset_ms": cue_content["startOffsetMs"],
                        "duration_ms": cue_content["durationMs"],
                    },
                )
    return {"text": result_text.strip(), "cues": result_cues}


class SyncTranscriptionAPI:
    def __init__(self) -> None:
        self.api_url = TRANSCRIPT_URL

    def __enter__(self) -> "SyncTranscriptionAPI":
        self._session = requests.Session().__enter__()
        return self

    def __exit__(self, *args: object, **kwargs: dict[str, t.Any]) -> None:
        self._session.__exit__(*args, **kwargs)

    @staticmethod
    def convert(response: dict) -> dict:
        return parse_transcriptions_youtube(response)

    def get_transcript(self, video_id: str) -> dict:
        headers = {
            "Content-Type": "application/json",
        }
        base64_string = base64.b64encode(f"\n\v{video_id}".encode()).decode("utf-8")
        data = {
            "context": {"client": {"clientName": "WEB", "clientVersion": "2.9999099"}},
            "params": base64_string,
        }
        with self._session.post(self.api_url, headers=headers, json=data) as resp:
            response_json = resp.json()
            return self.convert(response_json)

    def get_transcript_new(self, video_id: str) -> dict:
        headers = {}
        cues = []
        with self._session.get("https://www.youtube.com/watch?v=" + video_id, headers=headers) as resp:
            response_text = resp.text
        try:
            timedtext_link = (
                re.search(
                    r'(https://www\.youtube\.com/api/timedtext[^\"]*)\"',
                    response_text,
                )
                .group(1)
                .replace("\\u0026", "&")
            )

        except AttributeError:
            return {
                "cues": cues,
                "text": "",
            }
        with self._session.get(timedtext_link, headers=headers) as resp:
            html = resp.text
        timestamps = re.finditer(
            r'<text start=\"([.0-9]*)\" dur=\"([.0-9]*)\">([^<]*)</text>',
            html,
        )
        cues = []
        for g in timestamps:
            start, duration, content = g.group(1), g.group(2), g.group(3)
            cues.append(
                {
                    "text": content,
                    "start_offset_ms": float(start) * 1000,
                    "duration_ms": float(duration) * 1000,
                },
            )

        return {
            "cues": cues,
            "text": "",
        }
