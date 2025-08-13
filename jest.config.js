module.exports = {
  testEnvironment: "jsdom",
  roots: ["<rootDir>/blog/static/js"],
  testMatch: ["**/__tests__/**/*.test.js"],
  transform: { "^.+\\.js$": "babel-jest" },
  moduleFileExtensions: ["js"],
};
