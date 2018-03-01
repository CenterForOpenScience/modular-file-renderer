var webpack = require('webpack');
var path = require('path');
var builder = require('./node_modules/pdf.js/external/builder/builder.js');
const CopyWebpackPlugin = require('copy-webpack-plugin')


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

var defines = builder.merge(DEFINES, {GENERIC: true});
//var versionInfo = //JSON.parse(fs.readFileSync(BUILD_DIR + 'version.json').toString());

var bundleDefines = builder.merge(defines, {
    BUNDLE_VERSION: "0.0.0",
    BUNDLE_BUILD: "asdfqwer",
});

const config = {

    
    context: __dirname,
    entry: {
        mfr: "./src/mfr/mfr.js",
        pdf: "./mfr/extensions/pdf/index.js",
        'pdf.worker': 'pdfjs/pdf.worker.entry',
        'mfr.child': "./src/mfr/child.js",
        codepygments: "./mfr/extensions/codepygments/static/css/default.css",
        "jsc3d-init": "./src/jsc3d/index.js",
        tabular: "./src/tabular/index.js"
    },
    output: {
        path: path.resolve(__dirname, "dist"),
        filename: "[name].js",
        publicPath: '/assets/',
        chunkFilename: "./dist/[hash].chunk.js"
    },
    resolve: {
        alias: {
            'pdfjs': 'pdf.js/src',
            'pdfjs-web': 'pdf.js/web',
            'pdfjs-lib': path.join(__dirname, '/src/pdf/pdfjs-lib.js')
        },
        extensions: [ '.ts', '.tsx', ".js", ".json"],
        modules: [
            __dirname,
            'node_modules'
        ]
    },
    plugins: [
        new CopyWebpackPlugin([{
            from: "src/jsc3d/lib/*.js",
            to: "",
            flatten: true
        }, {
            from: "node_modules/jquery/dist/jquery.min.js",
            to: "jquery-1.11.3.min.js"
        }, {
            from: "src/pdb/*",
            to: "",
            flatten: true
        }, {
            from: "src/img/question-circle.png",
            to: "question-circle.png"
        }, {
            from: "src/style/md.css",
            to: ""
        }], {}),
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery"
        })
    ],
    module: {
        rules: [
            {
                loader: 'babel-loader',
                exclude: /src\/core\/(glyphlist|unicode)/, // babel is too slow
                options: {
                    plugins: ['transform-es2015-modules-commonjs'],
                    presets: ['env']
                }
            },
            {
                test: /\.js$/i,
                loader: path.join(__dirname, 'node_modules/pdf.js/external/webpack/pdfjsdev-loader.js'),
                options: {
                    rootPath: __dirname,
                    saveComments: false,
                    defines: bundleDefines,
                },
            },
            {
                test: /\.css$/i,
                use: ['style-loader', 'css-loader'],
            },
            {
                test: /\.(png|jpg|gif|cur|woff|woff2|ttf|eot|svg)$/,
                use: [ 'file-loader' ],
                
            }
        ]
    }
};

module.exports = config;
