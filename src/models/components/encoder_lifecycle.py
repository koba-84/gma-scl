from __future__ import annotations

from typing import Any, cast

import torch


class EncoderLifecycleMixin:
    """Share encoder compilation, initialization, and trainability handling."""

    encoder: torch.nn.Module
    encoder_freeze: bool
    pretrained_encoder_path: str | None

    def setup(self, stage: str) -> None:
        """Compile the shared encoder and task-specific auxiliary modules for GPU fit stages."""
        trainer = getattr(self, "trainer", None)
        root_device = None if trainer is None else getattr(trainer.strategy, "root_device", None)
        compile_enabled = (
            stage == "fit"
            and bool(getattr(getattr(self, "hparams", None), "compile", False))
            and getattr(root_device, "type", "cpu") != "cpu"
        )
        if compile_enabled:
            self.encoder = cast(torch.nn.Module, torch.compile(self.encoder))
            self._compile_additional_modules()

    def _compile_additional_modules(self) -> None:
        """Compile task-specific modules after the shared encoder when supported."""

    def _initialize_encoder(self, missing_pretrained_message: str) -> None:
        """Load optional pretrained weights and apply the configured trainability policy."""
        encoder_pretrained = getattr(self.encoder, "load_pretrained_weights", None)
        if (
            self.encoder_freeze
            and not self.pretrained_encoder_path
            and encoder_pretrained is False
        ):
            raise RuntimeError(missing_pretrained_message)
        if self.pretrained_encoder_path:
            self._load_pretrained_encoder(self.pretrained_encoder_path)
        for parameter in self.encoder.parameters():
            parameter.requires_grad = not self.encoder_freeze

    def _load_pretrained_encoder(self, ckpt_path: str) -> None:
        """Load encoder-prefixed weights from a trusted checkpoint."""
        checkpoint = torch.load(ckpt_path, map_location="cpu", weights_only=False)
        state_dict = checkpoint.get("state_dict", checkpoint)
        encoder_state = {
            key.removeprefix("encoder."): value
            for key, value in cast(dict[str, Any], state_dict).items()
            if key.startswith("encoder.")
        }
        missing, unexpected = self.encoder.load_state_dict(encoder_state, strict=False)
        if missing or unexpected:
            raise RuntimeError(
                f"Pretrained encoder state mismatch. Missing: {len(missing)}, "
                f"Unexpected: {len(unexpected)}"
            )
