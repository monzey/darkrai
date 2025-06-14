{
  description = "Environnement Python pour projet JDR-IA";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        p2nix = poetry2nix.legacyPackages.${system};
        poetryEnv = p2nix.mkPoetryEnv {
          projectDir = self;
          python = pkgs.python311;
        };
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [ poetryEnv ];

          shellHook = ''
            echo "🐍 Python JDR-IA environment ready via poetry2nix!"
          '';
        };
      }
    );
}
