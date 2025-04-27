const path = require('path');

module.exports = {
  entry: {
    'analytics-dashboard': './src/analytics-dashboard-mount.js',
    'question-content': './src/question-content-mount.js'
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, '../core/static/js'),
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              '@babel/preset-env',
              '@babel/preset-react'
            ]
          }
        }
      },
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
  mode: 'production',
};
