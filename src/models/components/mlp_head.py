import torch
from torch import nn


class MLPHead(nn.Module):
    """A simple MLP projection head."""

    def __init__(self, in_dim: int, hidden_dim: int, out_dim: int) -> None:
        """Initialize a `MLPHead` module.

        :param in_dim: Input feature dimension.
        :param hidden_dim: Hidden feature dimension.
        :param out_dim: Output feature dimension.
        """
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, out_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Project features.

        :param x: Input tensor.
        :return: Projected tensor.
        """
        return self.model(x)


if __name__ == "__main__":
    head = MLPHead(8, 16, 4)
    x = torch.randn(3, 8, dtype=torch.float32)
    out = head(x)
    assert out.shape == (3, 4)
    assert torch.isfinite(out).all()

    try:
        _ = head(torch.randn(3, 7, dtype=torch.float32))
    except RuntimeError:
        pass
    else:
        raise AssertionError("Input dimension mismatch must raise RuntimeError")

    print("MLPHead self-test passed.")
