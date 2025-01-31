import torch.nn as nn

from torchmeta.modules.module import MetaModule
from torchmeta.modules.utils import get_subdict

class MetaSequential(nn.Sequential, MetaModule):
    __doc__ = nn.Sequential.__doc__

    def forward(self, input, params=None,**kwargs):
        for name, module in self._modules.items():
            if isinstance(module, MetaModule):
                # print('inside metaseq, passing on, ', get_subdict(params, name).keys(), name, 'for siren', siren)
                input = module(input, params=get_subdict(params, name),**kwargs)
                # print('input.shape', input.shape)
            elif isinstance(module, nn.Module):
                input = module(input)
            else:
                raise TypeError('The module must be either a torch module '
                    '(inheriting from `nn.Module`), or a `MetaModule`. '
                    'Got type: `{0}`'.format(type(module)))
        return input
