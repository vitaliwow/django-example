import typing as t

import pytest
from apps.users.models import User
from apps.videos.models import Video

if t.TYPE_CHECKING:
    from core.testing.factory import FixtureFactory


@pytest.fixture()
def video(factory: "FixtureFactory", user: User) -> Video:
    return factory.video(
        user=user,
        title="Video",
        description="description",
        origin_link="https://www.youtube.com/watch?v=-47Q_ggvggM",
    )


@pytest.fixture()
def ya_video(factory: "FixtureFactory", user: User) -> Video:
    return factory.video(
        user=user,
        title="Yet Another Video",
        description="Yet Another description",
        origin_link="https://www.youtube.com/watch?v=iiATVGsIbIA",
    )
