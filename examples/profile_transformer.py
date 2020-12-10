import torch
from torch.nn.modules.transformer import Transformer
from torchprofile import profile_macs, profile_acts

if __name__ == '__main__':
    embed_size = 512
    num_tokens = 30

    model = Transformer(embed_size)
    inputs = (
        torch.randn(num_tokens, 1, embed_size),
        torch.randn(num_tokens, 1, embed_size),
    )

    macs = profile_macs(model, inputs)
    print('transformer macs: {:.4g} G'.format(macs / 1e9))
    acts = profile_acts(model, inputs)
    print('transformer acts: {:.4g} MB'.format(acts * 4 / 1024 / 1024))
