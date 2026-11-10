import asyncio
import os
from urllib.parse import urlparse

import aiohttp


class DownloadResult:
    """Result of a single download attempt."""

    def __init__(self, url: str):
        self.url = url
        self.status: str = "Pending"
        self.error: str | None = None

    def to_row(self) -> list[str]:
        return [self.url, self.status]


class Downloader:
    """Async image downloader using aiohttp."""

    def __init__(self, save_dir: str):
        self.save_dir = save_dir
        self.results: list[DownloadResult] = []
        self._tasks: list[asyncio.Task] = []
        self._session: aiohttp.ClientSession | None = None


    async def _get_session(self) -> aiohttp.ClientSession:
        """Lazily create the shared aiohttp session."""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=15)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session


    async def close(self) -> None:
        """Close the shared session."""
        if self._session and not self._session.closed:
            await self._session.close()


    def _filename_from_url(self, url: str) -> str:
        parsed = urlparse(url)
        name = os.path.basename(parsed.path)
        return name or "image"


    def _unique_path(self, filename: str) -> str:
        """Avoid overwriting an existing file."""
        target = os.path.join(self.save_dir, filename)
        base, ext = os.path.splitext(target)
        counter = 1
        while os.path.exists(target):
            target = f"{base}_{counter}{ext}"
            counter += 1
        return target


    async def _download_one(self, url: str) -> DownloadResult:
        """Download a single image using aiohttp."""
        result = DownloadResult(url)
        try:
            session = await self._get_session()
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.read()

            filename = self._filename_from_url(url)
            target = self._unique_path(filename)

            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._write_file, target, data)

            result.status = "Success"
        except Exception as e:
            result.status = "Error"
            result.error = f"{type(e).__name__}: {e}"
        return result

    @staticmethod
    def _write_file(path: str, data: bytes) -> None:
        """Blocking file write — runs in executor."""
        with open(path, "wb") as f:
            f.write(data)

    # public API
    def submit(self, url: str) -> None:
        """Schedule a URL for download."""
        result = DownloadResult(url)
        self.results.append(result)
        task = asyncio.create_task(self._download_one(url))
        self._tasks.append(task)
        task.add_done_callback(lambda t, r=result: self._on_done(t, r))

    @staticmethod
    def _on_done(task: asyncio.Task, result: DownloadResult) -> None:
        try:
            completed = task.result()
            result.status = completed.status
            result.error = completed.error
        except Exception as e:
            result.status = "Error"
            result.error = str(e)

    async def wait_all(self) -> None:
        """Wait for all scheduled downloads to finish."""
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)

    def pending_count(self) -> int:
        """How many downloads are still running."""
        return sum(1 for t in self._tasks if not t.done())