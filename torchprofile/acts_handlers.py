from .utils import math

__all__ = ['handlers']


def addmm(node):
    # [n, p] = aten::addmm([n, p], [n, m], [m, p], *, *)
    n, p = node.outputs[0].shape
    return n * p


def addmv(node):
    # [n] = aten::addmv([n], [n, m], [m], *, *)
    n = node.outputs[0].shape[0]
    return n


def bmm(node):
    # [b, n, p] = aten::bmm([b, n, m], [b, m, p])
    b, n, p = node.outputs[0].shape
    return b * n * p


def matmul(node):
    if node.inputs[0].ndim == 1 and node.inputs[1].ndim == 1:
        # [] = aten::matmul([n], [n])
        return 1
    elif node.inputs[0].ndim == 1 and node.inputs[1].ndim == 2:
        # [m] = aten::matmul([n], [n, m])
        m = node.outputs[0].shape[0]
        return m
    elif node.inputs[0].ndim == 2 and node.inputs[1].ndim == 1:
        # [n] = aten::matmul([n, m], [m])
        n = node.outputs[0].shape[0]
        return n
    elif node.inputs[0].ndim == 2 and node.inputs[1].ndim == 2:
        # [n, p] = aten::matmul([n, m], [m, p])
        n, p = node.outputs[0].shape
        return n * p
    elif node.inputs[0].ndim == 1:
        # [..., m] = aten::matmul([n], [..., n, m])
        *b, m = node.outputs[0].shape
        return math.prod(b) * m
    elif node.inputs[1].ndim == 1:
        # [..., n] = aten::matmul([..., n, m], [m])
        *b, n = node.outputs[0].shape
        return math.prod(b) * n
    else:
        # [..., n, p] = aten::matmul([..., n, m], [..., m, p])
        *b, n, p = node.outputs[0].shape
        return math.prod(b) * n * p


def mul(node):
    os = node.outputs[0].shape
    return math.prod(os)


def convolution(node):
    if node.outputs[0].shape[1] == node.inputs[1].shape[0]:
        oc, ic, *ks = node.inputs[1].shape
    else:
        ic, oc, *ks = node.inputs[1].shape
    os = node.outputs[0].shape
    return math.prod(os)


def batch_norm(node):
    # TODO: provide an option to not fuse `batch_norm` into `linear` or `conv`
    os = node.outputs[0].shape
    return math.prod(os)


def instance_norm_or_layer_norm(node):
    os = node.outputs[0].shape
    return math.prod(os)


def avg_pool_or_mean(node):
    os = node.outputs[0].shape
    return math.prod(os)


def leaky_relu(node):
    os = node.outputs[0].shape
    return math.prod(os)

handlers = (
    ('aten::addmm', addmm),
    ('aten::addmv', addmv),
    ('aten::bmm', bmm),
    ('aten::matmul', matmul),
    (('aten::mul', 'aten::mul_'), mul),
    ('aten::_convolution', convolution),
    ('aten::batch_norm', batch_norm),
    (('aten::instance_norm', 'aten::layer_norm'), instance_norm_or_layer_norm),
    (('aten::adaptive_avg_pool1d', 'aten::adaptive_avg_pool2d',
      'aten::adaptive_avg_pool3d', 'aten::avg_pool1d', 'aten::avg_pool2d',
      'aten::avg_pool3d', 'aten::mean'), avg_pool_or_mean),
    ('aten::leaky_relu', leaky_relu),
    (('aten::adaptive_max_pool1d', 'aten::adaptive_max_pool2d',
      'aten::adaptive_max_pool3d', 'aten::add', 'aten::add_',
      'aten::alpha_dropout', 'aten::cat', 'aten::chunk', 'aten::clamp',
      'aten::clone', 'aten::constant_pad_nd', 'aten::contiguous',
      'aten::detach', 'aten::div', 'aten::div_', 'aten::dropout',
      'aten::dropout_', 'aten::embedding', 'aten::eq', 'aten::feature_dropout',
      'aten::flatten', 'aten::floor', 'aten::gt', 'aten::hardtanh_',
      'aten::index', 'aten::int', 'aten::log_softmax', 'aten::lt',
      'aten::max_pool1d', 'aten::max_pool1d_with_indices', 'aten::max_pool2d',
      'aten::max_pool2d_with_indices', 'aten::max_pool3d',
      'aten::max_pool3d_with_indices', 'aten::max_unpool1d',
      'aten::max_unpool2d', 'aten::max_unpool3d', 'aten::ne',
      'aten::reflection_pad1d', 'aten::reflection_pad2d',
      'aten::reflection_pad3d', 'aten::relu', 'aten::relu_',
      'aten::replication_pad1d', 'aten::replication_pad2d',
      'aten::replication_pad3d', 'aten::rsub', 'aten::select', 'aten::sigmoid',
      'aten::size', 'aten::slice', 'aten::softmax', 'aten::softshrink',
      'aten::squeeze', 'aten::stack', 'aten::sub', 'aten::sum', 'aten::t',
      'aten::tanh', 'aten::threshold', 'aten::to', 'aten::transpose',
      'aten::upsample_nearest2d', 'aten::view', 'aten::zeros',
      'prim::constant', 'prim::listconstruct', 'prim::listunpack',
      'prim::numtotensor', 'prim::tupleconstruct'), None),
)
