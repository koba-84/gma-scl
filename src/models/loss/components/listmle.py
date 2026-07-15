from __future__ import annotations

import torch


def compute_listmle_loss(
    student_scores: torch.Tensor,
    teacher_scores: torch.Tensor,
    valid_mask: torch.Tensor,
    *,
    eps: float = 1e-10,
) -> torch.Tensor:
    """Compute row-wise ListMLE on a dense pairwise score matrix with an explicit validity mask."""
    if eps <= 0:
        raise ValueError("eps must be > 0.")
    if student_scores.ndim != 2 or teacher_scores.ndim != 2 or valid_mask.ndim != 2:
        raise ValueError("student_scores, teacher_scores, and valid_mask must be rank-2 tensors.")
    if student_scores.shape != teacher_scores.shape or student_scores.shape != valid_mask.shape:
        raise ValueError(
            "student_scores, teacher_scores, and valid_mask must share the same shape."
        )

    valid_mask = valid_mask.to(dtype=torch.bool, device=student_scores.device)
    if not torch.any(valid_mask):
        return student_scores.new_zeros(())

    random_indices = torch.randperm(student_scores.size(1), device=student_scores.device)
    student_shuffled = student_scores[:, random_indices]
    teacher_shuffled = teacher_scores[:, random_indices]
    mask_shuffled = valid_mask[:, random_indices]

    teacher_for_sort = teacher_shuffled.masked_fill(~mask_shuffled, float("-inf"))
    _, sorted_indices = teacher_for_sort.sort(descending=True, dim=-1)

    sorted_mask = torch.gather(mask_shuffled, dim=1, index=sorted_indices)
    sorted_student = torch.gather(student_shuffled, dim=1, index=sorted_indices)
    sorted_student = sorted_student.masked_fill(~sorted_mask, float("-inf"))

    max_scores = sorted_student.max(dim=1, keepdim=True).values
    shifted_scores = sorted_student - max_scores

    exp_scores = shifted_scores.exp().masked_fill(~sorted_mask, 0.0)
    cumsums = torch.cumsum(exp_scores.flip(dims=[1]), dim=1).flip(dims=[1])

    observation_loss = torch.log(cumsums + eps) - shifted_scores.masked_fill(~sorted_mask, 0.0)
    observation_loss = observation_loss.masked_fill(~sorted_mask, 0.0)

    valid_rows = sorted_mask.any(dim=1)
    if not torch.any(valid_rows):
        return student_scores.new_zeros(())
    return observation_loss.sum(dim=1)[valid_rows].mean()
