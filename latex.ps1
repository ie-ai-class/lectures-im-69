function Compile-LaTeXDocument {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Folder,

        [Parameter(Mandatory = $true)]
        [string]$Stem,

        [int]$Passes = 2
    )

    # Remove leading underscore from stem for the output filename
    $cleanStem = $Stem.TrimStart('_')

    # Define build targets: Key = suffix, Value = latex code preamble
    $targets = @(
        @{ Suffix = "student"; Code = "\def\studentflag{1}\input{$Stem}" },
        @{ Suffix = "solution"; Code = "\input{$Stem}" }
    )

    foreach ($target in $targets) {
        $jobName = "${cleanStem}_$($target.Suffix)"

        # Compile from the document's own folder so relative paths
        # (img/..., ../../*.sty) resolve the same way as in LaTeX Workshop
        Push-Location $Folder
        try {
            # Run pdflatex for the specified number of passes (to resolve references)
            1..$Passes | ForEach-Object {
                pdflatex -jobname "$jobName" "$($target.Code)"
            }
        }
        finally {
            Pop-Location
        }
    }
}

# Compile-LaTeXDocument -Folder "src/T02_ml_basics/S1" -Stem "_linear_regression"
# Compile-LaTeXDocument -Folder "src/T02_ml_basics/S2" -Stem "_classification"
# Compile-LaTeXDocument -Folder "src/T03_ffn_basics/S1" -Stem "_xor"
# Compile-LaTeXDocument -Folder "src/T03_ffn_basics/S2" -Stem "_gradient_descent"
Compile-LaTeXDocument -Folder "src/T03_ffn_basics/S3" -Stem "_forward_backprop"
Compile-LaTeXDocument -Folder "src/T03_ffn_basics/S4" -Stem "_mlp"