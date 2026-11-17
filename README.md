# Karaokê Festa das Cores — fonte v2.0

Projeto Android do app **Karaokê Festa das Cores**, pacote `br.com.ursoplayer.karaoke`, versão `2.0` (version code `9`). A interface web foi recuperada do APK v2.0. A atividade Android e a configuração foram reaproveitadas do projeto-fonte local anterior; compare e valide o comportamento no aparelho antes de publicar uma atualização.

## Introduções

Ao selecionar a pasta de mídia, o app procura `intro.mp4` e `intro2.mp4`. Também reconhece `intr2.mp4` como nome alternativo. A busca não diferencia maiúsculas de minúsculas. Quando os dois arquivos estão presentes, toca `intro.mp4` até o fim e em seguida toca o segundo vídeo até o fim. A tela principal só é liberada depois do fim dos vídeos e do carregamento dos arquivos.

## Abrir e compilar

Abra esta pasta no Android Studio, ou compile com Gradle 8.11.1, JDK 17 e Android SDK (compile SDK 35):

```sh
gradle assembleDebug
```

O APK ficará em `app/build/outputs/apk/debug/app-debug.apk`.

## GitHub Actions

O workflow em `.github/workflows/build-apk.yml` compila o projeto em cada `push` para `main`, `master` ou `principal`, e também pode ser iniciado manualmente pela aba **Actions**. O APK aparece como artefato do workflow.

Para publicar o código: crie um repositório GitHub, envie o conteúdo desta pasta para ele e use uma das branches listadas no workflow.

## Assinatura Android

O APK gerado pelo workflow usa assinatura de depuração. Para atualizar uma instalação existente, será necessário assinar a versão de produção com a mesma chave privada usada no app instalado. A chave privada não faz parte deste projeto; mantenha-a fora do GitHub.


## Ajustes v2.1 em preparação

As correções da v2.1 são aplicadas pelo script `tools/patch_karaoke_v21.py` após a extração da fonte ZIP e após o patch de compatibilidade já existente. O catálogo original `lista.txt` e o vínculo entre código e MP4 são preservados.

### Organização recomendada da mídia

Selecione a pasta principal `KARAOKE` no Android TV:

```text
KARAOKE/
├── lista.txt
├── intro.mp4
├── intro2.mp4
├── intro3.mp4
├── intro4.mp4
├── intro5.mp4
├── bgpadrao.jpg
├── bgpadrao2.jpg
├── bgpadrao3.jpg
├── bgpadrao4.jpg
├── bgpadrao5.jpg
├── logo.png                 (opcional)
├── bgoficial.png            (opcional)
├── A/                        (MP4 das músicas)
├── B/                        (MP4 das músicas)
├── BGS/                      (fundos/fotos de cantores)
└── MODO ROCKDOIDO/
    ├── video.mp4             (opcional; se ausente, mantém áudio/slides)
    ├── slides/
    └── ROCKDOIDO/
        └── easteregg.mp3     (opcional)
```

Os nomes das pastas não são obrigatórios para o catálogo: os MP4s de músicas continuam associados pelos códigos já presentes no nome do arquivo ou no `lista.txt`. Os cinco vídeos de abertura e os vídeos da pasta RockDoido não entram como músicas no catálogo.

### Segurança das atualizações

A versão principal não é substituída automaticamente. As alterações são propostas em uma ramificação e validadas pelo GitHub Actions antes de qualquer integração.
