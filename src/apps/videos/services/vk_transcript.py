import difflib
import typing
from dataclasses import dataclass
from io import StringIO
from json import loads

import requests
import webvtt

from apps.videos.models import Video
from core.services import BaseService

SUBS_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,gl;q=0.6,pt;q=0.5,ht;q=0.4,af;q=0.3,it;q=0.2",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Origin": "https://vk.com",
    "Pragma": "no-cache",
    "Referer": "https://vk.com/",
    "Sec-Fetch-Dest": "track",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
}


@dataclass
class VkParseTranscriptions(BaseService):
    video: Video

    def act(self) -> dict:
        link = self.video.origin_link
        params = self.get_video_data(link)
        if "subs" not in params or len(params["subs"]) == 0:
            return {"text": "", "cues": []}
        subs = self.get_subs(params["subs"][0]["url"])
        data = self.convert_subs_to_transcription(subs)
        return {"text": "", "cues": data}

    @staticmethod
    def get_video_data(url: str) -> dict:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36"
            "(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        }
        response = requests.get(url, headers=headers, timeout=200)
        content = response.content.decode("utf-8", errors="ignore")
        prefix = "var playerParams = "
        for line in content.splitlines():
            if line.startswith(prefix):
                break
        else:
            return {}

        player_params = line[len(prefix) : -1]
        data = loads(player_params)

        return data["params"][0]

    @staticmethod
    def get_subs(url: str) -> typing.Any:
        subs = requests.get(url, headers=SUBS_HEADERS, timeout=200)

        return subs.content.decode("utf-8")

    def convert_subs_to_transcription(self, subs: str) -> list:
        results = []
        buffer = StringIO(subs)
        prev_lines = set()
        for caption in webvtt.read_buffer(buffer):
            lines = [x.strip() for x in caption.text.strip().splitlines() if len(x.strip()) > 0]
            selected_lines = [line for line in lines if line not in prev_lines]

            prev_lines = set(selected_lines)
            text = " ".join(selected_lines)
            start = self.parse_time(caption.start)
            results.append(
                {"text": text, "start_offset_ms": start, "duration_ms": self.parse_time(caption.end) - start},
            )
        return self.trim_transcriptions(results)

    @staticmethod
    def parse_time(timestamp: str) -> float:
        hms, f = timestamp.split(".")
        f = float(f)
        h, m, s = map(int, hms.split(":"))
        return ((f / 1000) + (s + 60 * (m + 60 * h))) * 1000

    @staticmethod
    def trim_transcriptions(inputs: list, max_iter: int = 100) -> list:
        """For each neighboring cues pair trim the ending of the left cue, that coincides with the right cue start."""
        for _ in range(max_iter):
            results = []
            for cur, following in zip(inputs, inputs[1:] + [{"text": ""}], strict=False):
                longest_match = difflib.SequenceMatcher(None, cur["text"], following["text"]).find_longest_match()
                if longest_match.size > 1 and longest_match.b == 0:
                    text = cur["text"][: longest_match.a].strip()
                else:
                    text = cur["text"].strip()
                if len(text) == 0:
                    continue
                results.append(
                    {
                        "text": text,
                        "start_offset_ms": cur["start_offset_ms"],
                        "duration_ms": cur["duration_ms"],
                    },
                )
            if inputs == results:
                break
            inputs = results
        else:
            raise Exception("Maximum iterations exceeded")  # noqa: TRY002
        # fix durations
        inputs = results
        results = []
        for cur, following in zip(inputs, inputs[1:], strict=False):  # noqa:RUF007
            results.append(
                {
                    "text": cur["text"],
                    "start_offset_ms": cur["start_offset_ms"],
                    "duration_ms": following["start_offset_ms"] - cur["start_offset_ms"],
                },
            )
        results.append(inputs[-1])
        return results
