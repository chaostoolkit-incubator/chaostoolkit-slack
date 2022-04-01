# Chaos Toolkit Extension for Slack

[![Build](https://github.com/chaostoolkit-incubator/chaostoolkit-slack/actions/workflows/build.yaml/badge.svg)](https://github.com/chaostoolkit-incubator/chaostoolkit-slack/actions/workflows/build.yaml)

This project is an extension for the Chaos Toolkit to target [Slack][slack].

[slack]: https://slack.com/

## Install

This package requires Python 3.7+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

[chaostoolkit]: https://github.com/chaostoolkit/chaostoolkit

```
$ pip install -U chaostoolkit-slack
```

### Slack App

To use this extension, you need to create a Slack app in your workspace.
Please follow the Slack documentation to create a basic app:

https://api.slack.com/apps?new_app=1
https://api.slack.com/tutorials

You can start from this manifest if you want:

```yaml
display_information:
  name: Chaos Toolkit events
  long_description: Get live feedback information of all your Chaos Engineering
    experiments executed from Chaos Toolkit. See which experiments deviated and
    investigate their logs directly from a Slack thread.
  description: Chaos Engineering experiments live events from Chaos Toolkit.
  background_color: "#ffffff"
settings:
  org_deploy_enabled: false
  socket_mode_enabled: false
  is_hosted: false
  token_rotation_enabled: false
features:
  bot_user:
    display_name: chaostoolkit
oauth_config:
  scopes:
    bot:
      - channels:read
      - chat:write
      - files:write
```

Once your application is created, you may want to set the Chaos Toolkit
[logo][logo] to clarify to your users where these messages come from.

[logo]: https://chaostoolkit.org/resources/logos/

### Slack Token

Please follow the procedure on Slack to create a token suitable for
API calls made using the Python client. The token should start with `xoxb-`.
You can find the token in your app settings under the `OAuth & Permissions`
page.

The token should have at least the following scopes:

`channels:read`, `chat:write` and `files:write`

[tokendoc]: https://api.slack.com/authentication/basics

### Install your Slack app

Once created, you need to install the app in your workspace and invite it in
any channel you wish to send events to. This channel will also have to be part
specified as a controls argument (see below).

Now you should be good to go!

## Usage

Currently, this extension only provides a control to send Chaos
Toolkit events to Slack channels.

To use this extension, add the following to your experiment (or settings):

```json
"secrets": {
    "slack": {
        "token": "xoxb-..."
    }
},
"controls": [
    {
        "name": "slack",
        "provider": {
            "type": "python",
            "module": "chaosslack.control",
            "secrets": ["slack"],
            "arguments": {
                "channel": "general"
            }
        }
    }
]
```

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please fork this project, make your changes following the
usual [PEP 8][pep8] code style, add appropriate tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: https://docs.chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt
```

Then, point your environment to this directory:

```console
$ pip install -e .
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

To run the tests for the project execute the following:

```
$ pytest
```
