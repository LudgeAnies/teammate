// module.exports = {
//   moduleFileExtensions: ['js', 'json', 'vue'],
//   transform: {
//     '^.+\\.vue$': 'vue-jest',
//     '^.+\\.js$': 'babel-jest'
//   },
//   moduleNameMapper: {
//     '^@/(.*)$': '<rootDir>/src/$1'
//   },
//   testEnvironment: 'jsdom',
//   setupFilesAfterEnv: ['<rootDir>/jest.setup.js']
// }
module.exports = {
  moduleFileExtensions: ['js', 'vue'],
  transform: {
    '^.+\\.vue$': '@vue/vue3-jest',
    '^.+\\.js$': 'babel-jest'
  },
  testEnvironment: 'jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1'
  },
}