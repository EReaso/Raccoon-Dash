/* eslint-disable camelcase */

'use strict'

const path = require('node:path')

module.exports = {
  spec_dir: 'bootstrap',
  // Make Jasmine look for `.test.bootstrap` files
  spec_files: ['**/*.{test,spec}.bootstrap'],
  // Compile them into JS scripts running `sass-true`
  requires: [path.join(__dirname, 'sass-true/register')],
  // Ensure we use `require` so that the require.extensions works
  // as `import` completely bypasses it
  jsLoader: 'require'
}
