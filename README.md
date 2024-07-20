## Network Monitoring for processes

`netmon-proc` is a network monitoring CLI tool designed to monitor network traffic and provide detailed metrics for specified processes. It leverages Scapy for packet sniffing and offers multiple formatting options for the output.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Features

- Real-time network traffic monitoring for specific processes.
- Metrics aggregation and reporting.
- Support for different output formats, including JSON and tabular formats.
- Threaded implementation for efficient performance.
- Customizable filtering using BPF (Berkeley Packet Filter) syntax.

## Installation

You can install `netmon-proc` using the provided wheel or source distribution files.

### From Source

1. Clone the repository:

   ```sh
   git clone https://github.com/0xzer0x/netmon-proc.git
   cd netmon-proc
   ```

2. Install dependencies:

   ```sh
   poetry install
   ```

3. Build the package:

   ```sh
   poetry build
   ```

4. Install the package:

   ```sh
   pip install dist/netmon_proc-0.x.x-py3-none-any.whl
   ```

## Usage

### Command Line Interface

`netmon-proc` provides a CLI for starting the network monitoring tool. Below are some usage examples.

```sh
netmon-proc --help
```

### Example Command

To start monitoring network traffic for a specific process with a BPF filter and output the results in a table format:

```sh
netmon-proc --filter "tcp port 443" --format table --metrics rx_bytes firefox
```

## License

This project is licensed under the GPL v3 License. See the [LICENSE](LICENSE) file for more details.
