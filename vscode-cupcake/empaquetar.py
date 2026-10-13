"""Empaqueta la extensión como .vsix sin necesitar Node. Uso: python3 empaquetar.py"""
import json
import pathlib
import zipfile

AQUI = pathlib.Path(__file__).parent
pkg = json.loads((AQUI / "package.json").read_text(encoding="utf-8"))
salida = AQUI / f"{pkg['name']}-{pkg['version']}.vsix"

MANIFIESTO = f"""<?xml version="1.0" encoding="utf-8"?>
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
    <Asset Type="Microsoft.VisualStudio.Services.Icons.Default" Path="extension/icono.png" Addressable="true" />
  </Assets>
</PackageManifest>
"""

TIPOS = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension=".json" ContentType="application/json" />
  <Default Extension=".vsixmanifest" ContentType="text/xml" />
  <Default Extension=".md" ContentType="text/markdown" />
  <Default Extension=".png" ContentType="image/png" />
  <Default Extension=".svg" ContentType="image/svg+xml" />
</Types>
"""

ARCHIVOS = ["package.json", "language-configuration.json", "README.md", "syntaxes/cupcake.tmLanguage.json", "snippets/cupcake.json", "icono.png", "icono-archivo.svg"]

with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("extension.vsixmanifest", MANIFIESTO)
    z.writestr("[Content_Types].xml", TIPOS)
    for nombre in ARCHIVOS:
        z.write(AQUI / nombre, f"extension/{nombre}")

print(f"Creado {salida.name}")
