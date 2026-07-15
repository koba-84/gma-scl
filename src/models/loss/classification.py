from __future__ import annotations

import torch
from torch import nn


class AsymmetricLoss(nn.Module):
    """Asymmetric loss for multi-label classification."""

    def __init__(
        self,
        gamma_pos: float = 0.0,
        gamma_neg: float = 1.0,
        margin: float = 0.0,
        eps: float = 1e-8,
    ) -> None:
        super().__init__()
        if gamma_pos < 0 or gamma_neg < 0:
            raise ValueError("gamma_pos and gamma_neg must be >= 0.")
        if margin < 0:
            raise ValueError("margin must be >= 0.")
        self.gamma_pos = float(gamma_pos)
        self.gamma_neg = float(gamma_neg)
        self.margin = float(margin)
        self.eps = float(eps)

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """Run the forward computation and return model outputs."""
        if logits.shape != targets.shape:
            raise ValueError("logits and targets must have the same shape.")
        targets = targets.float()

        prob_pos = torch.sigmoid(logits)
        prob_neg = 1.0 - prob_pos
        if self.margin > 0:
            prob_neg = (prob_neg + self.margin).clamp(max=1.0)

        log_pos = torch.log(prob_pos.clamp_min(self.eps))
        log_neg = torch.log(prob_neg.clamp_min(self.eps))
        ce = targets * log_pos + (1.0 - targets) * log_neg

        pt = targets * prob_pos + (1.0 - targets) * prob_neg
        gamma = targets * self.gamma_pos + (1.0 - targets) * self.gamma_neg
        focal = torch.pow(1.0 - pt, gamma)

        return -(focal * ce).mean()


class ZLPRLoss(nn.Module):
    """Zero-bounded log-sum-exp pairwise ranking loss for multi-label classification."""

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """Run the forward computation and return model outputs."""
        if logits.shape != targets.shape:
            raise ValueError("logits and targets must have the same shape.")
        targets = targets.float()
        pos_mask = targets > 0.5
        neg_mask = ~pos_mask

        neg_inf = torch.finfo(logits.dtype).min
        pos_terms = torch.where(pos_mask, -logits, neg_inf)
        neg_terms = torch.where(neg_mask, logits, neg_inf)

        zeros = torch.zeros((logits.size(0), 1), dtype=logits.dtype, device=logits.device)
        pos_lse = torch.logsumexp(torch.cat([zeros, pos_terms], dim=1), dim=1)
        neg_lse = torch.logsumexp(torch.cat([zeros, neg_terms], dim=1), dim=1)

        return (pos_lse + neg_lse).mean()


if __name__ == "__main__":
    torch.manual_seed(0)

    logits = torch.randn(8, 5, requires_grad=True)
    targets = torch.randint(0, 2, (8, 5)).float()

    asl = AsymmetricLoss(gamma_pos=0.0, gamma_neg=1.0, margin=0.0)
    zlpr = ZLPRLoss()

    asl_out = asl(logits, targets)
    zlpr_out = zlpr(logits, targets)

    assert asl_out.ndim == 0 and torch.isfinite(asl_out)
    assert zlpr_out.ndim == 0 and torch.isfinite(zlpr_out)

    (asl_out + zlpr_out).backward()
    assert logits.grad is not None and torch.isfinite(logits.grad).all()

    try:
        _ = asl(logits, targets[:, :3])
        raise AssertionError("Shape mismatch must raise ValueError.")
    except ValueError:
        pass

    try:
        _ = zlpr(logits, targets[:, :3])
        raise AssertionError("Shape mismatch must raise ValueError.")
    except ValueError:
        pass

    print("classification loss self-test passed")
