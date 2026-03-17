declare module "@effect/platform-node" {
  // Minimal typings to satisfy typechecker; real types come from the package.
  export const NodeFileSystem: { layer: any }
  export const NodePath: { layer: any }
}

