import dataclasses

import strawberry


@strawberry.input
class UpdateCommentInput:
    token: str
    tweetId: str
    comment: str

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)
