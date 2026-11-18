#!/usr/bin/env python3
"""Ajustes seguros v2.1 do Karaokê das Cores.
Executado após o patch legado do workflow, tanto na cópia da raiz quanto
nos arquivos Android extraídos dos ZIPs de fonte.
"""
from pathlib import Path
import re

MARKER = "KARAOKE_CORES_PATCH_V21"

def replace_all(text, old, new, label):
    if old not in text:
        print("[AVISO] trecho não localizado:", label)
        return text
    print("[OK] aplicado:", label)
    return text.replace(old, new)

def patch_html(path: Path):
    text = path.read_text(encoding="utf-8")
    if MARKER in text and "KARAOKE_STARTUP_GATE_V22" in text:
        return
    # Corrige a inicialização: a interface permanece oculta até a pasta estar
    # autorizada e a intro ter exibido o primeiro quadro; o áudio só entra depois.
    STARTUP_MARKER = "KARAOKE_STARTUP_GATE_V22"
    if STARTUP_MARKER not in text:
        old_boot = "        let folderLoadFinished = true; var ui = document.getElementById('ui-wrapper'); if (ui && (!document.getElementById('intro-video') || !document.getElementById('intro-video').src || document.getElementById('intro-video').paused)) { ui.classList.remove('oculto-inicio'); ui.classList.add('liberado'); ui.style.display = ''; ui.style.opacity = ''; ui.style.visibility = ''; if (typeof aplicarLayoutFestaDasCores === 'function') aplicarLayoutFestaDasCores(); }"
        text = text.replace(old_boot, "        let folderLoadFinished = true;", 1)

        # Não deixar o elemento de vídeo iniciar sozinho durante a varredura SAF.
        text = text.replace("introVideo.autoplay = true;", "introVideo.autoplay = false;")

        # Primeiro termina a leitura da pasta/catálogo; só então começa a sequência.
        old_order = "                const introPlayback = intro ? iniciarIntroDuranteCarregamento() : null;\n                await handleFolderSelect({ target: { files } });"
        new_order = "                await handleFolderSelect({ target: { files } });\n                const introPlayback = intro ? iniciarIntroDuranteCarregamento() : null;"
        text = text.replace(old_order, new_order, 1)

        # Sem intro, libera a tela somente depois da leitura completa da pasta.
        old_no_intro = "                    logAviso('Pasta autorizada, mas não encontrei slides nem intro.mp4/intro2.mp4. Use Selecionar pasta para tentar outra pasta.');"
        new_no_intro = "                    if (typeof liberarInterfaceAposCarga === 'function') liberarInterfaceAposCarga();\n" + old_no_intro
        text = text.replace(old_no_intro, new_no_intro, 1)

        # Não liberar o palco por estar simplesmente pausado/sem src.
        old_final_unlock = "            folderLoadFinished = true; var ui = document.getElementById('ui-wrapper'); if (ui && (!document.getElementById('intro-video') || !document.getElementById('intro-video').src || document.getElementById('intro-video').paused)) { ui.classList.remove('oculto-inicio'); ui.classList.add('liberado'); ui.style.display = ''; ui.style.opacity = ''; ui.style.visibility = ''; if (typeof aplicarLayoutFestaDasCores === 'function') aplicarLayoutFestaDasCores(); }"
        text = text.replace(old_final_unlock, "            folderLoadFinished = true;", 1)

        old_fail = "        window.onNativeFolderLoadFailed = function() {\n            folderLoadFinished = true; var ui = document.getElementById('ui-wrapper'); if (ui && (!document.getElementById('intro-video') || !document.getElementById('intro-video').src || document.getElementById('intro-video').paused)) { ui.classList.remove('oculto-inicio'); ui.classList.add('liberado'); ui.style.display = ''; ui.style.opacity = ''; ui.style.visibility = ''; if (typeof aplicarLayoutFestaDasCores === 'function') aplicarLayoutFestaDasCores(); }\n        };"
        new_fail = "        window.onNativeFolderLoadFailed = function() {\n            folderLoadFinished = true;\n            if (typeof exibirErroIntro === 'function') exibirErroIntro('Não foi possível carregar a pasta autorizada. Escolha a pasta novamente.', true);\n        };"
        text = text.replace(old_fail, new_fail, 1)

        # A intro fica muda durante o carregamento e só libera som após o primeiro quadro.
        old_mute = "            introVideo.muted = false;\n            try {\n                await forcarPaisagem();"
        new_mute = "            introVideo.muted = true;\n            introVideo.volume = 1;\n            try {\n                await forcarPaisagem();"
        text = text.replace(old_mute, new_mute, 1)

        old_frame = "                    if (introVideo.requestVideoFrameCallback) {\n                        await new Promise(resolve => introVideo.requestVideoFrameCallback(resolve));\n                    }\n                    introCurtain.classList.add('hidden');"
        new_frame = "                    if (introVideo.requestVideoFrameCallback) {\n                        await new Promise(resolve => introVideo.requestVideoFrameCallback(resolve));\n                    } else {\n                        await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));\n                    }\n                    introCurtain.classList.add('hidden');\n                    introVideo.muted = false;"
        text = text.replace(old_frame, new_frame, 1)

        text = text.replace("        function exibirErroIntro(", "        function liberarInterfaceAposCarga() {\n            const ui = document.getElementById('ui-wrapper');\n            if (!ui) return;\n            ui.classList.remove('oculto-inicio');\n            ui.classList.add('liberado');\n            ui.style.display = '';\n            ui.style.opacity = '';\n            ui.style.visibility = '';\n            if (typeof aplicarLayoutFestaDasCores === 'function') aplicarLayoutFestaDasCores();\n        }\n        window.liberarInterfaceAposCarga = liberarInterfaceAposCarga;\n\n        function exibirErroIntro(", 1)

        text = text.replace("</body>", "\n<!-- " + STARTUP_MARKER + " -->\n</body>", 1)

    if MARKER in text:
        path.write_text(text, encoding="utf-8")
        print("[OK] HTML atualizado: inicialização sem tela preta", path)
        return

    # Cinco intros em ordem, mantendo intr2.mp4 como nome legado alternativo.
    helper = r"""
        function ordemArquivoIntro(nome) {
            const n = String(nome || '').toLowerCase();
            if (n === 'intro.mp4') return 0;
            const m = n.match(/^intro([1-5])\.mp4$/);
            if (m) return Number(m[1]);
            if (n === 'intr2.mp4') return 2;
            return 99;
        }
"""
    text = replace_all(text, "        async function reproduzirSequenciaIntro() {",
                       helper + "\n        async function reproduzirSequenciaIntro() {",
                       "ordenação das cinco intros")

    old_filter = r"const introFiles = (entries || []).filter(item => /^(?:intro2?|intr2)\.mp4$/i.test(item.name || '')).sort((a, b) => (/^intro\.mp4$/i.test(a.name) ? 0 : 1) - (/^intro\.mp4$/i.test(b.name) ? 0 : 1));"
    new_filter = r"const introFiles = (entries || []).filter(item => /^(?:intro(?:[1-5])?|intr2)\.mp4$/i.test(item.name || '')).sort((a, b) => ordemArquivoIntro(a.name) - ordemArquivoIntro(b.name));"
    text = replace_all(text, old_filter, new_filter, "detecção das intros na pasta SAF")

    old_map_native = r"introSequenceFiles = introFiles.map(item => ({ file: item, name: item.name, order: /^intro\.mp4$/i.test(item.name) ? 0 : 1 }));"
    new_map_native = r"introSequenceFiles = introFiles.map(item => ({ file: item, name: item.name, order: ordemArquivoIntro(item.name) }));"
    text = replace_all(text, old_map_native, new_map_native, "ordem das intros SAF")

    old_filter_local = r"const introFiles = files.filter(f => /^(?:intro2?|intr2)\.mp4$/i.test(f.name || '')).sort((a, b) => (/^intro\.mp4$/i.test(a.name) ? 0 : 1) - (/^intro\.mp4$/i.test(b.name) ? 0 : 1));"
    new_filter_local = r"const introFiles = files.filter(f => /^(?:intro(?:[1-5])?|intr2)\.mp4$/i.test(f.name || '')).sort((a, b) => ordemArquivoIntro(a.name) - ordemArquivoIntro(b.name));"
    text = replace_all(text, old_filter_local, new_filter_local, "detecção das intros no seletor web")

    old_map_local = r"introSequenceFiles = introFiles.map(file => ({ file, name: file.name, order: /^intro\.mp4$/i.test(file.name) ? 0 : 1 }));"
    new_map_local = r"introSequenceFiles = introFiles.map(file => ({ file, name: file.name, order: ordemArquivoIntro(file.name) }));"
    text = replace_all(text, old_map_local, new_map_local, "ordem das intros no seletor web")

    # Intro e vídeos da pasta RockDoido nunca entram no catálogo de músicas.
    old_catalog = r"const mp4s = files.filter(f => /\.mp4$/i.test(f.name || '') && (f.name || '').toLowerCase() !== 'intro.mp4');"
    new_catalog = r"const mp4s = files.filter(f => /\.mp4$/i.test(f.name || '') && !/^(?:intro(?:[1-5])?|intr2)\.mp4$/i.test(f.name || '') && !/(?:^|\/)(?:ROCK ?DOIDO|MODO ROCKDOIDO)(?:\/|$)/i.test(f.webkitRelativePath || ''));"
    text = replace_all(text, old_catalog, new_catalog, "exclusão de intros e vídeos RockDoido do catálogo")

    text = text.replace("Confira intro.mp4 e intro2.mp4.", "Confira intro.mp4, intro2.mp4, intro3.mp4, intro4.mp4 e intro5.mp4.")
    text = text.replace("Não encontrei intro.mp4 nem intro2.mp4 na pasta escolhida.", "Não encontrei os vídeos intro.mp4 até intro5.mp4 na pasta escolhida.")
    text = text.replace("intro.mp4/intro2.mp4 não encontrados", "intro.mp4 até intro5.mp4 não encontrados")
    text = text.replace("Não encontrei intro.mp4 nem intro2.mp4 na pasta escolhida. Selecione", "Não encontrei intro.mp4 até intro5.mp4 na pasta escolhida. Selecione")

    # Adia a leitura do MP3 até o momento da reprodução, evitando Base64 na varredura.
    old_eager_audio = """                        let audioSrc = f.contentUri || URL.createObjectURL(f);
                        if (f.contentUri && window.AndroidHost && AndroidHost.readDataUrl) {
                            try {
                                const inlineAudio = AndroidHost.readDataUrl(f.contentUri);
                                if (inlineAudio && inlineAudio.startsWith('data:audio/')) audioSrc = inlineAudio;
                            } catch (err) { logAviso('O MP3 será aberto pelo endereço da pasta selecionada.'); }
                        }
"""
    new_lazy_audio = """                        // A leitura nativa do MP3 só ocorre como fallback ao iniciar o áudio.
                        let audioSrc = f.contentUri || URL.createObjectURL(f);
"""
    text = replace_all(text, old_eager_audio, new_lazy_audio, "carregamento sob demanda do MP3 RockDoido")

    # Captura um MP4 dentro da pasta RockDoido para reprodução em vídeo.
    text = replace_all(text,
        "let videoFiles = {}, catalog = [], queue = [], rockDoidoSlides = [], bgCantores = {}, exitTimer, slideInterval;",
        "let videoFiles = {}, catalog = [], queue = [], rockDoidoSlides = [], bgCantores = {}, exitTimer, slideInterval;\n        let _videoRockDoido = null;",
        "variável de vídeo RockDoido")

    text = replace_all(text,
        "videoFiles = {}; rockDoidoSlides = []; bgCantores = {}; catalog = [];",
        "videoFiles = {}; rockDoidoSlides = []; bgCantores = {}; catalog = []; _videoRockDoido = null;",
        "reinicialização do vídeo RockDoido ao trocar pasta")

    old_rock = "const emRockdoido = path.includes('ROCKDOIDO') || path.includes('ROCK DOIDO') || \n                                    path.includes('MODO ROCKDOIDO');"
    new_rock = "const emRockdoido = path.includes('ROCKDOIDO') || path.includes('ROCK DOIDO') || \n                                    path.includes('MODO ROCKDOIDO');\n                if (emRockdoido && name.endsWith('.MP4') && !_videoRockDoido) _videoRockDoido = f;"
    text = replace_all(text, old_rock, new_rock, "identificação do MP4 RockDoido")

    text = replace_all(text, "                tocarAudioRockDoido();\n\n                startRockDoidoSync();",
                       "                if (!_videoRockDoido) tocarAudioRockDoido();\n\n                startRockDoidoSync();",
                       "prioridade do vídeo sobre o MP3 no RockDoido")

    # Reproduz o MP4 no palco RockDoido. Se a WebView não conseguir abrir o URI,
    # retorna automaticamente ao modo antigo de MP3 + slides.
    rock_insert = r"""
            if (_videoRockDoido) {
                const slideLayer = document.getElementById('bg-singer-layer-rock');
                if (slideLayer) { slideLayer.style.opacity = '0'; slideLayer.classList.remove('ativo'); }
                document.body.classList.remove('tem-slide');
                let rockVideo = document.getElementById('rockdoido-video');
                if (!rockVideo) {
                    rockVideo = document.createElement('video');
                    rockVideo.id = 'rockdoido-video';
                    rockVideo.setAttribute('playsinline', '');
                    rockVideo.setAttribute('webkit-playsinline', '');
                    rockVideo.setAttribute('preload', 'auto');
                    rockVideo.controls = false;
                    rockVideo.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1002;background:#000;display:none;';
                    tornadoLayer.appendChild(rockVideo);
                }
                const videoUrl = _videoRockDoido.contentUri || URL.createObjectURL(_videoRockDoido);
                rockVideo.pause();
                rockVideo.src = videoUrl;
                rockVideo.loop = true;
                rockVideo.muted = false;
                rockVideo.style.display = 'block';
                const tentativaVideo = rockVideo.play();
                if (tentativaVideo && typeof tentativaVideo.then === 'function') {
                    tentativaVideo.then(() => {
                        pararAudioRockDoido();
                        logOK('Vídeo do modo RockDoido em reprodução.');
                    }).catch(() => {
                        rockVideo.pause();
                        rockVideo.removeAttribute('src');
                        rockVideo.style.display = 'none';
                        _videoRockDoido = null;
                        logAviso('Este aparelho não conseguiu reproduzir o MP4 RockDoido. Voltando ao modo de áudio e slides.');
                        tocarAudioRockDoido();
                        startRockDoidoSync();
                    });
                }
                return;
            }
"""
    text = replace_all(text, "            logInfo('Slides disponíveis: ' + rockDoidoSlides.length);",
                       "            logInfo('Slides disponíveis: ' + rockDoidoSlides.length);\n" + rock_insert,
                       "reprodução opcional de vídeo RockDoido")

    text = replace_all(text, "                pararAudioRockDoido();\n\n                clearInterval(slideInterval);",
                       "                pararAudioRockDoido();\n                const rockVideo = document.getElementById('rockdoido-video');\n                if (rockVideo) { rockVideo.pause(); rockVideo.removeAttribute('src'); rockVideo.load(); rockVideo.style.display = 'none'; }\n\n                clearInterval(slideInterval);",
                       "encerramento do vídeo RockDoido")

    # Ordena fundo base + bgpadrao2..5; mantém nomes adicionais já existentes.
    old_bg = r"""if (bgPadraoGif) {
                bgPadraoList = [bgPadraoGif.contentUri || URL.createObjectURL(bgPadraoGif)];
                iniciarRotacaoBg();
            } else if (bgPadraoFiles.length > 0) {
                bgPadraoList = bgPadraoFiles.map(f => f.contentUri || URL.createObjectURL(f));
                iniciarRotacaoBg();
            }"""
    new_bg = r"""if (bgPadraoGif) bgPadraoFiles.unshift(bgPadraoGif);
            bgPadraoFiles.sort((a, b) => {
                const rank = f => {
                    const base = String(f.name || '').replace(/^bgpadr[ãa]o/i, '').replace(/\.[^.]+$/, '');
                    const n = base ? Number(base) : 0;
                    if (n === 0) return 0;
                    if (n >= 2 && n <= 5) return n - 1;
                    return 10 + (Number.isFinite(n) ? n : 99);
                };
                return rank(a) - rank(b) || String(a.name || '').localeCompare(String(b.name || ''), undefined, {numeric:true, sensitivity:'base'});
            });
            if (bgPadraoFiles.length > 0) {
                bgPadraoList = bgPadraoFiles.map(f => f.contentUri || URL.createObjectURL(f));
                iniciarRotacaoBg();
            }"""
    text = replace_all(text, old_bg, new_bg, "ordem dos fundos bgpadrao até bgpadrao5")

    # Corrige escrita do TXT: passa o URI exato da lista selecionada.
    text = replace_all(text,
        "try { gravou = !!AndroidHost.writeListaTxt(conteudo); } catch (_) { gravou = false; }",
        "try { gravou = !!AndroidHost.writeListaTxt(listas[0].contentUri, conteudo); } catch (_) { gravou = false; }",
        "gravação do lista.txt no arquivo selecionado")

    # O fundo padrão continua visível na contagem quando não existe foto do cantor.
    css_js = r"""
<style id="karaoke-cores-v21">
/* Palco realmente cheio: a fila e os controles laterais desaparecem e voltam ao sair. */
body.fullscreen-mode .search-bar,
body.fullscreen-mode .ui-panel {
    opacity: 0 !important;
    visibility: hidden !important;
    pointer-events: none !important;
}
body.fullscreen-mode .stage,
body.fullscreen-mode .stage-background {
    background-size: cover !important;
    background-position: center center !important;
}
body.countdown-ativo.countdown-sem-foto .stage-background {
    opacity: .78 !important;
    visibility: visible !important;
}
#rockdoido-video { object-fit: cover !important; }
#btn-sair-app-fixo, #btn-sair-topo-oficial, .btn-sair-topo-fixo, .btn-sair-transparente {
    position: fixed !important;
    top: 12px !important;
    right: 14px !important;
    left: auto !important;
    width: 36px !important;
    height: 36px !important;
    opacity: .56 !important;
    background: rgba(0,0,0,.22) !important;
    border: 1px solid rgba(255,255,255,.24) !important;
    box-shadow: none !important;
    z-index: 999999 !important;
}
#btn-sair-app-fixo:focus, #btn-sair-topo-oficial:focus,
.btn-sair-topo-fixo:focus, .btn-sair-transparente:focus {
    opacity: 1 !important;
    background: rgba(90,55,130,.72) !important;
    border-color: rgba(255,255,255,.7) !important;
}
</style>
<script id="karaoke-cores-v21-runtime">
(function () {
    if (window.__karaokeCoresV21Installed) return;
    window.__karaokeCoresV21Installed = true;

    function posicionarBotaoSair() {
        document.querySelectorAll('#btn-sair-app-fixo, #btn-sair-topo-oficial, .btn-sair-topo-fixo, .btn-sair-transparente').forEach(function (b) {
            b.style.position = 'fixed';
            b.style.top = '12px';
            b.style.right = '14px';
            b.style.left = 'auto';
            b.style.opacity = '.56';
        });
    }
    document.addEventListener('DOMContentLoaded', posicionarBotaoSair);
    window.addEventListener('load', posicionarBotaoSair);
    setTimeout(posicionarBotaoSair, 900);

    // Usa o fundo rotativo quando o cantor não possui foto própria.
    if (typeof window.startPlaylist === 'function') {
        const iniciarOriginal = window.startPlaylist;
        window.startPlaylist = async function () {
            let usarFundoPadrao = false;
            try {
                const atual = (typeof queue !== 'undefined' && queue.length) ? queue[0] : null;
                if (atual && document.body && !document.body.classList.contains('modo-jb')) {
                    const cantor = String(atual.singer || '').toUpperCase();
                    const chaves = cantor && cantor !== 'CONVIDADO' ? [cantor, cantor.charAt(0)] : [];
                    const temFoto = chaves.some(function (k) { return !!(bgCantores[k] || bgCantores[k + '2']); });
                    usarFundoPadrao = !temFoto && !_bgOficialUrl;
                    if (usarFundoPadrao) document.body.classList.add('countdown-sem-foto');
                }
            } catch (_) {}
            try { return await iniciarOriginal.apply(this, arguments); }
            finally { document.body.classList.remove('countdown-sem-foto'); }
        };
    }
})();
</script>
"""
    text = replace_all(text, "</body>", "\n" + MARKER + "\n" + css_js + "\n</body>", "estilos e fallback visual v2.1")

    path.write_text(text, encoding="utf-8")
    print("[OK] HTML atualizado:", path)

