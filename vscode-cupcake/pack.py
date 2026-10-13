"""Packs the extension as a .vsix without needing Node. Usage: python3 pack.py"""
import json
import pathlib
import zipfile

HERE = pathlib.Path(__file__).parent
pkg = json.loads((HERE / "package.json").read_text(encoding="utf-8"))
output = HERE / f"{pkg['name']}-{pkg['version']}.vsix"

MANIFEST = f"""<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011">
  <Metadata>
    <Identity Language="en-US" Id="{pkg['name']}" Version="{pkg['version']}" Publisher="{pkg['publisher']}" />
    <DisplayName>{pkg['displayName']}</DisplayName>
    <Description xml:space="preserve">{pkg['description']}</Description>
    <Categories>Programming Languages</Categories>
    <Properties>
      <Property Id="Microsoft.VisualStudio.Code.Engine" Value="{pkg['engines']['vscode']}" />
    </Properties>
  </Metadata>
  <Installation>
    <InstallationTarget Id="Microsoft.VisualStudio.Code" />
  </Installation>
  <Dependencies />
  <Assets>
    <Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true" />
    <Asset Type="Microsoft.VisualStudio.Services.Icons.Default" Path="extension/icon.png" Addressable="true" />
  </Assets>
</PackageManifest>
"""

CONTENT_TYPES = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension=".json" ContentType="application/json" />
  <Default Extension=".vsixmanifest" ContentType="text/xml" />
  <Default Extension=".md" ContentType="text/markdown" />
  <Default Extension=".png" ContentType="image/png" />
  <Default Extension=".svg" ContentType="image/svg+xml" />
</Types>
"""

FILES = ["package.json", "language-configuration.json", "README.md", "syntaxes/cupcake.tmLanguage.json", "snippets/cupcake.json", "icon.png", "file-icon.svg"]

with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("extension.vsixmanifest", MANIFEST)
    z.writestr("[Content_Types].xml", CONTENT_TYPES)
    for name in FILES:
        z.write(HERE / name, f"extension/{name}")

print(f"Created {output.name}")
