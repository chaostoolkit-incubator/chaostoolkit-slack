# Changelog

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/compare/0.7.0...HEAD

## [0.7.0][]

[0.7.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/compare/0.6.0...0.7.0

### Changed

- Switched to `files_upload_v2` to upload artefacts as per warning from slack
  sdk

## [0.6.0][]

[0.6.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/compare/0.5.7...0.6.0

### Added

- `get_channel_history` probe

### Changed

- Switched from flake8 to ruff for linting

## [0.5.7][]

[0.5.7]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/compare/0.5.6...0.5.7

- Fix signature again

## [0.5.6][]

[0.5.6]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/compare/0.5.5...0.5.6

- Fix signature again

## [0.5.5][]

[0.5.5]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/compare/0.5.4...0.5.5

- Fix signature

## [0.5.4][]

[0.5.4]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/compare/0.5.3...0.5.4

- Add missing context

## [0.5.3][]

[0.5.3]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/compare/0.5.2...0.5.3

- Handle default case

## [0.5.2][]

[0.5.2]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/compare/0.5.1...0.5.2

- Fix the fact secrets may not be set

## [0.5.1][]

[0.5.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/compare/0.5.0...0.5.1

- Fix call from `after_loading_experiment_control`

## [0.5.0][]

[0.5.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/compare/0.4.2...0.5.0

### Changed

- Allowing the channel name to be passed as an environment variable: `SLACK_CHANNEL`
  rather than an argument of the control

## [0.4.2][]

[0.4.2]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/compare/0.4.1...0.4.2

### Added

- Add text to messages as per Slack API

## [0.4.1][]

[0.4.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/compare/0.4.0...0.4.1

### Added

- Document app creation

## [0.4.0][]

[0.4.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/compare/0.3.0...0.4.0

### Added

- Control to replace notifications. Sending better messages to slack.

### Changed

- Major revamped of infrastructure so we now build on GitHub, we lint using
  `black`, we brought pyproject.toml to the build

### Fixed

-   Notification not sent when SSH has no before state[#10][10]

[10]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/pull/10

## [0.3.0][]

[0.3.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/compare/0.2.0...0.3.0

### Changed

-   Logging Slack Client output for debug purpose
-   Updated to Slack client 2.9
-   Cannot support Python 3.5 anymore as Slack client has dropped support
    for it

## [0.1.0][]

[0.1.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/tree/0.1.0

### Added

-   Initial release