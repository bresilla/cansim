{
  inputs = {
    # nixpkgs = { url = "nixpkgs/nixos-20.09"; };
    utils = { url = "github:numtide/flake-utils"; };
  };

  outputs = { self, nixpkgs, utils }: 
  utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs.outPath {
        config = { 
          allowUnfree = true;
          allowUnsupportedSystem = true; 
          # cudaSupport = if system == "x86_64-linux" then true else false;
        };
        inherit system;
        overlays = [ ];
      };
      py = pkgs.python38Packages;
    in {
      defaultPackage = pkgs.mkShell {
        name = "cmake";
        buildInputs = let
          opencv = pkgs.opencv.override (old : {
            pythonPackages = py;
            enablePython = true;
            enableGtk3 = true;
            enableGStreamer = true;
            enableFfmpeg = true;
          } );
          realsense = pkgs.librealsense.override (old : {
            pythonPackages = py;
            enablePython = true;
          } );
          pytorch_cuda = py.pytorch.override (old : {
            cudaSupport = true;
          } );
        in [
          pkgs.cudatoolkit_11_2
          pkgs.cudnn_cudatoolkit_11_2
          # opencv
          # realsense
          pkgs.stdenv
          pkgs.fmt
          pkgs.doctest
          pkgs.ccls
          pkgs.clang_11
          pkgs.clang-tools
          pkgs.cmake
          pkgs.armadillo
          pkgs.eigen
          pkgs.boost

          # pkgs.libtorch-bin
          # py.numpy
          # py.pandas
          # py.matplotlib
          # py.scikitlearn
          # pytorch_cuda
          # py.pytorch-bin
          # py.torchvision
        ];
        # shellHook = ''
        #   export TORCH_PATH="${pkgs.libtorch-bin}"
        # '';
      };
    }
  );
}
