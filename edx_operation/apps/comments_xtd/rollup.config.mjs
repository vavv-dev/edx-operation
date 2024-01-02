"use strict";

import path from "node:path";
import { babel } from "@rollup/plugin-babel";
import { nodeResolve } from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import replace from "@rollup/plugin-replace";
import postcss from "rollup-plugin-postcss";

import pkg from "./package.json";

const STATIC_DIR = path.resolve(
  __dirname,
  "django_comments_xtd",
  "static",
  "django_comments_xtd",
  "js",
);
const SOURCE_DIR = path.resolve(STATIC_DIR, "src");

const plugins = [
  babel({
    exclude: "node_modules/**",
    babelHelpers: "bundled",
  }),
  nodeResolve(),
  commonjs(),
  replace({
    "process.env.NODE_ENV": JSON.stringify("production"),
    preventAssignment: true,
  }),
  postcss(),
];

export default {
  input: path.resolve(SOURCE_DIR, "index.js"),
  output: {
    format: "iife",
    generatedCode: "es2015",
    file: path.resolve(STATIC_DIR, `django-comments-xtd-${pkg.version}.js`),
    globals: {
      django: "django",
    },
  },
  plugins,
  external: ["django"],
};
