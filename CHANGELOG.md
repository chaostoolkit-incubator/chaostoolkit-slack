# Changelog

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit-incubator/chaostoolkit-slack/compare/0.4.2...HEAD

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