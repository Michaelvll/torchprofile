import torch
from torchprofile import profile_macs, profile_acts
from torchvision import models

if __name__ == '__main__':
    for name, model in models.__dict__.items():
        if not name.islower() or name.startswith('__') or not callable(model):
            continue

        model = model().eval()
        if 'inception' not in name:
            inputs = torch.randn(1, 3, 224, 224)
        else:
            inputs = torch.randn(1, 3, 299, 299)

        macs = profile_macs(model, inputs)
        print('macs {}: {:.4g} G'.format(name, macs / 1e9))
        acts = profile_acts(model, inputs)
        print('acts {}: {:.4g} MB'.format(name, acts * 4 / 1024 / 1024))