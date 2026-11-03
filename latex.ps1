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
        @{ Suffix = "student"; Code = "\def\studentflag{1}\input{$Folder/$Stem}" },
        @{ Suffix = "solution"; Code = "\input{$Folder/$Stem}" }
    )

    foreach ($target in $targets) {
        $jobName = "$Folder/${cleanStem}_$($target.Suffix)"
        
        # Run pdflatex for the specified number of passes (to resolve references)
        1..$Passes | ForEach-Object {
            pdflatex -jobname "$jobName" "$($target.Code)"
        }
    }
}

Compile-LaTeXDocument -Folder "src/T02_ml_basics/S1" -Stem "_linear_regression"
Compile-LaTeXDocument -Folder "src/T02_ml_basics/S2" -Stem "_classification"
# Compile-LaTeXDocument -Folder "src/T03_ffn_basics/S1" -Stem "_xor"
# Compile-LaTeXDocument -Folder "src/T03_ffn_basics/S2" -Stem "_gradient_descent"
# Compile-LaTeXDocument -Folder "src/T03_ffn_basics/S3" -Stem "_forward_pass"
# Compile-LaTeXDocument -Folder "src/T03_ffn_basics/S4" -Stem "_backpropagation"
# Compile-LaTeXDocument -Folder "src/T03_ffn_basics/S5" -Stem "_adam"