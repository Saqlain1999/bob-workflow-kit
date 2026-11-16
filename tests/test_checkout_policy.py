"""Exercise the real Git checkout policy without using network or a user repo."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('git'), 'Git is required for the checkout-policy probe')
class CheckoutPolicyTests(unittest.TestCase):
    def test_autocrlf_checkout_preserves_committed_bytes(self):
        attributes = ROOT / '.gitattributes'
        self.assertTrue(attributes.is_file(), 'a committed-byte checkout policy is required')
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            source = base / 'source'
            clone = base / 'windows-policy-clone'
            source.mkdir()
            (source / '.gitattributes').write_bytes(attributes.read_bytes())
            original = {'lf.txt': b'first\nsecond\n', 'raw.bin': b'\x00\x0a\x0d\xff'}
            for name, content in original.items():
                (source / name).write_bytes(content)
            def git(*arguments, cwd=source):
                return subprocess.run(['git', *arguments], cwd=cwd, capture_output=True,
                                      text=True, check=True, timeout=30)
            git('init', '-q')
            git('add', '.')
            git('-c', 'user.name=Checkout Probe', '-c', 'user.email=probe@example.invalid',
                '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
            git('-c', 'core.autocrlf=true', 'clone', '--no-local', '--no-hardlinks',
                str(source), str(clone), cwd=base)
            for name, content in original.items():
                self.assertEqual((clone / name).read_bytes(), content, name)
            self.assertEqual(git('-c', 'core.autocrlf=true', 'status', '--porcelain',
                                 cwd=clone).stdout, '')


if __name__ == '__main__':
    unittest.main()
