import asyncio

from validator import validate_save_path
from downloader import Downloader
import renderer


def ask_save_path() -> str:
    """Prompt until the user provides a valid, writable directory."""
    while True:
        raw = input("Enter the directory to save images: ").strip()
        path = validate_save_path(raw)
        if path:
            return path
        print("Invalid path or no write access. Try again.")


async def prompt_urls(downloader: Downloader) -> None:
    """
    Ask the user for URLs in a loop.
    After each non-empty line, immediately schedule the download.
    An empty line stops input.
    """
    while True:
        url = input("Enter image URL (empty to finish): ").strip()
        if not url:
            break
        downloader.submit(url)


async def main_async() -> None:
    save_dir = ask_save_path()
    downloader = Downloader(save_dir)

    try:
        await prompt_urls(downloader)

        pending = downloader.pending_count()
        if pending:
            print(f"\nWaiting for {pending} download(s) to finish...")
        await downloader.wait_all()

        renderer.clear_screen()
        print("Summary of successful and unsuccessful downloads\n")
        rows = [r.to_row() for r in downloader.results]
        print(renderer.render_table(["Link", "Status"], rows))

        errors = [r for r in downloader.results if r.status == "Error"]
        if errors:
            print("\nErrors:")
            for r in errors:
                print(f"  {r.url} → {r.error}")

    finally:
        await downloader.close()


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()