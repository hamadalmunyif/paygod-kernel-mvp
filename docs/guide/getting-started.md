# Getting Started

This guide will walk you through the process of setting up and using the PayGod Kernel.

## Prerequisites

Before you begin, make sure you have the following installed:

*   .NET 8.0 SDK
*   Git

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/hamadalmunyif/paygod-kernel-mvp.git
    ```

2.  Navigate to the project directory:

    ```bash
    cd paygod-kernel-mvp
    ```

3.  Build the project:

    ```bash
    dotnet build
    ```

## Usage

To use the PayGod Kernel CLI, run the following command:

```bash
dotnet run --project src/PayGod.Cli -- [command]
```

For a list of available commands, run:

```bash
dotnet run --project src/PayGod.Cli -- --help
```
