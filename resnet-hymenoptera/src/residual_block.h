#ifndef RESIDUAL_BLOCK_H
#define RESIDUAL_BLOCK_H
#include <torch/torch.h>

namespace resnet
{
    class ResidualBlockImpl : public torch::nn::Module
    {
    public:
        ResidualBlockImpl(int64_t in_channels, int64_t out_channels, int64_t stride = 1,
                          torch::nn::Sequential downsample = nullptr);
        torch::Tensor forward(torch::Tensor x);

    private:
        torch::nn::Conv2d conv1;
        torch::nn::BatchNorm2d bn1;
        torch::nn::ReLU relu{true};
        torch::nn::Conv2d conv2;
        torch::nn::BatchNorm2d bn2;
        torch::nn::Sequential downsampler;
    };

    torch::nn::Conv2d conv1x1(int64_t in_channels, int64_t out_channels, int64_t stride = 2);
    torch::nn::Conv2d conv3x3(int64_t in_channels, int64_t out_channels, int64_t stride = 1);
    torch::nn::Conv2d conv7x7(int64_t in_channels, int64_t out_channels, int64_t stride = 2);

    TORCH_MODULE(ResidualBlock);
}

#endif
