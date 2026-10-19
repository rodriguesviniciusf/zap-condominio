import configparser
import struct
import unittest
import wave
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AndroidAssetsTests(unittest.TestCase):
    def test_quatro_sons_pcm_validos_e_curtos(self):
        for nome in ('toque', 'dia', 'decisao', 'alerta'):
            with wave.open(str(ROOT/'assets'/(nome+'.wav'))) as som:
                self.assertEqual(som.getnchannels(), 1)
                self.assertEqual(som.getsampwidth(), 2)
                self.assertGreater(som.getnframes(), 100)
                self.assertLess(som.getnframes()/som.getframerate(), 1)

    def test_configuracao_empacota_audio_icone_e_vibracao(self):
        spec = configparser.ConfigParser(interpolation=None)
        spec.read(ROOT/'buildozer.spec', encoding='utf-8')
        self.assertIn('wav', spec['app']['source.include_exts'].split(','))
        self.assertIn('VIBRATE', spec['app']['android.permissions'].split(','))
        caminho = ROOT/spec['app']['icon.filename']
        with caminho.open('rb') as f:
            self.assertEqual(f.read(8), bytes([137, 80, 78, 71, 13, 10, 26, 10]))
            f.read(8)
            w, h = struct.unpack('>II', f.read(8))
        self.assertEqual(w, h)
        self.assertGreaterEqual(w, 192)
        dados = caminho.read_bytes()
        pos = 8
        terminou = False
        while pos < len(dados):
            tamanho = struct.unpack('>I', dados[pos:pos+4])[0]
            bloco = dados[pos+4:pos+8+tamanho]
            crc = struct.unpack('>I', dados[pos+8+tamanho:pos+12+tamanho])[0]
            self.assertEqual(zlib.crc32(bloco), crc)
            pos += 12+tamanho
            if bloco[:4] == b'IEND':
                terminou = True
                break
        self.assertTrue(terminou)