def patch_java(path: Path):
    text = path.read_text(encoding="utf-8")
    changed = False

    if "import java.io.OutputStream;" not in text:
        text = text.replace("import java.io.InputStream;", "import java.io.InputStream;\nimport java.io.OutputStream;")
        changed = True

    text = text.replace(
        "Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION | Intent.FLAG_GRANT_PREFIX_URI_PERMISSION",
        "Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION | Intent.FLAG_GRANT_PREFIX_URI_PERMISSION"
    )

    text = text.replace(
        "try { getContentResolver().takePersistableUriPermission(treeUri, grants & Intent.FLAG_GRANT_READ_URI_PERMISSION); }",
        "try { getContentResolver().takePersistableUriPermission(treeUri, grants); }"
    )

    # A sequência completa começa após a listagem SAF, evitando tocar intro.mp4 duas vezes.
    text = text.replace("                    notifyRootIntro(treeUri, rootId);",
                        "                    // Intros são iniciadas em ordem pelo JavaScript após a listagem completa.")

    # A leitura SAF envia ao JavaScript apenas tipos de arquivo usados pelo app.
    collect_anchor = """                } else {
                    JSONObject item = new JSONObject();
                    item.put("name", name);"""
    collect_replacement = """                } else {
                    String lowerName = name.toLowerCase(java.util.Locale.ROOT);
                    boolean relevant = lowerName.equals("lista.txt") || lowerName.equals("logo.png") ||
                        lowerName.equals("bgoficial.png") ||
                        lowerName.matches(".*\\\\.(mp4|mp3|jpg|jpeg|png|gif|webp|bmp|svg|avif)$");
                    if (!relevant) continue;
                    JSONObject item = new JSONObject();
                    item.put("name", name);"""
    if collect_anchor in text:
        text = text.replace(collect_anchor, collect_replacement, 1)
        changed = True

    if "writeListaTxt(String uriStr, String conteudo)" not in text:
        bridge = r"""
        @JavascriptInterface public boolean writeListaTxt(String uriStr, String conteudo) {
            try (OutputStream out = getContentResolver().openOutputStream(Uri.parse(uriStr), "wt")) {
                if (out == null) return false;
                out.write(conteudo.getBytes(StandardCharsets.UTF_8));
                out.flush();
                return true;
            } catch (Exception e) { return false; }
        }
"""
        text = text.replace("        @JavascriptInterface public String cacheIntroVideo(String value) {",
                            bridge + "\n        @JavascriptInterface public String cacheIntroVideo(String value) {")
        changed = True

    if text != path.read_text(encoding="utf-8"):
        changed = True
    if changed:
        path.write_text(text, encoding="utf-8")
        print("[OK] Java atualizado:", path)

def main():
    html_files = list(Path(".").rglob("index.html"))
    java_files = list(Path(".").rglob("MainActivity.java"))
    for path in html_files:
        patch_html(path)
    for path in java_files:
        patch_java(path)
    print(f"[RESUMO] {len(html_files)} HTML(s), {len(java_files)} MainActivity.java(s) verificados.")

if __name__ == "__main__":
    main()
