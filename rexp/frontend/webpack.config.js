const webpack = require('webpack');
const path = require('path');


module.exports = {
    optimization: {
        splitChunks: {
            cacheGroups: {
                commons: {
                    test: /[\\/]node_modules[\\/]/,
                    name: 'commons',
                    chunks: 'all'
                }
            }
        }
    },
    entry: {
        "home/index": './apps/home/index.js'
    },
    output: {
        path: path.resolve(__dirname, '../../static/dist'),
        filename: '[name].js',
    },

    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader'],
            },
            {
                test: /\.svg$/,
                loader: 'svg-inline-loader'
            }
        ]
    }
};