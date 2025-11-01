from io import TextIOBase
from collections import deque
from typing import Any, Iterable, Optional, Deque

class StreamTransducer:
    """
    Base class for streaming transducers that read from a text stream,
    convert the text into structured tokens, apply contextual rules,
    and write transformed text to an output stream.
    """

    def __init__(self, 
                 input_stream: TextIOBase,
                 output_stream: TextIOBase,
                 rules: Optional[Iterable[Any]] = None,
                 buffer_limit: int = 1024):
        self.input_stream = input_stream
        self.output_stream = output_stream
        self.rules = list(rules or [])
        self.buffer: Deque[Any] = deque()
        self.buffer_limit = buffer_limit
        self.end_of_stream = False

    # ------------------------
    # Core pipeline
    # ------------------------
    def process_stream(self, chunk_size: int = 256):
        """Main loop: read from input, buffer, apply rules, and emit."""
        while not self.end_of_stream:
            chunk = self.input_stream.read(chunk_size)
            if not chunk:
                self.end_of_stream = True
            else:
                tokens = self.tokenize(chunk)
                self.buffer.extend(tokens)

            # Apply rules as far as possible
            self.apply_rules()

            # Emit safely finalized tokens
            self.emit_ready()

        # Flush remaining buffered data at end
        self.flush()

    # ------------------------
    # Hooks for subclasses
    # ------------------------
    def tokenize(self, chunk: str) -> Iterable[Any]:
        """Convert raw input string into structured tokens."""
        raise NotImplementedError

    def apply_rules(self):
        """Apply contextual transformation rules to buffered tokens."""
        raise NotImplementedError

    def serialize(self, token: Any) -> str:
        """Convert processed token back into output text."""
        return str(token)

    def is_token_ready(self, token: Any) -> bool:
        """
        Return True if this token is safe to emit (i.e., no pending
        rules require further context).
        Override for context-sensitive logic.
        """
        return True

    # ------------------------
    # Emission / flushing
    # ------------------------
    def emit_ready(self):
        """Emit tokens from buffer that are safe to output."""
        while self.buffer and self.is_token_ready(self.buffer[0]):
            token = self.buffer.popleft()
            self.output_stream.write(self.serialize(token))
            self.output_stream.flush()

    def flush(self):
        """Emit all remaining buffered tokens at end-of-stream."""
        while self.buffer:
            token = self.buffer.popleft()
            self.output_stream.write(self.serialize(token))
        self.output_stream.flush()

