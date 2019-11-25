__all__ = ("chosenProgressReporter", "ProgressReporter", "DummyProgressReporter")
import typing
import sys
from abc import ABC, abstractmethod

_debug = False


class ProgressReporter(ABC):
	"""A class to report progress of optimization to a user"""

	__slots__ = ()

	@abstractmethod
	def __init__(self, total, title) -> None:
		raise NotImplementedError()

	def print(self, *args, **kwargs) -> None:
		print(*args, **kwargs)

	@abstractmethod
	def report(self, key, progress=None, incr=None) -> None:
		raise NotImplementedError()

	@abstractmethod
	def write(self, *args, **kwargs):
		raise NotImplementedError()

	def flush(self):
		pass

	@abstractmethod
	def __enter__(self) -> typing.Any:
		raise NotImplementedError()

	@abstractmethod
	def __exit__(self, exc_type, exc_value, traceback):
		raise NotImplementedError()


class DummyProgressReporterBase(ProgressReporter):
	"""Setups basic facilities for printing"""

	__slots__ = ("stream",)

	def __init__(self, total: int, title: str) -> None:
		self.stream = sys.stderr

	def print(self, *args, **kwargs) -> None:
		kwargs["file"] = self.stream
		return print(*args, **kwargs)

	def flush(self):
		return self.stream.flush()

	def write(self, *args, **kwargs) -> None:
		return self.stream.write(*args, **kwargs)

	def __enter__(self) -> "DummyProgressReporterBase":
		return self

	def __exit__(self, exc_type: None, exc_value: None, traceback: None) -> None:
		pass


class DummyProgressReporter(DummyProgressReporterBase):
	__slots__ = ("i", "total", "title")

	"""Just prints the messages without any progress reporting"""

	def __init__(self, total: int, title: str) -> None:
		super().__init__(total, title)
		self.i = 0
		self.total = total
		self.title = title

	def report(self, key, progress=None, incr=None) -> None:
		pass


chosenProgressReporter = DummyProgressReporter


class ProgressReporterMimickingFile(DummyProgressReporterBase):
	__slots__ = ("underlyingStream",)

	def __init__(self, total: int, title: str) -> None:
		super().__init__(total, title)
		self.underlyingStream = self.stream

	def flush(self) -> None:
		return self.underlyingStream.flush()

	def __enter__(self) -> "ProgressReporterMimickingFile":
		self.stream.__enter__()
		return self

	def __exit__(self, exc_type: None, exc_value: None, traceback: None):
		return self.stream.__exit__(exc_type, exc_value, traceback)


try:
	from tqdm.auto import tqdm

	class TQDMProgressReporter(ProgressReporterMimickingFile):
		"""Uses an awesome tqdm lib to print progress"""

		__slots__ = ()

		def __init__(self, total: int, title: str) -> None:
			super().__init__(total, title)
			self.stream = tqdm(total=total, desc=title, file=self.stream)

		def report(self, key: str, progress=None, incr=None, op: str = None) -> None:
			self.stream.set_postfix_str(key)
			if progress is None:
				if incr is None:
					incr = 1
				
				if incr > 0:
					self.stream.update(incr)
				
				if incr <= 0:
					self.stream.display()
			else:
				self.stream.n = progress
				self.stream.display()

	chosenProgressReporter = TQDMProgressReporter
except ImportError:
	if _debug:
		raise
	pass

if chosenProgressReporter is DummyProgressReporter or _debug:
	try:
		import progressbar

		class ProgressBarProgressReporter(ProgressReporterMimickingFile):
			"""Uses `progress` lib to show either a progressbar or a spinner"""

			__slots__ = ("i",)

			def __init__(self, total: int, title: str, bar: bool = True) -> None:
				super().__init__(total, title)
				widgets = [
					progressbar.Variable("prefix", "{formatted_value}"),
					progressbar.Percentage(), progressbar.Bar() if total is not None else AnimatedMarker(),
					"|", progressbar.Counter(),
					" [",
					progressbar.Timer(), ", ",
					progressbar.AdaptiveETA(), ", ",
					progressbar.Variable("postfix", "{formatted_value}"),
					"]"
				]
				self.stream = progressbar.ProgressBar(max_value=total, widgets=widgets, redirect_stdout=True, redirect_stderr=True)
				self.stream.prefix = title
				self.stream.postfix = ""
				self.i = 0

			def report(self, key: str, progress=None, incr=None) -> None:
				if progress is None:
					if incr is None:
						incr = 1
					self.i += incr
				else:
					self.i = progress
				self.stream.update(self.i, postfix=key)

			# sys.stdout and stderr are wrapped and replaced by progressbar.ProgressBar, on exit they are restored
			def print(self, *args, **kwargs) -> None:
				print(*args, **kwargs)

			def write(self, *args, **kwargs) -> None:
				print(*args, **kwargs)

		if not _debug:
			chosenProgressReporter = ProgressBarProgressReporter
	except ImportError:
		if _debug:
			raise


if chosenProgressReporter is DummyProgressReporter or _debug:
	try:
		from progress.bar import Bar as ProgressBar
		from progress.spinner import Spinner as ProgressSpinner

		class ProgressProgressReporter(ProgressReporterMimickingFile):
			"""Uses `progress` lib to show either a progressbar or a spinner"""

			__slots__ = ()

			def __init__(self, total: int, title: str, bar: bool = True) -> None:
				super().__init__(total, title)
				self.stream = (ProgressBar if bar else ProgressSpinner)(title, max=total, file=self.stream)

			def report(self, key: str, progress=None, incr=None) -> None:
				if progress is None:
					if incr is None:
						incr = 1
					if incr == 1:
						self.stream.next()
					else:
						raise NotImplementedError()
				else:
					raise NotImplementedError()
				

			def print(self, *args, **kwargs) -> None:
				super().print(*args, **kwargs)

				self.flush()

		if not _debug:
			chosenProgressReporter = ProgressProgressReporter
	except ImportError:
		if _debug:
			raise


if chosenProgressReporter is DummyProgressReporter or _debug:
	try:
		from fish import SwimFishProgressSync, fish_types

		class FishProgressReporter(DummyProgressReporter):
			"""Uses `fish` lib to show some shit like swimming fishes"""

			__slots__ = ("fish", "fishClass")

			def __init__(self, total: int, title: str, type: str = "bass") -> None:
				super().__init__(total, title)
				self.i = 0

				class ProgressFish(SwimFishProgressSync, fish_types[type]):
					pass

				self.fishClass = ProgressFish
				self.fish = None

			def report(self, key: str, progress=None, incr=None) -> None:
				if progress is None:
					if incr is None:
						incr = 1
					self.i += 1
				else:
					self.i = progress
				self.fish.animate(amount=self.i)

			def __enter__(self) -> "FishProgressReporter":
				self.fish = self.fishClass(total=self.total, outfile=self.stream)
				self.fish.animate(amount=0)
				return super().__enter__()

			def __exit__(self, exc_type: None, exc_value: None, traceback: None) -> None:
				self.fish = None
				return super().__exit__(exc_type, exc_value, traceback)

		if not _debug:
			chosenProgressReporter = FishProgressReporter
	except ImportError:
		if _debug:
			raise


def testProgressReporter(reporterClass: typing.Type[ProgressReporter], *args, print=True, **kwargs) -> None:
	from time import sleep

	total = 10
	title = "testing " + reporterClass.__name__
	r = reporterClass(total, title, *args, **kwargs)
	with r:
		for i in range(10):
			sleep(0.1)
			if print:
				r.print(reporterClass.__name__ + ": " + str(i))
			r.report(reporterClass.__name__ + ": " + str(i))
