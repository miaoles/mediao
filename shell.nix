# shell.nix
{ pkgs ? import <nixpkgs> {} }:
let
    my-python-packages = p: with p; [
        twitchapi
        mpv
        google-api-python-client
        google-auth-oauthlib
        google-auth-httplib2
        isodate
        #yt-dlp
    ];
    my-python = pkgs.python3.withPackages my-python-packages;
in my-python.env
