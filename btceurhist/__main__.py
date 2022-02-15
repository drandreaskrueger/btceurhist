import argparse  # pragma: no cover

from . import BaseClass, base_function, base_server  # pragma: no cover


def main() -> None:  # pragma: no cover
    """
    The main function executes on commands:
    `python -m btceurhist` and `$ btceurhist `.

    This is your program's entry point.

    You can change this function to do whatever you want.
    Examples:
        * Run a test suite
        * Run a server
        * Do some other stuff
        * Run a command line application (Click, Typer, ArgParse)
        * List all available tasks
        * Run an application (Flask, FastAPI, Django, etc.)
    """
    parser = argparse.ArgumentParser(
        description="btceurhist.",
        epilog="Enjoy the btceurhist functionality!",
    )
    # This is required positional argument
    parser.add_argument(
        "method",
        type=str,
        help="the method to call",
        default="startserver",
    )
    # This is optional named argument
    parser.add_argument(
        "-m",
        "--message",
        type=str,
        help="The Message",
        default="Hello",
        required=False,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Optionally adds verbosity",
    )
    args = parser.parse_args()
    print(f"{args.message} !")
    if args.verbose:
        print("Verbose mode is on.")

    print("Executing main function")
    base = BaseClass()
    print(base.base_method())
    print(base_function())
    print("End of main function")

    if args.method == "startserver":
        print("starting server:")
        base_server()


if __name__ == "__main__":  # pragma: no cover
    main()
