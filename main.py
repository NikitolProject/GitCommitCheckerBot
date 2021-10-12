import asyncio
import os

from github import Github
from vkbottle.api import API


class GitHubCommitCheckerBot:

    api = API(os.environ["BOT_TOKEN"])
    git = Github(os.environ["GITHUB_TOKEN"])
    repo = git.get_repo(os.environ["REPOSITORY_NAME"])
    last_commit = None

    async def run(self: "GitHubCommitCheckerBot") -> None:
        """
        Starts checking new commits in the repository. If they are available, it will be
        a new message sent on behalf of the group/user whose token was
        inserted in the configuration file (.env) in conversation/private messages,
        the peer_id of which is specified in the configuration file (.env).
        """
        while True:
            commits = self.repo.get_commits().reversed
            if self.last_commit is None or self.last_commit != commits[0]:
                self.last_commit = commits[0]
                await self.api.request(
                    "messages.send", {
                        "peer_id": os.environ["CHAT_ID"],
                        "message": f"🌟| Новое обновление от {commits[0].raw_data['commit']['author']['name']}\n"
                                   f"💌| Сообщение : {commits[0].raw_data['commit']['message']}\n"
                                   f"🕛| {commits[0].last_modified}",
                        "random_id": 0
                    }
                )
            await asyncio.sleep(1)


loop = asyncio.get_event_loop()
loop.run_until_complete(GitHubCommitCheckerBot().run())
