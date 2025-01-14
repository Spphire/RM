import torch
import torch.nn as nn

weights = "runs/train/exp/weights/best.pt"
np = 4
colors = 4
tags = 9


ckpt = torch.load(weights, map_location="cpu")

key = "ema" if ckpt.get("ema") else "model"

nc = colors + tags
no = np*2 + 1 + colors + tags

model = ckpt[key].float()
for i, m in enumerate(model.model[-1].m):
    c = m.out_channels // 3
    conv = nn.Conv2d(m.in_channels, 3 * no, m.kernel_size)
    conv.weight.data = torch.cat([m.weight.data[0 * c:0 * c + no],
                                  m.weight.data[1 * c:1 * c + no],
                                  m.weight.data[2 * c:2 * c + no]]).clone()
    conv.bias.data = torch.cat([m.bias.data[0 * c:0 * c + no],
                                m.bias.data[1 * c:1 * c + no],
                                m.bias.data[2 * c:2 * c + no]]).clone()
    model.model[-1].m[i] = conv
model.model[-1].nc = nc
model.model[-1].no = no

ckpt[key] = model
torch.save(ckpt, weights.replace(".pt", "-cut.pt"))
