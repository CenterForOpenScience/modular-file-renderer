var webpack = require('webpack');
var path = require('path');
var builder = require('./node_modules/pdf.js/external/builder/builder.js');


// Configuration for preprocessor?
var DEFINES = {
  PRODUCTION: true,
  // The main build targets:
  GENERIC: false,
  FIREFOX: false,
  MOZCENTRAL: false,
  CHROME: false,
  MINIFIED: false,
  COMPONENTS: false,
  LIB: false,
  SKIP_BABEL: false,
};

var defines = builder.merge(DEFINES, { GENERIC: true, });
//var versionInfo = //JSON.parse(fs.readFileSync(BUILD_DIR + 'version.json').toString());

var bundleDefines = builder.merge(defines, {
    BUNDLE_VERSION: "0.0.0",
    BUNDLE_BUILD: "asdfqwer",
});

const config = {
    context: __dirname,
    entry: {
        mfr: "./index.js",
        pdf: "./mfr/extensions/pdf/client/index.js",
        'mfr.worker': 'pdfjs/pdf.worker.entry'
    },
    output: {
        filename: "./static/[name].js",
        chunkFilename: "./static/[hash].chunk.js"
    },
    resolve: {
        alias: {
            'pdfjs': path.join(__dirname, 'node_modules/pdf.js/src'),
            'pdfjs-web': path.join(__dirname, 'node_modules/pdf.js/web'),
            'pdfjs-lib': path.join(__dirname, 'pdfjs-lib.js')
        },
    },
    module: {
        loaders: [
            {
                loader: 'babel-loader',
                exclude: /src\/core\/(glyphlist|unicode)/, // babel is too slow
                options: {
                    plugins: ['transform-es2015-modules-commonjs'],
                    presets: ['env']
                }
            },
            {
                loader: path.join(__dirname, 'node_modules/pdf.js/external/webpack/pdfjsdev-loader.js'),
                options: {
                    rootPath: __dirname,
                    saveComments: false,
                    defines: bundleDefines,
                },
            },
        ]
    }
};

module.exports = config;
