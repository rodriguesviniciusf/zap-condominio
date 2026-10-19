"""Preferências locais, sons sintetizados e feedback Android opcional."""
import json
import logging
from pathlib import Path

DEFAULTS = dict(som=True, vibracao=False, texto=1.0, transicoes=True, tutorial=False)


class Preferencias:
    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.valores = dict(DEFAULTS)
        self.sons = {}
        self.vibrador = None
        try:
            salvo = json.loads(self.caminho.read_text(encoding='utf-8'))
            for k, padrao in DEFAULTS.items():
                valor = salvo.get(k, padrao)
                if (k == 'texto' and valor in (1.0, 1.15, 1.3)) or (k != 'texto' and isinstance(valor, bool)):
                    self.valores[k] = valor
        except (OSError, ValueError, AttributeError):
            pass

    def salvar(self):
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.caminho.with_suffix('.tmp')
        tmp.write_text(json.dumps(self.valores), encoding='utf-8')
        tmp.replace(self.caminho)

    def preparar(self):
        from kivy.core.audio import SoundLoader
        for nome in ('toque', 'dia', 'decisao', 'alerta'):
            try:
                self.sons[nome] = SoundLoader.load(str(Path(__file__).parent/'assets'/(nome+'.wav')))
            except Exception as exc:
                logging.warning('Áudio indisponível: %s', exc)

    def testar_vibracao(self):
        try:
            from jnius import autoclass
            activity = autoclass('org.kivy.android.PythonActivity').mActivity
            context = autoclass('android.content.Context')
            vibrator = activity.getSystemService(context.VIBRATOR_SERVICE)
            if not vibrator or not vibrator.hasVibrator():
                return False
            sdk = autoclass('android.os.Build$VERSION').SDK_INT
            if sdk >= 29:
                effect = autoclass('android.os.VibrationEffect').createPredefined(2)
                vibrator.vibrate(effect)
            elif sdk >= 26:
                effect = autoclass('android.os.VibrationEffect').createOneShot(35, -1)
                vibrator.vibrate(effect)
            else:
                vibrator.vibrate(35)
            return True
        except Exception:
            return False

    def tocar(self, nome, haptico=False):
        if self.valores['som']:
            som = self.sons.get(nome)
            if som:
                try:
                    som.stop()
                    som.volume = .35
                    som.play()
                except Exception as exc:
                    logging.warning('Não foi possível reproduzir áudio: %s', exc)
        if haptico and self.valores['vibracao']:
            self.testar_vibracao()
