const path = require("path");

function resolve(dir) {
  return path.join(__dirname, dir);
}

module.exports = {
  configureWebpack: (config) => {
    config.resolve = {
      alias: {
        ...config.resolve.alias,
        "slap-client": resolve("src/modules/slap-client/src"),
      },
    };
  },
};
