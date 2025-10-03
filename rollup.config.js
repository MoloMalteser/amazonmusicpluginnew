import resolve from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import typescript from "@rollup/plugin-typescript";

export default {
  input: "src/index.tsx",
  output: {
    dir: "dist",
    format: "esm"
  },
  plugins: [
    resolve({
      extensions: [".js", ".ts", ".tsx"]
    }),
    commonjs(),
    typescript()
  ]
};
