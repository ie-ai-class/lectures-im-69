"""
Checking nn.Sequential against the hand calculation in Section 3.3.

We build the same XOR network as S41/S42, overwrite its random weights with
the numbers used in the Section 3.3 forward pass, and feed it x = (0, 1).
Calling each piece of the Sequential one at a time shows which node of the
diagram each PyTorch module produces.
"""

import torch
from torch import nn

model = nn.Sequential(
    nn.Linear(2, 2),  # model[0]: x      -> z^(1)   (weights W^(1), b^(1))
    nn.Sigmoid(),  # model[1]: z^(1)  -> h       (no parameters)
    nn.Linear(2, 1),  # model[2]: h      -> z^(2)   (weights W^(2), b^(2))
)

# ── 1. Where are the parameters? ───────────────────────────────────────────
# Only model[0] and model[2] appear: the Sigmoid has nothing to learn.
# nn.Linear stores weight with shape (out, in), so row i holds the weights
# feeding INTO unit i -- the same convention as W^(1) in Section 3.3.
for name, p in model.named_parameters():
    print(f"{name:9s} shape = {tuple(p.shape)}")
print(f"Total parameters: {sum(p.numel() for p in model.parameters())}\n")

# ── 2. Load the Section 3.3 weights ────────────────────────────────────────
with torch.no_grad():
    model[0].weight[:] = torch.tensor([[0.5, -0.5], [0.5, 0.5]])  # W^(1)
    model[0].bias[:] = torch.tensor([0.5, 0.0])  # b^(1)
    model[2].weight[:] = torch.tensor([[0.5, 0.5]])  # W^(2)
    model[2].bias[:] = 0.0  # b^(2)

# ── 3. Forward pass, one module at a time ──────────────────────────────────
x = torch.tensor([[0.0, 1.0]])
y = torch.tensor([[1.0]])

with torch.no_grad():
    z1 = model[0](x)  # pre-activations of the hidden layer
    h = model[1](z1)  # activations of the hidden layer
    z2 = model[2](h)  # pre-activation of the output neuron
    out = model(x)  # the whole Sequential stops here, at z^(2)

print(f"z1        = {[round(v, 4) for v in z1.squeeze().tolist()]}")
print(f"h         = {[round(v, 4) for v in h.squeeze().tolist()]}")
print(f"z2        = {z2.item():.4f}")
print(f"model(x)  = {out.item():.4f}   <- same as z2, NOT y_hat\n")

# ── 4. Output activation + loss ────────────────────────────────────────────
# Section 3.3 used a sigmoid output and a squared-error loss:
y_hat = torch.sigmoid(out)
print(f"sigmoid(z2)            = {y_hat.item():.4f}   (y_hat in Section 3.3)")
print(f"MSE with sigmoid output = {nn.MSELoss()(y_hat, y).item():.4f}   (J in Section 3.3)")

# The two scripts make different choices for the end of the network:
print(f"S41  MSELoss(z2, y)           = {nn.MSELoss()(out, y).item():.4f}")
print(f"S42  BCEWithLogitsLoss(z2, y) = {nn.BCEWithLogitsLoss()(out, y).item():.4f}")
