param(
    [string]$RepoId = "nomic-ai/nomic-embed-text-v1.5",
    [string]$ModelFile = "onnx/model_int8.onnx",
    [string]$OutputRoot = ".",
    [switch]$InstallDeps
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python is not available on PATH. Install Python 3.10+."
}

# Install dependencies if requested
if ($InstallDeps) {
    Write-Host "Installing huggingface_hub..."
    python -m pip install huggingface_hub --quiet --upgrade
}

# Ensure output directory exists
if (-not (Test-Path $OutputRoot)) {
    New-Item -ItemType Directory -Path $OutputRoot | Out-Null
}

$resolvedOutput = (Resolve-Path $OutputRoot).Path
$onnxDir = Join-Path $resolvedOutput "onnx"
New-Item -ItemType Directory -Path $onnxDir -Force | Out-Null

# Python script (safe, no f-strings)
$pythonScript = @"
from huggingface_hub import hf_hub_download

model_path = hf_hub_download(
    repo_id="$RepoId",
    filename="$ModelFile",
    local_dir=r"$onnxDir"
)

print("Model downloaded to:", model_path)
"@

# Write to temp file (avoids PowerShell parsing issues)
$tempFile = Join-Path $env:TEMP "download_model.py"
$pythonScript | Out-File -Encoding utf8 $tempFile

try {
    Write-Host "Downloading $RepoId/$ModelFile ..."
    python $tempFile

    # Verify file exists
    $expectedFile = Join-Path $onnxDir (Split-Path $ModelFile -Leaf)
    if (Test-Path $expectedFile) {
        Write-Host "Download successful: $expectedFile"
    } else {
        Write-Host "Warning: File not found after download."
    }
}
catch {
    Write-Host "Download failed. Try running with -InstallDeps."
    throw
}
finally {
    Remove-Item $tempFile -ErrorAction SilentlyContinue
}