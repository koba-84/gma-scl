from __future__ import annotations

from typing import Any

import torch
from torch import nn
from transformers import AutoConfig, AutoModel


class Encoder(nn.Module):
    """RoBERTa text encoder for pre-tokenized tensor inputs."""

    def __init__(
        self,
        model_name: str = "roberta-base",
        cache_dir: str | None = None,
        load_pretrained_weights: bool = True,
    ) -> None:
        super().__init__()
        self.model_name = model_name
        self.load_pretrained_weights = load_pretrained_weights

        if load_pretrained_weights:
            self.model = AutoModel.from_pretrained(model_name, cache_dir=cache_dir)
        else:
            config = AutoConfig.from_pretrained(model_name, cache_dir=cache_dir)
            self.model = AutoModel.from_config(config)
        self.hidden_size = int(self.model.config.hidden_size)

    def _pool(self, outputs: Any) -> torch.Tensor:
        return outputs.last_hidden_state[:, 0]

    def forward(self, inputs: dict[str, torch.Tensor]) -> torch.Tensor:
        """Run the forward computation and return model outputs."""
        encoded = {
            "input_ids": inputs["input_ids"],
            "attention_mask": inputs["attention_mask"],
        }

        device = next(self.model.parameters()).device
        encoded = {k: v.to(device) for k, v in encoded.items()}
        outputs = self.model(**encoded)
        return self._pool(outputs)


if __name__ == "__main__":
    _ = Encoder()
