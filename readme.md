<h1 align="center">CCL</h1>
<h3 align="center">A low-level language inspired by C</h3>

<p>Designed for use on bios / uefi, so the compiler has a specific mode for that</p>

<h2>How to install</h2>
<p>Once you have downloaded the files, move the ccl1.0 folder into:
<ul>
    <li>linux   - (user Home)/.vscode/extensions/</li>
    <li>windows - %USERPROFILE%/.vscode/extensions/</li>
    <li>mac     - I have no idea, I don't use mac</li>
</ul>
<p>When you open a .ccl or .cclh file in vscode, the logo and highlighting should change, if not, don't ask me.</p>
<p>Move the cclc.py file into your folder, and you can compile with it using the terminal</p>

<p>THE COMPILER DOESN'T CURRENTLY WORK</p>

<h3>Compiler arguments</h3>

<ul>
    <li>-f / --format - determines what the compiler will compiler for. Possible arguments - efi, os</li>
    <li>-o / --output - choose which file the executable will be written to</li>
</ul>