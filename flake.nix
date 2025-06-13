{
  description = "Environnement Python pour projet JDR-IA";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonEnv = pkgs.python311.withPackages (ps: with ps; [
          fastapi
          uvicorn
          openai
          langchain
          requests
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [ pythonEnv pkgs.poetry ];

          shellHook = ''
            echo "🐍 Python JDR-IA environment ready!"
            export PYTHONPATH=$(pwd)
            python -m venv .venv
            source .venv/bin/activate
          '';
        };
      }
    );
}
