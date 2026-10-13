"""Build a complete Windows ZIP using the source's version; no network/publishing."""
import ast
from pathlib import Path
import re
import zipfile

root = Path(__file__).resolve().parent
source = root / 'voice_typing.pyw'
version = None
for node in ast.parse(source.read_text(encoding='utf-8')).body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'APP_VERSION' for t in node.targets):
        version = ast.literal_eval(node.value)
if not isinstance(version, str) or not re.fullmatch(r'\d+\.\d+\.\d+', version):
    raise SystemExit('Set APP_VERSION to MAJOR.MINOR.PATCH before building.')
required = ['Open_LumaScribe.bat', 'voice_typing.pyw', 'Assets/lumascribe_portrait.png',
            'Assets/LumaScribe_Opening_Tune.wav', 'Assets/LumaScribe_Voice_Op.wav', 'README.md',
            'RELEASING.md', 'REQUIREMENTS.md', 'VERIFICATION.md', 'build_release.py',
            'tests/test_features.py', '.gitignore', 'Model/.gitkeep', 'Assets/title_preview.png', 'Assets/lumascribe_title.png']
for name in required:
    if not (root / name).is_file():
        raise SystemExit(f'Missing release file: {name}')
engine_files = sorted(p.relative_to(root).as_posix() for p in (root / 'Engine').rglob('*') if p.is_file())
if any('Engine/' + name not in engine_files for name in ('whisper-cli.exe', 'whisper.dll', 'ggml.dll', 'ggml-base.dll', 'ggml-cpu.dll', 'ggml-cuda.dll')):
    raise SystemExit('Engine must include whisper-cli.exe, whisper.dll and its GGML DLLs.')
required.extend(engine_files)
output = root.parent / f'LumaScribe-v{version}-Windows.zip'
with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=1) as archive:
    archive.writestr('LumaScribe/Model/', b'')
    for name in required:
        archive.write(root / name, 'LumaScribe/' + name)
with zipfile.ZipFile(output) as archive:
    if archive.testzip() is not None:
        raise SystemExit('Archive integrity check failed.')
    for name in required:
        import hashlib
        def digest_stream(stream):
            digest = hashlib.sha256()
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(chunk)
            return digest.digest()
        with archive.open('LumaScribe/' + name) as packed, (root / name).open('rb') as original:
            if digest_stream(packed) != digest_stream(original):
                raise SystemExit(f'Package parity failed: {name}')
print(output)
