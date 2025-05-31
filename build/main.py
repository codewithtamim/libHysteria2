#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result.stdout

def build_android():
    """Build for Android using gomobile"""
    print("Building for Android...")
    
    # Check if gomobile is installed
    try:
        run_command(["gomobile", "version"])
    except FileNotFoundError:
        print("gomobile not found. Please install it first:")
        print("go install golang.org/x/mobile/cmd/gomobile@latest")
        print("gomobile init")
        sys.exit(1)
    
    # Build Android AAR
    cmd = [
        "gomobile", "bind",
        "-target", "android",
        "-androidapi", "21",
        "-o", "libHysteria2.aar",
        "."
    ]
    run_command(cmd)
    print("Android build completed: libHysteria2.aar")

def build_apple_gomobile():
    """Build for iOS/macOS using gomobile"""
    print("Building for Apple platforms using gomobile...")
    
    # Check if gomobile is installed
    try:
        run_command(["gomobile", "version"])
    except FileNotFoundError:
        print("gomobile not found. Please install it first:")
        print("go install golang.org/x/mobile/cmd/gomobile@latest")
        print("gomobile init")
        sys.exit(1)
    
    # Build iOS framework
    cmd = [
        "gomobile", "bind",
        "-target", "ios",
        "-o", "LibHysteria2.xcframework",
        "."
    ]
    run_command(cmd)
    print("Apple build completed: LibHysteria2.xcframework")

def build_apple_cgo():
    """Build for Apple platforms using cgo"""
    print("Building for Apple platforms using cgo...")
    
    platforms = [
        ("ios", "arm64"),
        ("ios", "amd64"),  # iOS Simulator
        ("darwin", "arm64"),  # macOS Apple Silicon
        ("darwin", "amd64"),  # macOS Intel
    ]
    
    output_dir = Path("build/apple")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for goos, goarch in platforms:
        print(f"Building for {goos}/{goarch}...")
        env = os.environ.copy()
        env.update({
            "GOOS": goos,
            "GOARCH": goarch,
            "CGO_ENABLED": "1",
        })
        
        if goos == "ios":
            if goarch == "arm64":
                env["CC"] = "clang -arch arm64 -isysroot $(xcrun --sdk iphoneos --show-sdk-path)"
            else:
                env["CC"] = "clang -arch x86_64 -isysroot $(xcrun --sdk iphonesimulator --show-sdk-path)"
        
        output_file = output_dir / f"libhysteria2_{goos}_{goarch}.a"
        cmd = ["go", "build", "-buildmode=c-archive", "-o", str(output_file), "."]
        subprocess.run(cmd, env=env, check=True)
    
    print("Apple cgo build completed in build/apple/")

def build_linux():
    """Build for Linux"""
    print("Building for Linux...")
    
    # Check if clang is available
    try:
        run_command(["clang", "--version"])
    except FileNotFoundError:
        print("clang not found. Please install clang and clang++")
        sys.exit(1)
    
    env = os.environ.copy()
    env.update({
        "GOOS": "linux",
        "GOARCH": "amd64",
        "CGO_ENABLED": "1",
        "CC": "clang",
        "CXX": "clang++",
    })
    
    cmd = ["go", "build", "-buildmode=c-archive", "-o", "libhysteria2_linux.a", "."]
    subprocess.run(cmd, env=env, check=True)
    print("Linux build completed: libhysteria2_linux.a")

def build_windows():
    """Build for Windows"""
    print("Building for Windows...")
    
    # Check if LLVM MinGW is available
    try:
        run_command(["x86_64-w64-mingw32-gcc", "--version"])
    except FileNotFoundError:
        print("LLVM MinGW not found. Please install it:")
        print("winget install MartinStorsjo.LLVM-MinGW.UCRT")
        sys.exit(1)
    
    env = os.environ.copy()
    env.update({
        "GOOS": "windows",
        "GOARCH": "amd64",
        "CGO_ENABLED": "1",
        "CC": "x86_64-w64-mingw32-gcc",
        "CXX": "x86_64-w64-mingw32-g++",
    })
    
    cmd = ["go", "build", "-buildmode=c-archive", "-o", "libhysteria2_windows.a", "."]
    subprocess.run(cmd, env=env, check=True)
    print("Windows build completed: libhysteria2_windows.a")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 build/main.py <platform> [options]")
        print("Platforms:")
        print("  android")
        print("  apple gomobile")
        print("  apple cgo")
        print("  linux")
        print("  windows")
        sys.exit(1)
    
    platform = sys.argv[1].lower()
    
    if platform == "android":
        build_android()
    elif platform == "apple":
        if len(sys.argv) > 2 and sys.argv[2] == "gomobile":
            build_apple_gomobile()
        elif len(sys.argv) > 2 and sys.argv[2] == "cgo":
            build_apple_cgo()
        else:
            print("Please specify: gomobile or cgo")
            print("Example: python3 build/main.py apple gomobile")
            sys.exit(1)
    elif platform == "linux":
        build_linux()
    elif platform == "windows":
        build_windows()
    else:
        print(f"Unknown platform: {platform}")
        sys.exit(1)

if __name__ == "__main__":
    main() 