const path = require('path');

config.devServer = {
    static: [
                "kotlin",
                "../../../processedResources/js/main"
              ],
    port: 8000,
    open: false,
    client: {
        "overlay": {
          "errors": true,
          "warnings": false
        }
      }
};

config.module.rules.push({
    test: /\.css$/i,
    use: ["style-loader", "css-loader"]});

/*
config.entry = {
                      main: path.resolve(__dirname, './src/App.kt'),
};
config.output = {
        path: path.resolve(__dirname, './dist'),
        filename: 'main.bundle.js',
};*/



