import os
import json
import requests


class GithubAPI:

    def __init__(self):

        # These are default Travis variables identifying a pull request
        # https://docs.travis-ci.com/user/environment-variables/#Default-Environment-Variables
        self.repo = os.environ["TRAVIS_REPO_SLUG"]
        self.pr = os.environ["TRAVIS_PULL_REQUEST"]
        # Set in Travis settings
        # https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/
        self.token = {"Authorization": "token %s" % os.environ["GITHUB_TOKEN"]}

        self.label_url = (
                             "https://api.github.com/repos/%s/issues/%s/labels"
                         ) % (self.repo, self.pr)

    def comment_on_pull(self, problems, warnings):

        # Checks for pull build
        if self.pr == "false":
            return

        # Getting pull request to comment on
        url = (
                  "https://api.github.com/repos/%s/issues/%s/comments"
              ) % (self.repo, self.pr)

        # Find out github username of pull creator
        url_for_name = (
                           "https://api.github.com/repos/%s/issues/%s"
                       ) % (self.repo, self.pr)

        req = requests.get(url_for_name, headers=self.token)
        username = req.json()["user"]["login"]

        # Comment message in markdown format
        comment = "Hey @%s, We found the following issues:" % username

        if problems:
            comment += "\n#### Problems: \n * %s" % "\n* ".join(problems)

        if warnings:
            comment += "\n#### Warnings: \n * %s" % "\n* ".join(warnings)

        message = {"body": comment}

        # Posting comment
        requests.post(url, data=json.dumps(message), headers=self.token)

    def set_label(self, label):
        requests.post(self.label_url, data=json.dumps(label),
                      headers=self.token)

    def remove_label(self, label):
        requests.delete(self.label_url, data=json.dumps(label),
                        headers=self.token)
