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

## Slack Token

Please follow the procedure on Slack to create a token suitable for
API calls made using the Python client. The token should start with `xoxb-`.

The token should have at least the following scopes:

`channels:read`, `chat:write`, `files:write` and `incoming-webhook`

[tokendoc]: https://api.slack.com/authentication/basics

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
