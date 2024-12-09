# Latest Earthquake ID

![Blocked](http://bmkg-content-inatews.storage.googleapis.com/a.JPG)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

This project provides the latest earthquake information in Indonesia. It fetches data from reliable sources and presents it in an easy-to-understand format.

## Features

- Real-time earthquake data
- Detailed information on each earthquake
- User-friendly interface
- telegram notification

## Installation

To install this project, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/ridwaanhall/latest-earthquake-id.git
    ```

2. Navigate to the project directory:

    ```bash
    cd latest-earthquake-id
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To use this project, run the following command:

```bash
py manage.py runserver
```

```bash
import asyncio
from geoscience_api.views import check_earthquake_and_notify

async def main():
    await check_earthquake_and_notify()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())

```

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) first.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any inquiries, please contact [ridwaanhall.dev@gmail.com](mailto:ridwaanhall.dev@gmail.com).
